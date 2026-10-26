#!/usr/bin/env python3

from collections import deque
from datetime import date
from fractions import Fraction
from itertools import groupby
from os import PathLike
from pathlib import Path

import tomli_w

def outbound_file_path(inbound: PathLike, i: int) -> tuple[Path, Path]:
    inbound = Path(inbound)
    info = inbound.parent / f"{inbound.stem}_{i}.toml"
    instruction = info.with_suffix(".md")
    return info, instruction

def convert_nyc(file_path: PathLike):
    with open(file_path) as f:
        stripped_lines = [line.strip() for line in f]
        assert stripped_lines[0] == "@@@@@"
        recipes = [deque(g) for k, g in groupby(stripped_lines, lambda x: x == "@@@@@") if not k]
    for i, recipe in enumerate(recipes):
        info_file, instruction_file = outbound_file_path(file_path, i)
        convert_recipe(recipe, info_file, instruction_file)


def convert_recipe(recipe: deque[str], info_file: Path, instruction_file: Path):
    title = parse_title(recipe)
    categories = parse_categories(recipe)
    ingredients = parse_ingredients(recipe)
    directions = parse_directions(recipe)
    yield_, contrib, prep = parse_endlines(recipe)
    # FIXME: Match internal TOML format
    recipe_output = {
        "type": "recipe",
        "name": title,
        "author": contrib or "Unknown",
        "lastUpdated": date.today().strftime("%Y-%m-%d"),
        "ingredients": {
            "list": [
                [ingredient[4], f"{float(ingredient[1]):.2f}", ingredient[2] or ""]
                for ingredient in ingredients
            ]
        },
        "instructions": instruction_file.name,
    }

    with open(info_file, "wb") as f:
        tomli_w.dump(recipe_output, f)

    with open(instruction_file, "w") as f:
        f.write("\n\n".join(directions))


def parse_title(recipe: deque[str]) -> str:
    return parse_paragraph(recipe)


def parse_categories(recipe: deque[str]) -> list[str]:
    pass_blank_lines(recipe)
    if recipe[0][0].isnumeric():
        return []
    categories = parse_paragraph(recipe)
    return [line.strip() for line in categories.split(",")]


def parse_ingredients(recipe: deque[str]):
    pass_blank_lines(recipe)
    ingredients = []
    while recipe[0]:
        ingredients.append(parse_ingredient(recipe.popleft()))
    return ingredients


def parse_ingredient(line: str):
    # FIXME: "$ingredient to taste" lines are parsed wrong
    split_line = deque(line.split())
    quantity = parse_quantity(split_line)
    unit, unit_size = parse_unit(split_line)
    ingredient = " ".join(split_line)
    # TODO: Make a proper class
    return (split_line, quantity, unit, unit_size, ingredient)


def parse_quantity(line: deque[str]):
    quantities = []
    while line[0][0].isnumeric():
        quantities.append(Fraction(line.popleft()))
    return sum(quantities)


def parse_unit(line: deque[str]):
    if len(line) == 1:
        return None, None
    elif line[0] == "x":
        line.popleft()
        return None, None
    else:
        unit = line.popleft()
        if line[0].startswith("("):
            # FIXME: Parse number/quantity out of this
            unit_sizes = []
            while True:
                unit_sizes.append(line.popleft())
                if unit_sizes[-1].endswith(")"):
                    break
            unit_size = " ".join(unit_sizes)
        else:
            unit_size = None
        return unit, unit_size


def parse_directions(recipe: deque[str]) -> list[str]:
    directions = []
    pass_blank_lines(recipe)
    while recipe and not recipe[0].startswith(("Yield: ", "Contributor: ", "Preparation Time: ")):
        directions.append(parse_paragraph(recipe))
        pass_blank_lines(recipe)
    return directions


def parse_endlines(recipe: deque[str]) -> tuple[str | None, str | None, str | None]:
    pass_blank_lines(recipe)
    if recipe and recipe[0].startswith("Yield: "):
        yield_ = recipe.popleft()[7:].strip()
        pass_blank_lines(recipe)
    else:
        yield_ = None

    if recipe and recipe[0].startswith("Contributor: "):
        contrib = recipe.popleft()[13].strip()
        pass_blank_lines(recipe)
    else:
        contrib = None

    if recipe and recipe[0].startswith("Preparation Time: "):
        prep_time = recipe.popleft()[18].strip()
        pass_blank_lines(recipe)
    else:
        prep_time = None

    return yield_, contrib, prep_time


def pass_blank_lines(recipe: deque[str]) -> None:
    while recipe and not recipe[0]:
        recipe.popleft()


def parse_paragraph(recipe: deque[str]) -> str:
    pass_blank_lines(recipe)
    lines = []
    while recipe and recipe[0]:
        lines.append(recipe.popleft())
    return " ".join(lines)


def ensure_end(recipe: deque[str]) -> None:
    if recipe:
        raise ValueError("Expected end of recipe")
