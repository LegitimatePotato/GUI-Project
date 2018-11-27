from window.window import *
class CharMap:
    def __init__(self,width,height,map=None):
        self.width=width
        self.height=height
        if map is None:
            self.map=[[""for n in range(height)]for n in range(width)]
        else:
            self.map=map
    def __getitem__(self,key):
        return self.map[key[0]][key[1]]
    def __setitem__(self,key,value):
        x,y=key
        if type(value)==str:
            self.map[x][y]=value
        else:
            for _x in range(len(value)):
                if x+_x>=self.width:
                    return
                self.map[x+_x][y]=value[_x]
    def blit(self,other,x,y):
        for _x in range(other.width):
            for _y in range(other.height):
                try:
                    posX=x+_x
                    posY=y+_y
                    if posX<0 or posY<0:
                        continue
                    self[posX,posY]=other[_x,_y]
                except IndexError:
                    if posY>=self.height:
                        break
                    else:
                        return
    def fill(self,char):
        self.map=[[char for n in range(self.height)]for n in range(self.width)]
def createMap(chars):
    if type(chars)==str:
        map=[[char]for char in chars]
    elif type(chars)==list:
        if type(chars[0])==str:
            w=max(len(char)for char in chars)
            h=len(chars)
            map=[[""for y in range(h)]for x in range(w)]
            for y in range(h):
                for x in range(w):
                    try:
                        map[x][y]=chars[y][x]
                    except IndexError:
                        break
        else:
            map=chars
    return CharMap(len(map),len(map[0]),map)
class ConsoleSurf:
    charMap:CharMap
    fgMap:CharMap
    bgMap:CharMap
    def __init__(self,width,height):
        self.width=width
        self.height=height
        self.charMap=CharMap(width,height)
        self.fgMap=CharMap(width,height)
        self.bgMap=CharMap(width,height)
        self.charMap.fill(" ")
        self.fgMap.fill("7")
        self.bgMap.fill("0")
    def __getitem__(self,key):
        return(self.charMap[key],self.fgMap[key],self.bgMap[key])
    def __setitem__(self,key,values):
        if len(values)==1:
            self.charMap[key]=values
        else:
            self.charMap[key],self.fgMap[key],self.bgMap[key]=values
    def blit(self,other,x,y):
        self.charMap.blit(other.charMap,x,y)
        self.fgMap.blit(other.fgMap,x,y)
        self.bgMap.blit(other.bgMap,x,y)
def createSurf(text,fg="7",bg="0"):
    w=max(len(t)for t in text)
    h=len(text)
    surf=ConsoleSurf(w,h)
    if str in(type(fg),type(bg)):
        for y in range(h):
            for x in range(w):
                try:
                    surf.charMap[x,y]=text[y][x]
                    if type(fg)==str:
                        surf.fgMap[x,y]=fg
                    if type(bg)==str:
                        surf.bgMap[x,y]=bg
                except IndexError:
                    break
    if type(fg)==CharMap:
        surf.fgMap==fg
    if type(bg)==CharMap:
        surf.bgMap==bg
    return surf
