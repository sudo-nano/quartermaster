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

# This is so evil
# https://en.wikipedia.org/wiki/Comparison_of_the_imperial_and_US_customary_measurement_systems
# Volume units for imperial and US customary are different. Additionally, US
# customary differentiates between liquid and dry measure, but only for some units.
class VolumeUnit(Enum):
    milliliters = 0
    liters = 1
    fl_oz_imperial = 2
    fl_oz_customary = 3
    pint_imperial = 4
    pint_customary_liquid = 5
    pint_customary_dry = 6
    quart_imperial = 7
    quart_customary_liquid = 8
    quart_customary_dry = 9

    # For some reason gallons in US customary units do not differentiate
    # between liquid and dry measure, even though pint and quart do
    gallon_imperial = 10
    gallon_customary = 11

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
        match unit:
            case VolumeUnit.milliliters:
                return self.volume_mL

            case VolumeUnit.liters:
                return self.volume_mL / 1000

            case VolumeUnit.fl_oz_imperial:
                return self.volume_mL / 28.4130625

            case VolumeUnit.fl_oz_customary:
                return self.volume_mL / 29.5735295625

            case VolumeUnit.pint_imperial:
                return self.volume_mL / 568.26125

            case VolumeUnit.pint_customary_liquid:
                return self.volume_mL / 473.176473

            case VolumeUnit.pint_customary_dry:
                return self.volume_mL / 550.6104713575

            case VolumeUnit.quart_imperial:
                return self.volume_mL / 1136.5225

            case VolumeUnit.quart_customary_liquid:
                return self.volume_mL / 946.352946

            case VolumeUnit.quart_customary_dry:
                return self.volume_mL / 1101.220942715

            case VolumeUnit.gallon_imperial:
                return self.volume_mL / 4546.09

            case VolumeUnit.gallon_customary:
                return self.volume_mL / 3785.411784

            case other:
                raise TypeError(f"Could not convert to invalid volume unit {unit}")

    # Return a tuple containing the value for this volume and its unit
    def get(self):
        return (self.convert_to(self.unit), self.unit)
