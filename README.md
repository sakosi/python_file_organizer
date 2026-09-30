# Python File Organizer

A lightweight Python utility that automatically sorts new files in a selected folder. By default, it watches `~/Downloads`, detects a file extension, and moves the file to the appropriate category folder.

## Features

- Watches for new files with `watchdog`.
- Sorts files into `Images`, `Documents`, `Tables`, `Archives`, and `Other`.
- Creates category folders automatically.
- Prevents filename conflicts: `photo.jpg` becomes `photo (1).jpg` when needed.
- Saves activity history to `logs/app.log`.
- Includes a one-time mode for sorting files that already exist in a folder.

## Tech Stack

Python, watchdog, pathlib, shutil, logging.

## Installation

Python 3.10 or newer is required.

```bash
git clone https://github.com/sakosi/python_file_organizer.git
cd python_file_organizer

python -m venv .venv
source .venv/bin/activate        # macOS / Linux
# .\.venv\Scripts\Activate.ps1    # Windows PowerShell

pip install -r requirements.txt
```

## Usage

Start watching the default Downloads folder:

```bash
python main.py
```

Watch a different folder:

```bash
python main.py --watch-dir /path/to/folder
```

Sort files that are already in a folder once, then exit:

```bash
python main.py --watch-dir /path/to/folder --once
```

Press `Ctrl+C` to stop the continuous watcher.

## File Categories

| Extensions | Destination folder |
| --- | --- |
| JPG, JPEG, PNG, GIF, BMP, WEBP, SVG, HEIC | `Images` |
| PDF, DOC, DOCX | `Documents` |
| XLS, XLSX, CSV | `Tables` |
| ZIP, RAR, 7Z, TAR, GZ | `Archives` |
| All other files | `Other` |

Temporary download files such as `.crdownload`, `.part`, and `.tmp` are skipped until the final file is available.

## Example Folder Structure

```text
Downloads/
├── Images/
│   ├── photo.jpg
│   └── logo.png
├── Documents/
│   └── contract.pdf
├── Tables/
│   └── report.xlsx
├── Archives/
│   └── assets.zip
└── Other/
    └── notes.txt
```


