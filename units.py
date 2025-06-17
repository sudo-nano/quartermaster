# Quartermaster Unit Conversions
from enum import Enum
from math import isnan

class TempUnit(Enum):
    celsius = 0
    fahrenheit = 1
    kelvin = 2
    rankine = 3

class Temperature:
    # Temperature is internally stored in Celsius.
    def __init__(self, temp, unit):
        self.set_temp(temp, unit)

    def set_temp(self, temp, unit):
        # Type check temperature value
        if type(temp) not in [int, float]:
            raise TypeError(f"Temperature value is invalid type {type(temp)}. Use int or float instead.")

        if isnan(temp):
            raise ValueError("Provided temperature is NaN")

        # Type check input unit and convert to celsius
        match unit:
            case TempUnit.celsius:
                self.temp_celsius = temp

            case TempUnit.fahrenheit:
                self.temp_celsius = (temp - 32) * 1.8

            case TempUnit.kelvin:
                self.temp_celsius = temp - 273.15

            case TempUnit.rankine:
                self.temp_celsius = (temp * 1.8) - 273.15

            case other:
                raise TypeError(f"Cannot convert from invalid temperature unit {unit}. See TempUnit enum for valid units.")

    def convert_to(self, unit_to):
        match unit_to:
            case TempUnit.celsius:
                return self.temp_celsius

            case TempUnit.fahrenheit:
                output_value = (self.temp_celsius * 1.8) + 32
                return output_value

            case TempUnit.kelvin:
                return self.temp_celsius + 273.15

            case TempUnit.rankine:
                output_value = (self.temp_celsius + 273.15) / 1.8
                return output_value

            case other:
                raise TypeError(f"Cannot convert to invalid temperature unit {unit_to}. See TempUnit enum for valid units.")

'''
This is so evil.
https://en.wikipedia.org/wiki/Comparison_of_the_imperial_and_US_customary_measurement_systems
Volume units for imperial and US customary are different. Additionally, US
customary differentiates between liquid and dry measure, but only for some units.

Each member's value is its conversion factor to the reference unit. In this case,
the reference unit is mL. Yes, I know the SI reference unit is L.
'''

class VolumeUnit(Enum):
    milliliters = 1.0
    liters = 1000.0
    fl_oz_imperial = 28.4130625
    fl_oz_customary = 29.5735295625
    pint_imperial = 568.26125
    pint_customary_liquid = 473.176473
    pint_customary_dry = 550.6104713575
    quart_imperial = 1136.5225
    quart_customary_liquid = 946.352946
    quart_customary_dry = 1101.220942715

    # For some reason gallons in US customary units do not differentiate
    # between liquid and dry measure, even though pint and quart do
    gallon_imperial = 4546.09
    gallon_customary = 3785.411784

'''
Parse a string and attempt to convert it to a VolumeUnit.

The defaults parameter will, in the future, take an object describing what
imperial units to use in ambiguous cases. allow_interactive tells the function
whether it's being used as part of an interactive session. If it is,
then it's allowed to prompt the user to select a unit in ambiguous cases.

TODO: Implement defaults object and its handling
TODO: Implement interactive prompt for ambiguous units
'''
def str_to_VolumeUnit(unit_str: str, defaults=None, allow_interactive=False):
    if type(unit_str) != str:
        raise TypeError("Provided input is not a string.")

    # First attempt exact matches
    match unit_str.lower():
        case "ml" | "milliliter" | "milliliters":
            return VolumeUnit.milliliters

        case "l" | "liter" | "liters":
            return VolumeUnit.liters

        # For now, we default to customary liquid pints.
        case "pt" | "pint" | "pints":
            return VolumeUnit.pint_customary_liquid

        case "qt" | "quart" | "quarts":
            return VolumeUnit.quart_customary_liquid

        case "gal" | "gallon" | "gallons":
            return VolumeUnit.gallon_customary

    # Now we attempt hellish fuzzy matching for the other units
    # TODO: Write hellish fuzzy matching

    # If matching fails, raise an error.
    raise ValueError("Could not convert string to VolumeUnit")


class Volume:
    def __init__(self, volume: float, unit: VolumeUnit):
        self.set_volume(volume, unit)

    def set_volume(self, volume: float, unit: VolumeUnit):
        # Type check inputs
        if type(volume) not in [int, float]:
            raise TypeError(f"Volume provided is invalid type {type(volume)}. Please provide an int or float.")

        if isnan(volume):
            raise ValueError("Volume provided is NaN")

        self.volume_mL = volume
        self.unit = unit

    def convert_to(self, unit: VolumeUnit):
        try:
            value = self.volume_mL / unit.value
            return value
        except:
            raise TypeError(f"Could not convert to invalid volume unit {unit}")

    # Return a tuple containing the value for this volume and its unit
    def get(self):
        return (self.convert_to(self.unit), self.unit)
