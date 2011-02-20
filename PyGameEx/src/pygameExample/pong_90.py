# adapted from Arinoid
# http://www.scriptedfun.com/
import pygame
from pygame.locals import *   
from copy import copy
import math

class Ball:
    def __init__(self, filename, background, screen, paddle):
        self.image=pygame.image.load(filename)
        self.image.set_colorkey(self.image.get_at((0,0)), RLEACCEL)
        self.image.convert()
        self.rect=self.image.get_rect()
        self.screenRect=screen.get_rect()
        self.rect.centerx=self.screenRect.centerx
        self.rect.centery=self.screenRect.centery
        self.background=background
        self.screen=screen
    
        self.speed=3.0
        self.angle=math.pi/4.0
        # we keep a floating point true position and and integer approximation
        self.fx=float(self.rect.centerx)
        self.fy=float(self.rect.centery)
        self.paddle=paddle
        
    def update(self):
        dirtyRects=[copy(self.rect)]
        # move the ball
        self.fx+=self.speed*math.cos(self.angle)
        self.fy+=self.speed*math.sin(self.angle)
        
        self.rect.centerx=int(self.fx)
        self.rect.centery=int(self.fy)

        # check for collisions with screen edge
        if self.rect.right>self.screenRect.right:
            self.rect.right=self.screenRect.right
            self.fx=float(self.rect.centerx)
            self.angle=-(self.angle+math.pi)
        elif self.rect.left<self.screenRect.left:
            self.rect.left=self.screenRect.left
            self.fx=float(self.rect.centerx)
            self.angle=-(self.angle+math.pi)            
        elif self.rect.top<self.screenRect.top:
            self.rect.top=self.screenRect.top
            self.fy=float(self.rect.centery)
            self.angle=-self.angle
        elif self.rect.bottom>self.screenRect.bottom:
            self.rect.bottom=self.screenRect.bottom
            self.fy=float(self.rect.centery)
            self.angle=-self.angle

        return dirtyRects

    def draw(self):
        self.screen.blit(self.image, self.rect.topleft)

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
        self.ball=Ball("ball.png", self.bgSurface, self.screen, self.paddle)
        pygame.display.update()
        self.clock = pygame.time.Clock()
        self.score=0

    def updateBackground(self, dirtyRects):
        for rect in dirtyRects:
            self.screen.blit(self.bgSurface, rect, rect)

    def eventLoop(self):
        while 1:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key==K_ESCAPE):
                    return
            dirtyRects=[]
            dirtyRects.extend(self.ball.update())
            self.updateBackground(dirtyRects)
            self.ball.draw()
            pygame.display.update()

            self.clock.tick(60)
            self.score+=1

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
