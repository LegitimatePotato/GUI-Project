from console.console import *
from opensimplex import OpenSimplex
hudWidth=15
worldWidth=80-hudWidth
class RPG(ConsoleWindow):
    playerHealth=80
    playerMaxHealth=80
    playerX=20
    playerY=3
    map={}
    noise=OpenSimplex(random.randrange(10000))
    biomeScale=150
    temperatureScale=12
    moistureScale=4
    elevationScale=9
    biomes={
        "desert":"6",
        "mountain":"8",
        "grassland":"2",
        "swamp":"3",
        "corrupt":"4",
        "arctic":"F",
        "lake":"1",
        "rainforest":"A",
        "tundra":"B",
        "forest":"2",
        "river":"9",
    }
    display=ConsoleSurf(80,25)
    background=CharMap(65,25)
    miniMap=ConsoleSurf(14,7)
    def __init__(self):
        for x in range(65):
            for y in range(25):
                self.updatePixel(x,y)
        super().__init__("")
    def updatePixel(self,x,y):
        noiseX=(self.playerX+x)/self.biomeScale
        noiseY=(self.playerY+y)/self.biomeScale
        temperature=self.getNoise(noiseX/self.temperatureScale,noiseY/self.temperatureScale)
        moisture=self.getNoise(noiseX/self.moistureScale,noiseY/self.moistureScale)
        elevation=self.getNoise(noiseX/self.elevationScale,noiseY/self.elevationScale)**1.5
        if elevation<0.1:
            biome="lake"
        elif 0.005>abs((9*temperature+2*moisture)/11-0.5):
            biome="river"
        elif elevation>0.8:
            biome="mountain"
        elif moisture<0.3 and temperature>0.55:
            biome="desert"
        elif moisture<0.35 and temperature<0.3:
            biome="tundra"
        elif temperature<0.2:
            biome="arctic"
        elif moisture>0.75 and temperature>0.6:
            biome="rainforest"
        elif moisture>0.6 and temperature>0.3 and elevation<0.3:
            biome="swamp"
        elif moisture>0.5 and temperature<0.75 and elevation>0.2:
            biome="forest"
        else:
            biome="grassland"
        self.background[_x,_y]=self.biomes[biome]
    def getNoise(self,x,y):
        return min(1,max(0,(self.noise.noise2d(x,y)+1)/2+self.noise.noise2d(x*3.5,y*3.5)/3.5))
    def handleInput(self,event):
        pass
    def update(self):
        super().update()
        keys=pygame.key.get_pressed()
        if self.tick%3==0:
            if keys[pygame.K_UP]:
                self.playerY-=1
            elif keys[pygame.K_DOWN]:
                self.playerY+=1
        if self.tick%2==0:
            if keys[pygame.K_LEFT]:
                self.playerX-=1
            elif keys[pygame.K_RIGHT]:
                self.playerX+=1
        actualX=self.playerX//13
        actualY=self.playerY//5
        if actualX!=self.activeChunk.x or actualY!=self.activeChunk.y:
            for x in range(-7,7):
                for y in range(-4,4):
                    self.loadChunk(actualX+x,actualY+y)
            self.activeChunk=self.map[actualX,actualY]
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
        self.display.bgMap.fill("0")
        self.display.bgMap.blit(self.background,0,0)
        self.miniMap.fill("0")
        HUD.blit(createSurf(["HP: %s/%s"%(self.playerHealth,self.playerMaxHealth)],("C","4")[self.playerHealth>self.playerMaxHealth<0.5]),2,1)
        HUD.blit(miniMap,1,18)
        self.display.blit(HUD,worldWidth,0)
        self.display.charMap[worldWidth//2,12]="■"
        self.display.fgMap[worldWidth//2,12]="E"
        self.renderSurf(self.display,0,0)
        pygame.display.flip()