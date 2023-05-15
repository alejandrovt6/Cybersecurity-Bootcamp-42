""""
You have to make a program that will be an interactive guessing game. It will ask the
user to guess a number between 1 and 99. The program will tell the user if their input is
too high or too low. The game ends when the user finds out the secret number or types
exit. You will import the random module with the randint function to get a random
number. You have to count the number of trials and print that number when the user
wins.
"""

import random

secret_number = random.randint(1, 99)
num_guesses = 0

name = input("Hello, What's your name? \n>>")
print("Hello, ", name, ". Welcome to the hardest game you've ever played.")

while True:
    guess = input("Guess a number between 1 and 99 (or type 'exit' to quit): ")
    if guess == "exit":
        break

    try:
        guess = int(guess)
    except ValueError:
        print("Invalid input. Please enter a number between 1 and 99.")
        continue

    if guess < 1 or guess > 99:
        print("Invalid input. Please enter a number between 1 and 99.")
        continue

    num_guesses += 1

    if guess == secret_number:
        if num_guesses == 1:
            print("Congratulations, you've got it!")
        else:
            print("Congratulations, you guessed the secret number in", num_guesses, "guesses!")
            if secret_number == 42:
                print("You've discovered the meaning of life, the universe, and everything!")
        break
    elif guess < secret_number:
        print("Too low.")
    elif guess > secret_number:
        print("Too high.")


    