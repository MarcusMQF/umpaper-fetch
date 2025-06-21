"""
umpaper-fetch: Automated downloader for University Malaya past year exam papers.

This package provides tools to automatically download past year exam papers
from University Malaya's repository through an automated browser interface.
"""

__version__ = "1.0.3"
__author__ = "Marcus Mah"
__email__ = "marcusmah6969@gmail.com"
__description__ = "Automated downloader for University Malaya past year exam papers"

# Import main classes for easier access
from .auth.um_authenticator import UMAuthenticator
from .scraper.paper_scraper import PaperScraper
from .downloader.pdf_downloader import PDFDownloader
from .utils.zip_creator import ZipCreator
from .utils.logger import setup_logger

__all__ = [
    'UMAuthenticator',
    'PaperScraper', 
    'PDFDownloader',
    'ZipCreator',
    'setup_logger'
] 