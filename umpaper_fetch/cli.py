#!/usr/bin/env python3
"""
Command-line interface for umpaper-fetch package.

This module provides the main entry point for the um-papers command.
"""

import argparse
import getpass
import logging
import os
import sys
from pathlib import Path

from .auth.um_authenticator import UMAuthenticator
from .scraper.paper_scraper import PaperScraper
from .downloader.pdf_downloader import PDFDownloader
from .utils.zip_creator import ZipCreator
from .utils.logger import setup_logger

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        prog="python -m umpaper_fetch.cli",
        description="⬇️  UM PastYear Paper Downloader (CLI Tools)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        usage=argparse.SUPPRESS,
        epilog="""
How to run:
  python -m umpaper_fetch.cli                               # Interactive mode 
  um-papers                                                 # Alternative if install in virtual environment

Basic Examples:
  python -m umpaper_fetch.cli -s WIA1005                    # Download WIA1005 papers (will prompt for username/password)
  python -m umpaper_fetch.cli -u your_username -s WIA1006   # Pre-specify username
  python -m umpaper_fetch.cli -s CSC1025 --no-location-prompt  # Use default Downloads folder

Batch Processing:
  python -m umpaper_fetch.cli -s WIA1005 --no-location-prompt -o "./Papers/WIA1005"
  python -m umpaper_fetch.cli -s WIA1006 --no-location-prompt -o "./Papers/WIA1006"

Advanced Options:
  python -m umpaper_fetch.cli -s WIA1005 --show-browser     # Show browser for debugging
  python -m umpaper_fetch.cli -s WIA1005 --verbose          # Enable detailed logging
  python -m umpaper_fetch.cli -s WIA1005 --browser chrome   # Use specific browser
        """
    )
    
    parser.add_argument(
        '--username', '-u',
        help='UM username (without @siswa.um.edu.my)',
        type=str
    )
    
    parser.add_argument(
        '--subject-code', '-s',
        help='Subject code(s) to search for (e.g., WIA1005 WIA1006)',
        nargs='+',
        type=str
    )
    
    parser.add_argument(
        '--output-dir', '-o',
        help='Output directory for downloads (default: ~/Downloads)',
        default=str(Path.home() / 'Downloads'),
        type=str
    )
    
    parser.add_argument(
        '--no-location-prompt',
        help='Skip location prompt, use default output directory',
        action='store_true'
    )
    
    parser.add_argument(
        '--show-browser',
        help='Show browser window for debugging (default: headless)',
        action='store_true'
    )
    
    parser.add_argument(
        '--browser', '-b',
        help='Browser to use: auto, chrome, edge (default: chrome)',
        choices=['auto', 'chrome', 'edge'],
        default='chrome',
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
        help='Enable detailed debug logging',
        action='store_true'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 1.0.7'
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
    print("1. Use default location (user Downloads folder)")
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
        # Create default output directory object but don't create folder yet
        default_output_dir = Path(args.output_dir)
        # default_output_dir.mkdir(parents=True, exist_ok=True)  <-- Removed to prevent empty folder creation
        
        logger.info("=== UM Past Year Paper Downloader ===")
        
        # Get credentials
        username, password = get_credentials(args.username)
        
        # Get subject codes
        # args.subject_code is now a list of strings due to nargs='+'
        # We also support comma separation within strings
        raw_subjects = args.subject_code if args.subject_code else []
        if not raw_subjects:
             # If no subject provided via args, ask interatively (returns string)
             raw_input = get_subject_code(None)
             raw_subjects = [raw_input]
             
        subject_codes = []
        for s in raw_subjects:
            # Split by comma just in case mixed usage
            parts = [p.strip().upper() for p in s.split(',') if p.strip()]
            subject_codes.extend(parts)
            
        # Get download location (once for all)
        if args.no_location_prompt:
            base_output_dir = default_output_dir
            logger.info(f"Using default output directory: {base_output_dir.absolute()}")
        else:
            base_output_dir = get_download_location(default_output_dir)
        
        # Show configuration summary
        print(f"\n📋 Configuration Summary")
        print("="*50)
        print(f"Username: {username}")
        print(f"Subjects ({len(subject_codes)}): {', '.join(subject_codes)}")
        print(f"Output Directory: {base_output_dir.absolute()}")
        print(f"Browser: {args.browser}")
        print(f"Headless Mode: {not args.show_browser}")
        print(f"Timeout: {args.timeout}s")
        print(f"Max Retries: {args.max_retries}")
        
        # Confirm before proceeding
        print(f"\n🚀 Ready to start downloading papers for {len(subject_codes)} subjects")
        confirm = input("Continue? (y/N): ").strip().lower()
        
        if confirm not in ['y', 'yes']:
            print("❌ Operation cancelled by user")
            sys.exit(0)
        
        print("\n" + "="*60)
        print("🔄 Starting Download Process...")
        print("="*60)
        
        # Step 1: Authentication (Once for all subjects)
        logger.info("Step 1: Authenticating with UM portal...")
        authenticator = UMAuthenticator(
            headless=not args.show_browser,
            browser=args.browser,
            timeout=args.timeout
        )
        
        session = authenticator.login(username, password)
        if not session:
            logger.error("❌ Authentication failed")
            sys.exit(1)
        
        logger.info("✅ Authentication successful")
        
        # Loop through each subject
        total_downloaded = 0
        
        for index, subject_code in enumerate(subject_codes, 1):
            print(f"\n" + "="*60)
            print(f"📚 Processing Subject {index}/{len(subject_codes)}: {subject_code}")
            print("="*60)
            
            try:
                # Step 2: Search for papers
                logger.info(f"Searching for papers: {subject_code}")
                scraper = PaperScraper(session)
                papers = scraper.search_papers(subject_code)
                
                if not papers:
                    logger.warning(f"❌ No papers found for subject code: {subject_code}")
                    print(f"❌ No papers found for {subject_code}")
                    continue
                
                logger.info(f"✅ Found {len(papers)} papers for {subject_code}")
                
                # Display found papers list
                print(f"\n{'='*80}")
                print(f"📄 FOUND {len(papers)} PAST YEAR PAPERS FOR {subject_code}")
                print(f"{'='*80}")
                for i, paper in enumerate(papers, 1):
                    print(f"{i:2d}. {paper.title}")
                    print(f"    📅 Year: {paper.year}, Semester: {paper.semester}")
                    print(f"    📝 Type: {paper.paper_type}")
                    print(f"    🔗 URL: {paper.download_url}")
                    print()
                
                # Auto-confirm for batch processing if multiple subjects, or ask if single
                if len(subject_codes) > 1:
                    print(f"Batch mode: Automatically downloading {len(papers)} papers...")
                else:
                    # Provide list preview only for single subject if requested?
                    # For consistency, let's just ask confirmation for single subject
                    download_confirm = input(f"Download {len(papers)} papers? (y/N): ").strip().lower()
                    if download_confirm not in ['y', 'yes']:
                        print("❌ Download skipped by user")
                        continue

                # Prepare output directory
                output_dir = base_output_dir
                
                # Ensure output directory exists before downloading
                if not output_dir.exists():
                    try:
                        output_dir.mkdir(parents=True, exist_ok=True)
                    except Exception as e:
                        logger.error(f"Failed to create directory {output_dir}: {e}")
                        continue

                # Step 3: Download papers
                logger.info(f"Downloading {len(papers)} papers for {subject_code}...")
                downloader = PDFDownloader(session, output_dir, max_retries=args.max_retries)
                downloaded_files = downloader.download_papers(papers)
                
                if not downloaded_files:
                    print(f"❌ Failed to download papers for {subject_code}")
                    continue
                
                total_downloaded += len(downloaded_files)
                
                # Step 4: Create ZIP archive
                logger.info("Creating ZIP archive...")
                zip_creator = ZipCreator()
                zip_filename = f"{subject_code}_Past_Year_Papers.zip"
                zip_path_full = output_dir / zip_filename
                zip_path = zip_creator.create_zip(downloaded_files, str(zip_path_full), subject_code)
                
                if zip_path:
                    print(f"✅ ZIP created: {zip_filename}")
                    
                    # Ask cleanup for subject
                    print(f"📁 Individual files in: {output_dir}")
                    delete_confirm = input("Delete individual files (keep ZIP only)? (y/N): ").strip().lower()
                    if delete_confirm in ['y', 'yes']:
                        deleted_count = 0
                        for f in downloaded_files:
                            try:
                                if Path(f).exists(): 
                                    Path(f).unlink()
                                    deleted_count += 1
                            except: pass
                        print(f"✅ Individual files deleted ({deleted_count} files)")
                        
                else:
                    print("⚠️ ZIP creation failed")

            except Exception as e:
                logger.error(f"Error processing {subject_code}: {e}")
                print(f"❌ Error processing {subject_code}: {e}")
                continue
        
        # Cleanup
        authenticator.cleanup()
        
        if total_downloaded > 0:
            print("\n" + "="*60)
            if len(subject_codes) > 1:
                print(f"🎉 Batch Process Complete!")
            else:
                print(f"🎉 Download Complete!")
            print(f"Total papers downloaded: {total_downloaded}")
            print(f"Check output directory: {base_output_dir.absolute()}")
            print("="*60)
        
    except KeyboardInterrupt:
        logger.info("❌ Operation cancelled by user (Ctrl+C)")
        print("\n❌ Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
        print(f"\n❌ An error occurred: {e}")
        print("Check the logs for more details.")
        sys.exit(1)


if __name__ == "__main__":
    main() 
