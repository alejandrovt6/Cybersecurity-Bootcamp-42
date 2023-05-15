"""
    Make a program that takes a string as argument, reverses it, swaps its letters case
and print the result.
• If more than one argument are provided, merge them into a single string with each
argument separated by a space character.
• If no argument are provided, do nothing or print an usage.
"""

# Libraries
import tkinter as tk
import sys

# Program
def reverse_argument(arguments):
    """
    You must enter a valid string.
    """
    if len(arguments) != 0:
        args_to_string = ' '.join(arguments)
        args_swaps = args_to_string.swapcase()
        args_swapped_reversed = args_swaps[::-1]
        result_label.config(text=args_swapped_reversed)
    else:
        result_label.config(text=reverse_argument.__doc__)

# GUI
def on_click():
    arguments = input_entry.get().split()
    reverse_argument(arguments)

window = tk.Tk()
window.title("Reverse Argument")
window.geometry("400x150")

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width - window.winfo_reqwidth()) / 2)
y = int((screen_height - window.winfo_reqheight()) / 2)

window.geometry("+{}+{}".format(x, y))

input_label = tk.Label(text="Enter a string:")
input_label.pack(pady=10)

input_entry = tk.Entry(width=50)
input_entry.pack()

result_label = tk.Label(text="")
result_label.pack(pady=10)

button = tk.Button(text="Reverse", command=on_click)
button.pack()

window.mainloop()
