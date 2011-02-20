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
        self.bgSurface=self.drawBackground(bgTile)
        self.screen.blit(self.bgSurface, (0,0))
        pygame.display.update()

    def eventLoop(self):
        while 1:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return
            pygame.display.update()

    def drawBackground(self, bgTile):
        bgTileRect=bgTile.get_rect()
        tileWidth=bgTileRect.width
        tileHeight=bgTileRect.height

        background=pygame.Surface((simpleGame.GAME_WIDTH, simpleGame.GAME_HEIGHT))

        x=0
        while (x<simpleGame.GAME_WIDTH):
            y=0
            while (y<simpleGame.GAME_HEIGHT):
                background.blit(bgTile, (x,y))
                y+=tileHeight
            x+=tileWidth
        return background

if __name__ == '__main__':
    myGame=simpleGame()
    myGame.eventLoop()
