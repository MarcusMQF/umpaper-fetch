# 🎓 Open Source UM PastYear Paper Downloader

**One-click bulk download solution for University Malaya (UM) past year exam papers**

Automate the tedious process of manually downloading past year papers one by one. Simply provide your UM credentials and subject code, and get all available papers in a single organized ZIP file.

[![PyPI version](https://badge.fury.io/py/umpaper-fetch.svg)](https://badge.fury.io/py/umpaper-fetch)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🚀 Quick Start (For Regular Users)

### **Installation**
```bash
# Install from PyPI
pip install umpaper-fetch

# Upgrade to latest version
pip install --upgrade umpaper-fetch
```

### **Basic Usage**
```bash
# Run the downloader
python -m umpaper_fetch.cli

# Or with command-line shortcut (if available)
um-papers
```

### **First Run**
Follow the interactive prompts:
1. Enter your UM username (without @siswa.um.edu.my)
2. Enter your password securely
3. Enter subject code (e.g., WIA1005)
4. Choose download location
5. Confirm download of found papers

---

## ✨ Key Features

### 🚀 **Core Functionality**
- **🔄 One-Click Bulk Download**: Download all past year papers for any subject code automatically
- **📦 Smart ZIP Organization**: Automatically organizes papers by year and creates a structured ZIP archive
- **🔐 Secure Authentication**: Handles complex UM OpenAthens authentication flow seamlessly
- **⚡ Concurrent Downloads**: Multi-threaded downloading for faster performance
- **🔄 Auto-Retry Logic**: Robust error handling with configurable retry attempts
- **📊 Real-time Progress**: Live progress bars and detailed status updates

### 📁 **File Organization**
- **📂 Hierarchical Structure**: Papers organized by subject → year → semester
- **🏷️ Smart File Naming**: Automatically detects and preserves meaningful filenames
- **📋 Auto-Generated README**: Includes download summary and paper inventory in ZIP
- **🗂️ Organized Output**: Individual PDFs + consolidated ZIP file
- **🧹 Optional Cleanup**: Choice to keep individual files or ZIP only

### 🖥️ **User Experience**
- **📱 Terminal-Based Interface**: Clean, intuitive command-line interface
- **🎯 Interactive Mode**: Prompts for credentials and settings when needed
- **⚙️ Command-Line Mode**: Full automation with command-line arguments
- **📍 Custom Download Locations**: Choose where to save your papers
- **🔍 Browser Options**: Support for Edge, Chrome with auto-detection
- **📝 Comprehensive Logging**: Detailed logs for troubleshooting

---

## 📋 Complete Command Reference

### **For Regular Users**

#### **Interactive Mode (Recommended for beginners)**
```bash
python -m umpaper_fetch.cli
```
*Prompts for all required information*

#### **Quick Commands**
```bash
# With username and subject code
python -m umpaper_fetch.cli --username john_doe --subject-code WIA1005

# With custom output directory
python -m umpaper_fetch.cli -u student123 -s WXES1116 -o "C:/Downloads/Papers"

# Skip location prompt for automation
python -m umpaper_fetch.cli -s WIA1005 --no-location-prompt
```

#### **Available Options**
| Command | Short | Description | Default |
|---------|-------|-------------|---------|
| `--username` | `-u` | UM username (without @siswa.um.edu.my) | *prompted* |
| `--subject-code` | `-s` | Subject code to search for (e.g., WIA1005) | *prompted* |
| `--output-dir` | `-o` | Custom download directory | `./downloads` |
| `--browser` | `-b` | Browser choice: `auto`, `chrome`, `edge` | `edge` |
| `--timeout` | | Session timeout in seconds | `30` |
| `--max-retries` | | Maximum retry attempts for failed downloads | `3` |
| `--no-location-prompt` | | Skip interactive location selection | `false` |
| `--verbose` | `-v` | Enable detailed debug logging | `false` |

### **For Developers & Advanced Users**

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

#### **Debug Commands**
```bash
# Show browser window for debugging
python -m umpaper_fetch.cli --show-browser --verbose --subject-code WIA1005

# High-performance mode with extended timeouts
python -m umpaper_fetch.cli -s WIA1005 --max-retries 5 --timeout 60

# Force specific browser
python -m umpaper_fetch.cli --browser chrome --subject-code CSC1025
```

#### **Developer Options**
| Command | Description | Use Case |
|---------|-------------|----------|
| `--show-browser` | Show browser window (disable headless mode) | Debugging authentication |
| `--verbose` | Enable detailed debug logging | Troubleshooting issues |
| `--timeout 60` | Extended session timeout | Slow connections |
| `--max-retries 5` | More retry attempts | Unstable connections |

---

## 💡 Tips for Best Experience

### **Choose the Right Browser**
```bash
# Windows users (recommended)
python -m umpaper_fetch.cli --browser edge --subject-code WIA1005

# Mac/Linux users
python -m umpaper_fetch.cli --browser chrome --subject-code WIA1005

# Auto-detect (fallback)
python -m umpaper_fetch.cli --browser auto --subject-code WIA1005
```

### **Optimize for Your Connection**
```bash
# For slow/unstable connections
python -m umpaper_fetch.cli --timeout 90 --max-retries 5 --subject-code WIA1005

# For fast connections
python -m umpaper_fetch.cli --timeout 15 --max-retries 2 --subject-code WIA1005
```

### **Batch Processing Multiple Subjects**
```bash
# Process multiple subjects
python -m umpaper_fetch.cli -s WIA1005 --no-location-prompt -o "./Papers/WIA1005"
python -m umpaper_fetch.cli -s WIX1116 --no-location-prompt -o "./Papers/WXES1116"
python -m umpaper_fetch.cli -s CSC1025 --no-location-prompt -o "./Papers/CSC1025"
```

### **Automation-Friendly Commands**
```bash
# Fully automated (only prompts for password)
python -m umpaper_fetch.cli -u your_username -s WIA1005 --no-location-prompt -o "./Papers"

# Silent mode with custom browser
python -m umpaper_fetch.cli -u your-username -s WXES1116 --browser edge --no-location-prompt
```

---

## 📊 What You Get

### **Organized File Structure**
```
📁 downloads/
├── 📁 WIA1005/
│   ├── 📁 Year_2023/
│   │   ├── WIA1005_Final_2023_S1.pdf
│   │   └── WIA1005_Final_2023_S2.pdf
│   ├── 📁 Year_2022/
│   │   ├── WIA1005_Final_2022_S1.pdf
│   │   └── WIA1005_Final_2022_S2.pdf
│   └── 📁 Unsorted/
│       └── WIA1005_Additional_Papers.pdf
├── 📦 WIA1005_past_years.zip
└── 📄 WIA1005_README.txt
```

### **ZIP Archive Contents**
- **Hierarchical Organization**: Subject → Year → Files
- **Automatic README**: Download summary and file inventory
- **Optimized Compression**: Balanced compression for size/speed
- **Preserve Metadata**: Original filenames and dates maintained

---

## 🔧 Prerequisites & Setup

### **System Requirements**
- **Python 3.8+** installed
- **Internet connection** (stable recommended)
- **UM student account** with active credentials
- **Browser**: Microsoft Edge (Windows) or Google Chrome (Mac/Linux)

### **Browser Setup**
- **Windows**: Microsoft Edge (pre-installed, recommended)
- **Mac/Linux**: Google Chrome (install from google.com/chrome)
- **Auto-detection**: Tool will find the best available browser

### **Firewall/Network**
- Tool connects to `exampaper.um.edu.my` via HTTPS
- No special firewall configuration needed
- Works on UM campus network and external networks

---

## 🎯 Quick Command Cheat Sheet

### **For Regular Users**
```bash
# Install and run
pip install umpaper-fetch
python -m umpaper_fetch.cli

# Quick download with subject code
python -m umpaper_fetch.cli -s WIA1005

# Custom download location
python -m umpaper_fetch.cli -s WIA1005 -o "C:/MyPapers"

# Batch mode (no prompts except password)
python -m umpaper_fetch.cli -u your_username -s WIA1005 --no-location-prompt
```

### **For Developers**
```bash
# Development setup
git clone https://github.com/MarcusMQF/umpaper-fetch.git
cd umpaper-fetch
pip install -e .[dev]

# Debug mode
python -m umpaper_fetch.cli --show-browser --verbose -s WIA1005

# Performance testing
python -m umpaper_fetch.cli --max-retries 5 --timeout 60 -s WXES1116
```

---

## 🔒 Security & Privacy

### **What We Do**
- ✅ Use secure HTTPS connections only
- ✅ Handle UM authentication through official channels
- ✅ Clean up browser data after each session
- ✅ Never store or log passwords
- ✅ Respect server rate limits

### **What We Don't Do**
- ❌ Store credentials anywhere
- ❌ Bypass security measures
- ❌ Access unauthorized content
- ❌ Share or transmit personal data
- ❌ Violate UM terms of service

---

## ⚖️ Legal & Academic Use

**Educational Purpose Only**: This tool is designed for UM students to efficiently access past year papers for their studies. Users must:
- Have valid UM credentials
- Comply with UM's terms of service
- Use papers for academic purposes only
- Respect copyright and intellectual property rights

**Disclaimer**: This is an unofficial tool not affiliated with University Malaya.

---

## 🤝 Support & Contributing

### **Get Help**
- 📖 Check this README for common usage patterns
- 🐛 Report issues on [GitHub Issues](https://github.com/MarcusMQF/umpaper-fetch/issues)
- 💡 Request features via GitHub Issues

### **Contributing**
Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes with tests
4. Submit a pull request
5. Follow existing code style

### **Development Setup**
```bash
git clone https://github.com/MarcusMQF/umpaper-fetch.git
cd umpaper-fetch
pip install -e .[dev]
pytest  # Run tests
```