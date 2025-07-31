import json
import os
import secrets

DISCUSSIONS_FILE = "all_discussions.json"
DISCUSSIONS_PATH = "./discussions/"

def init_discussions_file(name: str = DISCUSSIONS_FILE):
    if not os.path.exists(name):
        with open(DISCUSSIONS_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f)


def add_new_discussion(name: str):
    init_discussions_file()
    with open(DISCUSSIONS_FILE, 'r+', encoding='utf-8') as f:
        try:
            discussions = json.load(f)
        except json.JSONDecodeError:
            discussions = []

        last_disc = None
        if len(discussions):
            last_disc = discussions[len(discussions) - 1]
        print("last disc:")
        print(last_disc)
        if last_disc is not None and last_disc.get("id") >= 0:
            new_index = last_disc["id"] + 1
        else:
            new_index = 0
        filename = secrets.token_hex(8)  # 16 caractères hex aléatoires
        new_path = DISCUSSIONS_PATH + filename + ".txt"
        new_chat = {"name": name, "path": new_path, "id": new_index};
        discussions.append(new_chat)
        f.seek(0)
        json.dump(discussions, f, ensure_ascii=False, indent=2)
        f.truncate()

        init_history_file(new_path)

        return new_chat
    
def delete_discussion(id: int):
    with open(DISCUSSIONS_FILE, 'r+', encoding='utf-8') as f:
        try:
            discussions = json.load(f)
        except json.JSONDecodeError:
            return {}
        index = 0
        for disc in discussions:
            if disc.get("id") is id:
                discussions.pop(index)
            index += 1
        f.seek(0)
        json.dump(discussions, f, ensure_ascii=False, indent=2)
        f.truncate()

def rename_discussion(id: int, new_name: str):
    with open(DISCUSSIONS_FILE, 'w+', encoding='utf-8') as f:
        try:
            discussions = json.load(f)
        except json.JSONDecodeError:
            discussions = []
        for disc in discussions:
            if disc.get("id") is id:
                disc['name'] = new_name
        f.seek(0)
        json.dump(discussions, f, ensure_ascii=False, indent=2)
        f.truncate()

def get_last_discussion():
    init_discussions_file()
    with open(DISCUSSIONS_FILE, 'r+', encoding='utf-8') as f:
        try:
            discussions = json.load(f)
        except json.JSONDecodeError:
            return []
        if len(discussions):
            return discussions[len(discussions) - 1]
        return {}

def get_discussion(id: int):
    init_discussions_file()
    with open(DISCUSSIONS_FILE, 'r+', encoding='utf-8') as f:
        try:
            discussions = json.load(f)
        except json.JSONDecodeError:
            discussions = []
        for disc in discussions:
            disc_id = disc["id"]
            if id == disc_id:
                print(disc)
                return disc
        return None
    
def get_all_discussions():
    init_discussions_file()
    with open(DISCUSSIONS_FILE, 'r+', encoding='utf-8') as f:
        try:
            discussions = json.load(f)
        except json.JSONDecodeError:
            discussions = []
        return discussions

def init_history_file(path: str):
    if not os.path.exists(path):
        with open(path, 'w', encoding='utf-8') as f:
            json.dump([], f)

def append_to_history(id: int, question: str, answer: str):
    discussion = get_discussion(id)

    with open(discussion["path"], 'r+', encoding='utf-8') as f:
        try:
            history = json.load(f)
        except json.JSONDecodeError:
            history = []
        last_mess = get_last_messages(id, 1)
        if (len(last_mess)):
            new_id = last_mess[0]["id"] + 1
        else:
            new_id = 0;
        history.append({"question": question, "answer": answer, "id": new_id})
        f.seek(0)
        json.dump(history, f, ensure_ascii=False, indent=2)
        f.truncate()

def get_all_messages(id: int):
    discussion = get_discussion(id)

    with open(discussion["path"], 'r', encoding='utf-8') as file:
        try:
            history = json.load(file)
        except json.JSONDecodeError:
            return []
        return history

def get_last_messages(id: int, n: int = 5):
    discussion = get_discussion(id)
    print("Discussion: ")
    print(discussion)
    with open(discussion["path"], 'r', encoding='utf-8') as f:
        try:
            history = json.load(f)
        except json.JSONDecodeError:
            return []
        return history[-n:]

def clear_history(id: int):
    discussion = get_discussion(id)

    with open(discussion["path"], 'w', encoding='utf-8') as f:
        json.dump([], f)
