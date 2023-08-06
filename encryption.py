from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
import os, sys



def generate_and_save_private_key(private_key_file, public_key_file):
    if os.path.exists(private_key_file):
        return
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )

    # Serialize the private key to PEM format and save it to a file
    with open(private_key_file, "wb") as f:
        f.write(
            private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption(),
            )
        )
    # Get the corresponding public key
    public_key = private_key.public_key()

    # Serialize the public key to PEM format and save it to a file
    with open(public_key_file, "wb") as f:
        f.write(
            public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo,
            )
        )

def load_private_key(private_key_file):
    # Load the private key from the file
    with open(private_key_file, "rb") as f:
        return serialization.load_pem_private_key(f.read(), password=None)
    
def load_public_key(public_key_file):
    # Load the public key from the file
    if not os.path.exists(public_key_file):
        #print('waiting for public key file to be created by server...')
        print('please create public key !')
        sys.exit()
    with open(public_key_file, "rb") as f:
        pem_data = serialization.load_pem_public_key(f.read(), backend=default_backend())
        return pem_data

def encrypt_message(message, public_key):
    return public_key.encrypt(
        message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        )
    )

def decrypt_message(message, private_key):
    return private_key.decrypt(
        message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        )
    )