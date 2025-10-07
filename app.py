# === Python Modules ===
import os
import streamlit as st
import requests
from dotenv import load_dotenv

# === Utils ===
from rag_pipeline.utils.common import (
    init_session,
    stream_text,
    load_yaml
)

# === Load Environment ===
load_dotenv()
API_URL = os.getenv("API_URL")

# === Main UI Body ===
def main():
    """
    Streamlit Frontend for Retrieval-Augmented Generation Pipeline
    """
    # === Page Configurations ===
    st.set_page_config(
        page_title = "Retrieval Augmented Generation Model",
        layout = "wide"
    )

    st.title("📊 AI-Powered Document Analyzer")
    init_session()

    # === Sidebar (Upload Section) ===
    with st.sidebar:
        st.header("📁 Upload Documents")
        uploaded_files = st.file_uploader(
            "Upload up to 20 documents",
            type = ["pdf", "txt"],
            accept_multiple_files = True,
            help = "You can upload up to 20 PDF or TXT files."
        )

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
                        # Prepare multi-file payload
                        files = [("files", (f.name, f.getvalue(), f.type)) for f in uploaded_files]

                        # Send upload request
                        resp = requests.post(
                            f"{API_URL}/upload/",
                            files = files
                        )

                        if resp.status_code == 200:
                            data = resp.json()
                            if data.get("status") == "success":
                                st.session_state.session_id = data["session_id"]
                                st.success(f"✅ Uploaded {len(uploaded_files)} files under session **{data['session_id']}**")
                            else:
                                st.error(f"⚠️ {data.get('message', 'Upload failed')}")

                        else:
                            st.error(f"❌ Upload failed ({resp.status_code})")

                    except Exception as e:
                        st.error(f"⚠️ Error during upload: {e}")

    # === Chat Section ===
    st.markdown("---")
    st.subheader("💬 Chat with Your Uploaded Documents")

    # Validate session before chat
    if "session_id" not in st.session_state or not st.session_state.session_id:
        st.info("Please upload files first to start chatting.")
        st.stop()

    # Initialize message states
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "pending_stream" not in st.session_state:
        st.session_state.pending_stream = None

    # === Display Chat History ===
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            if msg["role"] == "assistant" and msg["content"] == st.session_state["pending_stream"]:
                st.write_stream(stream_text(msg["content"]))
                st.session_state.pending_stream = None

            else:
                st.markdown(msg["content"])

    # === User Input ===
    user_query = st.chat_input("Ask your question here...")

    # === Backend Call ===
    if user_query:
        # Store user message immediately
        st.session_state.messages.append(
            {
                "role": "user",
                "content": user_query
            }
        )

        # Display the user message right away (before backend reply)
        with st.chat_message("user"):
            st.markdown(user_query)

        # Show a spinner for the assistant reply while processing
        with st.chat_message("assistant"):
            with st.spinner("🤖 Thinking..."):
                try:
                    resp = requests.post(
                        url = f"{API_URL}/query/",
                        json = {
                            "session_id": st.session_state["session_id"],
                            "user_query": user_query
                        },
                        timeout = 120
                    )

                    if resp.status_code == 200:
                        data = resp.json()
                        if data.get("status") == "success":
                            bot_reply = data.get("answer", "No answer returned.")
                        else:
                            bot_reply = f"⚠️ {data.get('message', 'Query failed')}"

                    else:
                        bot_reply = f"❌ Server responded with status {resp.status_code}"

                except Exception as e:
                    bot_reply = f"⚠️ Error connecting to backend: {str(e)}"

        # Store assistant message
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": bot_reply
            }
        )
        st.session_state.pending_stream = bot_reply

        st.rerun()

if __name__ == "__main__":
    main()