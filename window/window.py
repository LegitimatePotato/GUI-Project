from definitions import *
class Window:
    game=game
    padding={
        "padx":8,
        "pady":12
    }
    alive=True
    px=PhotoImage(width=1,height=1)
    ups=20
    tick=0
    clock=pygame.time.Clock()
    def __init__(self,title="",resizable=(False,False)):
        self.top=tk.Toplevel(root)
        self.top.protocol("WM_DELETE_WINDOW",self.close)
        self.top.title(title)
        self.top.resizable(*resizable)
        self.widgets=[]
    @staticmethod
    def convert(*args):
        try:
            return"#%02x%02x%02x"%args
        except TypeError:
            return"#%02x%02x%02x"%args[0]
    def addPadding(self,*args,**kwargs):
        return{**self.padding,**kwargs,**args[0]}
    def blank(self,width,height):
        return{"image":self.px,"width":width,"height":height}
    def widget(self,cls,x,y,padding=None,top=None,**kwargs):
        if padding is None:
            padding=self.padding
        if top is None:
            top=self.top
        widget=cls(top,**kwargs)
        widget.grid(column=x,row=y,**padding)
        self.widgets.append(widget)
        return widget
    def close(self):
        self.alive=False
        self.top.destroy()
    def handleInput(self,event):
        pass
    @thread
    def run(self):
        try:
            self.update
        except AttributeError:
            pass
        else:
            while self.alive:
                self.tick+=1
                self.update()
                self.clock.tick(self.ups)