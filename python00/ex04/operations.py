"""
Write a program that takes two integers A and B as arguments and prints the result
of the following operations:

Sum: A+B
Difference: A-B
Product: A*B
Quotient: A/B
Remainder: A%B

If more or less than two argument are provided or if either of the argument is not
an integer, print an error message.
• If no argument are provided, do nothing or print an usage.
• If an operation is impossible, print an error message instead of a numerical result.
"""

# Libraries
import tkinter as tk

# Program
def operations():
    """
    You must enter two numbers.
    """

    num1 = entry1.get()
    num2 = entry2.get()

    if not num1.isnumeric() or not num2.isnumeric():
        result_label.config(text="Error. Strings no valid.")
        return

    A = int(num1)
    B = int(num2)

    sum = A + B
    rest = A - B
    mult = A * B

    if B == 0:
        div = "Operation is impossible."
        rem = "Operation is impossible."
    else:
        div = A / B
        rem = A % B

    result_label.config(text="Sum: {}\nDifference: {}\nProduct: {}\nQuotient: {}\nRemainder: {}".format(sum, rest, mult, div, rem))

# GUI
window = tk.Tk()
window.title("Operations")
window.geometry("400x150")

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width - window.winfo_screenmmwidth()) / 2)
y = int((screen_height - window.winfo_screenmmheight()) / 2)

window.geometry("+{}+{}".format(x, y))

input_label1 = tk.Label(window, text="Number 1:", padx=10, pady=5)
input_label1.grid(row=0, column=0)

entry1 = tk.Entry(window)
entry1.grid(row=0, column=1)

input_label2 = tk.Label(window, text="Number 2:", padx=10, pady=5)
input_label2.grid(row=1, column=0)

entry2 = tk.Entry(window)
entry2.grid(row=1, column=1)

button = tk.Button(window, text="Operate", command=operations)
button.grid(row=2, column=0)

result_label = tk.Label(window, text="", padx=10, pady=5)
result_label.grid(row=2, column=1)


window.mainloop()


