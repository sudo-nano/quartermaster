# Quartermaster Tests
import units

'''
str_to_VolumeUnit tests
'''

def test_strToVolumeUnit_mL():
    result_0 = units.str_to_VolumeUnit("mL")
    result_1 = units.str_to_VolumeUnit("milliliter")
    result_2 = units.str_to_VolumeUnit("milliliters")
    result_3 = units.str_to_VolumeUnit("mIlLiLiTeRs") # Case should not need to match

    results = [result_0, result_1, result_2, result_3]
    for item in results:
        if item != units.VolumeUnit.milliliters:
            raise RuntimeError("Unit string not converted to milliliters")

def test_strToVolumeUnit_L():
    result_0 = units.str_to_VolumeUnit("L")
    result_1 = units.str_to_VolumeUnit("liter")
    result_2 = units.str_to_VolumeUnit("liters")
    result_3 = units.str_to_VolumeUnit("lItErS")

    results = [result_0, result_1, result_2, result_3]
    for item in results:
        if item != units.VolumeUnit.liters:
            raise RuntimeError("Unit string not converted to liters")
