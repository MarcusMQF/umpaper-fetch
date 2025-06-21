# UM Paper Fetch

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Automated downloader for University Malaya past year exam papers. No more manual navigation through multiple systems - just one command to download all papers for any subject!

## 🚀 Quick Start

### Installation

```bash
pip install umpaper-fetch
```

### Usage

After installation, use the `um-papers` command:

```bash
# Interactive mode (recommended for first-time users)
um-papers

# With subject code
um-papers --subject-code WIA1005

# With username and subject code
um-papers --username 24056789 --subject-code WXES1116

# Non-interactive mode
um-papers --username 24012345 --subject-code WIA1005 --no-location-prompt

# Show browser for debugging
um-papers --show-browser --verbose
```

## ✨ Features

- **One-command download**: Get all past year papers for any UM subject
- **Automatic authentication**: Handles complex UM OpenAthens/SAML login
- **Smart organization**: Papers organized by subject code with proper naming
- **ZIP archive creation**: All papers bundled in a convenient ZIP file
- **Progress tracking**: Real-time download progress with retry logic
- **Cross-platform**: Works on Windows, macOS, and Linux
- **Browser flexibility**: Supports Chrome, Edge, and auto-detection

## 📋 Requirements

- Python 3.8 or higher
- Valid UM student/staff credentials
- Internet connection
- Chrome or Edge browser installed

## 🎯 How it Works

1. **Authentication**: Automatically logs into UM systems via OpenAthens proxy
2. **Search**: Finds all past year papers for the specified subject code
3. **Download**: Downloads all papers with proper naming and organization
4. **Archive**: Creates a ZIP file containing all downloaded papers

## 📖 Command Options

```
Options:
  -u, --username TEXT         UM username (without @siswa.um.edu.my)
  -s, --subject-code TEXT     Subject code (e.g., WIA1005, WXES1116)
  -o, --output-dir TEXT       Output directory (default: ./downloads)
  --no-location-prompt        Skip location selection prompt
  --show-browser              Show browser window (default: headless)
  -b, --browser [auto|chrome|edge]  Browser choice (default: edge)
  --timeout INTEGER           Session timeout in seconds (default: 30)
  --max-retries INTEGER       Maximum retry attempts (default: 3)
  -v, --verbose               Enable verbose logging
  --version                   Show version information
  -h, --help                  Show help message
```

## 📁 Output Structure

```
downloads/
└── WIA1005/
    ├── Y2023_S1_Final_Exam.pdf
    ├── Y2023_S1_Mid_Term_Test.pdf
    ├── Y2022_S2_Final_Exam.pdf
    └── ...
└── WIA1005_papers.zip
```

## 🔧 Troubleshooting

### Browser Issues
- **Windows**: Tool prefers Edge browser (better compatibility)
- **Chrome driver errors**: Try using `--browser edge`
- **Browser not found**: Ensure Chrome or Edge is installed

### Authentication Issues
- **Login failed**: Verify your UM credentials
- **Timeout**: Increase timeout with `--timeout 60`
- **Network issues**: Check your internet connection

### Download Issues
- **No papers found**: Verify the subject code is correct
- **Download failures**: Use `--max-retries 5` for unstable connections

For detailed troubleshooting, run with `--verbose` flag.

## 🤝 Support

- **Issues**: Report bugs or request features
- **Documentation**: Full documentation available in the repository
- **Contributions**: Pull requests welcome!

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Disclaimer

This tool is for educational purposes only. Please respect University Malaya's terms of service and use responsibly. Only download papers you have legitimate access to as a registered student or staff member. 