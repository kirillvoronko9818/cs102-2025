def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.
    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""

    keyword_upper = keyword.upper()
    key_length = len(keyword_upper)

    for i in range(len(plaintext)):
        char = plaintext[i]

        if char.isalpha():

            key_index = i % key_length
            key_char = keyword_upper[key_index]
            shift = ord(key_char) - ord('A')

            if char.isupper():
                new_char = chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
                ciphertext = ciphertext + new_char
            else:
                new_char = chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
                ciphertext = ciphertext + new_char
        else:
            ciphertext = ciphertext + char

    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.
    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """  
    plaintext = ""

    keyword_upper = keyword.upper()
    key_length = len(keyword_upper)

    for i in range(len(ciphertext)):
        char = ciphertext[i]

        if char.isalpha():

            key_index = i % key_length
            key_char = keyword_upper[key_index]
            shift = ord(key_char) - ord('A')

            if char.isupper():
                new_char = chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
                plaintext = plaintext + new_char
            else:
                new_char = chr((ord(char) - ord('a') - shift) % 26 + ord('a'))
                plaintext = plaintext + new_char
        else:
            plaintext = plaintext + char





    return plaintext