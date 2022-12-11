# quartermaster
A program for calculating recipe ingredient quantities and costs, given parameters such as amount or time and consumption rate. 

## Long description 
Quartermaster is a command line program that aims to ease logistics calculations for recipes. While primarily designed for cooking, non-food ingredients can be used to plan other things. The program is given one TOML file each for ingredients and recipes. (These files are currently hardcoded, you'll be able to provide multiple files in future versions.) Given these files, you can calculate how much of each ingredient you'll need for a given amount of a recipe, and approximately how much it'll cost.

This program is in *very* early development. Input sanitization is iffy or nonexistent, most features are not implemented yet. 

## Currently Implemented Commands

### calc 
The `calc` command takes the name of the recipe and an int or float for the quantity of that recipe. 

Example:
`calc default_breakfast 5` calculates the necessary ingredients to produce a `default_breakfast` 5 times.

## Planned Features
- Manual specification of ingredient and recipe TOML files
- Abilitiy to load more than one ingredient or recipe file
- Ability to load files with data for people
