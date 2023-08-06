from encryption import (
    generate_and_save_private_key, 
    load_private_key, load_public_key, 
    encrypt_message, decrypt_message
    )
import base64

CLIENT_PRIVATE_KEY_FILE = "client_private_key.pem"
CLIENT_PUBLIC_KEY_FILE = "client_public_key.pem"
SERVER_PUBLIC_KEY_FILE = "server_public_key.pem"
SERVER_PRIVATE_KEY_FILE = "server_private_key.pem"


def test_encryption():
    # Generate or load the private key
    generate_and_save_private_key(CLIENT_PRIVATE_KEY_FILE, CLIENT_PUBLIC_KEY_FILE)
    generate_and_save_private_key(SERVER_PRIVATE_KEY_FILE, SERVER_PUBLIC_KEY_FILE)
    client_private_key = load_private_key(CLIENT_PRIVATE_KEY_FILE)
    client_public_key = load_public_key(CLIENT_PUBLIC_KEY_FILE)
    server_private_key = load_private_key(SERVER_PRIVATE_KEY_FILE)
    server_public_key = load_public_key(SERVER_PUBLIC_KEY_FILE)
    # Encrypt a message
    message = b"async can sometimes be confusing, but I believe in you!"
    print(f"message: {message}")
    encrypted_msg = encrypt_message(message, client_public_key) # server encrypts message with client's public key
    print(f"encrypted_msg: {encrypted_msg}")
    # Encode the encrypted message to Base64 for human-readable representation
    encoded_encrypted_msg = base64.b64encode(encrypted_msg).decode('utf-8')
    print(f"encoded_encrypted_msg: {encoded_encrypted_msg}")
    # Decrypt the message
    decrypted_msg = decrypt_message(encrypted_msg, client_private_key) # client decrypts message with it's own private key
    print(f"decrypted_msg: {decrypted_msg}")
    # Make sure the message is the same
    assert decrypted_msg == message
    print("encryption: success!")


if __name__ == "__main__":
    test_encryption()