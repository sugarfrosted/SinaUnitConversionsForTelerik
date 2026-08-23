from collections import namedtuple
import unittest
from typing import NamedTuple, Literal
from decimal import Decimal
from src.conversions_sugarfrosted import units

class TestUnitFormatting(unittest.TestCase):
    def case_helper_formatting_for_quantization(self, value, quantization: Decimal|None):
        class pair(NamedTuple):
            abbr: Literal["Un", "In", "Px", "Pt"]
            data: units.Unit

        items = [
            pair("Un", units.Unit(value, quantization=quantization)),
            pair("In", units.Inch(value, quantization=quantization)),
            pair("Px", units.Pixel(value, quantization=quantization)),
            pair("Pt", units.Point(value, quantization=quantization)),
        ]
        if (quantization is None):
            quantization = units.Unit.DEFAULT_QUANTIZATION
        testValue = str(Decimal(value).quantize(quantization)).rstrip("0").rstrip(".")
        for item in items:
            testString = testValue + item.abbr
            self.assertEqual(item.data.toTelerikString(), testString)

    def test_formatting(self):
        self.case_helper_formatting_for_quantization(1/3, None)
        self.case_helper_formatting_for_quantization(1/3, Decimal("0.0001"))
        self.case_helper_formatting_for_quantization("0.0001", None)
        self.case_helper_formatting_for_quantization("0.0001", Decimal("0.0001"))

class TestUnitConversions(unittest.TestCase):
    __quantization1 = Decimal("1E-5")
    def test_conversion_inch_to_inch(self):
        length = units.Inch(1, quantization=self.__quantization1)
        convertedLength = length.convertToInch()
        self.assertEqual(length.toTelerikValue(), convertedLength.toTelerikValue())
        self.assertEqual(length.toTelerikString(), convertedLength.toTelerikString())
    def test_conversion_inch_to_pixel(self):
        length = units.Inch(1, quantization=self.__quantization1)
        convertedLength = length.convertToPixel()
        expectedLength = units.Pixel("96.0000", self.__quantization1)
        self.assertEqual(convertedLength.toTelerikValue(), expectedLength.toTelerikValue())
        self.assertEqual(convertedLength.toTelerikString(), expectedLength.toTelerikString())
    def test_conversion_inch_to_points(self):
        length = units.Inch(1, self.__quantization1)
        convertedLength = length.convertToPoint()
        expectedLength = units.Point("72.0000", self.__quantization1)
        self.assertEqual(convertedLength.toTelerikValue(), expectedLength.toTelerikValue())
        self.assertEqual(convertedLength.toTelerikString(), expectedLength.toTelerikString())

    def test_conversion_pixel_to_inch(self):
        length = units.Pixel(96, quantization=self.__quantization1)
        convertedLength = length.convertToInch()
        expectedLength = units.Inch("1.0000", self.__quantization1)
        self.assertEqual(convertedLength.toTelerikValue(), expectedLength.toTelerikValue())
        self.assertEqual(convertedLength.toTelerikString(), expectedLength.toTelerikString())
    def test_conversion_pixel_to_pixel(self):
        length = units.Pixel(96, quantization=self.__quantization1)
        convertedLength = length.convertToPixel()
        self.assertEqual(length.toTelerikValue(), convertedLength.toTelerikValue())
        self.assertEqual(length.toTelerikString(), convertedLength.toTelerikString())
    def test_conversion_pixel_to_points(self):
        length = units.Pixel(96, self.__quantization1)
        convertedLength = length.convertToPoint()
        expectedLength = units.Point("72.0000", self.__quantization1)
        self.assertEqual(convertedLength.toTelerikValue(), expectedLength.toTelerikValue())
        self.assertEqual(convertedLength.toTelerikString(), expectedLength.toTelerikString())

    def test_conversion_point_to_inch(self):
        length = units.Point(72, self.__quantization1)
        convertedLength = length.convertToInch()
        expectedLength = units.Inch("1.0000", self.__quantization1)
        self.assertEqual(convertedLength.toTelerikValue(), expectedLength.toTelerikValue())
        self.assertEqual(convertedLength.toTelerikString(), expectedLength.toTelerikString())
    def test_conversion_point_to_pixel(self):
        length = units.Point(72, quantization=self.__quantization1)
        convertedLength = length.convertToPixel()
        expectedLength = units.Pixel(96, self.__quantization1)
        self.assertEqual(convertedLength.toTelerikValue(), expectedLength.toTelerikValue())
        self.assertEqual(convertedLength.toTelerikString(), expectedLength.toTelerikString())
    def test_conversion_point_to_point(self):
        length = units.Point(72, quantization=self.__quantization1)
        convertedLength = length.convertToPoint()
        self.assertEqual(length.toTelerikValue(), convertedLength.toTelerikValue())
        self.assertEqual(length.toTelerikString(), convertedLength.toTelerikString())
    
