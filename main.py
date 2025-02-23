# Quartermaster
# A supply planning program by sudo-nano

from math import *
from mechanics import *
import help
import sys
import argparse
import shlex

# Initialize base argument parser
parser_base = argparse.ArgumentParser(prog="Quartermaster")
subparsers = parser_base.add_subparsers(dest="subcommand", help='subcommand help')

# Scale subcommand takes parameters recipe and amount
parser_scale = subparsers.add_parser("scale", help="scale help")
parser_scale.add_argument("recipe")
parser_scale.add_argument("amount")

# Run the interactive prompt
def prompt(session: DataSet):
    command = input("quartermaster > ")
    args = parser_base.parse_args(shlex.split(command))

    # Command parser
    match args.subcommand:
        case "scale" | "sc":
            try:
                amount = float(args.amount)
                calc_and_output(current_session, args.recipe, amount)

            except ValueError:
                print("Please provide an integer or decimal for amount.s")

        case "exit" | "quit" | "q":
            exit()

        case "load_ingredients" | "loadi":
            if len(command_words) < 2:
                print("Please provide a file name.")

            elif len(command_words) > 2:
                print("Too many parameters provided. Please provide only a file name.")
            else:
                try:
                    session.load_ingredients(command_words_upper[1])

                except FileNotFoundError:
                    print("File not found.")

        case "load_recipes" | "loadr":
            if len(command_words) < 2:
                print("Please provide a file name.")

            elif len(command_words) > 2:
                print("Too many parameters provided. Please provide only a file name.")

            else:
                try:
                    session.load_recipes(command_words_upper[1])

                except FileNotFoundError:
                    print("File not found.")

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
current_session = DataSet()

# Load test ingredients and recipes
#session.load_ingredients("Test Datasets/test_ingredients.toml")
#session.load_recipes("Test Datasets/test_recipes.toml")
current_session.load_file("Test Datasets/test_ingredients.toml", "ingredient")
current_session.load_file("Test Datasets/test_recipes.toml", "recipe")

# Main program loop
match len(sys.argv):
    case 1:
        pass

    case 2:
        # Should debug status be part of the session class and/or specified
        # per-session?
        if "--debug" in sys.argv:
            debug = True

    case other:
        print("Error: Runtime arguments are not supported at this time. They will be implemented in the future.")
        exit()

running = True
while running:
        prompt(current_session)
        print()
