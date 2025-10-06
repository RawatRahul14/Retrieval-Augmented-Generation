# === Python Modules ===
import streamlit as st
from typing import Dict , Any, Literal
import time
import yaml
from pathlib import Path

## === Function to initialise the state session inside the Streamlit UI ===
def init_session():
    """
    Initialises the required state sessions
    """
    ### === Requierd State sessions ===
    sessions: Dict[str, Any] = {
        "messages": [],
        "start_interview": False,
        "session_id": None,
        "intro_shown": False,
        "pending_stream": None,
        "first_message_verification": None
    }

    ### === Initialising using the for loop ===
    for key, value in sessions.items():
        if key not in st.session_state:
            st.session_state[key] = value

# === Streaming generator ===
def stream_text(
        text: str,
        delay: float = 0.1
):
    """
    Creates a streaming-like effect in Streamlit UI.
    Preserves line breaks while typing word by word.
    """
    ## === Iterating over the text split by spaces ===
    for part in text.split(" "):

        ## === If there is a line break in the word ===
        if "\n" in part:

            # Split the part into lines
            lines = part.split("\n")

            # Stream each line (except the last one) with newline preserved
            for l in lines[:-1]:
                yield l + "\n"
                time.sleep(delay)

            # Stream the last segment of the line with a space
            yield lines[-1] + " "

        ## === If no line break, stream normally ===
        else:
            yield part + " "

        ## === Apply delay after each streamed part ===
        time.sleep(delay)

# === Function to Load a Specific YAML Topic ===
def load_yaml(
        file_name: Literal["config.yaml", "details.yaml"],
        topic: str,
        path: Path = Path("config")
) -> str:
    """
    Loads a specific topic section from a YAML file.

    Args:
        file_name (Literal): The name of the YAML file to load (e.g., "config.yaml", "details.yaml").
        topic (str): The topic key inside the YAML file to retrieve.
        path (Path, optional): Directory path where the YAML file is stored.

    Returns:
        str: The content corresponding to the provided topic.
    """

    ## === Construct File Path ===
    file_path: Path = path / file_name

    ## === Read YAML File and Extract Topic ===
    data = yaml.safe_load(
        file_path.read_text(encoding = "utf-8")
    )

    ## === Return the Requested Topic ===
    return data[topic]