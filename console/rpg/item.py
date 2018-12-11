import math
class TypeMap:
    colours=[
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
    ]
    types=[
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
    ]
    def __mul__(self,other):
        return[other*i for i in self.types]
class Item:
    pass
