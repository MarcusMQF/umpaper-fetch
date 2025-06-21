# 🎓 UM Past Year Paper Downloader - PaperFetch

**One-click bulk download solution for University Malaya (UM) past year exam papers**

Automate the tedious process of manually downloading past year papers one by one. Simply provide your UM credentials and subject code, and get all available papers in a single organized ZIP file.

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

### 🔒 **Security & Reliability**
- **🛡️ Secure Password Input**: Hidden password entry (never stored/logged)
- **🧹 Session Cleanup**: Automatic browser data cleanup after use
- **✅ Download Verification**: Validates PDF integrity after download
- **🔐 HTTPS Enforcement**: Secure connections to UM servers
- **⏱️ Configurable Timeouts**: Customizable session and download timeouts

---

## 📋 Complete Command Reference

### **Available Commands (9 total)**

| Command | Short | Description | Default |
|---------|-------|-------------|---------|
| `--username` | `-u` | UM username (without @siswa.um.edu.my) | *prompted* |
| `--subject-code` | `-s` | Subject code to search for (e.g., WIA1005) | *prompted* |
| `--output-dir` | `-o` | Custom download directory | `./downloads` |
| `--browser` | `-b` | Browser choice: `auto`, `chrome`, `edge` | `edge` |
| `--timeout` | | Session timeout in seconds | `30` |
| `--max-retries` | | Maximum retry attempts for failed downloads | `3` |
| `--show-browser` | | Show browser window (disable headless mode) | `false` |
| `--no-location-prompt` | | Skip interactive location selection | `false` |
| `--verbose` | `-v` | Enable detailed debug logging | `false` |

### **Usage Examples**

**1. Interactive Mode (Recommended for first-time users)**
```bash
python main.py
```
*Prompts for username, password, subject code, and download location*

**2. Quick Command-Line Mode**
```bash
python main.py --username john_doe --subject-code WIA1005
```
*Only prompts for password*

**3. Fully Automated Mode**
```bash
python main.py -u student123 -s WXES1116 -o "C:/Downloads/Papers" --no-location-prompt
```
*No prompts except secure password entry*

**4. Debug Mode with Visible Browser**
```bash
python main.py --subject-code WIA1005 --show-browser --verbose
```
*Shows browser actions and detailed logging*

**5. High-Performance Mode**
```bash
python main.py -s WIA1005 --max-retries 5 --timeout 60
```
*Extended timeouts and retries for slow connections*

**6. Custom Browser Selection**
```bash
python main.py --browser chrome --subject-code CSC1025
```
*Force use of Chrome browser*

---

## 🚀 Quick Start Guide

### **Prerequisites**
- Python 3.8+ installed
- One of these browsers: **Microsoft Edge** (recommended), Google Chrome
- UM student account with active credentials
- Stable internet connection

### **Installation**
```bash
# 1. Clone/download this repository
git clone <repository-url>
cd um-past-year-downloader

# 2. Install dependencies
pip install -r requirements.txt

# 3. Ready to use!
python main.py
```

### **First Run**
```bash
python main.py
```
Follow the interactive prompts:
1. Enter your UM username (without @siswa.um.edu.my)
2. Enter your password securely
3. Enter subject code (e.g., WIA1005)
4. Choose download location
5. Confirm download of found papers

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

### **Generated Reports**
- **Download Summary**: Shows total papers found and downloaded
- **Failed Downloads**: Lists any papers that couldn't be downloaded
- **File Inventory**: Complete list of papers with years and types
- **Timestamp**: When the download was performed

---

## 🔧 Advanced Configuration

### **Browser Selection Guide**

| Browser | Best For | Advantages | Notes |
|---------|----------|------------|-------|
| **Edge** | Windows users | Built-in, no driver conflicts, memory efficient | **Recommended** |
| **Chrome** | Mac/Linux users | Wide compatibility, stable | May need driver updates |
| **Auto** | Uncertain | Detects best available | Falls back to Edge → Chrome |

### **Performance Tuning**
```bash
# For slow connections
python main.py --timeout 60 --max-retries 5

# For fast connections  
python main.py --timeout 15 --max-retries 2

# For debug/troubleshooting
python main.py --verbose --show-browser
```

### **Output Directory Options**
- **Default**: `./downloads` (project folder)
- **Custom**: Any valid path (e.g., `C:/Users/Student/Papers`)
- **Interactive**: Choose during runtime
- **Auto**: Use `--no-location-prompt` to skip selection

---

## 🧪 Testing & Validation

### **Built-in Test Scripts**

**1. Complete System Test**
```bash
python test_setup.py
```
*Tests Python environment, dependencies, browser drivers, and network connectivity*

**2. Authentication Test**
```bash
python test_login.py
```
*Tests only the UM login process (useful for credential verification)*

**3. Search Functionality Test**
```bash
python test_search_debug.py
```
*Tests paper search without downloading*

### **Validation Features**
- **PDF Integrity Check**: Verifies downloaded files are valid PDFs
- **Size Validation**: Ensures files aren't empty or corrupted
- **Download Verification**: Confirms all expected papers were downloaded
- **ZIP Integrity**: Validates ZIP file creation and contents

---

## 🛠️ Technical Architecture

### **Modular Components**

**1. Authentication (`auth/um_authenticator.py`)**
- Handles complex UM OpenAthens SAML authentication
- Manages session cookies and security tokens
- Supports multiple browser backends

