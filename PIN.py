import hashlib

def hash_pin(pin):
    """Hashes the given PIN using SHA-256."""
    pin_str = str(pin)
    hash_object = hashlib.sha256(pin_str.encode())
    hashed_pin = hash_object.hexdigest()
    return hashed_pin
def request_pin():
    """Requests a PIN from the user with input validation."""
    while True:
        try:
            pin = int(input("Please enter your 4-digit PIN: "))
            if 0000 <= pin <= 9999:
                hashed_pin = hash_pin(pin)
                print(hashed_pin)
                return pin
            else:
                print("Invalid PIN. Please enter a 4-digit number.")
        except ValueError:
            print("Invalid input. Please enter a number.")
request_pin()