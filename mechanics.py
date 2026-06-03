import tomli
from enum import Enum
from math import ceil, floor
import units

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
        self.dietary_restrictions = {}

    def list_dietary_restrictions(self):
        for item in self.dietary_restrictions:
            print("\t" + item)


class DataSet:
    def __init__(self):
        self.ingredients = {}   # Dict of valid ingredients
        self.recipes = {}       # Dict of valid recipes
        self.people = {}        # Dict of people
        self.groups = {}        # Dict of groups
        self.dietary_restrictions = []    # List of valid dietary restrictions
        self.debug = False


    def list(self, type: str):
        if type not in DataType:
            raise TypeError(f"Invalid data type " + type + " provided to list.")

        match type:
            case "ingredient" | "ingredients" | "i":
                for ingredient in list(self.ingredients.values()):
                    print(f"\t{ingredient["name"]}")

            case "recipe" | "recipes" | "r":
                for recipe in self.recipes:
                    print("\t" + recipe)
                    print()

            case "person" | "people" | "p":
                for person in self.people:
                    print("\t" + person)
                    print()

            case "group" | "groups" | "g":
                for item in self.groups:
                    print("\t" + item)
                    print()

            case "dietary_restriction" | "restriction" | "dr":
                for item in self.dietary_restrictions:
                    print("\t" + item)
                    print()



    # Load a file of the specified type into the DataSet
    def load_file(self, file_path, type):
        toml_dict = None
        file_type = None

        try:
            with open(file_path, "rb") as file:
                toml_dict = tomli.load(file)
                file_type = str(DataType[type]) # Check that provided type is valid

        except FileNotFoundError:
            print("[ERROR] File " + file_path + " not found.")
            return

        except KeyError:
            raise TypeError("[ERROR] Invalid data type " + type + " provided to load_file.")

        except tomli.TOMLDecodeError as e:
            print(f"[ERROR] TOML syntax error in file {file_path}: {e}")
            return

        except UnicodeDecodeError as e:
            print(f"[ERROR] Unicode decode error in file {file_path}: {e}. This is probably not a text file.")

        if toml_dict == None:
            raise RuntimeError("test test")

        # Check that loaded file is of provided type
        if toml_dict["type"] != file_type:
            raise TypeError("Provided file " + file_path + " is type " + toml_dict["type"] + " instead of specified type " + type)

        # Do different things on import depending on type
        match toml_dict["type"]:
            case "person":
                # Import additional valid dietary restrictions from new person file
                self.dietary_restrictions.extend(toml_dict["valid_dietary_restrictions"])

                # Check that all people in file have valid restrictions
                for person in toml_dict:
                    if person == "type":
                        continue

                    restrictions_valid = True
                    for item in toml_dict[person].dietary_restrictions:
                        if item not in self.dietary_restrictions:
                            restrictions_valid = False

                    # TODO: Add configurable option for behavior when importing a person
                    # with a new type of dietary restriction
                    if restrictions_valid:
                        self.people.update({person:toml_dict[person]})

                    else:
                        print("Warning: Person " + person + "not added due to invalid dietary restrictions.")

            case "ingredient":
                # TODO: Check whether ingredients have valid units
                match toml_dict:
                    case {
                        "restrictions": {
                            "dietary": {
                                "animalProduct": bool(),
                                "meat": bool(),
                                "egg": bool(),
                                "dairy": bool(),
                                "gluten": bool(),
                                "treeNuts": bool(),
                                "sesame": bool(),
                                "shellfish": bool()
                            }
                        }
                    }:
                        self.ingredients.update({toml_dict["name"]:toml_dict})
                        print(f"Importing ingredient {toml_dict['name']} from {file_path}")

                    case _:
                        print(f"[WARN] Ingredient file {file_path} doesn't match schema")

            case "recipe":
                # TODO: Check that all ingredients in recipes are loaded into session
                # TODO: Compute whether each recipe can be fractionally scaled, and
                # store it as a property
                for recipe in toml_dict:
                    if recipe != "type":
                        self.recipes.update({recipe:toml_dict[recipe]})


    def inspect(self, item_type: DataType, item: str):
        match item_type:
            case DataType.recipe:
                print()
                print("Recipe:     " + item)

                try:
                    print("Fractional: " + str(self.recipes[item]["fractional"]))
                except KeyError:
                    print("Fractional: not specified")

                print("Ingredients: ")

                for ingredient in self.recipes[item]["ingredients"]:
                    print("\t" + ingredient + ": " + str(self.recipes[item]["ingredients"][ingredient]))

            case DataType.ingredient:
                print()
                print("Ingredient: " + item)

                # Print diet incompatibilities
                the_ingredient = self.ingredients[item]
                print("Diet Incompatibilities: ", end="")

                if the_ingredient["diet_incompat"] == []:
                    print("None")

                else:
                    print(the_ingredient["diet_incompat"])

                # Print unit
                print("Unit: " + str(self.ingredients[item]["unit"]))

                # Print price per unit
                print("Price per unit: " + str(self.ingredients[item]["price_per_unit"]))

                # Print purchase increments
                print("Purchase Increments:")
                for increment in self.ingredients[item]["purchase_increments"]:
                    print("\t" + str(item[0]) + " " + str(self.ingredients[item]["unit"]) + " for $" + str(increment[1]))

            case _:
                print(f"[ERROR] DataSet.inspect() could not match type {item_type}. Please report this as a bug.")
                print_bug_report_info()

    # Check whether an item of the specified name and type exist in the current dataset
    def item_exists(self, item_type, item):
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

            case _:
                return False

