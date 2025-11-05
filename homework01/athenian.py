def encrypt_affine(plaintext, a, b):
    alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    n = len(alphabet)  # 33


    char_to_num = {char: idx for idx, char in enumerate(alphabet)}

    num_to_char = {idx: char for idx, char in enumerate(alphabet)}

    encrypted_text = []

    for char in plaintext.lower():
        if char in char_to_num:

            x = char_to_num[char]

            encrypted_pos = (a * x + b) % n

            encrypted_char = num_to_char[encrypted_pos]
            encrypted_text.append(encrypted_char)
        else:
            encrypted_text.append(char)

    return ''.join(encrypted_text)


