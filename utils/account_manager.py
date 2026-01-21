import json
import os

FILE = "accounts.json"


def load_accounts():
    if not os.path.exists(FILE):
        with open(FILE, "w") as f:
            json.dump([], f)
        return []

    with open(FILE, "r") as f:
        return json.load(f)


def save_accounts(accounts):
    with open(FILE, "w") as f:
        json.dump(accounts, f, indent=4)


def create_account(username, password):
    accounts = load_accounts()

    # nome duplicado
    for acc in accounts:
        if acc["username"] == username:
            return None

    new_id = len(accounts) + 1

    account = {
    "id": new_id,
    "username": username,
    "password": password,
    "inventory": {
        "skins": [],
        "banners": [],
        "avatars": []
    },
    "equipped": {
        "skin": None,
        "banner": None,
        "avatar": None
    }
}

    accounts.append(account)
    save_accounts(accounts)
    return account


def login_account(username, password):
    accounts = load_accounts()

    for acc in accounts:
        if acc["username"] == username and acc["password"] == password:
            return acc

    return None