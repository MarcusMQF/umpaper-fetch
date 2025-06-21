# Publishing Guide for umpaper-fetch

This guide will help you build and publish the `umpaper-fetch` package to PyPI so users can install it with `pip install umpaper-fetch`.

## 📋 Prerequisites

### 1. Install Build Tools

```bash
pip install --upgrade pip
pip install build twine setuptools wheel
```

### 2. Create PyPI Account

1. Go to [PyPI.org](https://pypi.org) and create an account
2. Verify your email address
3. (Optional) Go to [TestPyPI.org](https://test.pypi.org) for testing

### 3. Set Up API Tokens

1. Go to your PyPI account settings
2. Create an API token for uploading packages
3. Save the token securely (starts with `pypi-`)

## 🔧 Pre-Publishing Setup

### 1. Update Package Information

Edit these files with your actual information:

**setup.py**:
```python
author="Your Actual Name",
author_email="your.actual.email@example.com",
url="https://github.com/yourusername/umpaper-fetch",
```

**pyproject.toml**:
```toml
authors = [
    {name = "Your Actual Name", email = "your.actual.email@example.com"}
]
[project.urls]
Homepage = "https://github.com/yourusername/umpaper-fetch"
Repository = "https://github.com/yourusername/umpaper-fetch"
"Bug Reports" = "https://github.com/yourusername/umpaper-fetch/issues"
```

### 2. Choose Package Name

Check if `umpaper-fetch` is available on PyPI:
```bash
pip install umpaper-fetch
# If it fails, the name is available
```

If taken, modify the name in:
- `setup.py` → `name="your-chosen-name"`
- `pyproject.toml` → `name = "your-chosen-name"`

### 3. Update README for PyPI

Replace the current README.md with PYPI_README.md:
```bash
cp PYPI_README.md README.md
```

## 🚀 Building the Package

### 1. Clean Previous Builds

```bash
# Remove old build artifacts
rm -rf build/ dist/ *.egg-info/
```

### 2. Build the Package

```bash
# Build source distribution and wheel
python -m build
```

This creates:
- `dist/umpaper-fetch-1.0.0.tar.gz` (source distribution)
- `dist/umpaper_fetch-1.0.0-py3-none-any.whl` (wheel)

### 3. Verify the Build

```bash
# Check package contents
tar -tzf dist/umpaper-fetch-1.0.0.tar.gz
unzip -l dist/umpaper_fetch-1.0.0-py3-none-any.whl
```

## 🧪 Testing Before Publishing

### 1. Test Local Installation

```bash
# Install locally in development mode
pip install -e .

# Test the command
python -m umpaper_fetch.cli --help
```

### 2. Test with TestPyPI (Recommended)

```bash
# Upload to TestPyPI first
twine upload --repository testpypi dist/*

# Install from TestPyPI
pip install --index-url https://test.pypi.org/simple/ umpaper-fetch

# Test the installation
um-papers --version
```

## 📦 Publishing to PyPI

### 1. Upload to PyPI

```bash
# Upload to real PyPI
twine upload dist/*
```

When prompted:
- Username: `__token__`
- Password: Your PyPI API token (including `pypi-` prefix)

### 2. Verify Publication

```bash
# Wait a few minutes, then test installation
pip install umpaper-fetch

# Test the command
um-papers --help
```

## 🔄 Updating the Package

### 1. Update Version Number

Update version in:
- `setup.py`: `version="1.0.1"`
- `pyproject.toml`: `version = "1.0.1"`
- `umpaper_fetch/__init__.py`: `__version__ = "1.0.1"`
- `umpaper_fetch/cli.py`: `version='%(prog)s 1.0.1'`

### 2. Build and Upload New Version

```bash
# Clean and build
rm -rf build/ dist/ *.egg-info/
python -m build

# Upload
twine upload dist/*
```

## 📁 Project Structure for PyPI

```
PastYear Accessor/
├── umpaper_fetch/                 # Main package directory
│   ├── __init__.py               # Package initialization
│   ├── cli.py                    # Command-line interface
│   ├── auth/                     # Authentication module
│   ├── scraper/                  # Scraping module
│   ├── downloader/               # Download module
│   └── utils/                    # Utility modules
├── setup.py                      # Setup configuration
├── pyproject.toml                # Modern Python project config
├── requirements.txt              # Dependencies
├── README.md                     # PyPI description
├── LICENSE                       # MIT license
├── MANIFEST.in                   # Include/exclude files
└── PUBLISHING_GUIDE.md           # This guide
```

## 🔒 Security Best Practices

### 1. Use API Tokens
- Never use username/password for uploading
- Use scoped API tokens for better security

### 2. Two-Factor Authentication
- Enable 2FA on your PyPI account
- Use app-based authentication (not SMS)

### 3. Environment Variables
```bash
# Set token as environment variable
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=pypi-your-api-token-here

# Upload without entering credentials
twine upload dist/*
```

## 🐛 Troubleshooting

### Build Errors
```bash
# If build fails, check:
python setup.py check
python -m build --verbose
```

### Upload Errors
```bash
# If upload fails:
twine check dist/*
twine upload --verbose dist/*
```

### Import Errors After Installation
```bash
# Check if package is properly installed
pip show umpaper-fetch
pip list | grep umpaper
```

## 📈 After Publishing

### 1. Monitor Downloads
- Check PyPI package page for download statistics
- Monitor for issues/feedback

### 2. Documentation
- Update GitHub README with PyPI installation instructions
- Create GitHub releases for version tags

### 3. Maintenance
- Respond to user issues
- Keep dependencies updated
- Regular security updates

## 🎉 Success!

Once published, users can install your package with:

```bash
pip install umpaper-fetch
um-papers --help
```

Your package will be available at: https://pypi.org/project/umpaper-fetch/ 