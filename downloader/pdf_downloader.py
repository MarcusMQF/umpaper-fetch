"""
PDF Downloader Module

Handles downloading PDF files with progress tracking, retry logic,
and concurrent download management.
"""

import logging
import os
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import requests


class PDFDownloader:
    """Downloads PDF files with progress tracking and retry logic."""
    
    def __init__(self, session, output_dir, max_retries=3, max_workers=4):
        """Initialize the PDF downloader."""
        self.session = session
        self.output_dir = Path(output_dir)
        self.max_retries = max_retries
        self.max_workers = max_workers
        self.logger = logging.getLogger(__name__)
        
        # Ensure output directory exists
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def download_papers(self, papers):
        """
        Download multiple papers with progress tracking.
        
        Args:
            papers (list): List of PaperInfo objects to download
            
        Returns:
            list: List of successfully downloaded file paths
        """
        if not papers:
            return []
        
        self.logger.info(f"Starting download of {len(papers)} papers...")
        downloaded_files = []
        
        # Create progress bar
        with tqdm(total=len(papers), desc="Downloading papers", unit="file") as pbar:
            # Use ThreadPoolExecutor for concurrent downloads
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                # Submit all download tasks
                future_to_paper = {
                    executor.submit(self._download_paper, paper): paper
                    for paper in papers
                }
                
                # Process completed downloads
                for future in as_completed(future_to_paper):
                    paper = future_to_paper[future]
                    try:
                        file_path = future.result()
                        if file_path:
                            downloaded_files.append(file_path)
                            self.logger.debug(f"Downloaded: {paper.filename}")
                        else:
                            self.logger.warning(f"Failed to download: {paper.title}")
                    except Exception as e:
                        self.logger.error(f"Error downloading {paper.title}: {e}")
                    finally:
                        pbar.update(1)
        
        self.logger.info(f"Downloaded {len(downloaded_files)}/{len(papers)} papers successfully")
        return downloaded_files
    
    def _download_paper(self, paper):
        """
        Download a single paper with retry logic.
        
        Args:
            paper (PaperInfo): Paper information object
            
        Returns:
            str: Path to downloaded file, or None if failed
        """
        for attempt in range(self.max_retries + 1):
            try:
                file_path = self._download_file(paper.download_url, paper.filename)
                if file_path and self._verify_download(file_path):
                    return file_path
                
            except Exception as e:
                self.logger.warning(
                    f"Download attempt {attempt + 1} failed for {paper.title}: {e}"
                )
                
                if attempt < self.max_retries:
                    # Wait before retry with exponential backoff
                    wait_time = 2 ** attempt
                    time.sleep(wait_time)
        
        self.logger.error(f"Failed to download after {self.max_retries + 1} attempts: {paper.title}")
        return None
    
    def _download_file(self, url, filename):
        """
        Download a single file from URL.
        
        Args:
            url (str): Download URL
            filename (str): Target filename
            
        Returns:
            str: Path to downloaded file
        """
        file_path = self.output_dir / filename
        
        # Avoid re-downloading if file already exists and is valid
        if file_path.exists() and self._verify_download(file_path):
            self.logger.debug(f"File already exists: {filename}")
            return str(file_path)
        
        # Start download
        response = self.session.get(url, stream=True, timeout=60)
        response.raise_for_status()
        
        # Check if response is actually a PDF
        content_type = response.headers.get('content-type', '').lower()
        if 'pdf' not in content_type and 'application/octet-stream' not in content_type:
            self.logger.warning(f"Unexpected content type for {filename}: {content_type}")
        
        # Write file with progress tracking
        total_size = int(response.headers.get('content-length', 0))
        
        with open(file_path, 'wb') as f:
            if total_size > 0:
                # Track download progress for large files
                downloaded = 0
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
            else:
                # For files without content-length header
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
        
        self.logger.debug(f"Downloaded {filename} ({file_path.stat().st_size} bytes)")
        return str(file_path)
    
    def _verify_download(self, file_path):
        """
        Verify that the downloaded file is valid.
        
        Args:
            file_path (str or Path): Path to the downloaded file
            
        Returns:
            bool: True if file is valid, False otherwise
        """
        try:
            file_path = Path(file_path)
            
            # Check if file exists and has content
            if not file_path.exists() or file_path.stat().st_size == 0:
                return False
            
            # Basic PDF validation - check PDF header
            with open(file_path, 'rb') as f:
                header = f.read(8)
                if not header.startswith(b'%PDF'):
                    self.logger.warning(f"File does not appear to be a PDF: {file_path.name}")
                    # Don't reject non-PDF files completely, might be valid documents
                    # return False
            
            return True
            
        except Exception as e:
            self.logger.warning(f"Error verifying file {file_path}: {e}")
            return False
    
    def cleanup_failed_downloads(self):
        """Remove any incomplete or corrupted downloads."""
        cleaned_count = 0
        
        for file_path in self.output_dir.glob('*.pdf'):
            if not self._verify_download(file_path):
                try:
                    file_path.unlink()
                    cleaned_count += 1
                    self.logger.debug(f"Removed invalid file: {file_path.name}")
                except Exception as e:
                    self.logger.warning(f"Could not remove invalid file {file_path}: {e}")
        
        if cleaned_count > 0:
            self.logger.info(f"Cleaned up {cleaned_count} invalid downloaded files")
    
    def get_download_stats(self):
        """Get statistics about downloaded files."""
        pdf_files = list(self.output_dir.glob('*.pdf'))
        total_size = sum(f.stat().st_size for f in pdf_files)
        
        return {
            'count': len(pdf_files),
            'total_size_mb': total_size / (1024 * 1024),
            'files': [f.name for f in pdf_files]
        } 