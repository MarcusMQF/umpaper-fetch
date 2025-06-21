#!/usr/bin/env python3
"""
UM Past Year Paper Downloader - Main Entry Point

This script provides a command-line interface for downloading all past year
exam papers for a given subject code from University Malaya's repository.
"""

import argparse
import getpass
import logging
import os
import sys
from pathlib import Path

from auth.um_authenticator import UMAuthenticator
from scraper.paper_scraper import PaperScraper
from downloader.pdf_downloader import PDFDownloader
from utils.zip_creator import ZipCreator
from utils.logger import setup_logger


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Download all past year papers for a UM subject code",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py
  python main.py --username siti_laila --subject-code WIA1005
  python main.py --username john_doe --subject-code WXES1116 --show-browser
  python main.py --no-location-prompt --output-dir "C:/Downloads"
        """
    )
    
    parser.add_argument(
        '--username', '-u',
        help='UM username (without @siswa.um.edu.my)',
        type=str
    )
    
    parser.add_argument(
        '--subject-code', '-s',
        help='Subject code to search for (e.g., WIA1005)',
        type=str
    )
    
    parser.add_argument(
        '--output-dir', '-o',
        help='Output directory for downloads (default: ./downloads)',
        default='./downloads',
        type=str
    )
    
    parser.add_argument(
        '--no-location-prompt',
        help='Skip location selection prompt and use default output directory',
        action='store_true'
    )
    
    parser.add_argument(
        '--show-browser',
        help='Show browser window (default is headless mode)',
        action='store_true'
    )
    
    parser.add_argument(
        '--browser', '-b',
        help='Browser to use (auto, chrome, edge). Default: edge',
        choices=['auto', 'chrome', 'edge'],
        default='edge',
        type=str
    )
    
    parser.add_argument(
        '--timeout',
        help='Session timeout in seconds (default: 30)',
        default=30,
        type=int
    )
    
    parser.add_argument(
        '--max-retries',
        help='Maximum retry attempts (default: 3)',
        default=3,
        type=int
    )
    
    parser.add_argument(
        '--verbose', '-v',
        help='Enable verbose logging',
        action='store_true'
    )
    
    return parser.parse_args()


def get_credentials(username=None):
    """Get user credentials securely."""
    if not username:
        username = input("Enter your UM username (without @siswa.um.edu.my): ").strip()
    
    if not username:
        print("Error: Username cannot be empty")
        sys.exit(1)
    
    password = getpass.getpass("Enter your UM password: ")
    
    if not password:
        print("Error: Password cannot be empty")
        sys.exit(1)
    
    return username, password


def get_subject_code(subject_code=None):
    """Get subject code from user."""
    if not subject_code:
        subject_code = input("Enter subject code (e.g., WIA1005): ").strip().upper()
    
    if not subject_code:
        print("Error: Subject code cannot be empty")
        sys.exit(1)
    
    return subject_code


def get_download_location(default_output_dir):
    """
    Get custom download location from user.
    
    Args:
        default_output_dir (Path): Default output directory
        
    Returns:
        Path: User-chosen download location or default
    """
    print(f"\n📂 Download Location Settings")
    print("="*50)
    print(f"Default location: {default_output_dir.absolute()}")
    print("\nOptions:")
    print("1. Use default location (project downloads folder)")
    print("2. Choose custom location")
    
    while True:
        choice = input("\nSelect option (1 or 2): ").strip()
        
        if choice == '1':
            print(f"✅ Using default location: {default_output_dir.absolute()}")
            return default_output_dir
        
        elif choice == '2':
            while True:
                custom_path = input("\nEnter custom download path: ").strip()
                
                if not custom_path:
                    print("❌ Path cannot be empty. Please try again.")
                    continue
                
                try:
                    # Convert to Path object and expand user home directory (~)
                    custom_dir = Path(custom_path).expanduser()
                    
                    # Try to create the directory if it doesn't exist
                    custom_dir.mkdir(parents=True, exist_ok=True)
                    
                    # Test if we can write to this directory
                    test_file = custom_dir / "test_write.tmp"
                    try:
                        test_file.write_text("test")
                        test_file.unlink()  # Delete test file
                        print(f"✅ Custom location set: {custom_dir.absolute()}")
                        return custom_dir
                    except Exception as write_error:
                        print(f"❌ Cannot write to this location: {write_error}")
                        print("Please choose a different path or check permissions.")
                        
                except Exception as path_error:
                    print(f"❌ Invalid path: {path_error}")
                    print("Please enter a valid directory path.")
        
        else:
            print("❌ Please enter '1' or '2'.")


def main():
    """Main execution function."""
    args = parse_arguments()
    
    # Setup logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logger = setup_logger(log_level)
    
    try:
        # Create default output directory
        default_output_dir = Path(args.output_dir)
        default_output_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info("=== UM Past Year Paper Downloader ===")
        
        # Get credentials and subject code first
        username, password = get_credentials(args.username)
        subject_code = get_subject_code(args.subject_code)
        
        # Get download location (with user choice, unless skipped)
        if args.no_location_prompt:
            output_dir = default_output_dir
            logger.info(f"Download location (default): {output_dir.absolute()}")
        else:
            output_dir = get_download_location(default_output_dir)
            logger.info(f"Download location: {output_dir.absolute()}")
        
        # Determine headless mode (default is True unless --show-browser is specified)
        headless_mode = not args.show_browser
        
        logger.info(f"Username: {username}")
        logger.info(f"Subject code: {subject_code}")
        logger.info(f"Browser: {args.browser}")
        logger.info(f"Headless mode: {headless_mode}")
        
        # Step 1: Authenticate with UM system
        logger.info("Step 1: Authenticating with UM system...")
        authenticator = UMAuthenticator(
            headless=headless_mode,
            timeout=args.timeout,
            browser=args.browser
        )
        
        session = authenticator.login(username, password)
        logger.info("✓ Authentication successful")
        
        # Step 2: Search for papers
        logger.info(f"Step 2: Searching for papers with subject code '{subject_code}'...")
        scraper = PaperScraper(session)
        papers = scraper.search_papers(subject_code)
        
        if not papers:
            logger.error(f"No papers found for subject code: {subject_code}")
            sys.exit(3)
        
        logger.info(f"✓ Found {len(papers)} papers")
        
        # Display found papers to user
        print("\n" + "="*80)
        print(f"📄 FOUND {len(papers)} PAST YEAR PAPERS FOR {subject_code}")
        print("="*80)
        
        for i, paper in enumerate(papers, 1):
            print(f"{i:2d}. {paper.title}")
            if paper.year and paper.semester:
                print(f"    📅 Year: {paper.year}, Semester: {paper.semester}")
            if paper.paper_type:
                print(f"    📝 Type: {paper.paper_type}")
            print(f"    🔗 URL: {paper.download_url}")
            print()
        
        print("="*80)
        
        # Ask user for confirmation
        while True:
            choice = input(f"\n💾 Do you want to download all {len(papers)} papers? (y/N): ").strip().lower()
            if choice in ['y', 'yes']:
                break
            elif choice in ['n', 'no', '']:  # Empty input defaults to 'no'
                print("Download cancelled by user.")
                sys.exit(0)
            else:
                print("Please enter 'y' for yes or 'N' for no.")
        
        # Step 3: Download papers to user-chosen location
        logger.info("Step 3: Downloading papers...")
        downloader = PDFDownloader(
            session=session,
            output_dir=output_dir,
            max_retries=args.max_retries
        )
        
        downloaded_files = downloader.download_papers(papers)
        
        if not downloaded_files:
            logger.error("No papers were successfully downloaded")
            sys.exit(3)
        
        logger.info(f"✓ Downloaded {len(downloaded_files)} papers")
        
        # Step 4: Create ZIP file in user-chosen location
        logger.info("Step 4: Creating ZIP archive...")
        zip_creator = ZipCreator()
        zip_path = output_dir / f"{subject_code}_past_years.zip"
        
        zip_result = zip_creator.create_zip(downloaded_files, zip_path, subject_code)
        if zip_result:
            logger.info(f"✓ ZIP file created: {zip_path.absolute()}")
        else:
            logger.error("Failed to create ZIP file")
            sys.exit(3)
        
        # Cleanup individual files (optional)
        print(f"\n🧹 Cleanup Options")
        print(f"Individual PDF files and ZIP file are both in: {output_dir.absolute()}")
        cleanup = input("\nDelete individual PDF files (keep only ZIP)? (y/N): ").strip().lower()
        if cleanup in ['y', 'yes']:
            for file_path in downloaded_files:
                try:
                    os.remove(file_path)
                    logger.debug(f"Deleted: {file_path}")
                except Exception as e:
                    logger.warning(f"Could not delete {file_path}: {e}")
            logger.info("✓ Individual PDF files cleaned up (ZIP file preserved)")
        
        logger.info("=== Download Complete ===")
        logger.info(f"ZIP file location: {zip_path.absolute()}")
        logger.info(f"Total papers downloaded: {len(downloaded_files)}")
        
    except KeyboardInterrupt:
        logger.info("\nOperation cancelled by user")
        sys.exit(130)
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        if args.verbose:
            logger.exception("Full error details:")
        sys.exit(1)
    finally:
        # Cleanup browser session
        try:
            if 'authenticator' in locals():
                authenticator.cleanup()
        except:
            pass


if __name__ == '__main__':
    main() 