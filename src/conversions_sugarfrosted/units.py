from decimal import Decimal, InvalidOperation
from numbers import Number

PIXELS_PER_INCH: Decimal = Decimal("96.000")
POINTS_PER_INCH: Decimal = Decimal("72.000")

class Unit:
    DEFAULT_QUANTIZATION: Decimal = Decimal("1E-3")
    UNIT_ABBR = "Un"
    UNIT_NAME = "Unit"

    @property
    def quantization(self) -> Decimal:
        return self.__quantization
    __quantization: Decimal = DEFAULT_QUANTIZATION

    @property
    def value(self) -> Decimal:
        return self.__value
    __value : Decimal = Decimal()

    def __init__(self, value: any, quantization: Decimal|str|None = None):
        if (value is not None):
            try:
                self.__value = Decimal(value)
            except InvalidOperation:
                raise ValueError("value is not a valid decimal format")
        if (quantization is not None):
            self.__quantization = Unit.formatQuantization(quantization)

    @staticmethod
    def formatQuantization(quantization: Decimal|str) -> Decimal:
        if (isinstance(quantization,Decimal)):
            return quantization
        elif (isinstance(quantization,str)):
            try:
                return Decimal(quantization)
            except InvalidOperation:
                raise ValueError("quantization is not a valid decimal string format")
        else:
            raise ValueError("quantization must be a decimal value")

    def toTelerikValue(self) -> Decimal:
        return self.__value.quantize(self.quantization)
    def toTelerikString(self) -> str:
        return str(self.toTelerikValue()).rstrip("0").removesuffix(".") + type(self).UNIT_ABBR
    def get_perInch(self) -> Decimal:
        pass
    def convertToPixel(self) -> Pixel:
        pass
    def convertToPoint(self) -> Point:
        pass
    def convertToInch(self) -> Inch:
        pass

    @staticmethod
    def get_name() -> str:
        return "Unit"

    def __add__(self, other: Unit) -> Unit:
        if(type(self) == type(other)):
            return type(self)(self.value + other.value, quantization = min(self.quantization, other.quantization))
        
        targetType = self if (self.get_perInch() > other.get_perInch()) else other

        if (isinstance(targetType, Inch)):
            return self.convertToInch() + other.convertToInch()
        elif (isinstance(targetType, Point)):
            return self.convertToPoint() + other.convertToPoint()
        elif (isinstance(targetType, Pixel)):
            return self.convertToPixel() + other.convertToPixel()
        raise NotImplementedError("Type not supported")

    def __minus__(self, other: Unit) -> Unit:
        return self - type(other)(-other.value, quantization = other.quantization)

    def scaleBy(self, scalar: Number) -> Unit:
        return type(self)(self.value * scalar, quantization = self.quantization)

    def reduceBy(self, scalar: Number) -> Unit:
        return type(self)(self.value / scalar, quantization = self.quantization)

    def getRatio(self, other) -> Decimal:
        if(type(self) == type(other)):
            return type(self)(self.value + other.value, quantization = min(self.quantization, other.quantization))
        
        targetType = self if (self.get_perInch() > other.get_perInch()) else other

        if (isinstance(targetType, Inch)):
            return self.convertToInch().value / other.convertToInch().value
        elif (isinstance(targetType, Point)):
            return self.convertToPoint().value / other.convertToPoint().value
        elif (isinstance(targetType, Pixel)):
            return self.convertToPixel().value / other.convertToPixel().value
        raise NotImplementedError("Type not supported")

class Inch(Unit):
    UNIT_ABBR = "In"
    UNIT_NAME = "Inch"
    def get_perInch(self):
        return Decimal(1)
    def convertToPixel(self) -> Pixel:
        newValue = self.value * PIXELS_PER_INCH
        return Pixel(newValue , quantization=self.quantization)
    def convertToPoint(self) -> Point:
        newValue = self.value * POINTS_PER_INCH
        return Point(newValue, quantization=self.quantization)
    def convertToInch(self) -> Inch:
        newValue = self.value
        return Inch(newValue, quantization=self.quantization)

class Point(Unit):
    UNIT_ABBR = "Pt"
    UNIT_NAME = "Point"
    def get_perInch(self) -> Decimal:
        return POINTS_PER_INCH

    def convertToPixel(self) -> Pixel:
        newValue = self.value * PIXELS_PER_INCH / POINTS_PER_INCH
        return Pixel(newValue, quantization=self.quantization)
    def convertToPoint(self) -> Point:
        newValue = self.value
        return Point(newValue, quantization=self.quantization)
    def convertToInch(self) -> Inch:
        newValue = self.value / POINTS_PER_INCH
        return Inch(newValue, quantization=self.quantization)

class Pixel(Unit):
    UNIT_ABBR = "Px"
    UNIT_NAME = "Pixel"
    def get_perInch(self) -> Decimal:
        return PIXELS_PER_INCH
    
    def convertToPixel(self) -> Pixel:
        newValue = self.value
        return Pixel(newValue, quantization=self.quantization)
    def convertToPoint(self) -> Point:
        newValue = self.value * POINTS_PER_INCH / PIXELS_PER_INCH
        return Point(newValue, quantization=self.quantization)
    def convertToInch(self) -> Inch:
        newValue = self.value / PIXELS_PER_INCH
        return Inch(newValue, quantization=self.quantization)

if __name__ == "__main__":
    #thing = Unit("0.123456789")
    #print(thing.toTelerikString())
    thing = Pixel("1.0001")
    #print(thing.convertToPoint().toTelerikValue())
    print(thing.toTelerikString())

