from console import *
import pprint
class Editor(ConsoleWindow):
    ups=60
    activeChar=StringVar()
    activeFG=StringVar()
    activeBG=StringVar()
    activeChar.set(" ")
    activeFG.set(" ")
    activeBG.set(" ")
    display=ConsoleSurf(80,25)
    def __init__(self):
        super().__init__()
        self.sidebar=self.widget(Frame,2,0)
        self.chars=self.widget(Frame,0,0,top=self.sidebar)
        settings={
            "padding":{},
            "indicatoron":0,
            "width":2,
            "borderwidth":1
        }
        for x in range(16):
            for y in range(16):
                char=self.codePage[x+16*y]
                self.widget(tk.Radiobutton,x,y,top=self.chars,text=char,variable=self.activeChar,value=char,**settings)
        self.fgs=self.widget(Frame,0,1,top=self.sidebar)
        self.bgs=self.widget(Frame,0,2,top=self.sidebar)
        self.widget(tk.Radiobutton,0,0,top=self.fgs,text="-",variable=self.activeFG,value=" ",**settings)
        self.widget(tk.Radiobutton,0,0,top=self.bgs,text="-",variable=self.activeBG,value=" ",**settings)
        for c in range(17):
            colour=list(self.colours.keys())[c]
            if colour!="":
                tkColour="#%02x%02x%02x"%self.colours[colour]
                self.widget(tk.Radiobutton,c+1,0,top=self.fgs,text=colour,variable=self.activeFG,value=colour,bg=tkColour,**settings)
                self.widget(tk.Radiobutton,c+1,0,top=self.bgs,text=colour,variable=self.activeBG,value=colour,bg=tkColour,**settings)
        maxDist=math.hypot(24,79)
        ratios=(
            (" ",0),
            ("░",1/3),
            ("▒",1/2),
            ("▓",2/3),
        )
        colours=(
            ("0",0),
            ("8",.5),
            ("7",.75),
            ("F",1),
        )
        values=[]
        gradient=[]
        for fg,fgr in colours:
            for bg,bgr in colours:
                for char,ratio in ratios:
                    value=ratio*fgr+(1-ratio)*bgr
                    for v in values:
                        if abs(value-v)<0.01:
                            break
                    else:
                        values.append(value)
                        gradient.append((value,char,fg,bg))
        gradient.sort(key=lambda x:x[0])
        pprint.pprint(gradient)
        for x in range(80):
            for y in range(25):
                value=math.hypot(x,y)/maxDist
                for grad in range(len(gradient)):
                    if value<gradient[grad][0]:
                        self.display[x,y]=gradient[grad-1][1:]
                        break
                else:
                    self.display[x,y]=gradient[-1][1:]
    def changeChar(self,char):
        def inner():
            self.activeChar=char
        return inner
    def update(self):
        super().update()
        pressed=pygame.mouse.get_pressed()
        x,y=pygame.mouse.get_pos()
        x//=8
        y//=12
        if pressed[0]:
            char=self.activeChar.get()
            fg=self.activeFG.get()
            bg=self.activeBG.get()
            if char!=" ":
                self.display.charMap[x,y]=char
            if not(fg.isspace()):
                self.display.fgMap[x,y]=fg
            if not(bg.isspace()):
                self.display.bgMap[x,y]=bg
        elif pressed[2]:
            self.display[x,y]=(" ","7","0")
        self.renderSurf(self.display,0,0)
        pygame.display.flip()
