"""
Make a program that takes a string as argument and encode it into Morse code.
• The program supports space and alphanumeric characters
• An alphanumeric character is represented by dots . and dashes -:
• A space character is represented by a slash /
• Complete morse characters are separated by a single space
If more than one argument are provided, merge them into a single string with each
argument separated by a space character.
If no argument is provided, do nothing or print an usage.
"""

import sys

MORSE_CODE_DICT = {'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.',
                'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---',
                'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---',
                'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
                'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--',
                'Z': '--..', '0': '-----', '1': '.----', '2': '..---',
                '3': '...--', '4': '....-', '5': '.....', '6': '-....',
                '7': '--...', '8': '---..', '9': '----.', ' ':'/'}

def morse_encode(message):
    morse_code = []
    error_flag = False
    
    for char in message:
        if char.upper() in MORSE_CODE_DICT:
            morse_code.append(MORSE_CODE_DICT[char.upper()])
        else:
            error_flag = True
    
    if error_flag:
        print("ERROR")
        return ""
    
    return ' '.join(morse_code)

if len(sys.argv) == 1:
    print("Usage: python3 morse_code.py <message>")
else:
    message = ' '.join(sys.argv[1:])
    print(morse_encode(message))
        
