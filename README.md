# Python File Organizer

Небольшая Python-утилита, которая автоматически сортирует новые файлы в выбранной папке. По умолчанию она наблюдает за `~/Downloads`, определяет расширение файла и переносит его в нужную подпапку.

## Возможности

- отслеживание новых файлов с помощью `watchdog`;
- категории `Images`, `Documents`, `Tables`, `Archives` и `Other`;
- автоматическое создание папок категорий;
- защита от совпадающих имён: `photo.jpg` → `photo (1).jpg`;
- логирование действий в `logs/app.log`;
- однократный режим сортировки для уже существующих файлов.

## Стек

Python, watchdog, pathlib, shutil, logging.

## Установка

Нужен Python 3.10 или новее.

```bash
cd file-organizer
python -m venv .venv
source .venv/bin/activate        # macOS / Linux
# .venv\Scripts\activate         # Windows PowerShell
pip install -r requirements.txt
```

## Запуск

Запустить наблюдение за стандартной папкой загрузок:

```bash
python main.py
```

Указать другую папку:

```bash
python main.py --watch-dir /путь/к/папке
```

Отсортировать уже существующие файлы один раз и завершить работу:

```bash
python main.py --watch-dir /путь/к/папке --once
```

Остановить постоянное наблюдение можно сочетанием `Ctrl+C`.

## Категории

| Расширения | Папка |
| --- | --- |
| JPG, JPEG, PNG, GIF, BMP, WEBP, SVG, HEIC | `Images` |
| PDF, DOC, DOCX | `Documents` |
| XLS, XLSX, CSV | `Tables` |
| ZIP, RAR, 7Z, TAR, GZ | `Archives` |
| Остальные | `Other` |

Временные файлы незавершённых загрузок (`.crdownload`, `.part`, `.tmp`) пропускаются до появления итогового файла.

## Пример структуры

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

## Описание для портфолио

> **Python File Organizer** — утилита для автоматической сортировки файлов в выбранной папке. Программа отслеживает появление новых файлов и распределяет их по категориям в зависимости от расширения. Реализованы логирование, обработка конфликтов имён и настройка целевой папки.