class ConsoleWindow(Window):
    ups=30
    scroll=0
    windowOpen=True
    padding={"padx":0,"pady":0}
    numLines=200
    writable=True
    try:
        font=pygame.font.Font("Font.ttf",12)
    except:
        print("failed to load font")
    colours={
        "" :(  0,  0,  0),
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
    }
    codePage=\
        """ ☺☻♥♦♣♠•◘○◙♂♀♪♫☼"""\
        """►◄↕‼¶§▬↨↑↓→←∟↔▲▼"""\
        """ !"#$%&'()*+,-./"""\
        """0123456789:;<=>?"""\
        """@ABCDEFGHIJKLMNO"""\
        """PQRSTUVWXYZ[\]^_"""\
        """`abcdefghijklmno"""\
        """pqrstuvwxyz{|}~⌂"""\
        """ÇüéâäàåçêëèïîìÄÅ"""\
        """ÉæÆôöòûùÿÖÜ¢£¥₧ƒ"""\
        """áíóúñÑªº¿⌐¬½¼¡«»"""\
        """░▒▓│┤╡╢╖╕╣║╗╝╜╛┐"""\
        """└┴┬├─┼╞╟╚╔╩╦╠═╬╧"""\
        """╨╤╥╙╘╒╓╫╪┘┌█▄▌▐▀"""\
        """αßΓπΣσµτΦΘΩδ∞φε∩"""\
        """≡±≥≤⌠⌡÷≈°∙·√ⁿ²■ """
    chars={
    }
    def __init__(self,title=""):
        self.top=root
        super().__init__(title)
        console=self.widget(tk.Frame,0,0,width=640,height=300)
        os.environ["SDL_WINDOWID"]=str(console.winfo_id())
        os.environ["SDL_VIDEODRIVER"]="windib"
        pygame.init()
        pygame.key.set_repeat(250,20)
        thickarrow_strings=(
            "X                       ",
            "XX                      ",
            "X.X                     ",
            "X..X                    ",
            "X...X                   ",
            "X....X                  ",
            "X.....X                 ",
            "X......X                ",
            "X.......X               ",
            "X........X              ",
            "X.........X             ",
            "X..........X            ",
            "X......XXXXXX           ",
            "X...X..X                ",
            "X..X X..X               ",
            "X.X  X..X               ",
            "XX    X..X              ",
            "      X..X              ",
            "       XX               ",
            "                        ",
            "                        ",
            "                        ",
            "                        ",
            "                        "
        )
        datatuple,masktuple=pygame.cursors.compile(thickarrow_strings,black='X',white='.',xor='o')
        pygame.mouse.set_cursor((24,24),(0,0),datatuple,masktuple)
        self.screen=pygame.display.set_mode((640,300))
        pygame.display.flip()
        self.scrollbarOffset=24/self.numLines
        self.scrollbar=self.widget(Scrollbar,1,0,padding={"padx":0,"pady":0,"sticky":"ns"},command=self.updateScroll)
        self.scrollbar.set(0,self.scrollbarOffset)
        self.top.iconbitmap(r"icon.ico")
        self.run()
    def updateScroll(self,moveType,pos,*args):
        if moveType=="moveto":
            pos=max(min(float(pos),(self.numLines-24)/self.numLines),0)
            self.scroll=int(pos*self.numLines)
            self.scrollbar.set(pos,pos+self.scrollbarOffset)
        elif moveType=="scroll":
            step=float(pos)/self.numLines
            newPos=self.scrollbar.get()[0]+step
            if newPos<0:
                self.scrollbar.set(0,self.scrollbarOffset)
                self.scroll=0
            elif newPos>1-self.scrollbarOffset:
                self.scrollbar.set(1-self.scrollbarOffset,1)
                self.scroll=self.numLines-24
            else:
                self.scrollbar.set(newPos,newPos+self.scrollbarOffset)
                self.scroll+=step*self.numLines
    def renderSurf(self,surf,x,y):
        for line in range(surf.height):
            dispY=y+line-self.scroll
            if dispY<0 or dispY>24:
                continue
            current=""
            startX=x
            fg=surf.fgMap[0,line]
            bg=surf.bgMap[0,line]
            for c in range(surf.width):
                dispX=x+c
                char,newFg,newBg=surf[c,line]
                if newFg!=fg or newBg!=bg or dispX>=79 or c==surf.width-1:
                    if dispX>=79 or c==surf.width-1:
                        current+=char
                    text=self.font.render(current,0,self.colours[fg],self.colours[bg])
                    self.screen.blit(text,(8*startX,12*dispY))
                    if dispX>=80:
                        break
                    fg=newFg
                    bg=newBg
                    current=""
                    startX=dispX
                if not(dispX>=79 or c==surf.width-1):
                    current+=char
    def update(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                self.close()
            else:
                self.handleInput(event)
        self.screen.fill((0,0,0))
