from console.console import *
class CommandPrompt(ConsoleWindow):
    text=[
        "Microsoft Windows [Version 10.0.16299.726]",
        "(c) 2017 Microsoft Corporation. All rights reserved.",
        "",
        "F:\\>",
    ]
    def __init__(self):
        super().__init__("Command Prompt")
    def handleInput(self,event):
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_RETURN:
                self.text.append("")
            elif event.key==pygame.K_BACKSPACE:
                if len(self.text[-1])>0:
                    self.text[-1]=self.text[-1][:-1]
                else:
                    self.text=self.text[:-1]
                    if self.text==[]:
                        self.text=[""]
            else:
                if len(self.text[-1])==80:
                    self.text.append("")
                else:
                    self.text[-1]+=event.unicode
            if not 0<=len(self.text)-self.scroll<=24:
                self.updateScroll("moveto",max(0,len(self.text)-25)/self.numLines)
    def update(self):
        super().update()
        l=len(self.text)-1
        u=pygame.time.get_ticks()%900>=450
        if u:
            self.text[l]+="▬"
        self.renderSurf(createSurf(self.text),0,0)
        if u:
            self.text[l]=self.text[l][:-1]
        pygame.display.flip()