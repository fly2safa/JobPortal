# TalentNest Testing Tracker - GUI Tool

## Overview

A standalone GUI application for tracking manual testing progress. Perfect for team collaboration where multiple testers can work independently and merge their results.

![Testing Tracker](screenshot.png)

---

## Features

✅ **Interactive Test List** - All 50+ test cases organized by section  
✅ **Status Tracking** - Mark tests as Pass/Fail/Blocked/Not Started  
✅ **Detailed Test View** - View description, steps, and document results  
✅ **Progress Tracking** - Visual progress bar showing completion percentage  
✅ **Save/Load Progress** - Save your work and continue later  
✅ **Export Reports** - Generate markdown reports for documentation  
✅ **Team Collaboration** - Each tester saves their own file  
✅ **Navigation** - Previous/Next buttons for easy navigation  
✅ **Tester Info** - Track who tested what and when  

---

## Installation

### Prerequisites

- **Python 3.8+** (Tkinter comes pre-installed with Python)
- No additional dependencies required!

### Quick Start

1. **Navigate to the testing_tool directory:**
   ```bash
   cd JobPortal/testing_tool
   ```

2. **Run the application:**
   ```bash
   python test_tracker.py
   ```

That's it! The GUI will open immediately.

---

## Usage Guide

### 1. First Time Setup

When you first open the application:

1. **Enter your name** in the "Tester" field (top right)
2. **Select your browser** from the dropdown
3. This information will be saved for future sessions

### 2. Running Tests

1. **Select a test case** from the left panel
2. **Read the description and steps** in the right panel
3. **Perform the test** following the steps
4. **Select the status:**
   - ⬜ **Not Started** - Haven't tested yet
   - ✅ **Pass** - Test passed successfully
   - ❌ **Fail** - Test failed (bug found)
   - 🚫 **Blocked** - Cannot test (dependency issue)
5. **Document results** in the "Actual Results" text area
6. **Add notes** if needed (e.g., bug details, screenshots location)
7. **Click "Next"** to move to the next test

### 3. Saving Progress

**Important:** Save your progress regularly!

1. Click **"Save Progress"** button
2. Choose a filename (suggested format: `test_progress_YourName_YYYYMMDD.json`)
3. Save to a location you can access later

**Recommended:** Save your file in the project under `testing_tool/results/`

### 4. Loading Progress

To continue where you left off:

1. Click **"Load Progress"** button
2. Select your previously saved JSON file
3. All your test results will be restored

### 5. Exporting Reports

When you're done testing (or want to share progress):

1. Click **"Export Report"** button
2. Choose a filename (suggested format: `test_report_YourName_YYYYMMDD.md`)
3. A markdown report will be generated with:
   - Summary statistics
   - All test results
   - Your notes and findings

---

## Team Collaboration Workflow

### For Individual Testers

1. **Start testing:**
   ```bash
   python test_tracker.py
   ```

2. **Enter your name** (e.g., "Alice", "Bob", "Charlie")

3. **Test your assigned sections** or all sections

4. **Save your progress** regularly:
   - File: `results/test_progress_Alice_20241112.json`

5. **When done, export report:**
   - File: `results/test_report_Alice_20241112.md`

6. **Commit your files:**
   ```bash
   git add testing_tool/results/test_progress_Alice_20241112.json
   git add testing_tool/results/test_report_Alice_20241112.md
   git commit -m "test: Alice's testing results for authentication and job seeker features"
   git push
   ```

### For Team Lead (Merging Results)

1. **Collect all JSON files** from team members:
   - `test_progress_Alice_20241112.json`
   - `test_progress_Bob_20241112.json`
   - `test_progress_Charlie_20241112.json`

2. **Use the merge script** (see below)

3. **Generate final report**

---

## File Structure

```
testing_tool/
├── test_tracker.py          # Main GUI application
├── README.md                # This file
├── merge_results.py         # Script to merge multiple test results (optional)
├── results/                 # Directory for saving test results
│   ├── test_progress_Alice_20241112.json
│   ├── test_progress_Bob_20241112.json
│   ├── test_report_Alice_20241112.md
│   └── test_report_Bob_20241112.md
└── tester_info.json         # Auto-saved tester info (gitignored)
```

---

## Test Sections

The tool includes all test cases from the Manual Testing Guide:

1. **Authentication & Authorization** (6 tests)
   - Registration, Login, Logout, Protected Routes

2. **Job Seeker Features** (7 tests)
   - Browse Jobs, Search, Apply, Resume Upload, Profile

3. **Employer Features** (10 tests)
   - Dashboard, Job Posting, Applications, Candidate Management

4. **AI Features** (4 tests)
   - Resume Parsing, AI Assistant, Cover Letter Generation, Recommendations

5. **Edge Cases & Error Handling** (7 tests)
   - Validation, Network Errors, Security, Concurrency

6. **Responsive Design** (3 tests)
   - Mobile, Tablet, Desktop

7. **Performance** (3 tests)
   - Page Load, Search, Large Datasets

**Total: 40 Test Cases**

