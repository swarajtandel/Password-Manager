# Password Manager

A secure, cross-platform command‑line password manager in Python.
Stores credentials in an encrypted SQLite database and protects them with a master password.

---

## Project Structure

```
password_manager/
├── main.py            # Entry point: CLI and user workflow
├── db_manager.py      # Database operations (create, read, update)
├── crypto_utils.py    # AES encryption/decryption and key derivation
├── utils.py           # Helpers (strong password generator)
├── requirements.txt   # Pinned dependencies
└── README.md          # This documentation
```

## Features

* **Secure Storage:** AES‑CBC encryption with PKCS#7 padding; IV prepended and Base64‑encoded.
* **Master Password:** Derives a 256‑bit key via PBKDF2 for all operations.
* **Credential Management:** Add, retrieve, and list service credentials.
* **Password Generation:** Built‑in generator for strong random passwords.
* **Cross‑Platform CLI:** Works on Windows, macOS, and Linux.

---

## Prerequisites

* Python 3.8+
* Git (optional, for cloning the repo)

---

## Environment Setup (Windows / VS Code)

1. **Select Python Interpreter**

   * Ctrl+Shift+P → “Python: Select Interpreter” → choose the one in `\.venv\Scripts\python.exe`

2. **Switch Terminal to CMD**

   * Open terminal (Ctrl+\`) → click ▾ → Select Default Profile → Command Prompt → reopen terminal

3. **Activate the Virtual Environment**

   ```bat
   .venv\Scripts\activate.bat
   ```

4. **Install Dependencies**

   ```bat
   pip install -r requirements.txt
   ```

> **Tip:** After adding new packages (e.g. `pycryptodome`), update with:
>
> ```bat
> pip install pycryptodome
> pip freeze > requirements.txt
> ```

---

## Quick Install & Run (Linux / macOS)

```bash
git clone https://github.com/yourusername/password_manager.git
cd password_manager
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

---

## Usage

```bash
python main.py
```

### First Run

1. You’ll be prompted to **set** a master password.
2. The app exits.
3. Re-run `python main.py` and **enter** your master password.

### Menu Options

* **\[1] Add credential**: Save a service, username, and password.
* **\[2] Retrieve credential**: Decrypts and displays credentials.
* **\[3] Generate password**: Outputs a strong random password.
* **\[4] Exit**: Quit.

---

## How It Works

1. **Key Derivation**

   * Master password → PBKDF2 → 32‑byte AES key (with salt stored in DB).

2. **Encryption / Decryption**

   * AES‑CBC with a fresh IV per entry → ciphertext stored as Base64.

3. **Storage**

   * SQLite holds:

   ```sql
   CREATE TABLE IF NOT EXISTS credentials (
     service TEXT PRIMARY KEY,
     username TEXT,
     password BLOB
   );
   ```

   * A separate table stores the salt+hashed master key.

---

Happy securing!
