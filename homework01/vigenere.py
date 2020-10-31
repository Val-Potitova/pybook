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
    s=[0]*26
    for i in range(26):
        s[i] = chr(ord('A') + i)
    m=len(plaintext)//len(keyword)
    if len(plaintext)%len(keyword)!=0:
        m +=1
    n=0
    for i in range(m):
        for j in range(len(keyword)):
            if plaintext[n].isalpha():
                for k in range(26):
                    if keyword[j].upper()==s[k]:
                        if ord(plaintext[n].upper())+k > ord('Z'):
                            ciphertext += chr(ord(plaintext[n])+k-26)
                            break
                        else:
                            ciphertext += chr(ord(plaintext[n]) + k)
                            break
            else:
                ciphertext += plaintext[n]
            if n==len(plaintext)-1:
                break
            n += 1

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
    s = [0] * 26
    for i in range(26):
        s[i] = chr(ord('A') + i)
    m = len(ciphertext) // len(keyword)
    if len(ciphertext) % len(keyword) != 0:
        m += 1
    n = 0
    for i in range(m):
        for j in range(len(keyword)):
            if ciphertext[n].isalpha():
                for k in range(26):
                    if keyword[j].upper() == s[k]:
                        if ord(ciphertext[n].upper()) - k < ord('A'):
                            plaintext += chr(ord(ciphertext[n]) - k + 26)
                            break
                        else:
                            plaintext += chr(ord(ciphertext[n]) - k)
                            break
            else:
                plaintext += ciphertext[n]
            if n == len(ciphertext) - 1:
                break
            n += 1

    return plaintext
