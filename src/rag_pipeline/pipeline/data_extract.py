# === Python Modules ===
from pathlib import Path

# === Utils ===
from rag_pipeline.utils.extract_doc import (
    extract_from_pdf,
    extract_from_text_files
)

# === Function to extract data from documents ===
def extract_data_pipeline(
        session_folder: Path
) -> tuple[list, list, list]:
    """
    Extracts text, tables, and file-level metadata from PDF and text files in the 'data' folder.

    Returns:
        texts (list[dict]): List of extracted text chunks with metadata (page/paragraph level).
        tables (list[list]): List of extracted tables from PDFs.
        file_metadata (list[dict]): List of file-level metadata for both PDFs and text files.
    """
    # === Extract from PDFs ===
    pdf_texts, pdf_tables, pdf_meta = extract_from_pdf(folder_path = session_folder)

    # === Extract from text files ===
    txt_texts, txt_meta = extract_from_text_files(folder_path = session_folder)

    # === Combine all text chunks ===
    all_texts = (pdf_texts or []) + (txt_texts or [])

    # === Combine file metadata ===
    all_file_meta = (pdf_meta or []) + (txt_meta or [])

    print(f"✅ Combined {len(all_texts)} text chunks from {len(all_file_meta)} files.")
    return all_texts, pdf_tables, all_file_meta