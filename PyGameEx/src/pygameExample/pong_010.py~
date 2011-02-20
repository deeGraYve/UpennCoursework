# adapted from Arinoid
# http://www.scriptedfun.com/
import pygame
from pygame.locals import *   
from copy import copy
import math

class simpleGame:
    GAME_WIDTH=500
    GAME_HEIGHT=400

    def __init__(self):
        pygame.init()
        pygame.display.set_mode((simpleGame.GAME_WIDTH, simpleGame.GAME_HEIGHT))
        self.screen=pygame.display.get_surface()
        pygame.display.set_caption("Pygame example ball game")
        bgTile=pygame.image.load("background.jpg")
        bgTile.convert()    
        self.screen.blit(bgTile, (0,0))
        pygame.display.update()

    def eventLoop(self):
        while 1:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return
            pygame.display.update()

if __name__ == '__main__':
    myGame=simpleGame()
    myGame.eventLoop()