**2. Paper Discovery (`scraper/paper_scraper.py`)**
- Searches UM repository by subject code
- Extracts paper metadata (year, semester, type)
- Handles pagination and result filtering

**3. Download Engine (`downloader/pdf_downloader.py`)**
- Concurrent multi-threaded downloads
- Progress tracking with visual indicators
- Retry logic with exponential backoff
- File integrity validation

**4. Archive Creator (`utils/zip_creator.py`)**
- Intelligent file organization by year/semester
- Optimized compression algorithms
- Auto-generated documentation
- Metadata preservation

**5. Logging System (`utils/logger.py`)**
- Structured logging with multiple levels
- Separate log files for debugging
- Performance metrics and timing

### **Dependencies**
- `selenium` - Web automation and browser control
- `requests` - HTTP session management  
- `beautifulsoup4` - HTML parsing and data extraction
- `tqdm` - Progress bars and status indicators
- `webdriver-manager` - Automatic browser driver management

---

## 🚨 Troubleshooting

### **Common Issues & Solutions**

**❌ Login Failed**
- ✅ Verify username/password are correct
- ✅ Check if your UM account is active  
- ✅ Try using Edge browser: `--browser edge`
- ✅ Enable debug mode: `--verbose --show-browser`

**❌ No Papers Found**  
- ✅ Verify subject code is correct (e.g., WIA1005, not wia1005)
- ✅ Check if papers exist for that subject
- ✅ Try different semester/year variations

**❌ Download Errors**
- ✅ Check internet connection stability
- ✅ Increase timeout: `--timeout 60`
- ✅ Increase retries: `--max-retries 5`  
- ✅ Check disk space in output directory

**❌ Browser/WebDriver Issues**
- ✅ **Windows users**: Use Edge first: `--browser edge`
- ✅ Update browser to latest version
- ✅ Try: `pip install --upgrade webdriver-manager`
- ✅ See `TROUBLESHOOTING.md` for detailed solutions

### **Exit Codes**
- `0` - Success
- `1` - Authentication failure  
- `2` - Network connectivity issues
- `3` - No papers found or download failed
- `4` - File system permissions error
- `130` - User cancelled (Ctrl+C)

---

## 📈 Performance Metrics

### **Typical Performance**
- **Authentication**: 5-10 seconds
- **Paper Search**: 2-5 seconds  
- **Download Speed**: 2-5 MB/s per file (concurrent)
- **ZIP Creation**: 1-3 seconds
- **Total Time**: 30 seconds - 2 minutes (depending on paper count)

### **Optimization Features**
- **Concurrent Downloads**: Up to 4 simultaneous downloads
- **Intelligent Caching**: Avoids re-downloading existing files
- **Compressed Archives**: ZIP compression reduces file size by 10-30%
- **Progress Tracking**: Real-time ETA and speed indicators

---

## ⚖️ Legal & Academic Use

### **Terms of Use**
- ✅ **Educational Purpose Only**: For UM students' academic use
- ✅ **Respect UM Policies**: Adheres to university terms of service
- ✅ **No Circumvention**: Uses standard authentication methods
- ✅ **Rate Limiting**: Respects server load limits
- ✅ **Valid Credentials Required**: Must have active UM account

### **What This Tool Does NOT Do**
- ❌ Bypass any security measures
- ❌ Access restricted content
- ❌ Store or share credentials
- ❌ Violate copyright or academic policies
- ❌ Access content you don't have permission for

---

## 💡 Tips for Best Experience

### **For Windows Users**
```bash
# Recommended command for Windows
python main.py --browser edge --subject-code WIA1005
```

### **For Mac/Linux Users**  
```bash
# Recommended command for Mac/Linux
python main.py --browser chrome --subject-code WIA1005
```

### **For Slow Connections**
```bash
python main.py --timeout 90 --max-retries 5 --subject-code WIA1005
```

### **For Batch Processing**
```bash
# Create a batch script for multiple subjects
python main.py -s WIA1005 --no-location-prompt -o "./Papers/WIA1005"
python main.py -s WXES1116 --no-location-prompt -o "./Papers/WXES1116"
```

---

## 🤝 Support & Contributing

### **Getting Help**
1. **📖 Read `TROUBLESHOOTING.md`** - Comprehensive solution guide
2. **🔍 Check logs** - Review log files for detailed error information  
3. **🧪 Run tests** - Use `python test_setup.py` to validate environment
4. **🔄 Try Edge browser** - Often resolves driver issues: `--browser edge`

### **Contributing**
Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch  
3. Make your changes with tests
4. Submit a pull request
5. Follow existing code style and documentation standards

---

## 📄 Disclaimer

**Disclaimer**: This tool is an unofficial utility created to help UM students access past year papers more efficiently. It is not affiliated with or endorsed by University Malaya. Users are responsible for complying with UM's terms of service and academic policies.

---

## 🎯 Quick Command Cheat Sheet

```bash
# Basic usage
python main.py

# Fast automated mode  
python main.py -u username -s WIA1005 --no-location-prompt

# Debug mode
python main.py --verbose --show-browser -s WIA1005

# High performance
python main.py --max-retries 5 --timeout 60 -s WXES1116

# Custom location
python main.py -o "C:/Papers" -s CSC1025

# Windows optimized
python main.py --browser edge -s WIA1005
```

---

*Time to lock in for your final*