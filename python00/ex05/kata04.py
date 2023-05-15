"""
The kata variable is always a tuple that contains, in the following order:
• 2 non-negative integer containing up to 2 digits
• 1 decimal
• 1 integer
• 1 decimal
Write a program that display this variable content according to the format shown
below:
"""

kata = (0, 4, 132.42222, 10000, 12345.67)

# Use string formatting to create the desired output string
output = "module_00, ex_04 : {:.2f}, {:.2e}, {:.2e}".format(kata[2], kata[3], kata[4])

# Print the output
print(output)
