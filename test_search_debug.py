#!/usr/bin/env python3
"""
Search Debug Script

Tests the search functionality to see what HTML structure we get
from the UM exam paper repository.
"""

import getpass
import sys
from pathlib import Path
import requests
from bs4 import BeautifulSoup

# Add project root to path
sys.path.append(str(Path(__file__).parent))

from auth.um_authenticator import UMAuthenticator
from utils.logger import setup_logger


def debug_search():
    """Debug the search functionality."""
    
    print("UM Search Debug Tool")
    print("=" * 50)
    
    # Setup logging
    logger = setup_logger()
    
    # Get credentials
    username = input("Enter your UM username (without @siswa.um.edu.my): ").strip()
    password = getpass.getpass("Enter your UM password: ")
    subject_code = input("Enter subject code to search (e.g., WIA1005): ").strip().upper()
    
    if not all([username, password, subject_code]):
        print("Error: All fields are required")
        return False
    
    print(f"\n🔍 Debugging search for: {subject_code}")
    
    # Authenticate
    print("🔐 Authenticating...")
    try:
        authenticator = UMAuthenticator(headless=True, browser='edge')
        session = authenticator.login(username, password)
        print("✅ Authentication successful")
    except Exception as e:
        print(f"❌ Authentication failed: {e}")
        return False
    
    try:
        base_url = "https://exampaper-um-edu-my.eu1.proxy.openathens.net"
        
        # Step 1: Access the main repository page
        print("\n📄 Accessing main repository page...")
        main_response = session.get(f"{base_url}/", timeout=30)
        print(f"Main page status: {main_response.status_code}")
        
        if main_response.status_code == 200:
            main_soup = BeautifulSoup(main_response.content, 'html.parser')
            title = main_soup.find('title')
            print(f"Page title: {title.text if title else 'No title'}")
            
            # Look for search form
            search_forms = main_soup.find_all('form')
            print(f"Found {len(search_forms)} forms on main page")
            
            for i, form in enumerate(search_forms):
                action = form.get('action', 'No action')
                method = form.get('method', 'GET')
                print(f"  Form {i+1}: action='{action}', method='{method}'")
                
                # Find search input
                search_inputs = form.find_all('input', {'name': 'q'})
                if search_inputs:
                    print(f"    Found search input: {search_inputs[0]}")
        
        # Step 2: Try direct search
        print(f"\n🔍 Performing search for '{subject_code}'...")
        
        # Try the search form submission
        search_url = f"{base_url}/cgi/search"
        
        # Method 1: Simple GET request
        search_params = {'q': subject_code}
        search_response = session.get(search_url, params=search_params, timeout=30)
        print(f"GET search status: {search_response.status_code}")
        
        if search_response.status_code == 200:
            print("✅ Search request successful")
            
            # Save response for debugging
            with open('search_response.html', 'w', encoding='utf-8') as f:
                f.write(search_response.text)
            print("💾 Saved search response to 'search_response.html'")
            
            # Parse search results
            soup = BeautifulSoup(search_response.content, 'html.parser')
            
            # Look for result indicators
            page_text = soup.get_text()
            
            # Check for "Item matches" text
            if "Item matches" in page_text:
                print("✅ Found 'Item matches' - search returned results")
                
                # Extract the number of results
                import re
                matches = re.search(r'Displaying results (\d+) to (\d+) of (\d+)', page_text)
                if matches:
                    start, end, total = matches.groups()
                    print(f"📊 Results: {start} to {end} of {total} total")
                else:
                    print("⚠️  Could not parse result count")
            
            # Look for numbered results (1., 2., etc.)
            numbered_results = re.findall(r'^\s*(\d+)\.\s+(.+?)$', page_text, re.MULTILINE)
            print(f"📝 Found {len(numbered_results)} numbered results")
            
            for i, (num, text) in enumerate(numbered_results[:5]):  # Show first 5
                print(f"  {num}. {text[:100]}...")
            
            # Look for links that might be papers
            all_links = soup.find_all('a', href=True)
            paper_links = []
            
            for link in all_links:
                href = link.get('href')
                text = link.get_text(strip=True)
                
                # Skip navigation links
                if any(skip in href.lower() for skip in ['search', 'browse', 'help', 'home', 'about']):
                    continue
                
                # Look for subject code in link text
                if subject_code.lower() in text.lower():
                    paper_links.append((text, href))
            
            print(f"🔗 Found {len(paper_links)} potential paper links")
            for i, (text, href) in enumerate(paper_links[:3]):  # Show first 3
                print(f"  Link {i+1}: {text[:80]}...")
                print(f"    URL: {href}")
            
            # Look for table structure
            tables = soup.find_all('table')
            print(f"📊 Found {len(tables)} tables")
            
            for i, table in enumerate(tables):
                rows = table.find_all('tr')
                if len(rows) > 1:  # Skip empty tables
                    print(f"  Table {i+1}: {len(rows)} rows")
                    
                    # Check if this looks like results table
                    first_row_text = rows[0].get_text(strip=True)
                    if subject_code.lower() in first_row_text.lower():
                        print(f"    ✅ Table {i+1} contains subject code")
        
        else:
            print(f"❌ Search failed with status: {search_response.status_code}")
            print(f"Response: {search_response.text[:500]}")
        
        return True
        
    except Exception as e:
        print(f"❌ Search debug failed: {e}")
        return False
    
    finally:
        if 'authenticator' in locals():
            authenticator.cleanup()


if __name__ == '__main__':
    try:
        debug_search()
    except KeyboardInterrupt:
        print("\n\nDebug cancelled by user")
    except Exception as e:
        print(f"Debug script error: {e}") 