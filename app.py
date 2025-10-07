# === Python Modules ===
import os
import streamlit as st
import requests
from dotenv import load_dotenv

load_dotenv()

# === Loading the Environment Variables ===
API_URL = os.getenv("API_URL")

# === Main UI Body ===
def main():
    """
    Function to render the main UI body of the app
    """
    # === Page Configurations ===
    st.set_page_config(
        page_title = "Retrieval Augmented Generation Model",
        layout = "wide"
    )

    st.title("📊 AI-Powered Document Analyzer")

    ## === Sidebar ===
    with st.sidebar:
        ### === File Upload ===
        uploaded_files = st.file_uploader(
            "📄 Upload up to 20 documents",
            type = ["pdf", "txt"],
            accept_multiple_files = True,
            help = "You can upload up to 20 documents (PDF or TXT)."
        )

        ### === Upload Button ===
        if st.button(
            "Upload Files",
            key = "upload_button"
        ):
            if not uploaded_files:
                st.warning("Please select at least one file.")

            elif len(uploaded_files) > 20:
                st.error("❌ Maximum 20 files allowed at once.")

            else:
                with st.spinner("📤 Uploading and processing all files..."):
                    try:
                        ## === Prepare multi-file upload ===
                        files = [
                            ("files", (file.name, file.getvalue(), file.type))
                            for file in uploaded_files
                        ]

                        ## === Send as a single POST request ===
                        resp = requests.post(
                            f"{API_URL}/upload/",
                            files = files
                        )

                        if resp.status_code == 200:
                            data = resp.json()
                            if data["status"] == "success":
                                st.session_state.session_id = data["session_id"]
                                st.success(
                                    f"✅ Uploaded {len(uploaded_files)} files under session {data['session_id']}"
                                )
                            else:
                                st.error(data["message"])

                        else:
                            st.error(f"❌ Upload failed ({resp.status_code})")

                    except Exception as e:
                        st.error(f"⚠️ Error: {str(e)}")

if __name__ == "__main__":
    main()