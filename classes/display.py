import pygame
from pygame.locals import *


class Display:
    def __init__(self):
        
        #Configure display
        self.black = (0,0,0)
        self.white = (255,255,255)
        self.green = (0, 255, 0)
        self.red = (255, 0 ,0)
        self.display = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.display.fill(self.black)
        #pygame.display.update()

    def show_img(self, img, approved):
        if approved:
            self.display.fill(self.green)
            print("Good")
        else:
            self.display.fill(self.red)
            print("Bad")
       
        self.display.blit(img, (0,0))
        pygame.display.update()

    def off(self):
        self.display.fill(self.black)