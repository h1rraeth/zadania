# storage.py
import json
import os
from datetime import datetime
from pathlib import Path

DATA_DIR = Path("transactions")
USERS_FILE = Path("users.json")


def ensure_directories():
    DATA_DIR.mkdir(exist_ok=True)
    if not USERS_FILE.exists():
        save_users({})


def load_users() -> dict:
    if not USERS_FILE.exists():
        return {}
    try:
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}


def save_users(users: dict):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)


def load_transactions(username: str) -> list:
    file_path = DATA_DIR / f"{username}.json"
    if not file_path.exists():
        return []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []


def save_transactions(username: str, transactions: list):
    file_path = DATA_DIR / f"{username}.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(transactions, f, ensure_ascii=False, indent=2)


def add_transaction(username: str, trans_type: str, amount: float, note: str = ""):
    transactions = load_transactions(username)
    transaction = {
        "type": trans_type,
        "amount": round(float(amount), 2),
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "note": note,
    }
    transactions.append(transaction)
    save_transactions(username, transactions)
