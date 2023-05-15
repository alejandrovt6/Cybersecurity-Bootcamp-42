"""
The kata variable is always a string whose length is not higher than 42.
Write a program that display this variable content according to the format shown
below:
"""

kata = "The right format"

# Add '-' characters to fill up to 42 characters
formatted_string = kata.ljust(42, '-')

# Print the formatted string followed by a newline character
print(formatted_string + '\n')
