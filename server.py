import trio
from encryption import (
    generate_and_save_private_key, 
    load_private_key, load_public_key, 
    encrypt_message, decrypt_message
    )

from itertools import count

# Port is arbitrary, but:
# - must be in between 1024 and 65535
# - can't be in use by some other program on your computer
# - must match what we set in our echo client
PORT = 12345

CONNECTION_COUNTER = count()


SERVER_PRIVATE_KEY_FILE = "server_private_key.pem"
SERVER_PUBLIC_KEY_FILE = "server_public_key.pem"
CLIENT_PUBLICK_KEY_FILE = "client_public_key.pem"



async def echo_server(server_stream):
    # Assign each connection a unique number to make our debug prints easier
    # to understand when there are multiple simultaneous connections.
    ident = next(CONNECTION_COUNTER)
    print(f"echo_server {ident}: started")
    try:
        async for data in server_stream:
            decrypted_msg = decrypt_message(data, private_key)
            print(f"echo_server {ident}: received data {decrypted_msg!r}")
            encrypted_msg = encrypt_message(decrypted_msg, public_key)
            await server_stream.send_all(encrypted_msg)
        print(f"echo_server {ident}: connection closed")
    # FIXME: add discussion of (Base)ExceptionGroup to the tutorial, and use
    # exceptiongroup.catch() here. (Not important in this case, but important
    # if the server code uses nurseries internally.)
    except Exception as exc:
        # Unhandled exceptions will propagate into our parent and take
        # down the whole program. If the exception is KeyboardInterrupt,
        # that's what we want, but otherwise maybe not...
        print(f"echo_server {ident}: crashed: {exc!r}")


    ## Decrypt the message using the private key
    #decrypted_msg = private_key.decrypt(
    #    encrypted_msg,
    #    padding.OAEP(
    #        mgf=padding.MGF1(algorithm=hashes.SHA256()),
    #        algorithm=hashes.SHA256(),
    #        label=None,
    #    )
    #)
    #print(f'Decrypted message: {decrypted_msg}')

    # Check if the client is authorized (using the admin password)
    #if decrypted_msg == b'NoSecret':
    #    print(f'Admin connected from {client_stream.socket.getpeername()}')
    #else:
    #    print(f'Unauthorized client connection from {client_stream.socket.getpeername()}')


async def main():
    await trio.serve_tcp(echo_server, PORT)


# We could also just write 'trio.run(trio.serve_tcp, echo_server, PORT)', but real
# programs almost always end up doing other stuff too and then we'd have to go
# back and factor it out into a separate function anyway. So it's simplest to
# just make it a standalone function from the beginning.
generate_and_save_private_key(SERVER_PRIVATE_KEY_FILE, SERVER_PUBLIC_KEY_FILE)
private_key = load_private_key(SERVER_PRIVATE_KEY_FILE)
public_key = load_public_key(CLIENT_PUBLICK_KEY_FILE)
trio.run(main)
