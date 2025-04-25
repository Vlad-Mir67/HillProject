import socket
from hill_cipher import encrypt, decrypt, K

HOST = '127.0.0.1'
PORT = 65432

encrypted_messages = []
decrypted_messages = []

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    while True:
        message = input("Enter message (or 'exit' to quit): ")
        if message.lower() == 'exit':
            break

        try:
            encryption_result = encrypt(message, K)
            encrypted_messages.append(encryption_result)
            s.sendall(encryption_result["ciphertext"].encode())
        except Exception as e:
            print(f"Encryption failed: {e}")
            continue

        try:
            decryption_result = decrypt(encryption_result["ciphertext"], K)
            decrypted_messages.append(decryption_result)
        except Exception as e:
            print(f"Decryption failed: {e}")