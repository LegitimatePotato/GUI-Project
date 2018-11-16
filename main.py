from window import *
from console import *
class Test(Window):
    def __init__(self):
        super().__init__("(name)")
        self.frame=self.widget(Frame,1,1,relief=RAISED,borderwidth=2)
        self.frame.bind("<Button-1>",self.sink)
        self.top.bind("<ButtonRelease-1>",self.raise_)
        text=self.widget(Label,0,0,top=self.frame,padding={},text="m33m")
        text.bind("<Button-1>",self.sink)
        text.grid(row=0,column=0)
        button=self.widget(Button,1,2,text="m33m")
    def raise_(self,event):
        self.frame.config(relief=RAISED)
    def sink(self,event):
        self.frame.config(relief=SUNKEN)
class Evil(Window):
    def __init__(self):
        super().__init__("Why")
        w=20
        h=15
        _x=random.randrange(w)
        _y=random.randrange(h)
        for x in range(w):
            for y in range(h):
                if x==_x and y==_y:
                    button=self.widget(Button,x,y,text=" It's this one ",command=root.destroy)
                else:
                    button=self.widget(Button,x,y,text="Not this one")
class MainMenu(Window):
    def __init__(self):
        super().__init__("Game")
        playButton=self.widget(Button,2,2,text="Play Game")
        optionsButton=self.widget(Button,2,3,text="Options",command=OptionsWindow)
        creditsButton=self.widget(Button,2,4,text="Credits",command=CreditsWindow)
class OptionsWindow(Window):
    def __init__(self):
        super().__init__("Options")
        graphicsLabel=self.widget(Label,1,1,text="Graphics Quality")
        graphicsBox=self.widget(Combobox,2,1,height=3,width=22,state="readonly",values=("Bad","Trash","Garbage","Crap","Like Seriously","Really","Really ","Awful","Why","Are","You","Still","Reading","These","Why ","Are ","You ","Even","Playing","This","Game"))
        soundLabel=self.widget(Label,1,2,text="Sound Quality")
        soundBox=self.widget(Combobox,2,2,height=1,width=22,state="readonly",values=("It's a freaking GUI game.",))
        doneButton=self.widget(Button,3,3,text="Done",command=self.top.destroy)
class CreditsWindow(Window):
    def __init__(self):
        super().__init__("Credits")
        me=self.widget(Label,1,1,text="Me")
class TreePassword(Window):
    alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    def __init__(self,password):
        super().__init__("The Tree of Knowledge")
        self.password=password.upper()
        self.tree=self.widget(Treeview,0,0,selectmode=NONE,height=26)
        self.tree.bind("<<TreeviewOpen>>",self.addAlphabet)
        self.tree.insert("",END,"_")
        self.addAlphabet("")
    def addAlphabet(self,parent):
        if type(parent)!=str:
            parent=self.tree.focus()
        if parent==self.password:
            self.top.destroy()
            return
        if self.tree.exists(parent+"A"):
            return
        self.tree.delete(parent+"_")
        l=list(self.alphabet)
        for letter in l:
            self.tree.insert(parent,END,parent+letter,text=letter)
            self.tree.insert(parent+letter,END,parent+letter+"_",text="_")
class Transfigurator(Window):
    def __init__(self):
        super().__init__("Transfigurator")
        self.text1=self.widget(Text,0,0)
        self.text2=self.widget(Text,2,0)
        self.run()
    def update(self):
        self.text2.delete(1.0,END)
        self.text2.insert(END,self.text1.get(1.0,END)[-2::-1])
class Colour(Window):
    def __init__(self):
        super().__init__("Colour")
        self.colourBox=self.widget(Label,0,0,padding=self.addPadding({"columnspan":3}),width=10,height=3,bg=self.convert(0,0,0))
        self.slider1=self.widget(Scale,0,1,command=self.updateColour,from_=1,to=0,resolution=0.05,showvalue=False)
        self.slider2=self.widget(Scale,1,1,command=self.updateColour,from_=1,to=0,resolution=0.05,showvalue=False)
        self.slider3=self.widget(Scale,2,1,command=self.updateColour,from_=1,to=0,resolution=0.05,showvalue=False)
    @staticmethod
    def convert(r,g,b):
        return"#%02x%02x%02x"%tuple(map(lambda x:int(x%1.01*255),(1-r,b**2,(1-(1-g)**2))))
    def updateColour(self,*args):
        self.colourBox.config(bg=self.convert(
            self.slider1.get(),
            self.slider2.get(),
            self.slider3.get()
        ))
class Memory(Window):
    colours=tuple(map(Window.convert,(
        (255,  0,  0),
        (255,128,  0),
        (255,255,  0),
        (  0,255,  0),
        (  0,255,255),
        (  0,  0,255),
        (128,  0,255),
        (255,  0,255)
    )))
    gettingResponse=False
    indexes=[]
    entered=[]
    updateTimer=0.25
    def __init__(self):
        super().__init__("Memory")
        self.background=self.convert((240,240,240))
        self.colourBox=self.widget(tk.Label,0,0,padding={"columnspan":4},width=10,height=3,bg=self.background,relief=FLAT)
        args=self.blank(25,25)
        self.buttons=[]
        for c,colour in enumerate(self.colours):
            self.buttons.append(self.widget(tk.Button,c%4,c//4+1,command=self.addColour(c),bg=colour,activebackground=colour,**args))
        self.run()
    def addColour(self,c):
        def addInternal():
            self.entered.append(c)
        return addInternal
    def update(self):
        if self.gettingResponse:
            if self.entered[-6:]==self.indexes:
                self.gettingResponse=False
                self.indexes=[]
        else:
            self.indexes.append(random.randrange(8))
            self.colourBox.config(bg=self.colours[self.indexes[-1]])
            time.sleep(1.5)
            self.colourBox.config(bg=self.background)
            if len(self.indexes)==6:
                self.gettingResponse=True
                self.entered=[]
class Piano(Window):
    pass
class Storybook(Window):
    pages=[
        """
            Somebody once
        """,
        """
            told me the world was gonna roll me.
        """,
        """
            I ain't the sharpest tool in the shed.
        """,
        """
            She was lookin' kinda dumb with her finger
        """,
        """
            and her thumb
        """,
        """
            in the shape of an L
        """,
        """
            on her forehead.
        """
    ]
    def __init__(self):
        super().__init__()
        self.notebook=self.widget(Notebook,0,0)
        self.frames=[Frame(self.notebook)for n in range(self.game.storyProgression)]
        for n in range(self.game.storyProgression):
            self.notebook.add(self.frames[n])
            self.widget(Label,0,0,top=self.frames[n],text=self.pages[n])
x=ConsoleWindow()
root.withdraw()
mainloop()