from console.console import *
class Entity:
    unload=True
    x=0
    y=0
    xOffset=0
    yOffset=0
    charMap=None
    fgMap=None
    def __init__(self,x,y):
        self.x=x
        self.y=y
    def render(self,display,scrollX,scrollY):
        relX=self.x+scrollX-self.xOffset
        relY=self.y+scrollY-self.yOffset
        display.charMap.blit(self.charMap,relX,relY)
        display.fgMap.blit(self.fgMap,relX,relY)
class Player(Entity):
    charMap=createMap("■")
    fgMap=createMap("E")
class Tree(Entity):
    def __init__(self,x,y,height):
        super().__init__(x,y)
        self.charMap=createMap(["▲"]+["║"]*height)
        self.fgMap=createMap(["A"]+["4"]*height)
        self.yOffset=height
