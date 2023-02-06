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
            calc_and_output(command_words[1], float(command_words[2]))

        case "exit":
            exit()

        case "load_ingredients":
            pass


        case "load_recipes":
            pass

        case "list_recipes":
            list_recipes()

        case "active_dataset":
            pass 

        case "help":
            print_help()

        case other:
            print("Invalid command. See 'help' for commands.")
            print()

running = True
while running:
        prompt()
