"""
Paper Scraper Module

Handles searching for papers by subject code and extracting download URLs
and metadata from the UM exam paper repository.
"""

import logging
import re
from urllib.parse import urljoin, parse_qs, urlparse
from bs4 import BeautifulSoup
import requests


class PaperInfo:
    """Data class for storing paper information."""
    
    def __init__(self, title, download_url, year=None, semester=None, paper_type=None):
        self.title = title
        self.download_url = download_url
        self.year = year
        self.semester = semester
        self.paper_type = paper_type
        self.filename = self._generate_filename()
    
    def _generate_filename(self):
        """Generate a clean filename for the paper."""
        # Extract useful parts from title - remove subject code and semester/year info to avoid duplication
        title_to_clean = self.title
        
        # Remove subject code pattern from title (e.g., "WIA1005 (Semester 1, 2024)")
        title_to_clean = re.sub(r'[A-Z]{2,4}\d{4}\s*\([^)]+\)\s*', '', title_to_clean)
        
        # Clean the remaining title
        clean_title = re.sub(r'[^\w\s-]', '', title_to_clean)
        clean_title = re.sub(r'\s+', '_', clean_title.strip())
        
        # Add year and semester if available
        parts = []
        if self.year:
            parts.append(f"Y{self.year}")
        if self.semester:
            parts.append(f"S{self.semester}")
        if self.paper_type:
            parts.append(self.paper_type)
        
        if parts:
            filename = f"{'_'.join(parts)}_{clean_title}.pdf"
        else:
            filename = f"{clean_title}.pdf"
        
        # Ensure filename is not too long
        if len(filename) > 100:
            filename = filename[:95] + ".pdf"
        
        return filename
    
    def __str__(self):
        return f"PaperInfo(title='{self.title}', year={self.year}, semester={self.semester})"


