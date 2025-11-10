# Quartermaster
# A supply planning program by sudo-nano

from math import *
import sys
import argparse
import shlex

import mechanics
import help
import units

# Initialize base argument parser
parser_base = argparse.ArgumentParser(prog="", exit_on_error=False)
parser_base.set_defaults(exit_on_error=False)
subparsers = parser_base.add_subparsers(dest="subcommand", help="subcommand help")

# Scale subcommand takes parameters recipe and amount
parser_scale = subparsers.add_parser(
    "scale", aliases=["sc"], help="scale help", exit_on_error=False
)
parser_scale.add_argument("recipe")
parser_scale.add_argument("amount")

# Exit subcommand closes the program
parser_exit = subparsers.add_parser("exit", aliases=["quit", "q"], exit_on_error=False)

# Load subcommand loads a file
parser_load = subparsers.add_parser(
    "load", aliases=["lo"], help="load help", exit_on_error=False
)
parser_load.add_argument("type")
parser_load.add_argument("file")

# List subcommand lists all items of the specified type
parser_list = subparsers.add_parser(
    "list", aliases=["ls"], help="list help", exit_on_error=False
)
parser_list.add_argument("type")

# Inspect subcommand allows you to inspect any item in the current data set
parser_inspect = subparsers.add_parser(
    "inspect", aliases=["i"], help="inspect help", exit_on_error=False
)
parser_inspect.add_argument("type")
parser_inspect.add_argument("item")

# Help subcommand shows help page
parser_help = subparsers.add_parser("help", aliases=["h"], exit_on_error=False)

# Convert command converts between units
# When converting between mass and volume, user must either explicitly specify a density
# or specify an ingredient whose density will be used.
parser_convert = subparsers.add_parser("convert", aliases=["c"], exit_on_error=False)
parser_convert.add_argument("initial")
parser_convert.add_argument("target")
parser_convert.add_argument("-d", "--density")
parser_convert.add_argument("-i", "--ingredient")


# Run the interactive prompt
def prompt(session: mechanics.DataSet):
    command = input("quartermaster > ")
    try:
        args = parser_base.parse_args(shlex.split(command))
        execute_command(session, args)
    except argparse.ArgumentError as error:
        print(error)


def execute_command(session: mechanics.DataSet, args: argparse.Namespace):
    # Create string listing valid data types. This will be presented to the user if
    # they send an invalid type.
    valid_types = str(mechanics.DataType._member_names_)
    valid_types_cleaned = valid_types[1 : len(valid_types) - 1].replace("'", "")

    match args.subcommand:
        case "scale" | "sc":
            try:
                amount = float(args.amount)
                mechanics.calc_and_output(current_session, args.recipe, amount)

            except ValueError:
                print("Please provide an integer or decimal for amount.")

        case "exit" | "quit" | "q":
            exit()

        case "load" | "lo":
            try:
                session.load_file(args.file, args.type)
            except TypeError:
                print(f"Invalid file type. Please choose from {valid_types_cleaned}")

        # List ingredients, recipes, or people
        case "list" | "ls":
            try:
                session.list(args.type)

            except TypeError:
                print(f"Invalid data type. Please choose from {valid_types_cleaned}")

        # Inspect an ingredient, recipe, or person
        case "inspect" | "i":
            if session.type_check(args.type, args.item):
                match args.type:
                    case "ingredient" | "i":
                        session.inspect(args.item, mechanics.DataType.ingredient)
                        return

                    case "recipe" | "r":
                        session.inspect(args.item, mechanics.DataType.recipe)
                        return

                    # TODO: Implement inspect handling of people and groups

                    case other:
                        print(
                            "command parser error: 'inspect' reached end of control flow"
                        )
                        return

            else:
                print(
                    "No item with name "
                    + args.item
                    + " of type "
                    + args.type
                    + "exists."
                )

        # Convert between two unit values.
        # When converting between mass and volume, the user must specify either density or
        # an ingredient whose density value will be used.
        # Not yet implemented. Needs str_to_MassUnit implemented first.
        case "convert" | "c":
            # Detect units of initial and target values
            pass

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
            help.print_help_db()
            print()

        case _:
            print("Invalid command. See 'help' for commands.")
            print()


# Initialize session
current_session = mechanics.DataSet()

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
        print(
            "Error: Runtime arguments are not supported at this time. They will be implemented in the future."
        )
        exit()

running = True
while running:
    prompt(current_session)
    print()
