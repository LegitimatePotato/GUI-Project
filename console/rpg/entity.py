from console.console import *
class Entity:
    x=0
    y=0
    xOffset=0
    yOffset=0
    charMap=None
    fgMap=None
    unload=True
    collision=True
    def __init__(self,game,x,y):
        self.game=game
        self.x=x
        self.y=y
    def render(self,display,scrollX,scrollY):
        relX=self.x+scrollX-self.xOffset
        relY=self.y+scrollY-self.yOffset
        display.charMap.blit(self.charMap,relX,relY)
        display.fgMap.blit(self.fgMap,relX,relY)
    def move(self,dx,dy):
        if not any(obj.collision and obj is not self and(self.x+dx,self.y+dy)==(obj.x,obj.y)for obj in self.game.entities):
            self.x+=dx
            self.y+=dy
            return True
class Player(Entity):
    unload=False
    health=80
    maxHealth=80
    charMap=createMap("■")
    fgMap=createMap("E")
class Tree(Entity):
    def __init__(self,game,x,y,height):
        super().__init__(game,x,y)
        self.charMap=createMap(["▲"]+["│"]*height)
        self.fgMap=createMap(["A"]+["4"]*height)
        self.yOffset=height
