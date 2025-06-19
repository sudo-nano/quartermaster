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
### Scale a recipe up or down
```
quartermaster > inspect recipe default_breakfast

Recipe: default_breakfast
Fractional: False
Ingredients:
	rice: 195.0
	egg: 1.0
	bacon: 2.0
	soy_sauce: 10.0

quartermaster > scale default_breakfast 5

[ 5.0 qty of default_breakfast ]

	Required quantity of rice: 975.0g
	Estimated price of required quantity: 4.875

	Required quantity of egg: 5.0
	Estimated price of required quantity: 2.08335

	Required quantity of bacon: 10.0
	Estimated price of required quantity: 5.0

	Required quantity of soy_sauce: 50.0mL
	Estimated price of required quantity: 0.25
```

## Planned Features
- Automatic conversion between imperial and units
- Conversion between mass and volume units!
- Load files with data for people
  - Dietary restrictions by type
  - Dietary restrictions by specific ingredients
  - Ability to specify non-default rate of consumption
- Create meal plans and check them against people's dietary restrictions
- Calculation of total consumption over a given period of time
- Save and load sessions
- New Data Type: `group` containing a collection of people

## Help Needed
These are the things we need help with. (No generative AI contributions please.)
### Data Gathering
- Ingredient data
  - Common ingredients
  - Ingredient prices
  - Ingredient densities

- Recipe gathering
  - Diverse set of real recipes for default data set and thorough testing of the program

### Implementing Planned Features
If you want to help but aren't sure what to work on, check the issue tracker and pick up
one of the issues marked "enhancement" or "feature request."
