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
    names=[
        "strike",
        "slice",
        "chill",
        "burn",
        "blast",
        "shock",
        "poison",
        "drain"
    ]
    def __init__(self,
        strike=0,
        slice=0,
        chill=0,
        burn=0,
        blast=0,
        shock=0,
        poison=0,
        drain=0
    ):
        self.types=[
            strike,
            slice,
            chill,
            burn,
            blast,
            shock,
            poison,
            drain
        ]
        self.normalize()
    def __setattr__(self,name,val):
        for n in range(8):
            if self.names[n]==name:
                self.types[n]=val
        else:
            super().__setattr__(name,val)
    def __iter__(self):
        return iter(self.types)
    def __add__(self,other):
        return TypeMap(*map(sum,zip(self,other)))
    def __sub__(self,other):
        return TypeMap(*map(lambda a:a[0]-a[1],zip(self,other)))
    def __mul__(self,other):
        return TypeMap([other*i for i in self.types])
    def __truediv__(self,other):
        return self*(1/other)
    def __iadd__(self,other):
        return self+other
        self.types=list(map(sum,zip(self,other)))
    def __isub__(self,other):
        self.types=list(map(lambda a:a[0]-a[1],zip(self,other)))
    def __imul__(self,other):
        self.types=[other*i for i in self.types]
    def __idiv__(self,other):
        self*=1/other
    def normalize(self):
        s=sum(self)
        if s!=0:
            print(s,self.types)
            self/=s
class Item:
    pass
