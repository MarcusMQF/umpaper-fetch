"""
ZIP Creator Module

Creates organized ZIP archives with proper file naming and structure.
"""

import logging
import zipfile
from pathlib import Path
import os


class ZipCreator:
    """Creates organized ZIP archives from downloaded papers."""
    
    def __init__(self):
        """Initialize the ZIP creator."""
        self.logger = logging.getLogger(__name__)
    
    def create_zip(self, file_paths, zip_path, subject_code):
        """
        Create a ZIP archive from downloaded files.
        
        Args:
            file_paths (list): List of file paths to include
            zip_path (str or Path): Output ZIP file path
            subject_code (str): Subject code for organization
            
        Returns:
            str: Path to created ZIP file
        """
        zip_path = Path(zip_path)
        
        if not file_paths:
            self.logger.warning("No files to zip")
            return None
        
        self.logger.info(f"Creating ZIP archive: {zip_path.name}")
        
        try:
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as zipf:
                # Organize files by year and semester
                organized_files = self._organize_files(file_paths)
                
                # Add files to ZIP with organized structure
                for file_path in file_paths:
                    file_path = Path(file_path)
                    
                    if not file_path.exists():
                        self.logger.warning(f"File not found, skipping: {file_path}")
                        continue
                    
                    # Determine archive path based on organization
                    archive_path = self._get_archive_path(file_path, subject_code, organized_files)
                    
                    # Add file to ZIP
                    zipf.write(file_path, archive_path)
                    self.logger.debug(f"Added to ZIP: {archive_path}")
                
                # Add a README file with information
                readme_content = self._generate_readme(subject_code, file_paths)
                zipf.writestr(f"{subject_code}_README.txt", readme_content)
            
            # Verify ZIP was created successfully
            if zip_path.exists() and zip_path.stat().st_size > 0:
                self.logger.info(f"ZIP archive created successfully: {zip_path}")
                self.logger.info(f"Archive size: {zip_path.stat().st_size / (1024*1024):.2f} MB")
                return str(zip_path)
            else:
                self.logger.error("ZIP archive creation failed")
                return None
                
        except Exception as e:
            self.logger.error(f"Error creating ZIP archive: {e}")
            return None
    
    def _organize_files(self, file_paths):
        """
        Organize files by extracting year and semester information.
        
        Args:
            file_paths (list): List of file paths
            
        Returns:
            dict: Dictionary mapping file paths to organization info
        """
        organized = {}
        
        for file_path in file_paths:
            file_path = Path(file_path)
            filename = file_path.name
            
            # Extract year and semester from filename
            year = self._extract_year_from_filename(filename)
            semester = self._extract_semester_from_filename(filename)
            paper_type = self._extract_paper_type_from_filename(filename)
            
            organized[str(file_path)] = {
                'year': year,
                'semester': semester,
                'paper_type': paper_type,
                'original_name': str(filename)
            }
        
        return organized
    
    def _get_archive_path(self, file_path, subject_code, organized_files):
        """
        Get the archive path for a file within the ZIP.
        
        Args:
            file_path (Path): Original file path
            subject_code (str): Subject code
            organized_files (dict): Organization information
            
        Returns:
            str: Path within the ZIP archive
        """
        file_info = organized_files.get(str(file_path), {})
        
        # Build hierarchical path: SubjectCode/Year/filename (simplified structure)
        path_parts = [subject_code]
        
        year = file_info.get('year')
        
        if year:
            path_parts.append(f"Year_{year}")
        else:
            # If no year info, put in "Unsorted" folder
            path_parts.append("Unsorted")
        
        # Use original filename or clean it up
        filename = file_info.get('original_name', file_path.name)
        path_parts.append(filename)
        
        return '/'.join(str(part) for part in path_parts)
    
    def _extract_year_from_filename(self, filename):
        """Extract year from filename."""
        import re
        
        # Look for 4-digit year (20xx)
        year_match = re.search(r'(20\d{2})', filename)
        if year_match:
            return year_match.group(1)
        
        # Look for Y followed by year
        year_match = re.search(r'Y(20\d{2}|0\d|1\d|2\d)', filename)
        if year_match:
            year = year_match.group(1)
            if len(year) == 2:
                # Convert 2-digit to 4-digit year
                year_int = int(year)
                if year_int <= 30:  # Assume 00-30 means 2000-2030
                    return f"20{year}"
                else:  # 31-99 means 1931-1999
                    return f"19{year}"
            return year
        
        return None
    
    def _extract_semester_from_filename(self, filename):
        """Extract semester from filename."""
        import re
        
        filename_lower = filename.lower()
        
        # Look for S1, S2, Sem1, Sem2, Semester 1, etc.
        if re.search(r's1|sem1|semester\s*1', filename_lower):
            return '1'
        elif re.search(r's2|sem2|semester\s*2', filename_lower):
            return '2'
        elif re.search(r's3|sem3|semester\s*3', filename_lower):
            return '3'
        
        return None
    
    def _extract_paper_type_from_filename(self, filename):
        """Extract paper type from filename."""
        filename_lower = filename.lower()
        
        if 'final' in filename_lower:
            return 'Final_Exam'
        elif any(word in filename_lower for word in ['mid', 'midterm']):
            return 'Midterm_Exam'
        elif 'quiz' in filename_lower:
            return 'Quiz'
        elif 'test' in filename_lower:
            return 'Test'
        elif 'assignment' in filename_lower:
            return 'Assignment'
        
        return 'Exam'
    
    def _generate_readme(self, subject_code, file_paths):
        """Generate README content for the ZIP archive."""
        content = f"""
{subject_code} Past Year Papers
===============================

This archive contains past year examination papers for {subject_code}.

Archive Contents:
- Total files: {len(file_paths)}
- Subject: {subject_code}
- Downloaded: {self._get_current_timestamp()}

File Organization:
- Files are organized by Year only
- Naming convention: Year_Semester_Type_Title.pdf

Usage Instructions:
1. Extract the archive to your desired location
2. Papers are organized in folders by year
3. Each year folder contains all papers for that year
4. File names include the year, semester, and exam type for identification

Notes:
- All papers are in PDF format
- Files maintain their original names with additional organization metadata
- This archive was created using the UM Past Year Paper Downloader tool

For questions or issues, please refer to the tool documentation.

Generated by UM Past Year Paper Downloader
==========================================
"""
        return content.strip()
    
    def _get_current_timestamp(self):
        """Get current timestamp as string."""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def verify_zip(self, zip_path):
        """
        Verify that the ZIP file is valid and contains expected files.
        
        Args:
            zip_path (str or Path): Path to ZIP file
            
        Returns:
            bool: True if ZIP is valid, False otherwise
        """
        try:
            zip_path = Path(zip_path)
            
            if not zip_path.exists():
                return False
            
            with zipfile.ZipFile(zip_path, 'r') as zipf:
                # Test the ZIP file
                bad_file = zipf.testzip()
                if bad_file:
                    self.logger.error(f"Corrupted file in ZIP: {bad_file}")
                    return False
                
                # Check if ZIP has content
                file_list = zipf.namelist()
                if not file_list:
                    self.logger.error("ZIP file is empty")
                    return False
                
                self.logger.info(f"ZIP verification successful: {len(file_list)} files")
                return True
                
        except Exception as e:
            self.logger.error(f"Error verifying ZIP file: {e}")
            return False
    
    def extract_zip_info(self, zip_path):
        """
        Extract information about the ZIP archive.
        
        Args:
            zip_path (str or Path): Path to ZIP file
            
        Returns:
            dict: Information about the ZIP archive
        """
        try:
            zip_path = Path(zip_path)
            
            with zipfile.ZipFile(zip_path, 'r') as zipf:
                file_list = zipf.namelist()
                total_size = sum(info.file_size for info in zipf.infolist())
                compressed_size = zip_path.stat().st_size
                
                return {
                    'file_count': len(file_list),
                    'total_uncompressed_size_mb': total_size / (1024 * 1024),
                    'compressed_size_mb': compressed_size / (1024 * 1024),
                    'compression_ratio': (1 - compressed_size / total_size) * 100 if total_size > 0 else 0,
                    'files': file_list
                }
        
        except Exception as e:
            self.logger.error(f"Error extracting ZIP info: {e}")
            return None 