class TestMathematicalOperations(unittest.TestCase):
    def test_inch_add(self):
        left = units.Inch("1")
        right = units.Inch("1")

        value = (left + right)
        expectedValue = units.Inch(2)

        self.assertEqual(value.toTelerikValue(), expectedValue.toTelerikValue())
        self.assertEqual(value.toTelerikString(), expectedValue.toTelerikString())
    def test_inch_add_different_quantization(self):
        left = units.Inch("0.1010101010", quantization = Decimal("1E-6"))
        right = units.Inch("0.0101010101", quantization = Decimal("1E-5"))

        value = (left + right)
        expectedValue = units.Inch("0.1111111", quantization = Decimal("1E-6"))

        self.assertEqual(value.toTelerikValue(), expectedValue.toTelerikValue())
        self.assertEqual(value.toTelerikString(), expectedValue.toTelerikString())
    def test_point_add(self):
        left = units.Point("1")
        right = units.Point("1")

        value = (left + right)
        expectedValue = units.Point(2)
        
        self.assertEqual(value.toTelerikValue(), expectedValue.toTelerikValue())
        self.assertEqual(value.toTelerikString(), expectedValue.toTelerikString())

    def test_pixel_add(self):
        left = units.Pixel("1")
        right = units.Pixel("1")

        value = (left + right)
        expectedValue = units.Pixel(2)

        self.assertEqual(value.toTelerikValue(), expectedValue.toTelerikValue())
        self.assertEqual(value.toTelerikString(), expectedValue.toTelerikString())

    def test_pixel_plus_inch(self):
        left = units.Pixel(96)
        right = units.Inch(1)

        value = (left + right)
        expectedValue = units.Pixel(2*96)

        self.assertIsInstance(value, units.Pixel)
        self.assertEqual(value.toTelerikValue(), expectedValue.toTelerikValue())
        self.assertEqual(value.toTelerikString(), expectedValue.toTelerikString())

    def test_pixel_plus_point(self):
        left = units.Pixel(96)
        right = units.Point(72)

        value = (left + right)
        expectedValue = units.Pixel(2*96)

        self.assertIsInstance(value, units.Pixel)
        self.assertEqual(value.toTelerikValue(), expectedValue.toTelerikValue())
        self.assertEqual(value.toTelerikString(), expectedValue.toTelerikString())
    
    def test_point_plus_inch(self):
        left = units.Point(72)
        right = units.Inch(1)

        value = (left + right)
        expectedValue = units.Point(2*72)

        self.assertIsInstance(value, units.Point)
        self.assertEqual(value.toTelerikValue(), expectedValue.toTelerikValue())
        self.assertEqual(value.toTelerikString(), expectedValue.toTelerikString())

    def test_inch_plus_pixel(self):
        left = units.Inch(1)
        right = units.Pixel(96)
        
        value = (left + right)
        expectedValue = units.Pixel(2*96)
        self.assertIsInstance(value, units.Pixel)
        self.assertEqual(value.toTelerikValue(), expectedValue.toTelerikValue())
        self.assertEqual(value.toTelerikString(), expectedValue.toTelerikString())

    def test_point_plus_pixel(self):
        left = units.Point(72)
        right = units.Pixel(96)

        value = (left + right)
        expectedValue = units.Pixel(2*96)
        self.assertIsInstance(value, units.Pixel)
        self.assertEqual(value.toTelerikValue(), expectedValue.toTelerikValue())
        self.assertEqual(value.toTelerikString(), expectedValue.toTelerikString())
    
    def test_inch_plus_point(self):
        left = units.Inch(1)
        right = units.Point(72)
        
        value = (left + right)
        expectedValue = units.Point(2*72)
        self.assertIsInstance(value, units.Point)
        self.assertEqual(value.toTelerikValue(), expectedValue.toTelerikValue())
        self.assertEqual(value.toTelerikString(), expectedValue.toTelerikString())

    def test_unitA_minus_unitB(self):
        pass

    def test_unitA_scaledBy_decimal(self):
        pass

    def test_unitA_reducedBy_decimal(self):
        pass

    def test_getRatioBetween_unitA_unitB(self):
        pass


if __name__ == '__main__':
    unittest.main()