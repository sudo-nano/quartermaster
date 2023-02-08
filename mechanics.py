import toml

class DataSet:
    def __init__(self):
        self.ingredient_sets = []
        self.recipe_sets = []
        self.person_sets = []

    def list_ingredients(self):
        for group in self.ingredient_sets:
            pass

    def list_recipes(self):
        pass 

    def list_people(self):
        pass

    def import_ingredients(self, file_name):
        pass 

    def import_recipes(self, file_name):
        pass

    def import_people(self, file_name):
        pass

# Initialize default dataset
default_dataset = DataSet()

def abbrev_unit(unit_string):
    match unit_string:
        case "discrete":
            return ""

        case "gram":
            return "g"

        case "milliliter":
            return "mL"

def print_help():
    # List of valid commands
    print("help, calc, exit")
    print()

    # Command descriptions
    print("help")
    print("\t List commands and their usage.")
    print()

    print("calc <recipe> <quantity>")
    print("\t Given a recipe and quantity, calculate the required quantity of\ ")
    print("\t ingredients for each.")
    print()

    print("exit")
    print("\t Exit quartermaster.")
    print()


# Pass recipe str and quantity int
def calc_and_output(recipe_str, recipe_quantity):
    recipe = recipes[recipe_str]

    # Debug stuff
    print("Debug: ingredients " + str(recipe["ingredients"]))
    # End debug stuff

    print("** " + str(recipe_quantity) + " quantity of " + recipe_str + " **")
    print()

    if (recipe["fractional"] == False) and ((recipe_quantity % 1) != 0):
        print("Warning: Recipe is not fractional, but specified quantity is not a whole number. Number will be rounded up.")
        recipe_quantity = ceil(quantity)

    for ingredient, amount in recipe["ingredients"].items():
        # Fetch ingredient dict from ingredients file
        ing_dict = ingredients[ingredient]

        required_qty = amount * recipe_quantity
        unit = abbrev_unit(ing_dict["unit"])
        price_of_rq = required_qty * ing_dict["price_per_unit"]

        print("Required quantity of " + ingredient + ": " + str(required_qty) + unit)
        print("Estimated price of required quantity: " + str(price_of_rq))
        print()

    print()


def load_recipes(curr_set):
    pass

def list_recipes():
    for recipe in recipes:

        # Filter out type value
        if recipe != "type":
            print(recipe)

        print()

def load_ingredients(file_name):
    pass 

def list_ingredients():
    for ingredient in ingredients:

        # Filter out type value
        if recipe != "type":
            print(ingredient)

        print()

# Load test ingredients
ingredients_file_name = "test_ingredients.toml"
ingredients = toml.load(ingredients_file_name)

## Check if ingredients file is of type "ingredients"
if ingredients["type"] != "ingredients":
    print("Warning: Ingredients file" + ingredients_file_name + "not of type 'ingredients', may not be correct file.")

recipes = toml.load("test_recipes.toml")