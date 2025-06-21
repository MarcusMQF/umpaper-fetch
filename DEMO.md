# UM Paper Fetch - Live Demo

This document shows how to use the `umpaper-fetch` package after installation.

## 🚀 Installation

```bash
pip install umpaper-fetch
```

## 📋 Quick Start

### Basic Usage (Interactive Mode)

```bash
um-papers
```

This will prompt you for:
1. Username (your UM student/staff ID without @siswa.um.edu.my)
2. Password (entered securely, no echo)
3. Subject code (e.g., WIA1005, WXES1116)
4. Download location (option to use default or custom path)

### Advanced Usage

```bash
# Specify username and subject code upfront
um-papers --username your_username --subject-code WIA1005

# Use custom output directory
um-papers --output-dir "C:/My Downloads/UM Papers"

# Non-interactive mode (good for automation)
um-papers --username your_username --subject-code WXES1116 --no-location-prompt

# Show browser for debugging/monitoring
um-papers --show-browser --verbose

# Use specific browser
um-papers --browser edge --timeout 60

# Increase retry attempts for unstable connections
um-papers --max-retries 5
```

## 🎯 What Happens When You Run It

1. **Authentication**: Logs into UM OpenAthens system
2. **Search**: Finds all papers for your subject code
3. **Download**: Downloads each paper with progress tracking
4. **Organization**: Creates organized folder structure
5. **Archive**: Bundles everything into a ZIP file

## 📁 Output Structure

After running `um-papers --subject-code WIA1005`, you'll get:

```
downloads/
├── WIA1005/
│   ├── Y2023_S1_Final_Exam.pdf
│   ├── Y2023_S1_Mid_Term_Test.pdf
│   ├── Y2022_S2_Final_Exam.pdf
│   ├── Y2022_S1_Final_Exam.pdf
│   └── ... (all available papers)
└── WIA1005_papers.zip  (contains all the above)
```

## 🔧 Common Options

| Option | Description | Example |
|--------|-------------|---------|
| `--username` | UM username (without @domain) | `--username 24012345` |
| `--subject-code` | Subject to download | `--subject-code WIA1005` |
| `--output-dir` | Where to save files | `--output-dir "C:/Downloads"` |
| `--no-location-prompt` | Skip location selection | `--no-location-prompt` |
| `--show-browser` | Show browser window | `--show-browser` |
| `--browser` | Choose browser | `--browser edge` |
| `--verbose` | Detailed logging | `--verbose` |

## 🚨 Troubleshooting

### Browser Issues
```bash
# If Chrome fails (common on Windows)
um-papers --browser edge

# Show browser to see what's happening
um-papers --show-browser --verbose
```

### Authentication Issues
```bash
# Increase timeout for slow connections
um-papers --timeout 60

# Check credentials by viewing browser
um-papers --show-browser
```

### Download Issues
```bash
# Increase retries for unstable connections
um-papers --max-retries 5

# Use verbose mode to see detailed progress
um-papers --verbose
```

## 💡 Tips

1. **First-time users**: Use `--show-browser` to see what's happening
2. **Windows users**: Edge browser works better than Chrome
3. **Slow connections**: Use `--timeout 60` and `--max-retries 5`
4. **Automation**: Use `--no-location-prompt` to skip interactive prompts
5. **Debugging**: Always use `--verbose` when troubleshooting

## 🎓 Example Session

```bash
$ um-papers --subject-code WIA1005 --verbose

=== UM Past Year Paper Downloader ===
Enter your UM username (without @siswa.um.edu.my): 24012345
Enter your UM password: [hidden]

📋 Configuration Summary
==================================================
Username: 24012345
Subject Code: WIA1005
Output Directory: C:\Users\User\downloads
Browser: edge
Headless Mode: True
Timeout: 30s
Max Retries: 3

🚀 Ready to start downloading papers for WIA1005
Continue? (y/N): y

============================================================
🔄 Starting download process...
============================================================
Step 1: Authenticating with UM portal...
✅ Authentication successful
Step 2: Searching for papers with subject code: WIA1005
✅ Found 12 papers
Step 3: Downloading papers...
Downloading papers: 100%|████████████| 12/12 [00:45<00:00,  3.78s/file]
Step 4: Creating ZIP archive...
✅ ZIP archive created: C:\Users\User\downloads\WIA1005_papers.zip

🎉 Success! All papers downloaded and zipped:
📦 ZIP file: C:\Users\User\downloads\WIA1005_papers.zip
📁 Individual files: C:\Users\User\downloads\WIA1005

✅ Download completed successfully!
Total papers downloaded: 12
```

## 📞 Support

If you encounter issues:
1. Run with `--verbose` flag for detailed logs
2. Try `--browser edge` if Chrome fails
3. Check your UM credentials
4. Ensure you have internet connectivity
5. Report bugs to the package maintainer

Happy downloading! 🎉 