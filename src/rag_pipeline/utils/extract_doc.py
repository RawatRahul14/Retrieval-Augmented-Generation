# === Python Modules ===
import pdfplumber
from pathlib import Path
from typing import List, Tuple, Dict
import os


# === Function to extract text and tables from PDF files ===
def extract_from_pdf(
        folder_path: Path = Path("data")
) -> Tuple[List[Dict[str, str]], List[list], List[Dict[str, str]]]:
    """
    Extracts text and tables from all PDF files inside a folder, with page-level and file-level metadata.

    Args:
        folder_path (Path): Path to the folder containing PDF files.

    Returns:
        texts (list[dict]): Page-level extracted text chunks.
        tables (list[list]): Extracted tables.
        file_metadata (list[dict]): File-level metadata (per PDF file).
    """
    texts: List[Dict[str, str]] = []
    tables: List[list] = []
    file_metadata: List[Dict[str, str]] = []

    for pdf_file in folder_path.glob("*.pdf"):
        print(f"📄 Reading {pdf_file.name} ...")

        try:
            file_info = {
                "file_name": pdf_file.name,
                "file_path": str(pdf_file.resolve()),
                "type": "pdf",
                "size_kb": round(os.path.getsize(pdf_file) / 1024, 2),
                "total_pages": 0,
                "total_tables": 0
            }

            with pdfplumber.open(pdf_file) as pdf:
                file_info["total_pages"] = len(pdf.pages)
                for i, page in enumerate(pdf.pages, start=1):
                    text = page.extract_text()
                    if text:
                        texts.append({
                            "content": text.strip(),
                            "metadata": {
                                "source": pdf_file.name,
                                "type": "pdf",
                                "page_number": i
                            }
                        })
                    page_tables = page.extract_tables()
                    if page_tables:
                        tables.extend(page_tables)
                        file_info["total_tables"] += len(page_tables)

            file_metadata.append(file_info)

        except Exception as e:
            print(f"⚠️ Error reading {pdf_file.name}: {e}")

    print(f"✅ Extracted {len(texts)} pages and {len(tables)} tables from PDFs.")
    return texts, tables, file_metadata


# === Function to extract text from text files ===
def extract_from_text_files(
        folder_path: Path = Path("data"),
        merge_n: int = 2
) -> Tuple[List[Dict[str, str]], List[Dict[str, str]]]:
    """
    Extracts text from .txt files, splits into chunks, merges them, and adds file-level metadata.

    Args:
        folder_path (Path): Path to folder containing .txt files.
        merge_n (int): Number of paragraphs to merge together.

    Returns:
        texts (list[dict]): Text chunks with metadata.
        file_metadata (list[dict]): File-level metadata.
    """
    texts: List[Dict[str, str]] = []
    file_metadata: List[Dict[str, str]] = []

    for txt_file in folder_path.glob("*.txt"):
        try:
            content = txt_file.read_text(encoding="utf-8").strip()
            if not content:
                print(f"⚠️ Skipped empty file: {txt_file.name}")
                continue

            paragraphs = [p.strip() for p in content.split("\n\n") if p.strip()]
            merged_chunks = [
                " ".join(paragraphs[i:i + merge_n])
                for i in range(0, len(paragraphs), merge_n)
            ]

            for idx, chunk in enumerate(merged_chunks, start=1):
                texts.append({
                    "content": chunk,
                    "metadata": {
                        "source": txt_file.name,
                        "type": "text",
                        "chunk_id": idx
                    }
                })

            file_info = {
                "file_name": txt_file.name,
                "file_path": str(txt_file.resolve()),
                "type": "text",
                "size_kb": round(os.path.getsize(txt_file) / 1024, 2),
                "total_chunks": len(merged_chunks)
            }
            file_metadata.append(file_info)

            print(f"📄 {txt_file.name}: {len(merged_chunks)} chunks")

        except Exception as e:
            print(f"⚠️ Error reading {txt_file.name}: {e}")

    print(f"✅ Extracted {len(texts)} text chunks from '{folder_path}'.")
    return texts, file_metadata