# === Python Modules ===
from typing import List, Dict, Any
from datetime import datetime, timezone
from pymongo import AsyncMongoClient
import os
from dotenv import load_dotenv

# === Load environment variables ===
load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("DB_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME_UPLOAD")

async def upload_file_metadata(
    session_id: str,
    file_metadata: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """
    Uploads file metadata to MongoDB for the given session_id.
    Handles its own MongoDB connection lifecycle.

    Args:
        session_id (str): Unique session identifier.
        file_metadata (List[Dict[str, Any]]): List of file metadata dicts.

    Returns:
        Dict[str, Any]: Document that was uploaded to MongoDB.
    """
    if not MONGODB_URI:
        raise ValueError("❌ MONGODB_URI is not set in environment variables.")

    client = None
    try:
        ## === Connect to MongoDB ===
        client = AsyncMongoClient(MONGODB_URI)
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]

        ## === Build the document ===
        document = {
            "session_id": session_id,
            "uploaded_files": file_metadata,
            "uploaded_at": datetime.now(timezone.utc)
        }

        ## === Insert or update existing record ===
        await collection.update_one(
            {"session_id": session_id},
            {"$set": document},
            upsert = True
        )

        print(f"✅ Metadata uploaded successfully for session_id: {session_id}")
        return document

    except Exception as e:
        print(f"⚠️ Error uploading metadata: {e}")
        raise e

    finally:
        ## === Close connection safely ===
        if client:
            await client.close()
            print("🔒 MongoDB connection closed.")