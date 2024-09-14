# quartermaster
A program for calculating recipe ingredient quantities and costs, given parameters such as amount, time, and consumption rate.

## Description
Quartermaster is a command line program that does logistical calculations and scaling for recipes.
While primarily designed for cooking, non-food ingredients can be used to plan other things.
Ingredients, recipes, and cost-per-unit is specified in TOML files. The program
uses these to calculate required ingredient amounts and costs for recipes.

This program is in *very* early development. It's being developed alongside its sister project,
the [Digitized Recipe Format](https://github.com/sudo-nano/digitized-recipe-format).

## Quick-Start
1. Install the `toml` Python library
2. Clone the repository
3. Run `python3 main.py`

For more detailed instructions, see [Installation Instructions](https://github.com/sudo-nano/quartermaster/wiki/Installation).

## Implemented Features
- Calculation of ingredients required for some quantity of a recipe
- Calculation of ingredient cost for some quantity of a recipe

## Planned Features
- Manual specification of ingredient and recipe TOML files
- Load more than one ingredient or recipe file
- Load files with data for people
  - Dietary restrictions by type
  - Dietary restrictions by specific ingredients
  - Ability to specify non-default rate of consumption
- Ability to specify duration of time when provided with rate of consumption
   - User specifies days and meals per day, person data provides amount consumed compared to one standard recipe/portion
- Ability to provide defaults in TOML files
  - Program will assume defaults if values are left unspecified
- Save and load sessions
- New Data Type: `group` containing a collection of people
