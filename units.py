# Quartermaster Unit Conversions
from enum import Enum

class TempUnit(Enum):
    celsius = 0
    fahrenheit = 1
    kelvin = 2
    rankine = 3

def convert_temp(temp, unit_from, unit_to):
    # Type check temperature value
    temp_is_int = isinstance(temp, int)
    temp_is_float = isinstance(temp, float)
    if not (temp_is_int or temp_is_float):
        raise TypeError(f"Temperature value is invalid type {type(temp)}. Use int or float instead.")

    # Type check input unit and convert to celsius as intermediate
    intermediate_celsius = TempUnit
    match unit_from:
        case TempUnit.celsius:
            intermediate_celsius = temp

        case TempUnit.fahrenheit:
            intermediate_celsius = (temp - 32) * 1.8

        case TempUnit.kelvin:
            intermediate_celsius = temp - 273.15

        case TempUnit.rankine:
            intermediate_celsius = (temp * 1.8) - 273.15

        case other:
            raise TypeError(f"Cannot convert from invalid temperature unit {unit_from}. See TempUnit enum for valid units.")

    # Type check output unit and convert intermediate to output unit
    match unit_to:
        case TempUnit.celsius:
            return [intermediate_celsius, TempUnit.celsius]

        case TempUnit.fahrenheit:
            output_value = (intermediate_celsius * 1.8) + 32
            return [output_value, TempUnit.fahrenheit]

        case TempUnit.kelvin:
            return [intermediate_celsius + 273.15, TempUnit.kelvin]

        case TempUnit.rankine:
            output_value = (intermediate_celsius + 273.15) / 1.8
            return [output_value, TempUnit.rankine]

        case other:
            raise TypeError(f"Cannot convert to invalid temperature unit {unit_to}. See TempUnit enum for valid units.")
