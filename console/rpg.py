from console.console import *
from opensimplex import OpenSimplex
hudWidth=15
worldWidth=80-hudWidth
class Biome:
    def __init__(self,viable,colour,treeChance):
        self.viable=viable
        self.colour=colour
        self.treeChance=treeChance
class Entity:
    x=0
    y=0
    charMap=None
    fgMap=None
    def __init__(self,x,y):
        self.x=x
        self.y=y
    def render(self,display,playerX,playerY):
        relX=self.x-playerX
        relY=self.y-playerY
        display.charMap.blit(self.charMap,relX,relY)
        display.fgMap.blit(self.fgMap,relX,relY)
class Tree(Entity):
    charMap=createMap(["▲","║"])
    fgMap=createMap(["A","4"])
class RPG(ConsoleWindow):
    playerHealth=80
    playerMaxHealth=80
    playerX=0
    playerY=0
    noise=OpenSimplex(random.randrange(10000))
    biomeScale=150
    temperatureScale=12
    moistureScale=4
    elevationScale=9
    biomes=(
        Biome(#Lake
            lambda t,m,e:e<0.1,
            "1",
            0
        ),Biome(#River
            lambda t,m,e:0.005>abs((9*t+2*m)/11-0.5),
            "9",
            0
        ),Biome(#Mountain
            lambda t,m,e:e>0.8,
            "8",
            0.0075
        ),Biome(#Desert
            lambda t,m,e:m<0.3 and t>0.55,
            "6",
            0
        ),Biome(#Tundra
            lambda t,m,e:m<0.35 and t<0.3,
            "B",
            0.001
        ),Biome(#Arctic
            lambda t,m,e:t<0.2,
            "F",
            0.0005
        ),Biome(#Rainforest
            lambda t,m,e:m>0.75 and t>0.6,
            "A",
            0.04
        ),Biome(#Swamp
            lambda t,m,e:m>0.6 and t>0.3>e,
            "3",
            0.03
        ),Biome(#Forest
            lambda t,m,e:m>0.5 and t<0.75 and e>0.2,
            "2",
            0.05
        ),Biome(#Grassland
            lambda t,m,e:True,
            "2",
            0.005
        )
    )
    display=ConsoleSurf(80,25)
    background=CharMap(worldWidth,25)
    miniMap=ConsoleSurf(14,7)
    temp=CharMap(worldWidth,25)
    entities=[]
    def __init__(self):
        for x in range(worldWidth):
            for y in range(25):
                self.updatePixel(x,y)
        super().__init__("")
    def updatePixel(self,x,y):
        noiseX=(self.playerX+x)/self.biomeScale
        noiseY=(self.playerY+y)/self.biomeScale
        temperature=self.getNoise(noiseX/self.temperatureScale,noiseY/self.temperatureScale)
        moisture=self.getNoise(noiseX/self.moistureScale,noiseY/self.moistureScale)
        elevation=self.getNoise(noiseX/self.elevationScale,noiseY/self.elevationScale)**1.5
        for biome in self.biomes:
            if biome.viable(temperature,moisture,elevation):
                colour=biome.colour
                break
        treeVal=moisture*10000
        treeVal=treeVal-int(treeVal)
        if biome.treeChance>treeVal:
            self.entities.append(Tree(x+self.playerX,y+self.playerY-1))
        self.background[x,y]=colour
    def getNoise(self,x,y):
        return min(1,max(0,(self.noise.noise2d(x,y)+1)/2+self.noise.noise2d(x*3.5,y*3.5)/3.5))
    def handleInput(self,event):
        pass
    def update(self):
        super().update()
        keys=pygame.key.get_pressed()
        dx=0
        dy=0
        if self.tick%3==0:
            if keys[pygame.K_UP]:
                dy=-1
            elif keys[pygame.K_DOWN]:
                dy=1
        if self.tick%2==0:
            if keys[pygame.K_LEFT]:
                dx=-1
            elif keys[pygame.K_RIGHT]:
                dx+=1
        self.playerX+=dx
        self.playerY+=dy
        self.temp.blit(self.background,0,0)
        self.background.fill("0")
        self.background.blit(self.temp,-dx,-dy)
        if dx:
            _x=(worldWidth-1)*(dx>0)
            for y in range(25):
                self.updatePixel(_x,y)
        if dy:
            _y=24*(dy>0)
            for x in range(worldWidth):
                self.updatePixel(x,_y)
        HUD=createSurf([
            "│",
            "│",
            "│",
            "│",
            "│",
            "│",
            "│",
            "│",
            "│",
            "│",
            "│",
            "│",
            "│",
            "│",
            "│",
            "│",
            "│",
            "├──────────────",
            "│",
            "│",
            "│",
            "│",
            "│",
            "│",
            "│",
        ])
        self.display.charMap.fill(" ")
        self.display.fgMap.fill("7")
        self.display.bgMap.fill("0")
        self.display.bgMap.blit(self.background,0,0)
        self.miniMap.bgMap.fill("0")
        HUD.blit(createSurf(["HP: %s/%s"%(self.playerHealth,self.playerMaxHealth)],("C","4")[self.playerHealth>self.playerMaxHealth<0.5]),2,1)
        HUD.blit(self.miniMap,1,18)
        for entity in self.entities:
            entity.render(self.display,self.playerX,self.playerY)
        self.display.blit(HUD,worldWidth,0)
        self.display.charMap[worldWidth//2,12]="■"
        self.display.fgMap[worldWidth//2,12]="E"
        self.renderSurf(self.display,0,0)
        pygame.display.flip()
