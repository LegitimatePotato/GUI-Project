from tkinter import *
from tkinter.ttk import *
import tkinter as tk
import os,threading,random,time,ctypes,math
try:
    import pygame
except ImportError:
    print("importing pygame broke")
else:
    pygame.font.init()
user32=ctypes.windll.user32
user32.SetProcessDPIAware()
import tkinter.scrolledtext
root=tk.Tk()
style=Style()
def thread(func):
    def wrapper(*args,**kwargs):
        threading.Thread(target=func,args=args,kwargs=kwargs).start()
    return wrapper
class Game:
    gameState=0
    storyProgression=2
game=Game()