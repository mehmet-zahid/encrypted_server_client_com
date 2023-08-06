import trio
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
import os
from encryption import (
    generate_and_save_private_key, 
    load_private_key, load_public_key, 
    encrypt_message, decrypt_message
    )


CLIENT_PRIVATE_KEY_FILE = "client_private_key.pem"
CLIENT_PUBLIC_KEY_FILE = "client_public_key.pem"
SERVER_PUBLIC_KEY_FILE = "server_public_key.pem"

PORT = 12345

async def sender(client_stream):
    print("sender: started!")
    while True:
        data = b"async can sometimes be confusing, but I believe in you!"
        encrypted_msg = encrypt_message(data, public_key)
        print(f"sender: sending {encrypted_msg!r}")
        await client_stream.send_all(encrypted_msg)
        await trio.sleep(1)

async def receiver(client_stream):
    print("receiver: started!")

    async for data in client_stream:
        decrypted_msg = decrypt_message(data, private_key)
        print(f"receiver: got data {decrypted_msg!r}")
    await try_to_connect()

async def try_to_connect():
    print(f"parent: trying to re-connect 127.0.0.1:{PORT}")
    client_stream = await trio.open_tcp_stream("127.0.0.1", PORT)
    print(f"parent: connection succesful!")
    return client_stream

async def parent():
    try:
        print(f"parent: trying to connect 127.0.0.1:{PORT}")
        client_stream = await trio.open_tcp_stream("127.0.0.1", PORT)
        print(f"parent: connection succesful!")
        async with client_stream:
            async with trio.open_nursery() as nursery:
                print("parent: spawning sender...")
                nursery.start_soon(sender, client_stream)

                print("parent: spawning receiver...")
                nursery.start_soon(receiver, client_stream)
    except Exception as e:
        await parent()


generate_and_save_private_key(CLIENT_PRIVATE_KEY_FILE, CLIENT_PUBLIC_KEY_FILE)
private_key = load_private_key(CLIENT_PRIVATE_KEY_FILE)
public_key = load_public_key(SERVER_PUBLIC_KEY_FILE)
trio.run(parent)
