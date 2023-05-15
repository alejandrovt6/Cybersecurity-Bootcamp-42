"""
Make a program that takes a string S and an integer N as argument and print the list
of words in S that contains more than N non-punctuation characters.
• Words are separated from each other by space characters
• Punctuation symbols must be removed from the printed list: they are neither part
of a word nor a separator
• The program must contains at least one list comprehension expression.
If the number of argument is different from 2, or if the type of any argument is wrong,
the program prints an error message.
"""

import string
import sys

if len(sys.argv) != 3:
    print("Usage: python program.py <string> <integer>.")
    sys.exit()
try:
    n = int(sys.argv[2])
    s = str(sys.argv[1])
    if isinstance(n, int) and isinstance(s, str):
        words = [word.translate(str.maketrans('', '', string.punctuation)) for word in s.split() 
            if len(word.translate(str.maketrans('', '', string.punctuation))) > n]
        print(words)
        if isinstance(s, str):
            sNew=int(s)
            if isinstance(sNew, int):
                print("Error. The first argument must be a string.")
    else: print("The first argument must be a string and the second argument must be an integer.(1)")
    sys.exit()
except ValueError:
    print("The first argument must be a string and the second argument must be an integer.(2)")

s = sys.argv[1]

