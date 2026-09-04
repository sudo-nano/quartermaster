import tomli
from enum import Enum
from math import ceil, floor
import units
import regex

class DataType(Enum):
    # best_match_substring was constructed assuming there are no substrings that match multiple
    # of these enum values at the same start and end point
    multiple = "multiple"
    none = "none"
    ingredient = "ingredient"
    recipe = "recipe"
    person = "person"
    group = "group"

    def __str__(self):
        return str(self.value)

    def from_str(input: str, debug=False):
        # First, automatically match using keys
        try:
            result = DataType[input]
            return result

        # If there isn't an exact match, perform fuzzy matching
        except KeyError:
            match len(input):
                case 0:
                    raise RuntimeError("Cannot type match empty string")

                case 1:
                    for item in DataType:
                        if input == str(item)[0]:
                            return item

                    raise RuntimeError(f"Single character {input} does not match the first letter of any command.")

                case _:
                    match_result = best_match_substring([e.value for e in DataType], input)

                    if debug:
                        print(f"[DEBUG] DataType.from_str(): match_result is {match_result}")

                    if type(match_result) == list:
                        raise NameError(f"Multiple DataType matches for string {input}")

                    return DataType[match_result]



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
        match type:
            case "ingredient" | "ingredients" | "i":
                for ingredient in list(self.ingredients.values()):
                    print(f"\t{ingredient["name"]}")
                    print()

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

            case _:
                raise TypeError(f"Invalid data type " + type + " provided to list.")





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
            raise RuntimeError("toml_dict is None after attempting to load file")

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
                # Ensure that mandatory restrictions fields are filled out
                match toml_dict:
                    case {
                        "name": str(),
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
                            },
                            "religious": {
                                "halal": bool(),
                                "kosher": bool(),
                                "leavened": bool()
                            }
                        }
                    }:
                        self.ingredients.update({toml_dict["name"]:toml_dict})

                    case _:
                        # TODO: Add link to DRF specification for required fields
                        print(f"[WARN] Ingredient file {file_path} doesn't match schema and will not be imported.")

            case "recipe":
                # TODO: Check that all ingredients in recipes are loaded into session
                # TODO: Compute whether each recipe can be fractionally scaled, and
                # store it as a property
                match toml_dict:
                    case {
                        "name": str(),
                        "ingredients": dict()
                    }:
                        self.recipes.update({toml_dict["name"]:toml_dict})

                    case _:
                        # TODO: Add link to DRF specification for required fields
                        print(f"[WARN] Recipe file {file_path} doesn't match schema and will not be imported.")


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
                print("-- Ingredient: " + item + " --")
                print()

                # Print diet incompatibilities
                the_ingredient = self.ingredients[item]
                dietary_restrictions = the_ingredient["restrictions"]["dietary"]
                religious_restrictions = the_ingredient["restrictions"]["religious"]

                print("Diet Incompatibilities: ", end="")

                if the_ingredient["restrictions"]["dietary"] == []:
                    print("None")

                else:
                    print()
                    for restriction in dietary_restrictions:
                        print(f"\t{restriction}: {dietary_restrictions[restriction]}")
                print()

                # Print religious restrictions
                print("Religious Restrictions: ", end="")
                if religious_restrictions == []:
                    print("None")

                else:
                    print()
                    for restriction in religious_restrictions:
                        print(f"\t{restriction}: {religious_restrictions[restriction]}")
                print()

                # Print purchase increments
                try:
                    print("Purchase Increments:")
                    for increment in self.ingredients[item]["purchase_increments"]:
                        print("\t" + str(increment[0]) + " " + str(increment[1]) + " for $" + str(increment[2]))

                except KeyError:
                    print("[WARN] There is no purchase_increments field in this ingredient. Price calculation will not be possible.")

            case _:
                print(f"[ERROR] DataSet.inspect() could not match type {item_type}. Please report this as a bug.")
                print_bug_report_info()

    # Check whether an item of the specified name and type exist in the current dataset
    def item_exists(self, item_type: DataType, item: str):
        match item_type:
            case DataType.recipe:
                if item in self.recipes:
                    return True

                else:
                    return False

            case DataType.ingredient:
                if item in self.ingredients:
                    return True

                else:
                    return False

            case DataType.person:
                if item in self.people:
                    return True

            case DataType.group:
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
        print("[DEBUG] Ingredients: " + str(recipe["ingredients"]))

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
            return None


    if not divisible and (recipe_quantity % 1) != 0:
        print(f"[WARN] Recipe has ingredients that are not divisible, but quantity {recipe_quantity} is not a whole number. Should it be rounded?")

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
    error = False
    not_in_session = []

    for ingredient in recipe["ingredients"]:
        try:
            if session.ingredients[ingredient]["unit"] == "discrete":
                return False

        except KeyError:
            error = True
            not_in_session.append(ingredient)

    if error:
        raise IngredientError(f"One or more ingredients are missing from the current session. Missing: {not_in_session}")

    return True

def print_bug_report_info():
    print("[INFO] Please file bug reports at https://github.com/sudo-nano/quartermaster/issues")
    print("[INFO] Include the command that caused the error, as well as any files it was operating upon.")

# Takes a list of strings and a substring to attempt to match against the list of strings.
# On a single match, returns the matching string. On multiple matches, attempts to find
# "best" match (first occurring, then longest) and return the best. In the event of a tie,
# returns a list of tied options.
def best_match_substring(candidates: list, input: str):
    matches = []
    for candidate in candidates:
        match = regex.search(input, candidate)
        if match != None:
            matches.append((candidate, match))

    match len(matches):
        case 0:
            raise NameError("No candidates match the provided string")

        case 1:
            return matches[0][0]

        case _:
            # Attempt to select earliest match
            best_start = matches[1][1].start()
            sub_matches = [matches[0]]
            for i in range(1, len(matches)):
                if matches[1][i].start() < best_start:
                    best_start = matches[1][i].start()
                    sub_matches = [matches[i]]

                if matches[1][i].start() == best_start:
                    sub_matches.append(matches[i])

                # if matches[i].start() > best_start, do nothing

            if len(sub_matches) == 1:
                return sub_matches[0][0]

            if len(sub_matches) == 0:
                print_bug_report_info()
                raise RuntimeError("Zero sub-matches found during selection of earliest match. This shouldn't happen!")

            # If multiple matches tie for earliest match, select from these the match with
            # the latest end (and therefore longest match)
            best_end = sub_matches[1][1].end()
            sub_sub_matches = [sub_matches[0]]
            for i in range(1, len(sub_matches)):
                if sub_matches[1][i].end() > best_end:
                    best_end = sub_matches[1][i].end()
                    sub_sub_matches = [sub_matches[i]]

                if sub_matches[1][i].end() == best_end:
                    sub_sub_matches.append(sub_matches[i])

                # If sub_matches[i].end() is less than best_end, do nothing.

            if len(sub_sub_matches) == 1:
                return sub_sub_matches[0][0]

            else:
                return sub_sub_matches