class IngredientError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class RecipeError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

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


# Pass session, recipe str and quantity int
def calc_and_output(session: DataSet, recipe_str: str, recipe_quantity: float, volume_unit = None):
    # Validate recipe string
    try:
        recipe = session.recipes[recipe_str]
    except KeyError:
        print(f"Recipe {recipe_str} not in dataset.")
        return

    # Validate volume_unit
    if volume_unit is not None and volume_unit not in units.VolumeUnit:
        raise TypeError("calc_and_output: Volume unit {volume_unit} not valid.")


    # Debug option: print raw dict of ingredients
    if session.debug:
        print("Debug: ingredients " + str(recipe["ingredients"]))

    print()
    print("[ " + str(recipe_quantity) + " qty of " + recipe_str + " ]")
    print()

    # Check whether user is attempting to scale a non-divisible recipe by
    # a non-integer amount. If they are, ask them which rounding behavior they
    # want.
    try:
        divisible = recipe["fractional"]

    except KeyError:
        try:
            divisible = is_divisible(session, recipe_str)

        except IngredientError as e:
            print(f"[ERROR] {e.message}")
            divisible = False


    if not divisible and (recipe_quantity % 1) != 0:
        print(f"* Warning: Recipe has ingredients that are not divisible, but quantity {recipe_quantity} is not a whole number. Should it be rounded?")

        selection = input("([C]losest/[u]p/[d]own/[n]o) ")

        while True:
            match selection.lower():
                case "c" | "closest" | "":
                    recipe_quantity = round(recipe_quantity)
                    break

                case "u" | "up":
                    recipe_quantity = ceil(recipe_quantity)
                    break

                case "d" | "down":
                    recipe_quantity = floor(recipe_quantity)
                    break

                case "n" | "no":
                    break

                case _:
                    print("Please select from closest/up/down/no.")

            selection = input("([C]losest/[u]p/[d]own/[n]o) ")

        print()



    for ingredient, amount in recipe["ingredients"].items():

        # Fetch ingredient dict from ingredients file
        ingredient_dict = session.ingredients[ingredient]

        required_qty = amount * recipe_quantity
        unit = abbrev_unit(ingredient_dict["unit"])
        price_of_rq = required_qty * ingredient_dict["price_per_unit"]

        print("\tRequired quantity of " + ingredient + ": " + str(required_qty) + unit)
        print("\tEstimated price of required quantity: " + str(price_of_rq))
        print()

def is_divisible(session: DataSet, recipe_str: str):
    recipe = session.recipes[recipe_str]

    for ingredient in recipe["ingredients"]:
        try:
            if session.ingredients[ingredient]["unit"] == "discrete":
                return False

        # Consider defining new IngredientError type for this?
        except KeyError:
            raise IngredientError(f"Ingredient {ingredient} is not imported into the current session.")

    return True

def print_bug_report_info():
    print("[INFO] Please file bug reports at https://github.com/sudo-nano/quartermaster/issues")
    print("[INFO] Include the command that caused the error, as well as any files it was operating upon.")
