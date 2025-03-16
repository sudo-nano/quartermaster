# Quartermaster
# A supply planning program by sudo-nano

from ast import alias
from math import *
from mechanics import *
import help
import sys
import argparse
import shlex

# Initialize base argument parser
parser_base = argparse.ArgumentParser(prog="Quartermaster", exit_on_error=False)
parser_base.set_defaults(exit_on_error=False)
subparsers = parser_base.add_subparsers(dest="subcommand", help='subcommand help')

# Scale subcommand takes parameters recipe and amount
parser_scale = subparsers.add_parser("scale", aliases=["sc"], help="scale help", exit_on_error=False)
parser_scale.add_argument("recipe")
parser_scale.add_argument("amount")

# Exit subcommand closes the program
parser_exit = subparsers.add_parser("exit", aliases=["quit", "q"], exit_on_error=False)

# Load subcommand loads a file
parser_load = subparsers.add_parser("load", aliases=["lo"], help="load help", exit_on_error=False)
parser_load.add_argument("type")
parser_load.add_argument("file")

# List subcommand lists all items of the specified type
parser_list = subparsers.add_parser("list", aliases=["ls"], help="list help")
parser_list.add_argument("type")

# Inspect subcommand allows you to inspect any item in the current data set
parser_inspect = subparsers.add_parser("inspect", aliases=["i"], help="inspect help")
parser_inspect.add_argument("type")
parser_inspect.add_argument("item")

# Run the interactive prompt
def prompt(session: DataSet):
    command = input("quartermaster > ")
    try:
        args = parser_base.parse_args(shlex.split(command))
        execute_command(session, args)
    except argparse.ArgumentError as error:
        print(error)

def execute_command(session: DataSet, args: argparse.Namespace):
    match args.subcommand:
        case "scale" | "sc":
            try:
                amount = float(args.amount)
                calc_and_output(current_session, args.recipe, amount)

            except ValueError:
                print("Please provide an integer or decimal for amount.s")

        case "exit" | "quit" | "q":
            exit()

        case "load" | "lo":
            try:
                session.load_file(args.file, args.type)
            except TypeError:
                print(f"Invalid file type. Please choose from {[e.value for e in DataType]}")

        # List ingredients, recipes, or people
        case "list" | "ls":
            try:
                session.list(args.type)

            except TypeError:
                print(f"Invalid data type. Please choose from ingredient, recipe, person, group, valid_restriction, active_restriction")

        # Inspect an ingredient, recipe, or person
        case "inspect" | "i":
            if session.type_check(args.type, args.item):
                match args.type:
                    case "ingredient" | "i":
                        session.inspect_ingredient(args.item)
                        return

                    case "recipe" | "r":
                        session.inspect_recipe(args.item)
                        return

                    case other:
                        print("command parser error: 'inspect' reached end of control flow")
                        return

            else:
                print("No item with name " + args.item + " of type " + args.type + "exists.")


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
current_session.load_file("Test Datasets/test_ingredients.toml", "ingredient")
current_session.load_file("Test Datasets/test_recipes.toml", "recipe")

# Main program loop
match len(sys.argv):
    case 1:
        pass

    case 2:
        if "--debug" in sys.argv:
            current_session.debug = True

    case other:
        print("Error: Runtime arguments are not supported at this time. They will be implemented in the future.")
        exit()

running = True
while running:
        prompt(current_session)
        print()
