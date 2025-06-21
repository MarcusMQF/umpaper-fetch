#!/usr/bin/env python3
"""
Example Usage Script

This script demonstrates how to use the UM Past Year Paper Downloader
programmatically without command-line interaction.
"""

import logging
from pathlib import Path

from auth.um_authenticator import UMAuthenticator
from scraper.paper_scraper import PaperScraper
from downloader.pdf_downloader import PDFDownloader
from utils.zip_creator import ZipCreator
from utils.logger import setup_logger


def download_papers_example():
    """Example function showing how to download papers programmatically."""
    
    # Setup logging
    logger = setup_logger(logging.INFO)
    
    # Configuration - UPDATE THESE VALUES
    USERNAME = "your_username"  # Your UM username (without @siswa.um.edu.my)
    PASSWORD = "your_password"  # Your UM password
    SUBJECT_CODE = "WIA1005"    # Subject code to download
    OUTPUT_DIR = "./downloads"  # Output directory
    
    # IMPORTANT: Replace the values above with your actual credentials
    # For security, consider using environment variables or a config file
    
    if USERNAME == "your_username" or PASSWORD == "your_password":
        logger.error("Please update the USERNAME and PASSWORD in this script!")
        logger.error("Replace 'your_username' and 'your_password' with your actual credentials")
        return False
    
    try:
        # Create output directory
        output_dir = Path(OUTPUT_DIR)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Starting download for subject: {SUBJECT_CODE}")
        
        # Step 1: Authenticate
        logger.info("Step 1: Authenticating...")
        authenticator = UMAuthenticator(
            headless=True,  # Run in headless mode
            browser='auto'  # Use auto-detection, or specify 'edge', 'chrome', 'firefox'
        )
        session = authenticator.login(USERNAME, PASSWORD)
        logger.info("✓ Authentication successful")
        
        # Step 2: Search for papers
        logger.info("Step 2: Searching for papers...")
        scraper = PaperScraper(session)
        papers = scraper.search_papers(SUBJECT_CODE)
        
        if not papers:
            logger.error(f"No papers found for {SUBJECT_CODE}")
            return False
        
        logger.info(f"✓ Found {len(papers)} papers")
        
        # Step 3: Download papers
        logger.info("Step 3: Downloading papers...")
        downloader = PDFDownloader(session, output_dir)
        downloaded_files = downloader.download_papers(papers)
        
        if not downloaded_files:
            logger.error("No papers were downloaded")
            return False
        
        logger.info(f"✓ Downloaded {len(downloaded_files)} papers")
        
        # Step 4: Create ZIP
        logger.info("Step 4: Creating ZIP archive...")
        zip_creator = ZipCreator()
        zip_path = output_dir / f"{SUBJECT_CODE}_past_years.zip"
        
        zip_creator.create_zip(downloaded_files, zip_path, SUBJECT_CODE)
        logger.info(f"✓ ZIP created: {zip_path}")
        
        # Step 5: Show results
        logger.info("=== Download Complete ===")
        logger.info(f"Subject: {SUBJECT_CODE}")
        logger.info(f"Papers downloaded: {len(downloaded_files)}")
        logger.info(f"ZIP file: {zip_path.absolute()}")
        
        return True
        
    except Exception as e:
        logger.error(f"Error during download: {e}")
        return False
    
    finally:
        # Cleanup
        try:
            if 'authenticator' in locals():
                authenticator.cleanup()
        except:
            pass


def download_multiple_subjects():
    """Example: Download papers for multiple subjects."""
    
    # Configuration
    USERNAME = "your_username"
    PASSWORD = "your_password"
    SUBJECT_CODES = ["WIA1005", "WXES1116", "WXES1112"]  # Add your subject codes
    
    if USERNAME == "your_username":
        print("Please update the credentials in this function!")
        return
    
    logger = setup_logger(logging.INFO)
    authenticator = None
    
    try:
        # Authenticate once
        authenticator = UMAuthenticator(headless=True, browser='auto')
        session = authenticator.login(USERNAME, PASSWORD)
        
        # Download each subject
        for subject_code in SUBJECT_CODES:
            logger.info(f"\n=== Processing {subject_code} ===")
            
            # Search and download
            scraper = PaperScraper(session)
            papers = scraper.search_papers(subject_code)
            
            if papers:
                output_dir = Path(f"./downloads/{subject_code}")
                downloader = PDFDownloader(session, output_dir)
                downloaded_files = downloader.download_papers(papers)
                
                if downloaded_files:
                    zip_creator = ZipCreator()
                    zip_path = output_dir / f"{subject_code}_past_years.zip"
                    zip_creator.create_zip(downloaded_files, zip_path, subject_code)
                    logger.info(f"✓ {subject_code}: {len(downloaded_files)} papers")
                else:
                    logger.warning(f"✗ {subject_code}: No papers downloaded")
            else:
                logger.warning(f"✗ {subject_code}: No papers found")
    
    except Exception as e:
        logger.error(f"Error: {e}")
    
    finally:
        if authenticator:
            authenticator.cleanup()


if __name__ == '__main__':
    print("UM Past Year Paper Downloader - Example Usage")
    print("=" * 50)
    print()
    print("This script demonstrates programmatic usage.")
    print("Please update the USERNAME and PASSWORD variables before running.")
    print()
    print("Available examples:")
    print("1. Single subject download")
    print("2. Multiple subjects download")
    print()
    
    choice = input("Select example (1 or 2): ").strip()
    
    if choice == "1":
        download_papers_example()
    elif choice == "2":
        download_multiple_subjects()
    else:
        print("Invalid choice. Please run again and select 1 or 2.") 