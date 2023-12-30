# Quartermaster
# A supply planning program by sudo-nano

from math import *
from mechanics import *
import help

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
            if len(command_words):
                print("Please provide a recipe and quantity.")

            if len(command_words) > 3:
                print("Too many parameters provided. Please provide only a file name.")

            calc_and_output(command_words[1], float(command_words[2]))

        case "exit" | "quit" | "q":
            exit()

        case "load_ingredients" | "loadi":
            if len(command_words) < 2:
                print("Please provide a file name.")

            if len(command_words) > 2:
                print("Too many parameters provided. Please provide only a file name.")

            load_ingredients(command_words_upper[1])

        case "list_ingredients" | "listi":
            session.list_ingredients()
            
        case "load_recipes" | "loadr":
            if len(command_words) < 2:
                print("Please provide a file name.")

            if len(command_words) > 2:
                print("Too many parameters provided. Please provide only a file name.")

            load_recipes(command_words_upper[1])

        # List recipes loaded into the current session
        case "list_recipes" | "listr":
            session.list_recipes()

        # Inspect an ingredient, recipe, or person 
        case "inspect" | "i":
            if len(command_words) < 2:
                print("Please provide an ingredient, recipe, or person to inspect.")
                return

            if len(command_words) > 3:
                print("Too many parameters provided. Please provide an item to inspect, optionally preceded by a type specifier.")
                return

            if len(command_words) == 2:
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


            if len(command_words) == 3:
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

# Main program loop
running = True
while running:
        prompt()
        print()
