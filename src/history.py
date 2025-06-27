import json
import os
from typing import List, Dict

HISTORY_FILE = "chat_history.json"

def init_history_file():
    if not os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f)

def append_to_history(question: str, answer: str):
    init_history_file()
    with open(HISTORY_FILE, 'r+', encoding='utf-8') as f:
        try:
            history = json.load(f)
        except json.JSONDecodeError:
            history = []

        history.append({"question": question, "answer": answer})
        f.seek(0)
        json.dump(history, f, ensure_ascii=False, indent=2)
        f.truncate()

def get_all_messages() -> List[Dict[str, str]]:
    init_history_file()
    with open(HISTORY_FILE, 'r', encoding='utf-8') as file:
        try:
            history = json.load(file)
        except json.JSONDecodeError:
            return []
        return history

def get_last_messages(n: int = 5) -> List[Dict[str, str]]:
    init_history_file()
    with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
        try:
            history = json.load(f)
        except json.JSONDecodeError:
            return []
        return history[-n:]

def clear_history():
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump([], f)
