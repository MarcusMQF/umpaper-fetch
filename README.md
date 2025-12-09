# Open Source UM PastYear Paper Downloader

**One-click bulk download solution for University Malaya (UM) past year exam papers**

Automate the tedious process of manually downloading past year papers one by one. Simply provide your UM credentials and subject code, and get all available papers in a organized ZIP file.

[![PyPI version](https://badge.fury.io/py/umpaper-fetch.svg)](https://badge.fury.io/py/umpaper-fetch)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## Quick Start  

**1. [Install Python](https://www.python.org/downloads/)**

**2. Install umpaper-fetch**

Create and activate a virtual environment (recommended):
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```
> If not using virtual environment, change all commands from "umpaper" to "python -m umpaper_fetch.cli"

Then install the package:
```bash
# Install from PyPI
pip install umpaper-fetch

# Upgrade to latest version
pip install --upgrade umpaper-fetch
```

**3. Basic Usage**
```bash
# See all available commands and options
umpaper --help
# Run the downloader interactively
umpaper
```

---

## Key Features

### **Core Functionality**
- **One-Click Bulk Download**: Download all past year papers for any subject code automatically
- **Smart ZIP Organization**: Automatically organizes papers by year and creates a structured ZIP archive
- **Secure Authentication**: Handles complex UM OpenAthens authentication flow seamlessly
- **Concurrent Downloads**: Multi-threaded downloading for faster performance
- **Auto-Retry Logic**: Robust error handling with configurable retry attempts
- **Real-time Progress**: Live progress bars and detailed status updates

### **File Organization**
- **Hierarchical Structure**: Papers organized by subject → year → semester
- **Custom Download Locations**: Choose where to save your papers
- **Smart File Naming**: Automatically detects and preserves meaningful filenames
- **Auto-Generated README**: Includes download summary and paper inventory in ZIP
- **Organized Output**: Individual PDFs + consolidated ZIP file
- **Optional Cleanup**: Choice to keep individual files or ZIP only

### **User Experience**
- **Terminal-Based Interface**: Clean, intuitive command-line interface
- **Interactive Mode**: Prompts for credentials and settings when needed
- **Command-Line Mode**: Full automation with command-line arguments
- **Browser Options**: Support for Edge, Chrome with auto-detection
- **Comprehensive Logging**: Detailed logs for troubleshooting
- **Customizable Command**: Extensive options to control timeouts, retries, browser selection, subjects code

---

## Complete Command Reference

### **For Regular Users**

#### **Interactive Mode (Recommended for beginners)**
```bash
# See all available options first
umpaper --help

# Run interactive mode and it will prompts for all required action
umpaper
```

#### **Available Options**
| Command | Short | Description | Default |
|---------|-------|-------------|---------|
| `--help` | `-h` | Available command to use |  |
| `--username` | `-u` | UM username (without @siswa.um.edu.my) | *prompted* |
| `--subject-code` | `-s` | Subject code to search for (e.g., WIA1005). Supported multiple subject code separated by space | *prompted* |
| `--output-dir` | `-o` | Custom download directory | `./downloads` |
| `--browser` | `-b` | Browser choice: `auto`, `chrome`, `edge` | `chrome` |
| `--timeout` | | Session timeout in seconds | `30` |
| `--max-retries` | | Maximum retry attempts for failed downloads | `3` |
| `--no-location-prompt` | | Skip interactive location selection | `false` |
| `--show-browser` | | Show browser window (disable headless mode) | `false` |
| `--verbose` | `-v` | Enable detailed debug logging | `false` |

#### **Quick Commands**
```bash
# With username and subject code
umpaper -u 23011111 -s WIA1005

# Process multiple subject
umpaper -s WIA1005 WIA1002 WIA2001

# With custom output directory
umpaper -u 23011111 -s WXES1116 -o "C:/Downloads/Papers"

# Skip location prompt for automation
umpaper -u 23011111 -s WIA1005 --no-location-prompt
```

### **For Developers**

#### **Development Installation**
```bash
# Clone repository
git clone https://github.com/MarcusMQF/umpaper-fetch.git
cd umpaper-fetch

# Install in development mode
pip install -e .

# Install development dependencies
pip install -e .[dev]
```

---

## What You Get

### **Organized File Structure**
```
downloads/
├── WIA1005/
│   ├── Year_2023/
│   │   ├── WIA1005_Final_2023_S1.pdf
│   │   └── WIA1005_Final_2023_S2.pdf
│   ├── Year_2022/
│   │   ├── WIA1005_Final_2022_S1.pdf
│   │   └── WIA1005_Final_2022_S2.pdf
│   └── Unsorted/
│       └── WIA1005_Additional_Papers.pdf
├── WIA1005_past_years.zip
└── WIA1005_README.txt
```

### **ZIP Archive Contents**
- **Hierarchical Organization**: Subject → Year → Files
- **Automatic README**: Download summary and file inventory
- **Optimized Compression**: Balanced compression for size/speed
- **Preserve Metadata**: Original filenames and dates maintained

---

## Prerequisites & Setup

### **System Requirements**
- **Python 3.8+** installed
- **Internet connection** (stable recommended)
- **UM student account** with active credentials
- **Browser**: Microsoft Edge (Windows) or Google Chrome (Mac/Linux)

### **Browser Setup**
- **Windows**: Google Chrome (pre-installed, recommended)
- **Mac/Linux**: Google Chrome (install from google.com/chrome)
- **Auto-detection**: Tool will find the best available browser

### **Firewall/Network**
- Tool connects to `exampaper.um.edu.my` via HTTPS
- No special firewall configuration needed
- Works on UM campus network and external networks

---

## Security & Privacy

### **What We Do**
- Use secure HTTPS connections only
- Handle UM authentication through official channels
- Clean up browser data after each session
- Never store or log passwords
- Respect server rate limits

### **What We Don't Do**
- Store credentials anywhere
- Bypass security measures
- Access unauthorized content
- Share or transmit personal data
- Violate UM terms of service

---

## Legal & Academic Use

**Educational Purpose Only**: This tool is designed for UM students to efficiently access past year papers for their studies. Users must:
- Have valid UM credentials
- Comply with UM's terms of service
- Use papers for academic purposes only
- Respect copyright and intellectual property rights

**Disclaimer**: This is an unofficial tool not affiliated with University Malaya.

---

## Support & Contributing

### **Get Help**
- Check this README for common usage patterns
- Report issues on [GitHub Issues](https://github.com/MarcusMQF/umpaper-fetch/issues)
- Request features via GitHub Issues

### **Contributing**
Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/feature-name`)
3. Make your changes with tests
4. Submit a pull request
