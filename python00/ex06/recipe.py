"""
Part 1: Nested Dictionaries
Create a dictionary called cookbook. You will use this cookbook to store recipe.
A recipe is a dictionary that stores (at least) 3 couples key-value:
• ”ingredients": a list of string representing the list of ingredients
• "meal": a string representing the type of meal
• "prep_time": a non-negative integer representing a time in minutes
In the cookbook, the key to a recipe is the recipe name.
Initialize your cookbook with 3 recipes:
• The Sandwich’s ingredients are ham, bread, cheese and tomatoes. It is a lunch and
it takes 10 minutes of preparation.
• The Cake’s ingredients are flour, sugar and eggs. It is a dessert and it takes 60
minutes of preparation.
• The Salad’s ingredients are avocado, arugula, tomatoes and spinach. It is a lunch
and it takes 15 minutes of preparation.
Part 2: A series of Helpful Functions
Create a series of useful functions to handle your cookbook:
1. A function that print all recipe names.
2. A function that takes a recipe name and print its details.
3. A function that takes a recipe name and delete it.
4. A function that add a recipe from user input. You will need a name, a list of
ingredient, a meal type and a preparation time.
Part 3: A command line executable !
Create a program that use your cookbook and your functions.
The program will prompt the user to make a choice between printing the cookbook
content, printing one recipe, adding a recipe, deleting a recipe or quitting the cookbook.
Your program will continue to ask for prompt until the user decide to quit it. The
program cannot crash if a wrong value is entered: you must handle the error and ask for
another prompt.
"""

cookbook = {
    "Sandwich": {
        "ingredients": ["ham", "bread", "cheese", "tomatoes"],
        "meal": "lunch",
        "prep_time": 10
    },
    "Cake": {
        "ingredients": ["flour", "sugar", "eggs"],
        "meal": "dessert",
        "prep_time": 60
    },
    "Salad": {
        "ingredients": ["avocado", "arugula", "tomatoes", "spinach"],
        "meal": "lunch",
        "prep_time": 15
    }
}


def print_recipe_names():
    print("Recipe names:")
    for recipe_name in cookbook.keys():
        print("- " + recipe_name)


def print_recipe(recipe_name):
    if recipe_name in cookbook:
        recipe = cookbook[recipe_name]
        print(f"Recipe for {recipe_name}:")
        print(f"Ingredients list: {', '.join(recipe['ingredients'])}")
        print(f"To be eaten for {recipe['meal']}.")
        print(f"Takes {recipe['prep_time']} minutes of cooking.")
    else:
        print(f"No recipe found for {recipe_name}")


def delete_recipe(recipe_name):
    if recipe_name in cookbook:
        del cookbook[recipe_name]
        print(f"{recipe_name} recipe deleted from the cookbook.")
    else:
        print(f"No recipe found for {recipe_name}")


def add_recipe():
    recipe_name = input("Enter recipe name: ")
    ingredients = input("Enter ingredients separated by commas: ").split(",")
    meal = input("Enter type of meal: ")
    prep_time = int(input("Enter preparation time in minutes: "))
    cookbook[recipe_name] = {"ingredients": [ingredient.strip() for ingredient in ingredients],
                            "meal": meal,
                            "prep_time": prep_time}
    print(f"{recipe_name} recipe added to the cookbook.")


def display_cookbook():
    print_recipe_names()
    print()


def display_recipe():
    recipe_name = input("Enter recipe name: ")
    print_recipe(recipe_name)
    print()


def delete_recipe_prompt():
    recipe_name = input("Enter recipe name: ")
    delete_recipe(recipe_name)
    print()


def add_recipe_prompt():
    add_recipe()
    print()


def display_prompt():
    print("1: Print the cookbook content")
    print("2: Print a recipe")
    print("3: Add a recipe")
    print("4: Delete a recipe")
    print("5: Quit") 
    print("\nPlease select an option: ")



def handle_choice(choice):
    if choice == "1":
        display_cookbook()
    elif choice == "2":
        display_recipe()
    elif choice == "3":
        add_recipe_prompt()
    elif choice == "4":
        delete_recipe_prompt()
    elif choice == "5":
        print("Cookbook closed.")
        return True
    else:
        print("Invalid choice, please try again.")
    return False


def main():
    print("Welcome to the cookbook!")
    while True:
        display_prompt()
        choice = input()
        if handle_choice(choice):
            break


if __name__ == '__main__':
    main()
