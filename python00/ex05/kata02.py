"""
The kata variable is always a tuple that contains 5 non-negative integers. The first
integer contains up to 4 digits, the rest up to 2 digits.
Write a program that display this variable content according to the format shown
below:

"""

# Libraries
import datetime
import tkinter as tk

# Program
kata = (2019,9,25,3,30)

date_time = datetime.datetime(*kata)
formatt = "%m/%d/%Y %H:%M"

string_format = date_time.strftime(formatt)
# print(string_format)

# GUI
window = tk.Tk()
window.title("Kata02")
window.geometry("400x150")

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width - window.winfo_screenmmwidth()) / 2)
y = int((screen_height - window.winfo_screenmmheight()) / 2)

window.geometry("+{}+{}".format(x, y))

label1 = tk.Label(window, text=string_format, font=("Arial", 14, "bold"),)
label1 = label1.place(x=100,y=50)

window.mainloop()
