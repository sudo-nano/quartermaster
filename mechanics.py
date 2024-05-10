import toml
from enum import Enum

class DataType(Enum):
    multiple = "multiple"
    none = "none"
    ingredient = "ingredient"
    recipe = "recipe"
    person = "person"
    group = "group"

    def __str__(self):
        return str(self.value)



class Person:
    def __init__(self, name):
        self.name = name
        self.dietary_restrictions = []

    def list_dietary_restrictions(self):
        for item in self.dietary_restrictions:
            print("\t" + item)


class DataSet:
    def __init__(self):
        self.ingredients = {}   # List of valid ingredients
        self.recipes = {}       # List of valid recipes
        self.people = {}        # List of people 
        self.valid_dietary_restrictions = []    # List of valid dietary restrictions

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
        try:
            ingredients = toml.load(file_name)

        except FileNotFoundError:
            print("Error: File " + file_name + " not found.")

        # Check if ingredients file is of type "ingredients"
        if ingredients["type"] != "ingredients":
            raise TypeError("Ingredients file " + file_name + " not of type 'ingredients', may not be correct file.")

        for ingredient in ingredients:
            if ingredient != "type":
                self.ingredients.update({ingredient:ingredients[ingredient]})

    # Load recipes from file into DataSet
    def load_recipes(self, file_name):
        recipes = toml.load(file_name)

        if recipes["type"] != "recipe":
            raise TypeError("Recipes file " + file_name + " not of type 'recipes', may not be correct file.")

        for recipe in recipes:
            if recipe != "type":
                self.recipes.update({recipe:recipes[recipe]})


    def load_people(self, file_name):
        file = toml.load(file_name)

        if file["type"] != "person":
            raise TypeError("Person file " + file_name + " not of type 'people', may not be correct file.")

        # Import valid dietary restrictions
        self.valid_dietary_restrictions.extend(file["valid_dietary_restrictions"])

        for person in people:
            # Prevent TOML file type specifier from being loaded into array of people
            if person == "type":
                continue

            # Check that dietary restrictions are valid
            restrictions_valid = True
            for item in person.dietary_restrictions:
                if item not in self.valid_dietary_restrictions:
                    restrictions_valid = False

            if not restrictions_valid:
                continue

            self.people.update({person:file[person]})


    # Load a file of the specified type into the DataSet
    def load_file(self, file_name, type):
        try:
            file = toml.load(file_name)

        except FileNotFoundError:
            print("Warning: File " + file_name + " not found.")

        # Check that provided type is valid
        try:
            file_type = str(DataType[type])

        except KeyError:
            raise TypeError("Invalid data type provided to load_file.")

        # TODO: Add code to handle the case where the provided file doesn't have
        # a type field

        # Check that loaded file is of provided type
        if file["type"] != file_type:
            raise TypeError("Provided file " + file_name + " is type " + file["type"] + " instead of specified type " + type)

        # Do different things on import depending on type
        match file["type"]:
            case "person":
                # Import additional valid dietary restrictions from new person file
                self.valid_dietary_restrictions.extend(file["valid_dietary_restrictions"])

                # Check that all people in file have valid restrictions
                for person in file:
                    if person == "type":
                        continue

                    restrictions_valid = True
                    for item in person.dietary_restrictions:
                        if item not in self.valid_dietary_restrictions:
                            restrictions_valid = False

                    if restrictions_valid:
                        self.people.update({person:file[person]})

                    else:
                        print("Warning: Person " + person + "not added due to invalid dietary restrictions.")

            case "ingredient":
                # TODO: Check whether ingredients have valid units
                for ingredient in ingredients:
                    if ingredient != "type":
                        self.ingredients.update({ingredient:ingredients[ingredient]})

            case "recipe":
                # TODO: Check that all ingredients in recipes are loaded into session
                for recipe in recipes:
                    if recipe != "type":
                        self.recipes.update({recipe:recipes[recipe]})


    # List properties of ingredient
    def inspect_ingredient(self, ingredient):
        print("Ingredient: " + ingredient)

        # Print diet incompatibilities 
        the_ingredient = self.ingredients[ingredient]
        print("Diet Incompatibilities: ", end="")
        
        if the_ingredient["diet_incompat"] == []:
            print("None")

        else:
            print(the_ingredient["diet_incompat"])

        # Print unit 
        print("Unit: " + str(self.ingredients[ingredient]["unit"]))

        # Print price per unit 
        print("Price per unit: " + str(self.ingredients[ingredient]["price_per_unit"]))

        # Print purchase increments
        print("Purchase Increments:")
        for item in self.ingredients[ingredient]["purchase_increments"]:
            print("\t" + str(item[0]) + " " + str(self.ingredients[ingredient]["unit"]) + " for $" + str(item[1]))

    def inspect_recipe(self, recipe):
        print("Recipe: " + recipe)
        print("Fractional: " + str(self.recipes[recipe]["fractional"]))
        print("Ingredients: ")

        for item in self.recipes[recipe]["ingredients"]:
            print("\t" + item + ": " + str(self.recipes[recipe]["ingredients"][item]))


    def list_dietary_restrictions(self):
        for item in self.dietary_restrictions:
            print(item)

    # Check whether an item of the specified name and type exist in the current dataset
    def type_check(self, item_type, item):
        match item_type:
            case "recipe":
                if item in self.recipes:
                    return True 

                else:
                    return False

            case "ingredient":
                if item in self.ingredients:
                    return True

                else: 
                    return False

            case "person":
                if item in self.people:
                    return True

            case "group":
                if item in self.groups:
                    return True

            case other:
                return False


# Converts a unit to its abbreviation
# TODO: Convert this to a dictionary
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


# Pass recipe str and quantity int
# TODO: Rework this to remove the "fractional" field
# and instead calculate at runtime whether a recipe can be
# multiplied/divided in the specified way.
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
