# Quartermaster
# A supply planning program by sudo-nano

from math import *
from mechanics import *

def prompt():
    command = input("quartermaster > ")
    command_words_upper = command.split()
    command_words = []

    # Force commands to be lowercase before interpreting
    for word in command_words_upper:
        command_words.append(word.lower())

    # Command parser
    match command_words[0]:
        case "calc":
            if len(command_words):
                print("Please provide a recipe and quantity.")

            if len(command_words) > 3:
                print("Too many parameters provided. Please provide only a file name.")

            calc_and_output(command_words[1], float(command_words[2]))

        case "exit":
            exit()

        case "quit":
            exit()

        case "load_ingredients":
            if len(command_words) < 2:
                print("Please provide a file name.")

            if len(command_words) > 2:
                print("Too many parameters provided. Please provide only a file name.")

            load_ingredients(command_words_upper[1])

        case "list_ingredients":
            session.list_ingredients()

        case "inspect_ingredient":
            if len(command_words) < 2:
                print("Please provide an ingredient to inspect.")

            if len(command_words) > 2:
                print("Too many parameters provided. Please provide only an ingredient.")

            if command_words[1] not in session.ingredients:
                print("Invalid ingredient.")
                return

            session.inspect_ingredient(command_words[1])
            
        case "load_recipes":
            if len(command_words) < 2:
                print("Please provide a file name.")

            if len(command_words) > 2:
                print("Too many parameters provided. Please provide only a file name.")

            load_recipes(command_words_upper[1])

        # List recipes loaded into the current session
        case "list_recipes":
            session.list_recipes()

        # Inspect the properties of a recipe (not yet implemented)
        case "inspect_recipe":
            pass

        # List which dataset is active (not yet implemented)
        case "active_dataset":
            print("Not yet implemented.")
            print()
            pass 

        # Export current session data set to file (not yet implemented)
        case "export_session":
            pass

        # Load session data set from file (not yet implemented)
        case "load_session":
            pass

        case "help":
            print_help()

        case other:
            print("Invalid command. See 'help' for commands.")
            print()

# Main program loop
running = True
while running:
        prompt()
