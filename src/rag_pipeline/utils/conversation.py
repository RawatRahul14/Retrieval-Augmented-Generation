# === Python Modules ===
from typing import Dict

# === Utility to manage conversation history ===
def update_recent_chats(
        recent_chats: Dict[int, Dict[str, str]],
        latest_question: str,
        latest_answer: str,
        max_chats: int = 3
) -> Dict[int, Dict[str, str]]:
    """
    Updates the conversation history to always contain the last `max_chats` turns.
    Automatically shifts and reindexes so keys remain sequential (1..max_chats).
    """
    # Ensure dictionary is valid
    if not isinstance(recent_chats, Dict):
        recent_chats = {}

    # Append the new chat at the end
    chats = list(recent_chats.values())
    chats.append({
        "question": latest_question.strip(),
        "answer": latest_answer.strip()
    })

    # Keep only the last N
    chats = chats[-max_chats:]

    # Rebuild with proper numeric keys (1..max_chats)
    recent_chats = {i + 1: chat for i, chat in enumerate(chats)}

    return recent_chats

def format_conversation_for_llm(
        recent_chats: Dict[int, Dict[str, str]]
) -> str:
    """
    Converts the structured recent_chats dictionary into a clean,
    LLM-readable text format preserving order and clarity.

    Example output:
        User: What is FAISS?
        Agent: A vector database used for similarity search.

        User: Explain embeddings.
        Agent: Embeddings represent text as numerical vectors.
    """
    if not recent_chats:
        return ""

    # Sort by key to maintain chronological order
    sorted_chats = dict(sorted(recent_chats.items()))

    # Convert into a plain-text chat log
    formatted = "\n\n".join(
        [f"User: {v['question']}\nAgent: {v['answer']}" for v in sorted_chats.values()]
    )

    return formatted