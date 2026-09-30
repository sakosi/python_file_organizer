"""Automatic organizer for files that appear in a selected directory."""

from __future__ import annotations

import argparse
import logging
import shutil
import time
from pathlib import Path

from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer


CATEGORIES: dict[str, set[str]] = {
    "Images": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg", ".heic"},
    "Documents": {".pdf", ".doc", ".docx"},
    "Tables": {".xls", ".xlsx", ".csv"},
    "Archives": {".zip", ".rar", ".7z", ".tar", ".gz"},
}
OTHER_CATEGORY = "Other"
SKIPPED_SUFFIXES = {".crdownload", ".part", ".tmp", ".download"}
PROJECT_DIR = Path(__file__).resolve().parent


def category_for(path: Path) -> str:
    """Return a folder category based on a file extension."""
    suffix = path.suffix.lower()
    for category, extensions in CATEGORIES.items():
        if suffix in extensions:
            return category
    return OTHER_CATEGORY


def unique_destination(destination_dir: Path, filename: str) -> Path:
    """Return a free destination path, preserving the original extension."""
    candidate = destination_dir / filename
    if not candidate.exists():
        return candidate

    original = Path(filename)
    number = 1
    while True:
        candidate = destination_dir / f"{original.stem} ({number}){original.suffix}"
        if not candidate.exists():
            return candidate
        number += 1


def configure_logging(log_file: Path) -> None:
    """Configure file and console logging for the application."""
    log_file.parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[logging.FileHandler(log_file, encoding="utf-8"), logging.StreamHandler()],
    )


class FileOrganizer:
    """Moves files from a watched folder into category subfolders."""

    def __init__(self, watch_dir: Path) -> None:
        self.watch_dir = watch_dir.resolve()

    def organize(self, source: Path) -> Path | None:
        """Move one file and return its new path; ignore incomplete or absent files."""
        if not source.is_file():
            return None
        if source.suffix.lower() in SKIPPED_SUFFIXES:
            logging.debug("Skipped incomplete download: %s", source.name)
            return None

        category = category_for(source)
        destination_dir = self.watch_dir / category
        destination_dir.mkdir(exist_ok=True)
        destination = unique_destination(destination_dir, source.name)

        try:
            shutil.move(str(source), str(destination))
        except (FileNotFoundError, PermissionError, OSError) as error:
            logging.warning("Could not move %s: %s", source.name, error)
            return None

        logging.info("Moved %s -> %s", source.name, destination.relative_to(self.watch_dir))
        return destination

    def organize_existing_files(self) -> int:
        """Organize files currently located directly in the watched folder."""
        count = 0
        for path in self.watch_dir.iterdir():
            if path.is_file() and self.organize(path) is not None:
                count += 1
        return count


class NewFileHandler(FileSystemEventHandler):
    """Pass newly created or renamed files to the organizer."""

    def __init__(self, organizer: FileOrganizer) -> None:
        super().__init__()
        self.organizer = organizer

    def on_created(self, event: FileSystemEvent) -> None:
        if not event.is_directory:
            self.organizer.organize(Path(event.src_path))

    def on_moved(self, event: FileSystemEvent) -> None:
        if not event.is_directory:
            self.organizer.organize(Path(event.dest_path))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Automatically sort files that appear in a selected folder."
    )
    parser.add_argument(
        "--watch-dir",
        type=Path,
        default=Path.home() / "Downloads",
        help="Folder to monitor (default: ~/Downloads).",
    )
    parser.add_argument(
        "--once",
        action="store_true",
        help="Sort current top-level files once, then exit.",
    )
    parser.add_argument(
        "--log-file",
        type=Path,
        default=PROJECT_DIR / "logs" / "app.log",
        help="Log file path (default: logs/app.log next to main.py).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    watch_dir: Path = args.watch_dir.expanduser()
    watch_dir.mkdir(parents=True, exist_ok=True)
    configure_logging(args.log_file.expanduser())

    organizer = FileOrganizer(watch_dir)
    if args.once:
        moved_count = organizer.organize_existing_files()
        logging.info("One-time sorting completed. Moved files: %d", moved_count)
        return

    handler = NewFileHandler(organizer)
    observer = Observer()
    observer.schedule(handler, str(watch_dir), recursive=False)
    observer.start()
    logging.info("Watching folder: %s", watch_dir.resolve())
    logging.info("Press Ctrl+C to stop.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logging.info("Stopped by user.")
    finally:
        observer.stop()
        observer.join()


if __name__ == "__main__":
    main()
