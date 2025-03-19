from encryption import encrypt, decrypt

def request_pin():
    """Requests a PIN from the user with input validation."""
    while True:
        try:
            pin = int(input("Please enter your 4-digit PIN: "))
            if 0000 <= pin <= 9999:
                encrypt(pin)
                return pin
            else:
                print("Invalid PIN. Please enter a 4-digit number.")
        except ValueError:
            print("Invalid input. Please enter a number.")
request_pin()