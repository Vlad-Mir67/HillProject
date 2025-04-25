import numpy as np

alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ '
modulus = len(alphabet)  # 27
num_to_letter = {i: letter for i, letter in enumerate(alphabet)}
letter_to_num = {letter: i for i, letter in enumerate(alphabet)}

K = np.array([[5, 8], [2, 3]])

def mod_inverse(a, m):
    a = a % m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    raise ValueError(f"No modular inverse for {a} mod {m}")

def matrix_inverse_mod(matrix, modulus):
    det = int(round(np.linalg.det(matrix)))
    det_mod = det % modulus
    det_inv = mod_inverse(det_mod, modulus)
    adj = np.round(det * np.linalg.inv(matrix)).astype(int)
    return (det_inv * adj) % modulus

def is_valid_input(text):
    return all(c in alphabet for c in text)

def preprocess(text):
    text = text.upper()
    if not is_valid_input(text):
        raise ValueError("Only A-Z and space are allowed.")
    if len(text) % 2 != 0:
        text += ' '
    return text

def encrypt(plaintext, key=K):
    plaintext = preprocess(plaintext)
    nums = [letter_to_num[c] for c in plaintext]
    pairs = np.array(nums).reshape(-1, 2).T  # 2 rows, N/2 columns

    ciphertext_matrix = (key @ pairs) % modulus
    ciphertext = ''.join(num_to_letter[num] for num in ciphertext_matrix.T.flatten())

    matrix_steps = [{
        'original_text': plaintext,
        'numeric_representation': nums,
        'text_matrix': pairs.tolist(),
        'key_matrix': key.tolist(),
        'result_matrix': ciphertext_matrix.tolist(),
        'final_text': ciphertext
    }]
    return ciphertext, matrix_steps

def decrypt(ciphertext, key=K):
    ciphertext = preprocess(ciphertext)
    nums = [letter_to_num[c] for c in ciphertext]
    pairs = np.array(nums).reshape(-1, 2).T

    key_inv = matrix_inverse_mod(key, modulus)
    plaintext_matrix = (key_inv @ pairs) % modulus
    plaintext = ''.join(num_to_letter[num] for num in plaintext_matrix.T.flatten())

    matrix_steps = [{
        'original_text': ciphertext,
        'numeric_representation': nums,
        'text_matrix': pairs.tolist(),
        'key_matrix': key_inv.tolist(),
        'result_matrix': plaintext_matrix.tolist(),
        'final_text': plaintext.rstrip()
    }]
    return plaintext.rstrip(), matrix_steps

