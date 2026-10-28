# Formats 

Quartermaster aims to support as many third party recipe formats as possible.
We are aware of the following formats: 
- [ ] Paprika 
- [ ] Now You're Cooking!
    - [X] Individual recipe format (thanks Patrick!)
    - [ ] Recipe book format 
- [ ] MealMaster

If there are other formats you'd like supported, please submit a feature request.

## Paprika 
The Truitt-Galt family has been kind enough to submit their Paprika recipe collection
to further Quartermaster's development.
The Paprika format is a zip file of `.paprika` files, which are actually JSON. 

## Now You're Cooking!
Support for the Now You're Cooking! recipe format was merged in commit 68a007f.
A generic recipe file containing multiple recipes is [available for testing](https://www.ffts.com/Generic.txt).
Their "recipe book" format, which includes `.tag`, `.cdx`, `.idx`, `.gcf`, and `cli`
files, needs more reverse engineering work to be supported.

## MealMaster 
MealMaster uses `.mmf` files, which are a custom plaintext format.
MealMaster formatted recipes are available from the 
[Now You're Cooking! recipes directory.](https://www.ffts.com/recipes.htm)
These are not yet supported, but their format is simple and shouldn't be too hard to
implement.
