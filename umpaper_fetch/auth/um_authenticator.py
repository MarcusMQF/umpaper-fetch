"""
UM Authentication Handler

Handles the complex University Malaya authentication flow through OpenAthens
and SAML authentication systems.
"""

import logging
import time
import platform
import subprocess
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.common.exceptions import TimeoutException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from .chrome_fix import get_chrome_driver_path, cleanup_chrome_cache
import requests


class UMAuthenticator:
    """Handles UM authentication through OpenAthens proxy."""
    
    # UM authentication URLs
    OPENATHENS_URL = "https://proxy.openathens.net/login?qurl=https%3A%2F%2Fexampaper.um.edu.my%2F&entityID=https%3A%2F%2Fidp.um.edu.my%2Fentity"
    EXAM_PAPER_BASE_URL = "https://exampaper-um-edu-my.eu1.proxy.openathens.net"
    
    def __init__(self, headless=False, timeout=30, browser='auto'):
        """Initialize the authenticator."""
        self.headless = headless
        self.timeout = timeout
        self.browser = browser
        self.driver = None
        self.session = None
        self.logger = logging.getLogger(__name__)
        
    def _setup_driver(self):
        """Setup WebDriver with appropriate options for the selected browser."""
        browser_type = self._detect_browser() if self.browser == 'auto' else self.browser
        
        try:
            if browser_type == 'edge':
                self.driver = self._setup_edge_driver()
            else:  # Default to Chrome
                self.driver = self._setup_chrome_driver()
            
            self.driver.set_page_load_timeout(self.timeout)
            self.logger.info(f"{browser_type.title()} WebDriver initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize {browser_type} WebDriver: {e}")
            
            # Try fallback browsers if auto-detection was used
            if self.browser == 'auto' and browser_type != 'chrome':
                self.logger.info("Trying Chrome as fallback...")
                try:
                    self.driver = self._setup_chrome_driver()
                    self.driver.set_page_load_timeout(self.timeout)
                    self.logger.info("Chrome WebDriver initialized as fallback")
                    return
                except Exception as chrome_error:
                    self.logger.error(f"Chrome fallback also failed: {chrome_error}")
            
            raise Exception(f"Failed to initialize any WebDriver: {e}")
    
    def _detect_browser(self):
        """Detect the best available browser."""
        import platform
        
        # On Windows, strongly prefer Edge since Chrome has driver issues
        if platform.system() == "Windows":
            try:
                import subprocess
                # Check if Edge is installed
                subprocess.run(['where', 'msedge'], check=True, capture_output=True)
                self.logger.info("Detected Edge browser on Windows")
                return 'edge'
            except (subprocess.CalledProcessError, FileNotFoundError):
                self.logger.warning("Edge not found, will try Chrome")
        
        # Default to Chrome for non-Windows or if Edge not found
        self.logger.info("Defaulting to Chrome browser")
        return 'chrome'
    
    def _setup_chrome_driver(self):
        """Setup Chrome WebDriver with proper architecture detection."""
        options = ChromeOptions()
        self._add_common_options(options)
        
        # Fix for Win32 application error - use our custom Chrome driver setup
        try:
            # First, try our custom driver setup
            driver_path = get_chrome_driver_path()
            
            return webdriver.Chrome(
                service=ChromeService(driver_path),
                options=options
            )
        except Exception as e:
            self.logger.error(f"Chrome driver setup failed: {e}")
            
            # Try cleaning cache and retry
            self.logger.info("Attempting to clean Chrome driver cache and retry...")
            try:
                cleanup_chrome_cache()
                driver_path = get_chrome_driver_path()
                
                return webdriver.Chrome(
                    service=ChromeService(driver_path),
                    options=options
                )
            except Exception as retry_error:
                self.logger.error(f"Chrome driver retry also failed: {retry_error}")
                raise Exception(f"Chrome driver setup failed even after cache cleanup: {retry_error}")
    
    def _setup_edge_driver(self):
        """Setup Edge WebDriver."""
        options = EdgeOptions()
        self._add_common_options(options)
        
        try:
            driver_path = EdgeChromiumDriverManager().install()
            
            return webdriver.Edge(
                service=EdgeService(driver_path),
                options=options
            )
        except Exception as e:
            self.logger.error(f"Edge driver setup failed: {e}")
            raise
    
    def _add_common_options(self, options):
        """Add common options for Chrome and Edge."""
        # Suppress logging and experimental features to reduce noise
        options.add_argument('--log-level=3')  # Fatal only
        options.add_argument('--silent')
        options.add_experimental_option("excludeSwitches", ["enable-logging"])

        if self.headless:
            options.add_argument('--headless=new')
        
        # Security and performance options
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-web-security')
        options.add_argument('--disable-features=VizDisplayCompositor')
        options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
    
    def _wait_for_element(self, by, value, timeout=None):
        """Wait for an element to be present and return it."""
        if timeout is None:
            timeout = self.timeout
            
        if not self.driver:
            raise Exception("WebDriver not initialized")
            
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except TimeoutException:
            self.logger.error(f"Timeout waiting for element: {by}={value}")
            raise
    
    def _wait_for_clickable(self, by, value, timeout=None):
        """Wait for an element to be clickable and return it."""
        if timeout is None:
            timeout = self.timeout
            
        if not self.driver:
            raise Exception("WebDriver not initialized")
            
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((by, value))
            )
            return element
        except TimeoutException:
            self.logger.error(f"Timeout waiting for clickable element: {by}={value}")
            raise
    
    def login(self, username, password):
        """
        Perform the complete UM login flow.
        
        Args:
            username (str): UM username (without @siswa.um.edu.my)
            password (str): UM password
            
        Returns:
            requests.Session: Authenticated session for making requests
        """
        try:
            self._setup_driver()
            
            if not self.driver:
                raise Exception("Failed to initialize WebDriver")
            
            # Step 1: Navigate to OpenAthens proxy
            self.logger.info("Navigating to OpenAthens proxy...")
            self.driver.get(self.OPENATHENS_URL)
            
            # Step 2: Select "UM Staff and Students" option
            self.logger.info("Selecting UM Staff and Students option...")
                       
            # Check for and close cookie overlay if present
            try:
                self.driver.execute_script("""
                    var overlay = document.getElementById('ccc-overlay');
                    if (overlay) { overlay.parentNode.removeChild(overlay); }
                    var notify = document.getElementById('ccc-notify');
                    if (notify) { notify.parentNode.removeChild(notify); }
                """)
            except Exception:
                pass

            um_option = self._wait_for_clickable(
                By.XPATH, 
                "//div[contains(text(), 'UM Staff and Students')]"
            )

            # Use JS click to bypass any remaining overlays
            self.driver.execute_script("arguments[0].click();", um_option)
            
            # Step 3: Fill in credentials
            self.logger.info("Entering credentials...")
            
            # Wait for username field and enter username
            username_field = self._wait_for_element(By.NAME, "username")
            username_field.clear()
            username_field.send_keys(username)
            
            # Enter password
            password_field = self._wait_for_element(By.NAME, "password")
            password_field.clear()
            password_field.send_keys(password)
            
            # Give the page a moment to process the entered credentials and load the status dropdown
            self.logger.info("Waiting for page to fully load after entering credentials...")
            time.sleep(3)
            
            # Select "Student" status
            self.logger.info("Selecting 'Student' status...")
            
            # Wait for the status dropdown to be available with longer timeout
            status_dropdown = None
            
            # First, wait for any select element to appear
            try:
                WebDriverWait(self.driver, 15).until(
                    EC.presence_of_element_located((By.TAG_NAME, "select"))
                )
                self.logger.info("Select elements are now available on page")
            except TimeoutException:
                self.logger.warning("No select elements found - the form might have a different structure")
            
            # Start with the method that actually works - searching through select elements
            self.logger.info("Looking for status dropdown through select elements...")
            try:
                select_elements = self.driver.find_elements(By.TAG_NAME, "select")
                self.logger.info(f"Found {len(select_elements)} select elements")
                for i, select_elem in enumerate(select_elements):
                    try:
                        options = select_elem.find_elements(By.TAG_NAME, "option")
                        option_texts = [opt.text for opt in options if opt.text.strip()]
                        self.logger.info(f"Select {i} options: {option_texts}")
                        
                        # Check if this select has Student/Staff options
                        has_student = any("student" in text.lower() for text in option_texts)
                        has_staff = any("staff" in text.lower() for text in option_texts)
                        
                        if has_student and has_staff:
                            status_dropdown = select_elem
                            self.logger.info(f"Found status dropdown in select {i}")
                            break
                    except Exception as e:
                        self.logger.warning(f"Error checking select {i}: {e}")
                        continue
            except Exception as e:
                self.logger.error(f"Error searching for select elements: {e}")
            
            # Only try name/ID if the working method failed
            if not status_dropdown:
                self.logger.info("Trying backup methods for status dropdown...")
                try:
                    status_dropdown = self._wait_for_element(By.NAME, "status", timeout=10)
                    self.logger.info("Found status dropdown by name")
                except Exception as e1:
                    self.logger.warning(f"Could not find status dropdown by name: {e1}")
                    try:
                        status_dropdown = self._wait_for_element(By.ID, "status", timeout=5)
                        self.logger.info("Found status dropdown by ID")
                    except Exception as e2:
                        self.logger.warning(f"Could not find status dropdown by ID: {e2}")
            
            if not status_dropdown:
                raise Exception("Could not find status dropdown - check if page loaded correctly")
            
            # Wait a moment for the dropdown to be fully interactive
            time.sleep(1)
            
            select = Select(status_dropdown)
            
            # Debug: Log available options first
            options = select.options
            option_texts = [opt.text for opt in options if opt.text.strip()]
            self.logger.info(f"Available status options: {option_texts}")
            
            # Try multiple ways to select Student with better error handling
            selection_successful = False
            
            # Method 1: Try by visible text (most reliable)
            try:
                select.select_by_visible_text("Student")
                self.logger.info("Selected Student by visible text")
                selection_successful = True
            except Exception as e1:
                self.logger.warning(f"Could not select by visible text 'Student': {e1}")
                
                # Method 2: Try by value
                try:
                    select.select_by_value("Student")
                    self.logger.info("Selected Student by value")
                    selection_successful = True
                except Exception as e2:
                    self.logger.warning(f"Could not select by value 'Student': {e2}")
                    
                    # Method 3: Try variations of text
                    for option in options:
                        if option.text.strip() and "student" in option.text.lower():
                            try:
                                select.select_by_visible_text(option.text)
                                self.logger.info(f"Selected Student by text variation: '{option.text}'")
                                selection_successful = True
                                break
                            except Exception as e3:
                                continue
                    
                    # Method 4: Try by index if nothing else worked
                    if not selection_successful:
                        try:
                            # Find the index of the Student option
                            for i, option in enumerate(options):
                                if option.text.strip() and "student" in option.text.lower():
                                    select.select_by_index(i)
                                    self.logger.info(f"Selected Student by index {i}")
                                    selection_successful = True
                                    break
                        except Exception as e4:
                            self.logger.error(f"Could not select by index: {e4}")
            
            if not selection_successful:
                raise Exception("Failed to select Student status using any method")
            
            # Verify selection and wait for it to be processed
            selected_option = select.first_selected_option
            self.logger.info(f"Status dropdown selected: {selected_option.text}")
            
            # Give the form time to process the selection
            time.sleep(3)
            
            # Final verification before submitting
            final_selection = select.first_selected_option
            self.logger.info(f"Final status before submit: {final_selection.text}")
            
            # Submit the form
            self.logger.info("Looking for sign-in button...")
            
            # Wait for submit button to be available
            try:
                WebDriverWait(self.driver, 10).until(
                    lambda driver: driver.find_elements(By.XPATH, "//button[@type='submit']") or 
                                  driver.find_elements(By.XPATH, "//input[@type='submit']") or
                                  driver.find_elements(By.XPATH, "//input[contains(@value, 'Sign')]")
                )
                self.logger.info("Submit button is now available")
            except TimeoutException:
                self.logger.warning("No submit button found with standard selectors")
            
            # Try multiple ways to find the sign-in button, starting with the method that works
            sign_in_button = None
            button_selectors = [
                (By.XPATH, "//button[@type='submit']", "submit button"),
                (By.XPATH, "//input[@type='submit']", "submit input"),
                (By.XPATH, "//input[@value='Sign in']", "exact Sign in value"),
                (By.XPATH, "//input[contains(@value, 'Sign')]", "contains Sign value"),
                (By.XPATH, "//button[contains(text(), 'Sign')]", "button with Sign text"),
                (By.XPATH, "//input[contains(@value, 'Login')]", "contains Login value"),
                (By.XPATH, "//button[contains(text(), 'Login')]", "button with Login text"),
                (By.CSS_SELECTOR, "button[type='submit']", "CSS submit button"),
                (By.CSS_SELECTOR, "input[type='submit']", "CSS submit input")
            ]
            
            for i, (by, selector, description) in enumerate(button_selectors):
                try:
                    self.logger.info(f"Trying method {i+1}: {description}")
                    sign_in_button = self._wait_for_clickable(by, selector, timeout=8)
                    self.logger.info(f"Found sign-in button using: {description}")
                    break
                except Exception as e:
                    self.logger.warning(f"Method {i+1} ({description}) failed: {e}")
                    continue
            
            if not sign_in_button:
                # Last resort: look for any clickable element that might be the button
                self.logger.info("Looking for any submit-like elements...")
                try:
                    all_inputs = self.driver.find_elements(By.TAG_NAME, "input")
                    all_buttons = self.driver.find_elements(By.TAG_NAME, "button")
                    
                    self.logger.info(f"Found {len(all_inputs)} input elements and {len(all_buttons)} button elements")
                    
                    for elem in all_inputs + all_buttons:
                        try:
                            elem_type = elem.get_attribute("type")
                            elem_value = elem.get_attribute("value")
                            elem_text = elem.text
                            self.logger.info(f"Element: type='{elem_type}', value='{elem_value}', text='{elem_text}'")
                        except:
                            pass
                    
                except Exception as e:
                    self.logger.error(f"Error examining form elements: {e}")
                
                raise Exception("Could not find sign-in button. Check if form structure changed.")
            
            self.logger.info("Clicking sign-in button...")
            sign_in_button.click()
            
            # Step 4: Wait for redirect to exam paper repository
            self.logger.info("Waiting for authentication to complete...")
            
            # Give some time for form submission
            time.sleep(3)
            
            # Check current URL and wait for redirect
            current_url = self.driver.current_url
            self.logger.info(f"Current URL after clicking sign-in: {current_url}")
            
            # Wait for successful redirect to exam paper site with increased timeout
            try:
                WebDriverWait(self.driver, self.timeout + 15).until(
                    lambda driver: self.EXAM_PAPER_BASE_URL in driver.current_url
                )
                self.logger.info(f"Successfully redirected to: {self.driver.current_url}")
            except TimeoutException:
                # Log current state for debugging
                current_url = self.driver.current_url
                page_title = self.driver.title
                self.logger.error(f"Timeout waiting for redirect. Current URL: {current_url}")
                self.logger.error(f"Page title: {page_title}")
                
                # Check if we're still on login page (indicates failed login)
                if "login" in current_url.lower() or "auth" in current_url.lower():
                    raise Exception("Login failed - still on authentication page. Check credentials.")
                else:
                    # We might be on a different page - let's continue and see
                    self.logger.warning("Redirect timeout but not on login page - continuing...")
            
            self.logger.info("Authentication successful, creating session...")
            
            # Step 5: Extract cookies and create requests session
            self.session = self._create_authenticated_session()
            
            return self.session
            
        except TimeoutException:
            self.logger.error("Authentication timeout - check credentials and network")
            raise Exception("Authentication failed: Timeout")
        except Exception as e:
            self.logger.error(f"Authentication failed: {e}")
            raise Exception(f"Authentication failed: {e}")
    
    def _create_authenticated_session(self):
        """Create a requests session with authentication cookies."""
        session = requests.Session()
        
        if not self.driver:
            raise Exception("WebDriver not initialized")
        
        # Copy cookies from Selenium to requests session
        for cookie in self.driver.get_cookies():
            session.cookies.set(
                cookie['name'], 
                cookie['value'],
                domain=cookie.get('domain'),
                path=cookie.get('path')
            )
        
        # Set common headers
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })
        
        self.logger.info("Authenticated session created successfully")
        return session
    
    def test_session(self):
        """Test if the session is still valid."""
        if not self.session:
            return False
            
        try:
            response = self.session.get(
                f"{self.EXAM_PAPER_BASE_URL}/",
                timeout=10
            )
            return response.status_code == 200
        except:
            return False
    
    def cleanup(self):
        """Clean up resources."""
        if self.driver:
            try:
                self.driver.quit()
                self.logger.info("WebDriver cleaned up")
            except:
                pass
        
        if self.session:
            try:
                self.session.close()
                self.logger.info("Session cleaned up")
            except:
                pass 