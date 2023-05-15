"""
Make a program that takes a number as argument, checks whether it is odd, even or
zero, and print the result.
• If more than one argument are provided or if the argument is not an integer, print
an error message.
• If no argument are provided, do nothing or print an usage.
"""

# Libraries
import sys
import tkinter as tk

# Program
def check_number():
    input_num = entry.get()
    try:
        num = int(input_num)
        if num == 0:
            result_label.config(text="I'm Zero.")
        elif num % 2 == 0:
            result_label.config(text="I'm Even.")
        elif num % 2 != 0:
            result_label.config(text="I'm Odd.")
    except ValueError:
        result_label.config(text="Error: argument is not an integer.")

# GUI
window = tk.Tk()
window.title("Who is?")
window.geometry("400x150")

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width - window.winfo_reqwidth()) / 2)
y = int((screen_height - window.winfo_reqheight()) / 2)

window.geometry("+{}+{}".format(x, y))

input_label = tk.Label(window, text="Enter a number:")
input_label.pack()

entry = tk.Entry(window)
entry.pack()

button = tk.Button(window, text="Check", command=check_number)
button.pack()

result_label = tk.Label(window, text="")
result_label.pack()

window.mainloop()

