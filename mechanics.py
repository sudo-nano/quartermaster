import toml

class DataSet:
    def __init__(self):
        self.ingredients = {}
        self.recipes = {}
        self.people = {}

    def list_ingredients(self):
        for ingredient in self.ingredients:
            print("\t" + ingredient)

    def list_recipes(self):
        for recipe in self.recipes:
            print("\t" + recipe)
            print()

    def list_people(self):
        for person in self.people:
            print("\t" + person)
            print()

    # Load ingredients from file into DataSet
    def load_ingredients(self, file_name):
        ingredients = toml.load(file_name)

        # Check if ingredients file is of type "ingredients"
        if ingredients["type"] != "ingredients":
            print("Warning: Ingredients file" + file_name + " not of type 'ingredients', may not be correct file.")

        for ingredient in ingredients:
            if ingredient != "type":
                self.ingredients.update({ingredient:ingredients[ingredient]})

    # Load recipes from file into DataSet
    def load_recipes(self, file_name):
        recipes = toml.load(file_name)

        if recipes["type"] != "recipes":
            print("Warning: Recipes file " + file_name + " not of type 'recipes', may not be correct file.")

        for recipe in recipes:
            if recipe != "type":
                self.recipes.update({recipe:recipes[recipe]})

    def load_people(self, file_name):
        people = toml.load(file_name)

        if people["type"] != "people":
            print("Warning: People file " + file_name + " not of type 'people', may not be correct file.")

        for person in people:
            if person != "type":
                self.people.update({person:people[person]})

    def inspect_ingredient(self, ingredient):
        try:
            pass
        except:
            pass


def abbrev_unit(unit_string):
    match unit_string:
        case "discrete":
            return ""

        case "gram":
            return "g"
        
        case "kilogram":
            return "kg"

        case "milliliter":
            return "mL"
        
        case "liter":
            return "L"

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


# Pass recipe str and quantity int
def calc_and_output(recipe_str, recipe_quantity):
    recipe = session.recipes[recipe_str]

    # Debug stuff
    print("Debug: ingredients " + str(recipe["ingredients"]))
    # End debug stuff

    print("** " + str(recipe_quantity) + " quantity of " + recipe_str + " **")
    print()

    if (recipe["fractional"] == False) and ((recipe_quantity % 1) != 0):
        print("Warning: Recipe is not fractional, but specified quantity is not a whole number. Number will be rounded up.")
        recipe_quantity = ceil(recipe_quantity)

    for ingredient, amount in recipe["ingredients"].items():
        # Fetch ingredient dict from ingredients file
        ing_dict = session.ingredients[ingredient]

        required_qty = amount * recipe_quantity
        unit = abbrev_unit(ing_dict["unit"])
        price_of_rq = required_qty * ing_dict["price_per_unit"]

        print("Required quantity of " + ingredient + ": " + str(required_qty) + unit)
        print("Estimated price of required quantity: " + str(price_of_rq))
        print()

    print()


# Initialize session
session = DataSet()

# Load test ingredients and recipes
session.load_ingredients("test_ingredients.toml")
session.load_recipes("test_recipes.toml")