# Troubleshooting Guide

This guide helps resolve common issues with the UM Past Year Paper Downloader.

## Chrome Driver "Win32 Application" Error

**Error Message:**
```
[WinError 193] %1 is not a valid Win32 application
```

**Cause:** This error occurs when there's an architecture mismatch between the downloaded Chrome driver and your system.

### Solution 1: Try Microsoft Edge Instead (Recommended)

Since you're on Windows, Microsoft Edge often works better:

```bash
python main.py --browser edge --subject-code WIA1005
```

Edge is:
- ✅ Built into Windows
- ✅ More reliable on Windows systems  
- ✅ Better memory usage
- ✅ No architecture conflicts

### Solution 2: Fix Chrome Driver Cache

If you prefer Chrome, try cleaning the driver cache:

1. **Close all browser windows**
2. **Delete Chrome driver cache:**
   ```bash
   # Windows
   rmdir /s "%USERPROFILE%\.wdm\drivers\chromedriver"
   
   # Or manually delete folder:
   # C:\Users\[YourUsername]\.wdm\drivers\chromedriver
   ```
3. **Run the tool again:**
   ```bash
   python main.py --browser chrome --subject-code WIA1005
   ```

### Solution 3: Update Chrome Browser

1. Open Chrome
2. Go to `chrome://settings/help`
3. Let it update automatically
4. Restart Chrome
5. Try the tool again

### Solution 4: Force 64-bit Chrome Driver

```bash
# Install specific Chrome version
pip install --upgrade webdriver-manager
python main.py --browser chrome --subject-code WIA1005
```

## Browser Priority Recommendations

### For Windows Users:
1. **Microsoft Edge** (Best choice) - `--browser edge`
2. **Chrome** (Backup) - `--browser chrome`

### For Mac/Linux Users:
1. **Chrome** (Best choice) - `--browser chrome`
2. **Auto-detect** - `--browser auto`

## Common Error Solutions

### 1. "No browsers are working"

**Solution:**
- Install Microsoft Edge: https://www.microsoft.com/edge
- Or install Chrome: https://www.google.com/chrome/

### 2. "Authentication failed"

**Solutions:**
- Check your username (don't include @siswa.um.edu.my)
- Verify your password
- Ensure you're connected to UM network or VPN
- Try different browser: `--browser edge`

### 2a. "Status dropdown not selecting Student"

**Symptoms:** Tool shows "Staff" instead of "Student" in dropdown

**Solutions:**
- The tool will now automatically try multiple ways to select "Student"
- If it still fails, manually check the UM login page for changes
- Try running without `--headless` to see what's happening:
  ```bash
  python main.py --browser edge --subject-code WIA1005
  ```

### 3. "No papers found"

**Solutions:**
- Check subject code spelling (e.g., WIA1005, not wia1005)
- Verify the subject has past year papers
- Try searching manually first at: https://exampaper.um.edu.my

### 4. "Network connectivity issues"

**Solutions:**
- Connect to UM VPN if off-campus
- Check internet connection
- Try again later (UM servers might be busy)

## Quick Test Commands

Test your setup:
```bash
# Test with Edge (recommended for Windows)
python main.py --browser edge --username YOUR_USERNAME --subject-code WIA1005

# Test with Chrome
python main.py --browser chrome --username YOUR_USERNAME --subject-code WIA1005

# Test setup
python test_setup.py
```

## Environment Information

When reporting issues, please include:

```bash
# Get system info
python -c "import platform; print(f'OS: {platform.system()} {platform.release()}')"
python -c "import platform; print(f'Architecture: {platform.architecture()}')"
python --version
```

## Getting Help

1. **Run test script first:**
   ```bash
   python test_setup.py
   ```

2. **Check log files:**
   - Look in `logs/` folder for detailed error information

3. **Try Edge browser:**
   ```bash
   python main.py --browser edge --subject-code WIA1005
   ```

4. **Common fix for 90% of issues:**
   - Use Edge instead of Chrome on Windows
   - Clear browser cache
   - Update browser to latest version

## Success Tips

✅ **Use Microsoft Edge on Windows** - Most reliable  
✅ **Keep browsers updated** - Avoid compatibility issues  
✅ **Connect to UM VPN** if off-campus  
✅ **Use correct subject codes** (check UM course catalog)  
✅ **Run test script first** to identify issues early 