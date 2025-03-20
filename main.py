import hashlib
import os
import json

import cryptography
from cryptography.fernet import Fernet

#Add account details to a JSON file

#set and encrypt a 4 digit pin
def get_encrypted_pin():
    # Check if the PIN is already set
    try:
        with open('data/pin.json', 'r') as f:
            data = json.load(f)
            if data.get('pin_set', False):

                print("PIN Already Set")
                return
    except FileNotFoundError:
        pass

    while True:
        print(" __      __       .__                               ")
        print("/  \    /  \ ____ |  |   ____  ____   _____   ____  ")
        print("\   \/\/   // __ \|  | _/ ___\/  _ \ /     \_/ __ \ ")
        print(" \        /\  ___/|  |_\  \__(  <_> )  Y Y  \  ___/ ")
        print("  \__/\  /  \___  >____/\___  >____/|__|_|  /\___  >")
        print("       \/       \/          \/            \/     \/ ")
        print("To start using the app, please set a PIN.")
        pin = input("Enter your 4-digit PIN: ")
        if len(pin) == 4 and pin.isdigit():
            break
        else:
            print("PIN must be exactly 4 digits.")
    #encrypt the PIN using SHA-256
    salt = os.urandom(16)  # Generate a random salt
    salted_pin = salt + pin.encode()
    encrypted_pin = hashlib.sha256(salted_pin).hexdigest()

    # Generate a Fernet key
    fernet_key = Fernet.generate_key()
    cipher_suite = Fernet(fernet_key)

    # Store the salt, encrypted PIN, Fernet key, and pin_set flag in a JSON file
    data.update(
        {'salt': salt.hex(), 'encrypted_pin': encrypted_pin, 'fernet_key': fernet_key.decode(), 'pin_set': True})
    with open('data/pin.json', 'w') as f:
        json.dump(data, f, indent=4)

    return salt, encrypted_pin
#check if the entered pin is correct
def add_account_details():
    # Load the Fernet key from the JSON file
    try:
        with open('data/pin.json', 'r') as f:
            data = json.load(f)
            fernet_key = data['fernet_key'].encode()
            cipher_suite = Fernet(fernet_key)
    except (FileNotFoundError, KeyError) as e:
        print(f"Error loading Fernet key: {e}")
        return
    account_details = {}
    try:
        username = input("Enter your username/email: ")
        if not username:
            raise ValueError("Username/email cannot be empty.")
        account_details['username'] = cipher_suite.encrypt(username.encode()).decode()

        password = input("Enter your password: ")
        if not password:
            raise ValueError("Password cannot be empty.")
        account_details['password'] = cipher_suite.encrypt(password.encode()).decode()

        account_details['website_app'] = input("Enter the website/app: ")
        if not account_details['website_app']:
            raise ValueError("Website/app cannot be empty.")

    except ValueError as e:
        print(f"Error: {e}")
        return

    # Load existing data from the JSON file
    try:
        with open('data/accounts.json', 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = []

    # Add new account details to the data
    data.append(account_details)

    # Save the updated data back to the JSON file
    try:
        with open('data/accounts.json', 'w') as file:
            json.dump(data, file, indent=4)
        print("Account details added successfully.")
    except IOError as e:
        print(f"Error saving account details: {e}")
#decrypt and view account details
def decrypt_account_details():
    # Load the Fernet key from the JSON file
    try:
        with open('data/pin.json', 'r') as f:
            data = json.load(f)
            fernet_key = data['fernet_key'].encode()
            cipher_suite = Fernet(fernet_key)
    except (FileNotFoundError, KeyError) as e:
        print(f"Error loading Fernet key: {e}")
        return

    # Load the account details from the JSON file
    try:
        with open('data/accounts.json', 'r') as f:
            accounts = json.load(f)
    except FileNotFoundError:
        print("No account details found.")
        return

    # Decrypt and display the account details
    for account in accounts:
        try:
            username = cipher_suite.decrypt(account['username'].encode()).decode()
            password = cipher_suite.decrypt(account['password'].encode()).decode()
            website_app = account['website_app']
            print(f"Website/App: {website_app}")
            print(f"Username/Email: {username}")
            print(f"Password: {password}")
            print("-" * 30)
        except cryptography.fernet.InvalidToken as e:
            print(f"Error decrypting account details: {e}")
def check_pin():
    # Load the salt and encrypted PIN from the JSON file
    with open('data/pin.json', 'r') as f:
        data = json.load(f)
        stored_salt = bytes.fromhex(data['salt'])
        stored_encrypted_pin = data['encrypted_pin']

    pin = input("Enter your PIN to check: ")
    salted_pin = stored_salt + pin.encode()
    encrypted_pin = hashlib.sha256(salted_pin).hexdigest()
    if encrypted_pin == stored_encrypted_pin:
        print("PIN is correct.")
        print("Entering app...")
    else:
        print("PIN is incorrect.")
#Clear the screen
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
#Welcome message
def welcome(typui):
    print(" __      __       .__                               ")
    print("/  \    /  \ ____ |  |   ____  ____   _____   ____  ")
    print("\   \/\/   // __ \|  | _/ ___\/  _ \ /     \_/ __ \ ")
    print(" \        /\  ___/|  |_\  \__(  <_> )  Y Y  \  ___/ ")
    print("  \__/\  /  \___  >____/\___  >____/|__|_|  /\___  >")
    print("       \/       \/          \/            \/     \/ ")
    if typui == 1:
        print("Welcome to the PIN Setup")
    if typui == 2:
        print("Please enter your PIN to continue")
#selection screen
def selection():
    clear_screen()
    print("__________                                               .___      ")
    print("\______   \_____    ______ ________  _  _____________  __| _/______")
    print(" |     ___/\__  \  /  ___//  ___/\ \/ \/ /  _ \_  __ \/ __ |/  ___/")
    print(" |    |     / __ \_\___ \ \___ \  \     (  <_> )  | \/ /_/ |\___ \ ")
    print(" |____|    (____  /____  >____  >  \/\_/ \____/|__|  \____ /____  >")
    print("                \/     \/     \/                          \/     \/ ")
    print("1. Add Account Details")
    print("2. View Account Details")
    print("3. Set PIN")
    print("4. Exit")
    select_option = input("Enter your choice: ")
    if select_option == '1':
        add_account_details()

clear_screen()
try:
    with open('data/pin.json', 'r') as f:
        data = json.load(f)
        if data.get('pin_set', False):
            welcome(1)
except FileNotFoundError:
    pass
get_encrypted_pin()
try:
    with open('data/pin.json', 'r') as f:
        data = json.load(f)
        if data.get('pin_set', False):
            clear_screen()
            welcome(2)
except FileNotFoundError:
    pass
check_pin()
#selection()
add_account_details()
