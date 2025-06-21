#!/usr/bin/env python3
"""
Setup Test Script

This script tests if all dependencies and requirements are properly installed
and working for the UM Past Year Paper Downloader.
"""

import sys
import subprocess
from pathlib import Path


def test_python_version():
    """Test if Python version is compatible."""
    print("Testing Python version...")
    
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✓ Python {version.major}.{version.minor}.{version.micro} is compatible")
        return True
    else:
        print(f"✗ Python {version.major}.{version.minor}.{version.micro} is not compatible")
        print("  Please upgrade to Python 3.8 or higher")
        return False


def test_package_imports():
    """Test if all required packages can be imported."""
    print("\nTesting package imports...")
    
    packages = [
        ('selenium', 'Selenium WebDriver'),
        ('requests', 'HTTP requests library'),
        ('bs4', 'BeautifulSoup4 HTML parser'),
        ('webdriver_manager', 'WebDriver Manager'),
        ('tqdm', 'Progress bar library'),
    ]
    
    all_passed = True
    
    for package, description in packages:
        try:
            __import__(package)
            print(f"✓ {description} imported successfully")
        except ImportError as e:
            print(f"✗ Failed to import {description}: {e}")
            print(f"  Install with: pip install {package}")
            all_passed = False
    
    return all_passed


def test_browser_availability():
    """Test if browsers are available."""
    print("\nTesting browser availability...")
    
    browsers_tested = {}
    
    # Test Edge (priority for Windows users)
    try:
        import platform
        if platform.system() == "Windows":
            print("  Testing Microsoft Edge...")
            from selenium import webdriver
            from selenium.webdriver.edge.options import Options as EdgeOptions
            from webdriver_manager.microsoft import EdgeChromiumDriverManager
            
            edge_options = EdgeOptions()
            edge_options.add_argument('--headless')
            edge_options.add_argument('--no-sandbox')
            edge_options.add_argument('--disable-dev-shm-usage')
            
            from selenium.webdriver.edge.service import Service as EdgeService
            driver = webdriver.Edge(
                service=EdgeService(EdgeChromiumDriverManager().install()),
                options=edge_options
            )
            driver.get("https://www.google.com")
            driver.quit()
            print("✓ Microsoft Edge browser and WebDriver are working")
            browsers_tested['edge'] = True
        else:
            print("  Microsoft Edge test skipped (not Windows)")
            browsers_tested['edge'] = None
    except Exception as e:
        print(f"✗ Microsoft Edge test failed: {e}")
        browsers_tested['edge'] = False
    
    # Test Chrome
    try:
        print("  Testing Google Chrome...")
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options as ChromeOptions
        from webdriver_manager.chrome import ChromeDriverManager
        
        chrome_options = ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        
        from selenium.webdriver.chrome.service import Service as ChromeService
        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=chrome_options
        )
        driver.get("https://www.google.com")
        driver.quit()
        print("✓ Google Chrome browser and WebDriver are working")
        browsers_tested['chrome'] = True
    except Exception as e:
        print(f"✗ Google Chrome test failed: {e}")
        browsers_tested['chrome'] = False
    

    
    # Summary
    working_browsers = [name for name, status in browsers_tested.items() if status is True]
    if working_browsers:
        print(f"✓ Working browsers: {', '.join(working_browsers)}")
        return True
    else:
        print("✗ No browsers are working properly")
        print("  Please install at least one of: Chrome or Edge")
        print("  Downloads:")
        print("    - Chrome: https://www.google.com/chrome/")
        print("    - Edge: https://www.microsoft.com/edge")
        return False


def test_network_connectivity():
    """Test network connectivity to UM servers."""
    print("\nTesting network connectivity...")
    
    try:
        import requests
        
        # Test general internet connectivity
        response = requests.get("https://www.google.com", timeout=10)
        if response.status_code == 200:
            print("✓ Internet connectivity is working")
        else:
            print("✗ Internet connectivity issue")
            return False
        
        # Test UM server accessibility (may require VPN)
        print("  Testing UM server accessibility...")
        try:
            response = requests.get(
                "https://proxy.openathens.net",
                timeout=10,
                allow_redirects=True
            )
            print("✓ UM OpenAthens proxy is accessible")
        except Exception as e:
            print(f"⚠ UM server may require VPN or campus network: {e}")
            print("  This is normal if you're not on campus network")
        
        return True
        
    except Exception as e:
        print(f"✗ Network connectivity test failed: {e}")
        return False


def test_file_permissions():
    """Test file system permissions."""
    print("\nTesting file system permissions...")
    
    try:
        # Test write permissions in current directory
        test_file = Path("test_write_permission.tmp")
        test_file.write_text("test")
        test_file.unlink()
        print("✓ Write permissions in current directory")
        
        # Test creating downloads directory
        downloads_dir = Path("downloads")
        downloads_dir.mkdir(exist_ok=True)
        print("✓ Can create downloads directory")
        
        # Test creating logs directory
        logs_dir = Path("logs")
        logs_dir.mkdir(exist_ok=True)
        print("✓ Can create logs directory")
        
        return True
        
    except Exception as e:
        print(f"✗ File system permissions test failed: {e}")
        return False


def test_module_imports():
    """Test if custom modules can be imported."""
    print("\nTesting custom module imports...")
    
    modules = [
        ('auth.um_authenticator', 'UM Authenticator'),
        ('scraper.paper_scraper', 'Paper Scraper'),
        ('downloader.pdf_downloader', 'PDF Downloader'),
        ('utils.zip_creator', 'ZIP Creator'),
        ('utils.logger', 'Logger'),
    ]
    
    all_passed = True
    
    for module, description in modules:
        try:
            __import__(module)
            print(f"✓ {description} module imported successfully")
        except ImportError as e:
            print(f"✗ Failed to import {description}: {e}")
            all_passed = False
    
    return all_passed


def main():
    """Run all tests."""
    print("UM Past Year Paper Downloader - Setup Test")
    print("=" * 50)
    
    tests = [
        ("Python Version", test_python_version),
        ("Package Imports", test_package_imports),
        ("Browser Availability", test_browser_availability),
        ("Network Connectivity", test_network_connectivity),
        ("File Permissions", test_file_permissions),
        ("Custom Modules", test_module_imports),
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"✗ {test_name} test crashed: {e}")
            results[test_name] = False
    
    # Summary
    print("\n" + "=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)
    
    passed = sum(results.values())
    total = len(results)
    
    for test_name, result in results.items():
        status = "PASS" if result else "FAIL"
        print(f"{test_name:<20} : {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Your setup is ready.")
        print("You can now run the main script with: python main.py")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed.")
        print("Please resolve the issues above before running the main script.")
        print("\nCommon solutions:")
        print("1. Install missing packages: pip install -r requirements.txt")
        print("2. Install Chrome browser if missing")
        print("3. Check network connectivity and VPN if needed")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(main()) 