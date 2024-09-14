# Quartermaster Unit Conversions
from enum import Enum

class TempUnit(Enum):
    celsius = 0
    fahrenheit = 1
    kelvin = 2
    rankine = 3

class Temperature:
    # Temperature is internally stored in Celsius.
    temp_celsius = 0

    def __init__(self, temp, unit):
        self.set_temp(temp, unit)

    def set_temp(self, temp, unit):
        # Type check temperature value
        temp_is_int = isinstance(temp, int)
        temp_is_float = isinstance(temp, float)
        if not (temp_is_int or temp_is_float):
            raise TypeError(f"Temperature value is invalid type {type(temp)}. Use int or float instead.")

        # Type check input unit and convert to celsius
        match unit:
            case TempUnit.celsius:
                self.intermediate_celsius = temp

            case TempUnit.fahrenheit:
                self.intermediate_celsius = (temp - 32) * 1.8

            case TempUnit.kelvin:
                self.intermediate_celsius = temp - 273.15

            case TempUnit.rankine:
                self.intermediate_celsius = (temp * 1.8) - 273.15

            case other:
                raise TypeError(f"Cannot convert from invalid temperature unit {unit_from}. See TempUnit enum for valid units.")

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
