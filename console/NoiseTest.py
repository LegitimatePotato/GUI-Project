from opensimplex import OpenSimplex
import random,pygame
noise=OpenSimplex(random.randrange(1000))
pygame.init()
class Biome:
    def __init__(self,viable,colour,treeChance):
        self.viable=viable
        self.colour=colour
        self.treeChance=treeChance
biomes=(
    Biome(#Lake
        lambda t,m,e:e<0.1,
        "1",
        0
    ),Biome(#Lava Flow
        lambda t,m,e:t>0.575 and 0<(m+e*2)%0.3<0.05 and e>0.685,
        "C",
        0
    ),Biome(#Volcano
        lambda t,m,e:t>0.6 and e>0.7,
        "8",
        0
    ),Biome(#River
        lambda t,m,e:0.005>abs((9*t+2*m)/11-0.5),
        "9",
        0
    ),Biome(#Mountain
        lambda t,m,e:e>0.7,
        "7",
        0.0075
    ),Biome(#Desert
        lambda t,m,e:t>0.55 and m<0.3,
        "6",
        0
    ),Biome(#Tundra
        lambda t,m,e:t<0.3 and m<0.4,
        "B",
        0.0005
    ),Biome(#Arctic
        lambda t,m,e:t<0.2,
        "F",
        0.00025
    ),Biome(#Beach
        lambda t,m,e:t>0.5 and e<0.12,
        "E",
        0
    ),Biome(#Acid
        lambda t,m,e:t>0.7 and m>0.75,
        "A",
        0.04
    ),Biome(#Swamp
        lambda t,m,e:t>0.3 and m>0.65 and e<0.4,
        "3",
        0.03
    ),Biome(#Forest
        lambda t,m,e:t<0.75 and m>0.5 and e>0.2,
        "G",
        0.05
    ),Biome(#Grassland
        lambda t,m,e:True,
        "2",
        0.0025
    )
)
colours={
    "0":(  0,  0,  0),  #0,0,0
    "1":(  0,  0,128),  #240,100,50
    "2":(  0,128,  0),  #120,100,50
    "3":(  0,128,128),  #180,100,50
    "4":(128,  0,  0),  #0,100,50
    "5":(128,  0,128),  #300,100,50
    "6":(128,128,  0),  #60,100,50
    "7":(192,192,192),  #0,0,75
    "8":(128,128,128),  #0,0,50
    "9":(  0,  0,255),  #240,100,100
    "A":(  0,255,  0),  #120,100,100
    "B":(  0,255,255),  #180,100,100
    "C":(255,  0,  0),  #0,100,100
    "D":(255,  0,255),  #300,100,100
    "E":(255,255,  0),  #60,100,100
    "F":(255,255,255),  #0,0,100
    "G":(  0, 64,  0)
}
screenSize=840
biomeScale=30
temperatureScale=12
moistureScale=4
elevationScale=8
size=1
screen=pygame.display.set_mode((screenSize,screenSize))
def getNoise(x,y):
    x/=biomeScale
    y/=biomeScale
    return min(1,max(0,(noise.noise2d(x,y)+1)/2+noise.noise2d(x*3.5,y*3.5)/3.5))
for x in range(int(screenSize/size)):
    for y in range(int(screenSize/size)): #factors of s,y =size of blobs?     other is other?
        noiseX=x*size
        noiseY=y*size
        temperature=getNoise(noiseX/temperatureScale,noiseY/temperatureScale)
        moisture=getNoise(noiseX/moistureScale,noiseY/moistureScale)
        elevation=getNoise(noiseX/elevationScale,noiseY/elevationScale)**1.5
        for biome in biomes:
            if biome.viable(temperature,moisture,elevation):
                colour=colours[biome.colour]
                break
        pygame.draw.rect(screen,colour,(x*size,y*size,size,size))
        pygame.event.pump()
pygame.display.flip()
print("done")
