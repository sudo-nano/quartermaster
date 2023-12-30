# Quartermaster
# A supply planning program by sudo-nano 
# help.py

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


def match_help(command):
	if command in help_database:
		print(help_database[command])

	else:
	    print("There is no command with that name. See 'help' for commands.")


help_database = {
	"load": "load <type> <file> \n\tLoad recipes, datasets, or ingredients from a file into the current session.", 

}