---

## Tips & Best Practices

### Testing Tips

1. **Test systematically** - Go through sections in order
2. **Document everything** - Be detailed in "Actual Results"
3. **Take screenshots** - Save them and reference in notes
4. **Report bugs immediately** - Don't wait until the end
5. **Save frequently** - Don't lose your work!

### Writing Good Test Results

**Bad:**
```
Actual Results: It works
```

**Good:**
```
Actual Results:
- Registration form appeared correctly
- All fields validated properly
- User was created successfully
- Redirected to dashboard
- Welcome message displayed with user's name
```

**For Failures:**
```
Actual Results:
- Registration form appeared
- Entered valid data
- Clicked Submit
- ERROR: Got 500 Internal Server Error
- Console shows: "TypeError: Cannot read property 'name' of undefined"
- Screenshot saved: screenshots/registration_error_001.png
```

### Status Guidelines

- **Pass** ✅: Everything works as expected, no issues
- **Fail** ❌: Bug found, feature doesn't work correctly
- **Blocked** 🚫: Cannot test (e.g., depends on failed test, server down)
- **Not Started** ⬜: Haven't tested yet

---

## Keyboard Shortcuts

- **Tab** - Navigate between fields
- **Enter** - (when in test list) Open selected test
- **Ctrl+S** - Save progress (when implemented)
- **Ctrl+N** - Next test (when implemented)
- **Ctrl+P** - Previous test (when implemented)

---

## Troubleshooting

### Application Won't Start

**Problem:** `python test_tracker.py` doesn't work

**Solution:**
1. Check Python version: `python --version` (need 3.8+)
2. Try: `python3 test_tracker.py`
3. On Windows: Make sure Python is in PATH

### Tkinter Not Found

**Problem:** `ModuleNotFoundError: No module named 'tkinter'`

**Solution:**

**On Ubuntu/Debian:**
```bash
sudo apt-get install python3-tk
```

**On macOS:**
```bash
brew install python-tk
```

**On Windows:**
Tkinter should come with Python. Reinstall Python with "tcl/tk" option checked.

### Cannot Save Files

**Problem:** Permission denied when saving

**Solution:**
1. Create `results/` directory manually
2. Check folder permissions
3. Save to a different location (Desktop, Documents)

### Progress Not Loading

**Problem:** Loaded file but no data appears

**Solution:**
1. Check if JSON file is valid (open in text editor)
2. Ensure file is from this version of the tool
3. Try exporting a new file and loading it

---

## Advanced Features

### Custom Test Cases

You can modify `test_tracker.py` to add your own test cases:

```python
test_cases.append(
    TestCase("8.1", "Custom Section", "My Custom Test",
            "Test description here",
            ["Step 1", "Step 2", "Step 3"])
)
```

### Merging Multiple Results

Create `merge_results.py` to merge multiple tester's results:

```python
import json
from pathlib import Path

def merge_results(file_list, output_file):
    """Merge multiple test result files."""
    merged_data = {"test_cases": {}}
    
    for file in file_list:
        with open(file, 'r') as f:
            data = json.load(f)
            for test in data["test_cases"]:
                test_id = test["id"]
                if test_id not in merged_data["test_cases"]:
                    merged_data["test_cases"][test_id] = test
                elif test["status"] != "Not Started":
                    # Prefer completed tests
                    merged_data["test_cases"][test_id] = test
    
    # Convert back to list
    merged_data["test_cases"] = list(merged_data["test_cases"].values())
    
    with open(output_file, 'w') as f:
        json.dump(merged_data, f, indent=2)

# Usage
merge_results([
    "results/test_progress_Alice_20241112.json",
    "results/test_progress_Bob_20241112.json"
], "results/merged_results.json")
```

---

## Contributing

Found a bug in the testing tool? Want to add features?

1. Create an issue describing the problem/feature
2. Fork the repository
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

## FAQ

**Q: Can multiple people use the same JSON file?**  
A: Not recommended. Each person should have their own file to avoid conflicts.

**Q: Can I edit the JSON file manually?**  
A: Yes, but be careful with the JSON syntax. It's better to use the GUI.

**Q: How do I share my results with the team?**  
A: Export the markdown report and share it, or commit your JSON file to Git.

**Q: Can I run this on Linux/Mac?**  
A: Yes! Python and Tkinter work on all platforms.

**Q: The window is too small/large. Can I resize it?**  
A: Yes, just drag the window edges. The layout is responsive.

**Q: Can I print the report?**  
A: Yes, export to markdown, then convert to PDF using tools like Pandoc or print from a markdown viewer.

---

## Support

Need help?

1. Check this README
2. Check the main [MANUAL_TESTING_GUIDE.md](../docs/MANUAL_TESTING_GUIDE.md)
3. Ask in the team chat
4. Create an issue on GitHub

---

## Version History

**v1.0** (2024-11-12)
- Initial release
- 40 test cases
- Save/Load/Export functionality
- Progress tracking
- Team collaboration support

---

**Happy Testing! 🧪✨**

