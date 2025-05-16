import getpass
import sys
from db_manager import DatabaseManager
from crypto_utils import CryptoManager
from utils import generate_password

def main():
    # Prompt user for master password
    master_password = getpass.getpass("Enter master password: ")
    crypto = CryptoManager(master_password)
    db = DatabaseManager("passwords.db", crypto)

    # First-run setup: create master entry if none exists
    if not db.master_exists():
        print("No master password set. Setting up new master password.")
        db.setup_master()
        print("Master password setup complete. Please restart the application.")
        sys.exit(0)
    else:
        # Verify entered master password
        if not db.verify_master(master_password):
            print("Invalid master password.")
            sys.exit(1)

    # Main CLI loop
    while True:
        print("\nHi Swaraj, Here are your options:")
        print("1. Add new credential")
        print("2. Retrieve credential")
        print("3. Generate random password")
        print("4. Exit")
        choice = input("Select an option: ")

        if choice == "1":
            service = input("Service name: ")
            username = input("Username: ")
            password = getpass.getpass("Password: ")
            db.add_credential(service, username, password)
            print("Credential added.")
        elif choice == "2":
            service = input("Service name to retrieve: ")
            creds = db.get_credential(service)
            if creds:
                print(f"Username: {creds['username']}")
                print(f"Password: {creds['password']}")
            else:
                print("No credentials found for that service.")
        elif choice == "3":
            length = int(input("Password length: "))
            print("Generated password:", generate_password(length))
        elif choice == "4":
            print("Exiting.")
            sys.exit(0)
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()