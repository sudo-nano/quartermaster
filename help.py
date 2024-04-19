# Quartermaster
# A supply planning program by sudo-nano 
# help.py

from textwrap import wrap 

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
