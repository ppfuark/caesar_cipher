import math
import string
from collections import Counter

FREQUENCY = {
    'A': 8.2,
    'B': 1.5,
    'C': 2.8,
    'D': 4.3,
    'E': 12.7,
    'F': 2.2,
    'G': 2.0,
    'H': 6.1,
    'I': 7.0,
    'J': 0.15,
    'K': 0.77,
    'L': 4.0,
    'M': 2.4,
    'N': 6.7,
    'O': 7.5,
    'P': 1.9,
    'Q': 0.095,
    'R': 6.0,
    'S': 6.3,
    'T': 9.1,
    'U': 2.8,
    'V': 0.98,
    'W': 2.4,
    'X': 0.15,
    'Y': 2.0,
    'Z': 0.074,
}
ALPHABET = string.ascii_uppercase
ALPHABET_LENGHT = 26

def encrypt(text: str, shift: int) -> str: 
    output = ''

    for char in text:
        if not char.isalpha():
            output+=char
            continue
        current_index = ALPHABET.index(char.upper())
        new_char = ALPHABET[(current_index + shift) % ALPHABET_LENGHT]
        output+= new_char if char.isupper() else new_char.lower()
    return output

def decrypt(text: str, shift: int)-> str:
    output = ''
    for char in text:
        if not char.isalpha():
            output+=char
            continue
        current_index = ALPHABET.index(char.upper())
        new_char = ALPHABET[(current_index - shift) % ALPHABET_LENGHT]
        output+= new_char if char.isupper() else new_char.lower()
    return output

def decrypt_without_key(text: str)-> int:
    key = 0;
    smallest_diff = math.inf
    total_letter = sum(1 for c in text if c.isalpha())
    if total_letter == 0:
        raise ValueError("Text without letters")
    for letter in range(ALPHABET_LENGHT):
        current_text = decrypt(text=text, shift=letter)
        counter = Counter(c for c in current_text.upper() if c.isalpha())
        current_total_diff = 0
        for letter in ALPHABET:
            current_total_diff += abs((counter.get(letter, 0) / len(total_letter)) * 100 - (FREQUENCY[letter]))
        current_total_diff = current_total_diff / ALPHABET_LENGHT

        if current_total_diff < smallest_diff:
            smallest_diff = current_total_diff
            key = letter

    return key