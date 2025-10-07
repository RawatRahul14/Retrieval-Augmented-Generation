# === Python Modules ===
from pydantic import BaseModel
from typing import Literal, List, Dict, Any

## === Response Model for File Upload ===
class UploadResponse(BaseModel):
    status: Literal["success", "failure"] = "failure"
    session_id: str | None = None
    saved_path: str | None = None
    uploaded_file: str | None = None
    message: str