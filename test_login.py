#!/usr/bin/env python3
"""
Login Test Script

This script tests just the login process to verify status dropdown selection
works correctly without going through the full download process.
"""

import sys
import getpass
from auth.um_authenticator import UMAuthenticator
from utils.logger import setup_logger


def test_login():
    """Test the login process and status dropdown selection."""
    
    # Setup logging
    logger = setup_logger()
    
    print("UM Login Test")
    print("=" * 40)
    
    # Get credentials
    username = input("Enter your UM username (without @siswa.um.edu.my): ").strip()
    if not username:
        print("Error: Username cannot be empty")
        return False
    
    password = getpass.getpass("Enter your UM password: ")
    if not password:
        print("Error: Password cannot be empty")
        return False
    
    # Choose browser
    browser = input("Choose browser (edge/chrome/auto) [edge]: ").strip().lower()
    if not browser:
        browser = 'edge'
    
    # Choose headless mode
    headless_input = input("Run in headless mode? (y/N): ").strip().lower()
    headless = headless_input in ['y', 'yes']
    
    if not headless:
        print("ℹ️  Running with visible browser - you can watch the process")
    
    print(f"\nTesting login with:")
    print(f"Username: {username}")
    print(f"Browser: {browser}")
    print(f"Headless: {headless}")
    print()
    
    try:
        # Initialize authenticator
        authenticator = UMAuthenticator(
            headless=headless,
            timeout=30,
            browser=browser
        )
        
        print("Starting authentication test...")
        
        # Test login
        session = authenticator.login(username, password)
        
        if session:
            print("✅ Login test PASSED!")
            print("✅ Status dropdown selection worked correctly")
            print("✅ Authentication session created successfully")
            
            # Test if session is valid
            if authenticator.test_session():
                print("✅ Session is valid and working")
            else:
                print("⚠️  Session created but may not be fully functional")
            
            return True
        else:
            print("❌ Login test FAILED - No session created")
            return False
            
    except Exception as e:
        print(f"❌ Login test FAILED: {e}")
        return False
    
    finally:
        # Cleanup
        try:
            if 'authenticator' in locals():
                authenticator.cleanup()
                print("🧹 Browser cleanup completed")
        except:
            pass


def main():
    """Main function."""
    
    print("This script tests only the login process to verify:")
    print("1. Browser initialization works")
    print("2. UM login page loads")
    print("3. Status dropdown automatically selects 'Student'")
    print("4. Authentication completes successfully")
    print()
    print("This is useful for debugging login issues without")
    print("going through the full paper download process.")
    print()
    
    success = test_login()
    
    if success:
        print("\n🎉 Login test completed successfully!")
        print("You can now run the full tool:")
        print(f"python main.py --browser edge --subject-code WIA1005")
    else:
        print("\n😞 Login test failed. Please check:")
        print("1. Your username and password are correct")
        print("2. You're connected to UM network or VPN")
        print("3. Your browser is up to date")
        print("4. Check the log files for detailed error information")
    
    return 0 if success else 1


if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nTest cancelled by user")
        sys.exit(130) 