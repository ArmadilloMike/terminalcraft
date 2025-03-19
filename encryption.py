from cryptography.fernet import Fernet

# Key generation (save this securely)
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# Encryption
def encypt(data):
    text = data
    cipher_text = cipher_suite.encrypt(text)
    print(f"Encrypted: {cipher_text}")

# Decryption
def decrypt():
    plain_text = cipher_suite.decrypt(cipher_text)
    print(f"Decrypted: {plain_text.decode()}")