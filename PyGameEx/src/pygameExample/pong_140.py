# adapted from Arinoid
# http://www.scriptedfun.com/
import pygame
from pygame.locals import *   
from copy import copy
import math

class Paddle:
    def __init__(self, filename, background, screen):
        self.image=pygame.image.load(filename)
        self.image.set_colorkey(self.image.get_at((0,0)), RLEACCEL)
        self.image.convert()
        self.rect=self.image.get_rect()
        self.rect.centerx=screen.get_rect().centerx
        self.rect.bottom=screen.get_rect().bottom-10
        self.background=background
        self.screen=screen

    # make the paddle track the mouse
    def update(self):
        dirtyRect=copy(self.rect)
        self.rect.centerx=pygame.mouse.get_pos()[0]
        return [dirtyRect]

    # draw the paddle
    def draw(self):
        self.screen.blit(self.image, self.rect.topleft)
        return [copy(self.rect)]

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
        
        self.bounces=0

        self.bounceCountSurf=None

        #self.scoreFont=pygame.font.Font("/usr/local/share/pygame/freesansbold.ttf", 30)

    def update(self):
        dirtyRects=[copy(self.rect)]
        # move the ball
        self.fx+=self.speed*math.cos(self.angle)
        self.fy+=self.speed*math.sin(self.angle)
        
        self.rect.centerx=int(self.fx)
        self.rect.centery=int(self.fy)

        bounced=False

        # check for collisions with screen edge
        if self.rect.right>self.screenRect.right:
            self.rect.right=self.screenRect.right
            self.fx=float(self.rect.centerx)
            self.angle=-(self.angle+math.pi)
            bounced=True
        elif self.rect.left<self.screenRect.left:
            self.rect.left=self.screenRect.left
            self.fx=float(self.rect.centerx)
            self.angle=-(self.angle+math.pi)            
            bounced=True
        elif self.rect.top<self.screenRect.top:
            self.rect.top=self.screenRect.top
            self.fy=float(self.rect.centery)
            self.angle=-self.angle
            bounced=True
        elif self.rect.bottom>self.screenRect.bottom:
            self.rect.bottom=self.screenRect.bottom
            self.fy=float(self.rect.centery)
            self.angle=-self.angle
            bounced=True

        # check for collisions with paddle
        # to keep things simple, we assume wrongly that 
        # the ball always hits the top of the paddle
        # this will make the ball "teleport" if it hits the sides!
        if self.rect.colliderect(self.paddle.rect) and (self.paddle.rect.top<self.rect.bottom<self.paddle.rect.bottom):
            self.angle=-self.angle
            self.rect.bottom=self.paddle.rect.top
            self.fy=float(self.rect.centery)
            bounced=True

        if bounced:
            self.bounces+=1
            self.bounceCountSurf=self.scoreFont.render("Score: %d" % self.bounces, True, (255,255,255))
            dirtyRects.append(self.bounceCountSurf.get_rect())


        return dirtyRects

    def draw(self):
        self.screen.blit(self.image, self.rect.topleft)
        dirtyRects = [self.rect]
        if (self.bounceCountSurf):
            self.screen.blit(self.bounceCountSurf, self.screenRect.topleft)
            dirtyRects.append(self.bounceCountSurf.get_rect())
        return dirtyRects

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
        self.paddle=Paddle("paddle.png", self.bgSurface, self.screen)
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
            dirtyRects.extend(self.paddle.update())
            dirtyRects.extend(self.ball.update())
            self.updateBackground(dirtyRects)
            dirtyRects.extend(self.paddle.draw())
            dirtyRects.extend(self.ball.draw())
            pygame.display.update(dirtyRects)

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
