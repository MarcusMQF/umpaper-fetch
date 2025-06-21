# Testing Guide for umpaper-fetch

This guide shows you how to thoroughly test your package before publishing to PyPI.

## 🧪 Testing Levels

### 1. Local Development Testing
### 2. Local Package Testing  
### 3. TestPyPI Testing
### 4. Production PyPI Testing

---

## 🔧 1. Local Development Testing

Test your package in development mode without building:

```bash
# Install in development mode (editable install)
pip install -e .

# Test the CLI command
um-papers --help
um-papers --version

# Test with your actual UM credentials (optional)
um-papers --username 24012345 --subject-code WIA1005 --show-browser --verbose
```

**Expected Results:**
- `um-papers --help` shows proper help text
- `um-papers --version` shows "1.0.0" 
- Command runs without import errors

---

## 📦 2. Local Package Testing

Test the built package locally:

```bash
# Clean any previous builds
rm -rf build/ dist/ *.egg-info/

# Build the package
python -m build

# Check what was built
ls dist/
# Should show:
# umpaper_fetch-1.0.0-py3-none-any.whl
# umpaper_fetch-1.0.0.tar.gz

# Uninstall development version first
pip uninstall umpaper-fetch

# Install from built wheel
pip install dist/umpaper_fetch-1.0.0-py3-none-any.whl

# Test the installation
um-papers --help
python -c "import umpaper_fetch; print(umpaper_fetch.__version__)"
```

**Expected Results:**
- Package installs without errors
- `um-papers` command works
- Version imports correctly

---

## 🌐 3. TestPyPI Testing

Test uploading and installing from TestPyPI (safe testing environment):

### Step 3a: Create TestPyPI Account

1. Go to [test.pypi.org](https://test.pypi.org)
2. Create an account (different from main PyPI)
3. Verify your email
4. Generate an API token

### Step 3b: Upload to TestPyPI

```bash
# Upload to TestPyPI
twine upload --repository testpypi dist/*

# When prompted:
# Username: __token__
# Password: pypi-[your-testpypi-token]
```

**Expected Output:**
```
Uploading distributions to https://test.pypi.org/legacy/
Uploading umpaper_fetch-1.0.0-py3-none-any.whl
100% ████████████████████████████████████████
Uploading umpaper_fetch-1.0.0.tar.gz
100% ████████████████████████████████████████

View at:
https://test.pypi.org/project/umpaper-fetch/
```

### Step 3c: Test Install from TestPyPI

```bash
# Create a fresh virtual environment
python -m venv test_env
source test_env/bin/activate  # On Windows: test_env\Scripts\activate

# Install from TestPyPI
pip install --index-url https://test.pypi.org/simple/ umpaper-fetch

# Test the installation
um-papers --help
um-papers --version

# Test with real credentials (optional)
um-papers --username 24012345 --subject-code WIA1005 --show-browser
```

**Expected Results:**
- Package installs from TestPyPI
- All dependencies install correctly
- Command works as expected

---

## 🚀 4. Production PyPI Testing

Only do this when TestPyPI testing passes:

### Step 4a: Upload to Real PyPI

```bash
# Upload to production PyPI
twine upload dist/*

# When prompted:
# Username: __token__
# Password: pypi-[your-real-pypi-token]
```

### Step 4b: Test Production Install

```bash
# Create fresh environment
python -m venv prod_test_env
source prod_test_env/bin/activate  # On Windows: prod_test_env\Scripts\activate

# Install from production PyPI
pip install umpaper-fetch

# Test
um-papers --help
```

---

## ✅ Test Checklist

Before publishing, ensure all these work:

### Basic Functionality
- [ ] `um-papers --help` shows correct help
- [ ] `um-papers --version` shows "1.0.0"
- [ ] `python -c "import umpaper_fetch"` works
- [ ] Package installs without errors

### CLI Arguments
- [ ] `um-papers --username 24012345 --subject-code WIA1005 --help` 
- [ ] `um-papers --browser edge --verbose --help`
- [ ] `um-papers --no-location-prompt --help`

### Error Handling
- [ ] `um-papers --username invalid` shows proper error
- [ ] `um-papers --browser invalid` shows proper error
- [ ] Interrupted process exits cleanly (Ctrl+C)

### Integration Test (Optional)
- [ ] Full download test with real credentials
- [ ] Test on different operating systems
- [ ] Test with different Python versions (3.8+)

---

## 🐛 Common Issues and Fixes

### Issue: "ModuleNotFoundError"
```bash
# Solution: Check package structure
python -c "import sys; print(sys.path)"
pip show umpaper-fetch
```

### Issue: "Command 'um-papers' not found"
```bash
# Solution: Check if scripts directory is in PATH
pip show umpaper-fetch
# Look for "Location:" and check if Scripts folder is in PATH
```

### Issue: "twine upload failed"
```bash
# Solution: Check credentials and package
twine check dist/*
# Fix any issues shown
```

### Issue: Dependencies not installing
```bash
# Solution: Check requirements in setup.py/pyproject.toml
pip install -r requirements.txt
```

---

## 📊 Quick Test Commands

Copy-paste these commands for quick testing:

```bash
# Quick local test
pip install -e . && um-papers --help

# Quick build test  
python -m build && pip install dist/*.whl && um-papers --version

# Quick TestPyPI test
twine upload --repository testpypi dist/* && pip install --index-url https://test.pypi.org/simple/ umpaper-fetch

# Quick production test
pip install umpaper-fetch && um-papers --help
```

---

## 🎯 Testing with Real Usage

To fully test the package, try a real download:

```bash
# Test with show-browser to see what happens
um-papers --username 24012345 --subject-code WIA1005 --show-browser --verbose

# Test batch mode
um-papers --username 24012345 --subject-code WXES1116 --no-location-prompt --max-retries 1
```

**Note**: Use your actual UM credentials and a subject code you have access to.

---

## ✅ When Testing is Complete

Your package is ready for production when:

1. ✅ All local tests pass
2. ✅ TestPyPI upload and install works
3. ✅ CLI commands work correctly
4. ✅ At least one full download test succeeds
5. ✅ Error handling works properly

Then you can confidently upload to production PyPI! 🚀 