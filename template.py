# === Python Modules ===
import os
from pathlib import Path
import logging

# === Logging Config ===
logging.basicConfig(
    level = logging.INFO,
    format = "[%(asctime)s] — %(message)s"
)

# === Project Metadata ===
PROJECT_NAME = "rag_pipeline"

# === File Structure ===
FILES = [
    f"src/{PROJECT_NAME}/__init__.py",
    f"src/{PROJECT_NAME}/components/__init__.py",
    f"src/{PROJECT_NAME}/utils/__init__.py",
    f"src/{PROJECT_NAME}/utils/common.py",
    f"src/{PROJECT_NAME}/agents/__init__.py",
    "config/config.yaml",
    "main.py",
    "app.py",
    "graph.py",
    "Dockerfile",
    "requirements.txt",
    "research/trials.ipynb",
    "setup.py"
]

# === Directory & File Creation ===
for path_str in FILES:
    path = Path(path_str)
    dir_path, file_name = os.path.split(path)

    ## === Create directories if missing ===
    if dir_path:
        os.makedirs(dir_path, exist_ok=True)
        logging.info(f"Ensured directory: {dir_path}")

    ## === Create file if missing or empty ===
    if not path.exists() or path.stat().st_size == 0:
        path.touch()
        logging.info(f"Created empty file: {path}")
    else:
        logging.info(f"Skipped (already exists): {file_name}")