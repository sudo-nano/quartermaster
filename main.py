# Quartermaster
# A supply planning program by sudo-nano

from math import *
from mechanics import *
import help
import sys

def prompt():
    command = input("quartermaster > ")
    command_words_upper = command.split()
    command_words = []

    # Force commands to be lowercase before interpreting
    for word in command_words_upper:
        command_words.append(word.lower())

    # Command parser
    match command_words[0]:
        case "calc" | "c":
            if len(command_words) < 3:
                print("Please provide a recipe and quantity.")

            elif len(command_words) > 3:
                print("Too many parameters provided. Please provide only a file name.")

            else:
                calc_and_output(command_words[1], float(command_words[2]))

        case "exit" | "quit" | "q":
            exit()

        case "load_ingredients" | "loadi":
            if len(command_words) < 2:
                print("Please provide a file name.")

            if len(command_words) > 2:
                print("Too many parameters provided. Please provide only a file name.")

            load_ingredients(command_words_upper[1])

        case "load_recipes" | "loadr":
            if len(command_words) < 2:
                print("Please provide a file name.")

            if len(command_words) > 2:
                print("Too many parameters provided. Please provide only a file name.")

            load_recipes(command_words_upper[1])

        # List ingredients, recipes, or people
        case "list" | "l":
            if len(command_words) < 2:
                print("Please provide a type: ingredient, recipe, or person.")

            elif len(command_words) == 2:
                match command_words[1]:
                    # List ingredients loaded into the current session
                    case "ingredient" | "ingredients" | "i":
                        session.list_ingredients()

                    # List recipes loaded into the current session
                    case "recipe" | "recipes" | "r":
                        session.list_recipes()

                    # List people loaded into the current session (not implemented yet)
                    case "person" | "people" | "persons" | "p":
                        print("People are not yet implemented. Please check back later.")

            elif len(command_words) > 2:
                print("Too many parameters provided. Please provide a type: ingredient, recipe, or person.")

        # Inspect an ingredient, recipe, or person 
        case "inspect" | "i":
            if len(command_words) < 2:
                print("Please provide an ingredient, recipe, or person to inspect.")
                return

            elif len(command_words) > 3:
                print("Too many parameters provided. Please provide an item to inspect, optionally preceded by a type specifier.")
                return

            elif len(command_words) == 2:
                # Check types 
                type_matches = 0
                for possible_type in ["ingredient", "recipe"]:
                    if (session.type_check(possible_type, command_words[1])):
                        type_matches += 1

                if type_matches == 0:
                    print("No item of any type was found for that item. Check for typos.")
    
                elif type_matches == 1:
                    # Check which type matched and execute correct command 
                    if session.type_check("ingredient", command_words[1]):
                        session.inspect_ingredient(command_words[1])

                    elif session.type_check("recipe", command_words[1]):
                        session.inspect_recipe(command_words[1])

                else:
                    print("Multiple type matches for item. Please specify a type, like 'inspect <type> <item>'. ")


            elif len(command_words) == 3:
                if session.type_check(command_words[1], command_words[2]):
                    match command_words[1]:
                        case "ingredient" | "i":
                            session.inspect_ingredient(command_words[2])
                            return

                        case "recipe" | "r":
                            session.inspect_recipe(command_words[2])
                            return

                        case other:
                            print("command parser error: 'inspect' reached end of control flow")
                            return

                else:
                    print("No item with name " + command_words[2] + " and type " + command_words[1] + "exists.")


        # List which dataset is active (not yet implemented)
        case "active_dataset":
            print("Not yet implemented.")
            print()
            pass 

        # Export all of specified type (ingredients, recipes, people, entire session) to file
        # TODO: Merge all save commands into this one, make it take type as argument
        case "save":
            print("Not yet implemented.")
            print()

        # Load all of specified type (ingredients, recipes, people, session) from file
        # TODO: Merge all load commands into this one, make it take type as an argument
        case "load":
            print("Not yet implemented.")
            print()

        case "help":
            # TODO: Add "help <command>" as a means of showing more in-depth help for
            # a single command 

            match len(command_words):
                case 1:
                    help.print_help_db()

                # If one argument is provided, attempt to match it with the help page for the
                # corresponding command
                case 2:
                    help.match_help(command_words[1])

                case 3: 
                    print("Too many arguments provided. See 'help' for commands.")



        case other:
            print("Invalid command. See 'help' for commands.")
            print()

# Initialize session
session = DataSet()

# Load test ingredients and recipes
#session.load_ingredients("Test Datasets/test_ingredients.toml")
#session.load_recipes("Test Datasets/test_recipes.toml")
session.load_file("Test Datasets/test_ingredients.toml", "ingredient")
session.load_file("recipes", "Test Datasets/test_recipes.toml")

# Main program loop
match len(sys.argv):
    case 1:
        pass

    case other:
        print("Error: Runtime arguments are not supported at this time. They will be implemented in the future.")
        exit()

running = True
while running:
        prompt()
        print()
