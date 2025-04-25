from flask import Flask, request, jsonify, render_template
from hill_cipher import encrypt, decrypt, K

app = Flask(__name__)

encrypted_messages = []
decrypted_messages = []

@app.route('/')
def home():
    return "Server is listening and ready to encrypt and decrypt!"

@app.route('/encrypt', methods=['POST'])
def encrypt_message():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400
    try:
        data = request.get_json()
        if 'message' not in data:
            return jsonify({"error": "Missing 'message' key"}), 400
        message = data['message']
        ciphertext, matrix_steps = encrypt(message, K)
        result = {
            "original_text": message,
            "cipher_text": ciphertext,
            "matrix_steps": matrix_steps
        }
        encrypted_messages.append(result)
        return jsonify({"encrypted_message": ciphertext})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/decrypt', methods=['POST'])
def decrypt_message():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400
    try:
        data = request.get_json()
        if 'ciphertext' not in data:
            return jsonify({"error": "Missing 'ciphertext' key"}), 400
        ciphertext = data['ciphertext']
        plaintext, matrix_steps = decrypt(ciphertext, K)
        result = {
            "original_text": ciphertext,
            "plain_text": plaintext,
            "matrix_steps": matrix_steps
        }
        decrypted_messages.append(result)
        return jsonify({"decrypted_message": plaintext})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/messages')
def show_messages():
    return render_template('messages.html',
                           encrypted_messages=encrypted_messages,
                           decrypted_messages=decrypted_messages)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
