"""
The kata variable is always a dictionary and can only be filled with strings.
Write a program that display this variable content according to the format shown
below:
"""

import tkinter as tk

kata = {
'Python': 'Guido van Rossum',
'Ruby': 'Yukihiro Matsumoto',
'PHP': 'Rasmus Lerdorf',
}

# GUI
window = tk.Tk()
window.title("Kata 00")
window.geometry("400x150")

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width - window.winfo_screenmmwidth()) / 2)
y = int((screen_height - window.winfo_screenmmheight()) / 2)

window.geometry("+{}+{}".format(x, y))

label1 =tk.Label(window, text="¿Who created this language?", font=("Arial", 14, "bold"))
label1.pack(pady=10)

for lang, creator in kata.items():
    label2 = tk.Label(window, text=(f"{lang} was created by {creator}"))
    label2.pack()

window.mainloop()
