from units import Unit

class Positition:
    left: Unit
    top: Unit
    def __init__(self, left: Unit, top: Unit):
        self.left = left
        self.top = top

class Size:
    width: Unit
    height: Unit
    def __init__(self, width: Unit, height: Unit):
        self.width = width
        self.height = height

class Layout:
    position : Positition
    size : Size
    def __init__(self, position: Positition, size: Size):
        self.position = position
        self.size = size

    @staticmethod
    def GetFromUnits(left: Unit, top: Unit, width: Unit, height: Unit) -> Layout:
        return Layout(Positition(left, top), Size(width, height))

class Element:
    layout: Layout