"""
Chrome Driver Fix Module

Handles Chrome driver setup issues, particularly the Win32 application error
that occurs due to architecture mismatches.
"""

import os
import platform
import logging
from webdriver_manager.chrome import ChromeDriverManager


def get_chrome_driver_path():
    """
    Get Chrome driver path with proper architecture handling.
    
    Returns:
        str: Path to the Chrome driver executable
    """
    logger = logging.getLogger(__name__)
    
    try:
        # Determine system architecture
        is_64bit = platform.machine().endswith('64')
        system = platform.system()
        
        logger.info(f"System: {system}, 64-bit: {is_64bit}")
        
        # Force specific Chrome driver version/architecture if needed
        if system == "Windows" and is_64bit:
            # Try to get the latest driver for Windows 64-bit
            driver_manager = ChromeDriverManager()
            driver_path = driver_manager.install()
            
            # Verify the driver is executable
            if os.path.exists(driver_path) and os.access(driver_path, os.X_OK):
                logger.info(f"Chrome driver ready: {driver_path}")
                return driver_path
            else:
                logger.warning(f"Chrome driver not executable: {driver_path}")
                # Try to fix permissions
                try:
                    os.chmod(driver_path, 0o755)
                    if os.access(driver_path, os.X_OK):
                        logger.info("Fixed Chrome driver permissions")
                        return driver_path
                except Exception as perm_error:
                    logger.error(f"Could not fix permissions: {perm_error}")
        else:
            # For other systems, use default behavior
            driver_path = ChromeDriverManager().install()
            return driver_path
            
    except Exception as e:
        logger.error(f"Chrome driver setup failed: {e}")
        raise
    
    raise Exception("Could not setup Chrome driver")


def test_chrome_driver(driver_path):
    """
    Test if the Chrome driver is working properly.
    
    Args:
        driver_path (str): Path to Chrome driver
        
    Returns:
        bool: True if driver works, False otherwise
    """
    logger = logging.getLogger(__name__)
    
    try:
        import subprocess
        
        # Test if the driver can start
        result = subprocess.run(
            [driver_path, '--version'], 
            capture_output=True, 
            text=True, 
            timeout=10
        )
        
        if result.returncode == 0:
            logger.info(f"Chrome driver test passed: {result.stdout.strip()}")
            return True
        else:
            logger.error(f"Chrome driver test failed: {result.stderr}")
            return False
            
    except Exception as e:
        logger.error(f"Chrome driver test error: {e}")
        return False


def cleanup_chrome_cache():
    """Clean up problematic Chrome driver cache."""
    logger = logging.getLogger(__name__)
    
    try:
        import shutil
        from pathlib import Path
        
        # Get the cache directory
        cache_dir = Path.home() / '.wdm' / 'drivers' / 'chromedriver'
        
        if cache_dir.exists():
            logger.info(f"Cleaning Chrome driver cache: {cache_dir}")
            shutil.rmtree(cache_dir)
            logger.info("Chrome driver cache cleaned")
            return True
        else:
            logger.info("No Chrome driver cache to clean")
            return True
            
    except Exception as e:
        logger.error(f"Could not clean Chrome driver cache: {e}")
        return False 