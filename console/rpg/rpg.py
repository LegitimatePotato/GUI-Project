from console.rpg.entity import *
from opensimplex import OpenSimplex
hudWidth=15
worldWidth=80-hudWidth
class Biome:
    def __init__(
            self,
            viable,
            colour,
            treeChance=0,
            maxTreeHeight=1
        ):
        self.viable=viable
        self.colour=colour
        self.treeChance=treeChance
        self.maxTreeHeight=maxTreeHeight
class RPG(ConsoleWindow):
    noise=OpenSimplex(random.randrange(10000))
    biomeScale=150
    temperatureScale=12
    moistureScale=4
    elevationScale=8
    b=(
        {#Lake
            "viable":lambda t,m,e:e<0.1,
            "colour":"1",
        },{#Lava Flow
            "viable":lambda t,m,e:t>0.575 and 0<(m+e*2)%0.3<0.05 and e>0.685,
            "colour":"C",
        },{#Volcano
            "viable":lambda t,m,e:t>0.6 and e>0.7,
            "colour":"8",
        },{#River
            "viable":lambda t,m,e:0.005>abs((9*t+2*m)/11-0.5),
            "colour":"9",
        },{#Mountain
            "viable":lambda t,m,e:e>0.7,
            "colour":"7",
            "treeChance":0.0075,
        },{#Desert
            "viable":lambda t,m,e:t>0.55 and m<0.3,
            "colour":"6",
        },{#Tundra
            "viable":lambda t,m,e:t<0.3 and m<0.4,
            "colour":"B",
            "treeChance":0.0005,
        },{#Arctic
            "viable":lambda t,m,e:t<0.2,
            "colour":"F",
            "treeChance":0.00025,
        },{#Beach
            "viable":lambda t,m,e:t>0.5 and e<0.12,
            "colour":"6",
        },{#Acid
            "viable":lambda t,m,e:t>0.7 and m>0.75,
            "colour":"A",
            "treeChance":0.04,
        },{#Swamp
            "viable":lambda t,m,e:t>0.3 and m>0.65 and e<0.4,
            "colour":"3",
            "treeChance":0.03,
            "maxTreeHeight":2,
        },{#Forest
            "viable":lambda t,m,e:t<0.75 and m>0.5 and e>0.2,
            "colour":"2",
            "treeChance":0.05,
            "maxTreeHeight":3,
        },{#Grassland
            "viable":lambda t,m,e:True,
            "colour":"2",
            "treeChance":0.0025,
        }
    )
    biomes=[]
    for biome in b:
        biomes.append(Biome(**biome))
    display=ConsoleSurf(80,25)
    background=CharMap(worldWidth,25)
    miniMapSurf=CharMap(14,7)
    temp=CharMap(worldWidth,25)
    entities=[]
    miniMapScale=16
    miniMap={}
    scrollX=0
    scrollY=0
    def __init__(self):
        self.player=Player(32,16)
        self.entities.append(self.player)
        super().__init__("")
        for x in range(worldWidth-1,-1,-1):
            for y in range(24,-1,-1):
                self.updatePixel(x,y)
    def updatePixel(self,x,y):
        realX=x-self.scrollX
        realY=y-self.scrollY
        noiseX=realX/self.biomeScale
        noiseY=realY/self.biomeScale
        temperature=self.getNoise(noiseX/self.temperatureScale,noiseY/self.temperatureScale)
        moisture=self.getNoise(noiseX/self.moistureScale,noiseY/self.moistureScale)
        elevation=self.getNoise(noiseX/self.elevationScale,noiseY/self.elevationScale)**1.5
        for biome in self.biomes:
            if biome.viable(temperature,moisture,elevation):
                colour=biome.colour
                break
        treeVal=moisture*10000+temperature
        treeVal=treeVal-int(treeVal)
        if biome.treeChance>treeVal:
            self.entities.append(Tree(realX,realY,random.randrange(1,biome.maxTreeHeight+1)))
        if realX%self.miniMapScale==0 and realY%self.miniMapScale==0:
            self.miniMap[int(realX/self.miniMapScale),int(realY/self.miniMapScale)]=colour
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
        if not(
                self.background[32+dx,12+dy]==self.biomes[0].colour or
                any((self.player.x+dx,self.player.y+dy)==(obj.x,obj.y)for obj in self.entities)
            ):
            self.player.x+=dx
            self.player.y+=dy
            self.scrollX-=dx
            self.scrollY-=dy
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
        if self.tick%15==0:
            for entity in self.entities:
                if entity.unload and(not 0<=entity.x+self.scrollX<worldWidth or not 0<=entity.y+self.scrollY<25):
                    self.entities.remove(entity)
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
        self.miniMapSurf.fill("0")
        xOff=self.scrollX//self.miniMapScale
        yOff=self.scrollY//self.miniMapScale
        for x,y in self.miniMap:
            realX=int(x+xOff+6)
            realY=int(y+yOff+3)
            if 0<=realX<=13 and 0<=y+yOff<=6:
                print(realX,realY)
                self.miniMapSurf[realX,realY]=self.miniMap[x,y]
        HUD.blit(createSurf(["HP: %s/%s"%(self.player.health,self.player.maxHealth)],("C","4")[self.player.health>self.player.maxHealth<0.5]),2,1)
        HUD.bgMap.blit(self.miniMapSurf,1,18)
        for entity in self.entities:
            entity.render(self.display,self.scrollX,self.scrollY)
        self.display.blit(HUD,worldWidth,0)
        self.renderSurf(self.display,0,0)
        pygame.display.flip()
