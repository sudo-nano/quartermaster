# Quartermaster
# A supply planning program by sudo-nano 
# help.py

from textwrap import wrap 

# print_help command is deprecated 
def print_help():
    # List of valid commands
    print("help, calc, exit, list_ingredients, load_ingredients, list_recipes, load_recipes")
    print()

    # Command descriptions
    print("help")
    print("\t List commands and their usage.")
    print()

    print("calc <recipe> <quantity>")
    print("\t Given a recipe and quantity, calculate the required quantity of ")
    print("\t ingredients for each.")
    print()

    print("list_ingredients")
    print("\t List all the ingredients that are currently loaded from data sets.")
    print()

    print("load_ingredients <file>")
    print("\t Load ingredients from a file into the session.")
    print()

    print("list_recipes")
    print("\t List all the recipes that are currently loaded from data sets.")
    print()

    print("load_recipes <file>")
    print("\t Load recipes from a file into the session")
    print()

    print("exit")
    print("\t Exit quartermaster.")
    print()


def print_help_db():
	for item in help_database:
		lines = help_database[item].split("\n")

		print(lines[0])
		for i in range(1, len(lines)):
			wrapped_lines = wrap(lines[i], 72)

			for w_line in wrapped_lines:
				print("\t" + w_line)


		print()


def match_help(command):
	if command in help_database:
		print(help_database[command])

	else:
	    print("There is no command with that name. See 'help' for commands.")


help_database = {
	"help": "help <command> \nList commands and their usage.", 
	"calc": "calc <recipe> <quantity> \nGiven a recipe and quantity, calculate the required quantity of ingredients for each.",
	"list": "list <type> \nList all items of the specified type that are loaded into the current session.",
	"load": "load <type> <file> \nLoad recipes, datasets, or ingredients from a file into the current session.", 
	"save": "save <type> <file> \nSave recipes, datasets, or ingredients from the current session into a file."
}