import numpy as np

# Alphabet: A-Z plus space
alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ '
num_to_letter = {i: letter for i, letter in enumerate(alphabet)}
letter_to_num = {letter: i for i, letter in enumerate(alphabet)}

# Key matrix
K = np.array([[5, 8], [2, 3]])

def mod_inverse(a, m):
    a = a % m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    raise ValueError(f"No modular inverse exists for {a} mod {m}")

def matrix_inverse_mod(matrix, modulus):
    det = int(np.round(np.linalg.det(matrix)))
    det_mod = det % modulus
    det_inv = mod_inverse(det_mod, modulus)
    adj = np.round(det * np.linalg.inv(matrix)).astype(int)
    return (det_inv * adj) % modulus

def is_valid_input(text):
    return all(c in alphabet for c in text)

def encrypt(plaintext, key=K, modulus=27):
    plaintext = plaintext.upper()
    if not is_valid_input(plaintext):
        raise ValueError("Input contains invalid characters. Use A-Z and space only.")
    if len(plaintext) % 2 != 0:
        plaintext += ' '
    
    nums = [letter_to_num[c] for c in plaintext]
    ciphertext = ''
    matrix_steps = []

    # Prepare plaintext matrix (2 rows, n/2 columns)
    plaintext_matrix = np.array(nums).reshape(2, -1)
    
    # Multiply key matrix by plaintext matrix mod modulus
    ciphertext_matrix = (key @ plaintext_matrix) % modulus
    
    # Convert ciphertext matrix back to letters
    for col in range(ciphertext_matrix.shape[1]):
        ciphertext += num_to_letter[ciphertext_matrix[0, col]] + num_to_letter[ciphertext_matrix[1, col]]

    # Store matrices as lists for JSON/template rendering
    matrix_steps.append({
        'original_text': plaintext,
        'numeric_representation': nums,
        'text_matrix': plaintext_matrix.tolist(),
        'key_matrix': key.tolist(),
        'result_matrix': ciphertext_matrix.tolist(),
        'final_text': ciphertext
    })

    return ciphertext, matrix_steps

def decrypt(ciphertext, key=K, modulus=27):
    key_inv = matrix_inverse_mod(key, modulus)
    if not is_valid_input(ciphertext):
        raise ValueError("Ciphertext contains invalid characters. Use A-Z and space only.")
    
    nums = [letter_to_num[c] for c in ciphertext]
    plaintext = ''
    matrix_steps = []

    # Prepare ciphertext matrix (2 rows, n/2 columns)
    ciphertext_matrix = np.array(nums).reshape(2, -1)
    
    # Multiply inverse key matrix by ciphertext matrix mod modulus
    plaintext_matrix = (key_inv @ ciphertext_matrix) % modulus
    
    # Convert plaintext matrix back to letters
    for col in range(plaintext_matrix.shape[1]):
        plaintext += num_to_letter[plaintext_matrix[0, col]] + num_to_letter[plaintext_matrix[1, col]]

    # Store matrices as lists for JSON/template rendering
    matrix_steps.append({
        'original_text': ciphertext,
        'numeric_representation': nums,
        'text_matrix': ciphertext_matrix.tolist(),
        'key_matrix': key_inv.tolist(),  # inverse key matrix for decryption
        'result_matrix': plaintext_matrix.tolist(),
        'final_text': plaintext.rstrip()
    })

    return plaintext.rstrip(), matrix_steps
