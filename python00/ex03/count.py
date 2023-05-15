"""
Part 1. text_analyzer
Create a function called text_analyzer that takes a single string argument and displays
the sums of its upper-case characters, lower-case characters, punctuation characters and
spaces.
• If None or nothing is provided, the user is prompted to provide a string.
• If the argument is not a string, print an error message.
• This function must have a docstring explaning its behavior.
Test your function with the python console

Part 2. __name__==__main__
In the previous part, you wrote a function that can be used in the console or in another
file when imported. Without changing this behavior, update your file so it can also be
launched as a standalone program.
• If more than one argument is provided to the program, print an error message.
• Otherwise, use the text_analyzer function.
"""

import tkinter as tk
import string

def text_analyzer():
    text = entry.get("1.0", "end-1c")

    if text is None or text == "":
        result_label.config(text="Please enter a string.")
    elif not isinstance(text, str):
        result_label.config(text="Error: argument must be a string.")
    else:
        upper_count = 0
        lower_count = 0
        punct_count = 0
        space_count = 0
        digit_count = 0

        for char in text:
            if char.islower(): 
                lower_count +=1
            elif char.isupper():
                upper_count +=1
            elif char.isspace():
                space_count += 1
            elif char in string.punctuation:
                punct_count += 1
            elif char.isdigit():
                digit_count += 1           

        result = "The text contains " + str(len(text)) + " characters: "
        result += f"\n - {upper_count} upper letters"
        result += f"\n - {lower_count} lower letters"
        result += f"\n - {punct_count} punctuations marks"
        result += f"\n - {space_count} spaces"
        result += f"\n - {digit_count} digits"
        result_label.config(text=result)

window = tk.Tk()
window.title("Text analyzer")
window.geometry("400x425")

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width - window.winfo_screenmmwidth()) / 2)
y = int((screen_height - window.winfo_screenmmheight()) / 2)

window.geometry("+{}+{}".format(x, y))

input_label = tk.Label(window, text="Enter a string:")
input_label.pack(pady=10)

entry = tk.Text(window, width=30, height=10)
entry.pack(pady=5)

button = tk.Button(window, text="Analyze", command=text_analyzer)
button.pack(pady=10)

result_label = tk.Label(window, text="")
result_label.pack(pady=5)

window.mainloop()