class PaperScraper:
    """Scrapes exam papers from UM repository."""
    
    def __init__(self, session):
        """Initialize scraper with authenticated session."""
        self.session = session
        self.base_url = "https://exampaper-um-edu-my.eu1.proxy.openathens.net"
        self.search_url = f"{self.base_url}/cgi/search"
        self.logger = logging.getLogger(__name__)
    
    def search_papers(self, subject_code, max_results=100):
        """
        Search for papers by subject code.
        
        Args:
            subject_code (str): Subject code to search for
            max_results (int): Maximum number of results to return
            
        Returns:
            list[PaperInfo]: List of paper information objects
        """
        self.logger.info(f"Searching for papers with subject code: {subject_code}")
        
        papers = []
        
        try:
            # Use the correct search URL and parameters based on the actual form
            search_params = {
                'q': subject_code,
                '_action_search': 'Search',
                '_order': 'bytitle',
                'basic_srchtype': 'ALL',
                '_satisfyall': 'ALL'
            }
            
            self.logger.info(f"Performing search with params: {search_params}")
            
            # Perform search request using GET (like the form does)
            response = self.session.get(
                "https://exampaper-um-edu-my.eu1.proxy.openathens.net/cgi/search",
                params=search_params,
                timeout=30
            )
            
            if response.status_code != 200:
                self.logger.error(f"Search request failed: {response.status_code}")
                return papers
            
            # Parse search results
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Check if we got results
            results_text = soup.find('div', class_='ep_search_controls')
            if results_text:
                text = results_text.get_text()
                self.logger.info(f"Search results info: {text}")
                
                # Extract number of results
                import re
                match = re.search(r'(\d+)\s+of\s+(\d+)', text)
                if match:
                    total_results = int(match.group(2))
                    self.logger.info(f"Found {total_results} total results")
                else:
                    self.logger.warning("Could not determine number of results")
            
            papers = self._parse_search_results(soup, subject_code)
            
            self.logger.info(f"Successfully extracted {len(papers)} papers for {subject_code}")
            
        except Exception as e:
            self.logger.error(f"Error searching for papers: {e}")
        
        return papers[:max_results]
    
    def _parse_search_results(self, soup, subject_code):
        """Parse search results from HTML."""
        papers = []
        
        # Look for the results table
        results_table = soup.find('table', class_='ep_paginate_list')
        if not results_table:
            self.logger.warning("No results table found with class 'ep_paginate_list'")
            return papers
        
        # Find all result rows
        result_rows = results_table.find_all('tr', class_='ep_search_result')
        self.logger.info(f"Found {len(result_rows)} result rows")
        
        for i, row in enumerate(result_rows, 1):
            try:
                self.logger.info(f"Processing result {i}...")
                paper_info = self._extract_paper_info_from_row(row, subject_code)
                if paper_info:
                    papers.append(paper_info)
                    self.logger.info(f"✅ Extracted: {paper_info.title}")
                else:
                    self.logger.warning(f"❌ Could not extract info from result {i}")
            except Exception as e:
                self.logger.warning(f"Error parsing result {i}: {e}")
                continue
        
        return papers
    
    def _extract_paper_info_from_row(self, row, subject_code):
        """Extract paper information from a search result row."""
        try:
            # Get all cells in the row
            cells = row.find_all('td')
            if len(cells) < 2:
                self.logger.warning("Row doesn't have enough cells")
                return None
            
            # The main content is in the second cell
            content_cell = cells[1]
            
            # Extract the title and basic info
            # Pattern: "WIA1005 (Semester X, YEAR) Title"
            text_content = content_cell.get_text(strip=True)
            self.logger.info(f"Row content: {text_content[:100]}...")
            
            # Extract semester and year
            semester_year_match = re.search(r'\(Semester (\d+), (\d{4})\)', text_content)
            if semester_year_match:
                semester = semester_year_match.group(1)
                year = semester_year_match.group(2)
            else:
                semester = None
                year = None
                self.logger.warning("Could not extract semester/year info")
            
            # Find the main paper link (usually the title link)
            title_link = content_cell.find('a', href=True)
            if title_link:
                title = title_link.get_text(strip=True)
                # Remove italic formatting
                title = re.sub(r'[/*]', '', title)
                paper_url = urljoin(self.base_url, title_link.get('href'))
                self.logger.info(f"Found title link: {title}")
            else:
                self.logger.warning("No title link found")
                return None
            
            # Look for direct PDF download link
            download_url = None
            
            # Check the third cell (if exists) for PDF links
            if len(cells) > 2:
                pdf_cell = cells[2]
                pdf_links = pdf_cell.find_all('a', href=True)
                for link in pdf_links:
                    href = link.get('href')
                    if href and '.pdf' in href.lower():
                        download_url = urljoin(self.base_url, href)
                        self.logger.info(f"Found direct PDF link: {download_url}")
                        break
            
            # If no direct PDF link found, try to get it from the paper page
            if not download_url:
                self.logger.info("No direct PDF link found, checking paper page...")
                download_url = self._get_download_url(paper_url)
            
            if not download_url:
                self.logger.warning(f"No download URL found for: {title}")
                return None
            
            # Generate a clean title without redundant info (year/semester will be in filename prefix)
            clean_title = f"{subject_code} {title}"
            
            paper_type = self._determine_paper_type(title)
            
            return PaperInfo(
                title=clean_title,
                download_url=download_url,
                year=year,
                semester=semester,
                paper_type=paper_type
            )
            
        except Exception as e:
            self.logger.warning(f"Error extracting paper info: {e}")
            return None
    
    def _determine_paper_type(self, title):
        """Determine the type of paper from the title."""
        title_lower = title.lower()
        
        if 'final' in title_lower:
            return 'Final'
        elif 'mid' in title_lower or 'midterm' in title_lower:
            return 'Midterm'
        elif 'quiz' in title_lower:
            return 'Quiz'
        elif 'test' in title_lower:
            return 'Test'
        else:
            return 'Exam'
    
    def _get_download_url(self, paper_url):
        """Get the actual PDF download URL from the paper page."""
        try:
            self.logger.info(f"Getting download URL from: {paper_url}")
            response = self.session.get(paper_url, timeout=15)
            if response.status_code != 200:
                self.logger.warning(f"Failed to access paper page: {response.status_code}")
                return None
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Method 1: Look for direct PDF download links
            download_links = soup.find_all('a', href=True)
            
            for link in download_links:
                href = link.get('href')
                link_text = link.get_text(strip=True).lower()
                
                # Look for PDF files or download links
                if href and ('.pdf' in href.lower() or 
                           'download' in href.lower() or 
                           'download' in link_text or
                           'pdf' in link_text):
                    download_url = urljoin(self.base_url, href)
                    self.logger.info(f"Found download link: {download_url}")
                    return download_url
            
            # Method 2: Look for repository-specific patterns
            # UM repository often uses /id/eprint/XXXXX/1/filename.pdf
            eprint_links = soup.find_all('a', href=re.compile(r'/\d+/\d+/.*\.pdf$', re.I))
            if eprint_links:
                download_url = urljoin(self.base_url, eprint_links[0].get('href'))
                self.logger.info(f"Found eprint PDF: {download_url}")
                return download_url
            
            # Method 3: Look for any PDF links
            pdf_links = soup.find_all('a', href=re.compile(r'\.pdf$', re.I))
            if pdf_links:
                download_url = urljoin(self.base_url, pdf_links[0].get('href'))
                self.logger.info(f"Found PDF link: {download_url}")
                return download_url
            
            # Method 4: Check for embedded objects or iframes
            objects = soup.find_all(['object', 'embed', 'iframe'])
            for obj in objects:
                src = obj.get('src') or obj.get('data')
                if src and '.pdf' in src.lower():
                    download_url = urljoin(self.base_url, src)
                    self.logger.info(f"Found embedded PDF: {download_url}")
                    return download_url
            
            self.logger.warning(f"No download URL found on page: {paper_url}")
        
        except Exception as e:
            self.logger.warning(f"Error getting download URL for {paper_url}: {e}")
        
        return None 