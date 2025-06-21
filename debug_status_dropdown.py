#!/usr/bin/env python3
"""
Status Dropdown Debug Script

This script specifically debugs the status dropdown selection issue
by showing detailed information about the dropdown and its options.
"""

import sys
import getpass
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager


def debug_status_dropdown():
    """Debug the status dropdown specifically."""
    
    print("UM Status Dropdown Debug Tool")
    print("=" * 50)
    
    # Get credentials
    username = input("Enter your UM username (without @siswa.um.edu.my): ").strip()
    password = getpass.getpass("Enter your UM password: ")
    
    if not username or not password:
        print("Error: Username and password are required")
        return False
    
    print("\n🔍 Starting debug session...")
    print("👀 Browser will be visible so you can watch the process")
    
    driver = None
    try:
        # Setup Edge browser (visible)
        options = EdgeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        driver = webdriver.Edge(
            service=EdgeService(EdgeChromiumDriverManager().install()),
            options=options
        )
        
        print("✅ Browser initialized")
        
        # Navigate to UM login
        print("📍 Navigating to UM OpenAthens proxy...")
        driver.get("https://proxy.openathens.net/login?qurl=https%3A%2F%2Fexampaper.um.edu.my%2F&entityID=https%3A%2F%2Fidp.um.edu.my%2Fentity")
        
        # Wait for and click UM option
        print("🎯 Looking for UM Staff and Students option...")
        wait = WebDriverWait(driver, 30)
        um_option = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'UM Staff and Students')]"))
        )
        um_option.click()
        print("✅ Clicked UM Staff and Students")
        
        # Fill credentials
        print("📝 Entering credentials...")
        username_field = wait.until(EC.presence_of_element_located((By.NAME, "username")))
        username_field.clear()
        username_field.send_keys(username)
        
        password_field = driver.find_element(By.NAME, "password")
        password_field.clear()
        password_field.send_keys(password)
        print("✅ Credentials entered")
        
        # Now debug the status dropdown
        print("\n🔍 DEBUGGING STATUS DROPDOWN...")
        print("=" * 40)
        
        # Give page time to load
        time.sleep(2)
        
        # Method 1: Try to find by name
        print("🔍 Method 1: Looking for dropdown by name='status'...")
        try:
            status_dropdown = driver.find_element(By.NAME, "status")
            print("✅ Found dropdown by name")
        except Exception as e:
            print(f"❌ Not found by name: {e}")
            status_dropdown = None
        
        # Method 2: Try to find by ID
        if not status_dropdown:
            print("🔍 Method 2: Looking for dropdown by id='status'...")
            try:
                status_dropdown = driver.find_element(By.ID, "status")
                print("✅ Found dropdown by ID")
            except Exception as e:
                print(f"❌ Not found by ID: {e}")
        
        # Method 3: Find all select elements
        print("🔍 Method 3: Finding all select elements...")
        select_elements = driver.find_elements(By.TAG_NAME, "select")
        print(f"📊 Found {len(select_elements)} select elements")
        
        for i, select_elem in enumerate(select_elements):
            try:
                options = select_elem.find_elements(By.TAG_NAME, "option")
                option_texts = [opt.text.strip() for opt in options if opt.text.strip()]
                print(f"  Select {i}: {option_texts}")
                
                # Check if this looks like the status dropdown
                has_student = any("student" in text.lower() for text in option_texts)
                has_staff = any("staff" in text.lower() for text in option_texts)
                
                if has_student or has_staff:
                    print(f"  🎯 Select {i} appears to be the status dropdown!")
                    status_dropdown = select_elem
                    
            except Exception as e:
                print(f"  ❌ Error reading select {i}: {e}")
        
        if not status_dropdown:
            print("❌ Could not find status dropdown!")
            print("📄 Current page source (first 1000 chars):")
            print(driver.page_source[:1000])
            return False
        
        # Try to work with the dropdown
        print(f"\n🎯 Working with status dropdown...")
        select = Select(status_dropdown)
        
        # Show current selection
        current = select.first_selected_option
        print(f"📌 Currently selected: '{current.text}'")
        
        # Show all options
        options = select.options
        print(f"📋 All options: {[opt.text for opt in options]}")
        
        # Try to select Student
        print("\n🔄 Attempting to select 'Student'...")
        
        for i, method in enumerate([
            ("by_value", lambda: select.select_by_value("Student")),
            ("by_visible_text", lambda: select.select_by_visible_text("Student")),
            ("by_index_1", lambda: select.select_by_index(1)),
        ]):
            method_name, method_func = method
            try:
                print(f"  🔍 Trying method {i+1}: {method_name}...")
                method_func()
                
                # Check if it worked
                time.sleep(1)
                new_selection = select.first_selected_option
                print(f"  ✅ Success! Now selected: '{new_selection.text}'")
                
                if "student" in new_selection.text.lower():
                    print("🎉 Student successfully selected!")
                    break
                else:
                    print(f"  ⚠️  Selected '{new_selection.text}' but expected Student")
                    
            except Exception as e:
                print(f"  ❌ Method {method_name} failed: {e}")
        
        # Final check
        final_selection = select.first_selected_option
        print(f"\n📊 Final status: '{final_selection.text}'")
        
        if "student" in final_selection.text.lower():
            print("🎉 SUCCESS: Student is selected!")
        else:
            print("❌ FAILURE: Student is not selected")
        
        # Keep browser open for inspection
        input("\n⏸️  Press Enter to continue with login (or Ctrl+C to stop)...")
        
        # Try to submit
        print("🚀 Looking for sign-in button...")
        
        # Try multiple selectors like in the main code
        button_selectors = [
            ("//input[@value='Sign in']", "exact value"),
            ("//input[@type='submit']", "submit input"),
            ("//button[@type='submit']", "submit button"),
            ("//input[contains(@value, 'Sign')]", "contains Sign"),
            ("//button[contains(text(), 'Sign')]", "button with Sign text")
        ]
        
        sign_in_button = None
        for selector, description in button_selectors:
            try:
                print(f"  🔍 Trying: {description}")
                sign_in_button = driver.find_element(By.XPATH, selector)
                print(f"  ✅ Found sign-in button: {description}")
                break
            except Exception as e:
                print(f"  ❌ {description} failed: {e}")
        
        if not sign_in_button:
            print("❌ Could not find sign-in button!")
            # Show all form elements for debugging
            all_inputs = driver.find_elements(By.TAG_NAME, "input")
            all_buttons = driver.find_elements(By.TAG_NAME, "button")
            
            print(f"📋 Found {len(all_inputs)} inputs and {len(all_buttons)} buttons:")
            for elem in all_inputs + all_buttons:
                try:
                    elem_type = elem.get_attribute("type")
                    elem_value = elem.get_attribute("value")
                    elem_text = elem.text
                    print(f"  - type='{elem_type}', value='{elem_value}', text='{elem_text}'")
                except:
                    pass
            return False
        
        print("🚀 Clicking sign-in button...")
        sign_in_button.click()
        
        print("✅ Form submitted! Waiting for redirect...")
        time.sleep(5)
        
        current_url = driver.current_url
        print(f"📍 Current URL: {current_url}")
        
        # Check if we reached the exam papers site
        if "exampaper" in current_url:
            print("🎉 SUCCESS: Reached exam papers site!")
        elif "login" in current_url.lower() or "auth" in current_url.lower():
            print("❌ Still on login page - authentication may have failed")
        else:
            print(f"⚠️  Unexpected page: {current_url}")
        
        return True
        
    except Exception as e:
        print(f"❌ Debug failed: {e}")
        return False
    
    finally:
        if driver:
            input("\n⏸️  Press Enter to close browser...")
            driver.quit()


if __name__ == '__main__':
    try:
        debug_status_dropdown()
    except KeyboardInterrupt:
        print("\n\nDebug cancelled by user")
    except Exception as e:
        print(f"Debug script error: {e}") 