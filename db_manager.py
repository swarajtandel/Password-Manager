import sqlite3
from crypto_utils import CryptoManager

class DatabaseManager:
    def __init__(self, db_path, crypto: CryptoManager):
        self.db_path = db_path
        self.crypto = crypto
        self.conn = sqlite3.connect(self.db_path)
        self._create_tables()

    def _create_tables(self):
        c = self.conn.cursor()
        c.execute(
            '''CREATE TABLE IF NOT EXISTS master (
                   id INTEGER PRIMARY KEY,
                   password_hash TEXT NOT NULL
               )''')
        c.execute(
            '''CREATE TABLE IF NOT EXISTS credentials (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   service TEXT NOT NULL,
                   username TEXT NOT NULL,
                   password TEXT NOT NULL
               )''')
        self.conn.commit()

    def master_exists(self):
        c = self.conn.cursor()
        c.execute("SELECT COUNT(*) FROM master")
        return c.fetchone()[0] > 0

    def setup_master(self):
        # Store hash of master password key
        password_hash = self.crypto.hash_master()
        c = self.conn.cursor()
        c.execute("INSERT INTO master (password_hash) VALUES (?)", (password_hash,))
        self.conn.commit()

    def verify_master(self, master_password):
        stored_hash = self.conn.cursor().execute(
            "SELECT password_hash FROM master").fetchone()[0]
        return self.crypto.verify_master(master_password, stored_hash)

    def add_credential(self, service, username, password):
        enc_username = self.crypto.encrypt(username)
        enc_password = self.crypto.encrypt(password)
        c = self.conn.cursor()
        c.execute(
            "INSERT INTO credentials (service, username, password) VALUES (?, ?, ?)",
            (service, enc_username, enc_password)
        )
        self.conn.commit()

    def get_credential(self, service):
        c = self.conn.cursor()
        c.execute("SELECT username, password FROM credentials WHERE service=?", (service,))
        row = c.fetchone()
        if row:
            return {
                "username": self.crypto.decrypt(row[0]),
                "password": self.crypto.decrypt(row[1])
            }
        return None