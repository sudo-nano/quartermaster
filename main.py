# Quartermaster
# A supply planning program by sudo-nano

import toml
from math import *

ingredients_file_name = "test_ingredients.toml"
ingredients = toml.load(ingredients_file_name)

# Check if ingredients file is of type "ingredients"
if ingredients["type"] != "ingredients":
    print("Warning: Ingredients file" + ingredients_file_name + "not of type 'ingredients', may not be correct file.")

recipes = toml.load("test_recipes.toml")

# I'm definitely going to have to put this stuff into different files later, but
# that's a problem for later me

def abbrev_unit(unit_string):
    match unit_string:
        case "discrete":
            return ""

        case "gram":
            return "g"

        case "milliliter":
            return "mL"

# Pass recipe str and quantity int
def calc_and_output(recipe_str, recipe_quantity):
    recipe = recipes[recipe_str]

    # Debug stuff
    print("Debug: ingredients " + str(recipe["ingredients"]))
    # End debug stuff

    print("** " + str(recipe_quantity) + " quantity of " + recipe_str + " **")
    print()

    if (recipe["fractional"] == False) and ((recipe_quantity % 1) != 0):
        print("Warning: Recipe is not fractional, but specified quantity is not a whole number. Number will be rounded up.")
        recipe_quantity = ceil(quantity)

    for ingredient, amount in recipe["ingredients"].items():
        # Fetch ingredient dict from ingredients file
        ing_dict = ingredients[ingredient]

        required_qty = amount * recipe_quantity
        unit = abbrev_unit(ing_dict["unit"])
        price_of_rq = required_qty * ing_dict["price_per_unit"]

        print("Required quantity of " + ingredient + ": " + str(required_qty) + unit)
        print("Estimated price of required quantity: " + str(price_of_rq))
        print()

    print()


def prompt():
    command = input("quartermaster > ")
    command_words_upper = command.split()
    command_words = []

    # Force commands to be lowercase before interpreting
    for word in command_words_upper:
        command_words.append(word.lower())

    match command_words[0]:
        case "calc":
            calc_and_output(command_words[1], float(command_words[2]))

        case "exit":
            exit()

running = True
while running:
        prompt()
