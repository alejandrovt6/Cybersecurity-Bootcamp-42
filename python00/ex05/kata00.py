"""
The kata variable is always a tuple and can only be filled with integer.
Write a program that display this variable content according to the format shown
below:

"""

# Libraries
import tkinter as tk

# Program
kata = (19,42,21)

print(f"The 3 numbers are: " , end = " ")

for num in kata:
    print(num, end= " ")

# GUI
window = tk.Tk()
window.title("Kata 00")
window.geometry("400x150")

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width - window.winfo_screenmmwidth()) / 2)
y = int((screen_height - window.winfo_screenmmheight()) / 2)

window.geometry("+{}+{}".format(x, y))

label1 = tk.Label(window, text="The 3 numbers are:")
label1.pack(pady=10)

label2 = tk.Label(window, text=f"{kata[0]}, {kata[1]}, {kata[2]}")
label2.pack()

window.mainloop()

