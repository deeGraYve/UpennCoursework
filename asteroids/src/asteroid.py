import pygame
from pygame.locals import *   
from copy import copy
from math import *
import random
import sys, os


class Player:
    def __init__(self, filename, background, screen):
        self.imageMaster=pygame.image.load(filename)
        self.imageMaster.set_colorkey(self.imageMaster.get_at((10,10)), RLEACCEL)
        self.imageMaster = self.imageMaster.convert()
        self.image = self.imageMaster
        self.rect=self.image.get_rect()
        self.screenRect=screen.get_rect()
        self.rect.centerx=self.screenRect.centerx
        self.rect.centery=self.screenRect.centery
        self.background=background
        self.screen=screen
        self.pos = [self.rect.centerx,self.rect.centery]
        self.speed = [0, 0]
        self.accel = 0.007
        self.rot = 90
        self.accel_append = 0.0005
        self.fired = False
        self.collideRect = self.rect.inflate( -10, -10 )
        self.dead = False
        
        self.shot = None
        
    def draw(self):
        self.screen.blit(self.image, self.rect.topleft)
        self.image = pygame.transform.rotate(self.imageMaster, self.rot)
        dirtyRects = [self.rect]
        return dirtyRects
    
    def update(self):
        self.pos[0] += self.speed[0]
        self.pos[1] += self.speed[1]
        dirtyRects=[copy(self.rect)]

        oldCenter = self.rect.center
        
        self.rect = self.image.get_rect()
        self.rect.center = oldCenter

        
        
        if self.pos[0]>self.screenRect.right:
            self.pos[0] = 0
        if self.pos[0]<self.screenRect.left:
            self.pos[0] = self.screenRect.right
        if self.pos[1]>self.screenRect.bottom:
            self.pos[1] = 0
        if self.pos[1]<self.screenRect.top:
            self.pos[1] = self.screenRect.bottom
#            if self.pos[0] < (self.screenRect.right/2):
#                self.pos[0] += (self.screenRect.right/2)
#            else:
#                self.pos[0] -= (self.screenRect.right/2)
            
        self.rect.centerx=int(self.pos[0])
        self.rect.centery=int(self.pos[1])
        self.collideRect = self.rect.inflate( -10, -10 )
        
        if self.fired and self.shot:
            if self.shot.distance > self.screenRect.bottom:
                self.fired = False
                self.shot = None
                self.screen.blit(self.background, self.screenRect.topleft)
            if self.fired:
                if self.shot.distance > 20:
                    self.shot.lethal = True
        
        return dirtyRects
    
    def shoot(self):
        self.shot = Shot("shot.png", self.background, self.screen, self.speed, self.pos, copy(self.rot))
        self.shot.update()
        self.fired = True

    def die(self):
        self.dead = True
        self.screen.blit(self.background, self.screenRect.topleft)
        self.Font = pygame.font.SysFont(None,32)
        LevelText = self.Font.render("Muahaha!!! Game over! q-quit, r-try again", True, (255,255,255))
        self.screen.blit(LevelText,(self.screenRect.centerx-220,self.screenRect.centery-10))
        self.fired = False
        self.shot = None
        
        
    
    
class Shot:
    def __init__(self, filename, background, screen, shipSpeed, shipPos, shipRot):
        self.imageMaster=pygame.image.load(filename)
        self.imageMaster.set_colorkey(self.imageMaster.get_at((0,0)), RLEACCEL)
        self.imageMaster = self.imageMaster.convert()
        self.image = self.imageMaster
        self.rect=self.image.get_rect()
        self.screenRect=screen.get_rect()
        self.rect.centerx=self.screenRect.centerx
        self.rect.centery=self.screenRect.centery
        self.background=background
        self.screen=screen
        self.pos = copy(shipPos)
        self.pos[0] += 70*sin(radians(shipRot))
        self.pos[1] += 70*cos(radians(shipRot))
        self.speed = copy(shipSpeed)
        self.speed[0] += 2*sin(radians(shipRot))
        self.speed[1] += 2*cos(radians(shipRot))
        self.lethal = False
        self.origPos = copy(self.pos)
        self.absPos = copy(self.pos)
        self.distance = 0
        #self.speed = [0.5,0]
        
    def draw(self):
        self.screen.blit(self.image, self.rect.topleft)
        dirtyRects = [self.rect]
        return dirtyRects
    
    def update(self):
        self.pos[0] += self.speed[0]
        self.pos[1] += self.speed[1]
        
        self.absPos[0] += self.speed[0]
        self.absPos[1] += self.speed[1]
        
        self.distance = sqrt((self.origPos[0]-self.absPos[0])**2+(self.origPos[1]-self.absPos[1])**2)
            
        
        dirtyRects=[copy(self.rect)]

        oldCenter = self.rect.center
        
        if self.pos[0]>self.screenRect.right:
            self.pos[0] = 0
        if self.pos[0]<self.screenRect.left:
            self.pos[0] = self.screenRect.right
        if self.pos[1]>self.screenRect.bottom:
            self.pos[1] = 0
        if self.pos[1]<self.screenRect.top:
            self.pos[1] = self.screenRect.bottom
        
        self.rect = self.image.get_rect()
        self.rect.center = oldCenter
            
        self.rect.centerx=int(self.pos[0])
        self.rect.centery=int(self.pos[1])

        return dirtyRects
    

class Asteroid:
    def __init__(self, filename, background, screen, life, arr, tellPos, tellSpeed, playerRect):
        self.imageMaster=pygame.image.load(filename)
        self.imageMaster.set_colorkey(self.imageMaster.get_at((0,0)), RLEACCEL)
        self.imageMaster = self.imageMaster.convert()
        self.image = self.imageMaster
        self.rect=self.image.get_rect()
        self.screenRect=screen.get_rect()
        self.rect.centerx=self.screenRect.centerx
        self.rect.centery=self.screenRect.centery
        self.background=background
        self.collideRect = self.rect.inflate( -10, -10 )
        self.arrRef = arr
        self.screen=screen
        self.life = life
        self.screenRect=screen.get_rect()
        self.rot = 180
        if tellSpeed == 0:
            self.speed = [0.8*random.random(),0.8*random.random()]
        else:
            self.speed = copy(tellSpeed)
        self.dir = random.uniform(-3, 3)
        if tellPos == 0:
            myposx = random.randint(0,self.screenRect.right)
            myposy = random.randint(0,self.screenRect.bottom)
            self.pos = [myposx,myposy]
            self.update()
            #print playerRect.colliderect(self.collideRect)
            while playerRect.colliderect(self.collideRect):
                myposx = random.randint(0,self.screenRect.right)
                myposy = random.randint(0,self.screenRect.bottom)
                self.pos = [myposx,myposy]
                self.update()
                print "collision on creation, moving..."
            self.pos = [myposx,myposy]
        else:
            self.pos = copy(tellPos)
        
        
    def draw(self):
        self.screen.blit(self.image, self.rect.topleft)
        self.image = pygame.transform.rotate(self.imageMaster, self.rot)
        dirtyRects = [self.rect]
        return dirtyRects
    
    def update(self):
        self.pos[0] += self.speed[0]
        self.pos[1] += self.speed[1]
        self.rot += self.dir
        if self.rot > 360:
                self.rot = 0
        if self.rot < 0:
                self.rot = 359
        dirtyRects=[copy(self.rect)]

        oldCenter = self.rect.center
        
        if self.pos[0]>self.screenRect.right:
            self.pos[0] = 0
        if self.pos[0]<self.screenRect.left:
            self.pos[0] = self.screenRect.right
        if self.pos[1]>self.screenRect.bottom:
            self.pos[1] = 0
        if self.pos[1]<self.screenRect.top:
            self.pos[1] = self.screenRect.bottom
        
        self.rect = self.image.get_rect()
        self.rect.center = oldCenter
            
        self.rect.centerx=int(self.pos[0])
        self.rect.centery=int(self.pos[1])
        self.collideRect = self.rect.inflate( -10, -10 )

        return dirtyRects
    
    def span(self):
        x1 = self.speed[0]/(sqrt(3))
        y1 = self.speed[1]/(sqrt(3))
        
        #first, same, but 4/3 of orig vector, 2/sqrt(3) scale
        nx1 = 2*x1
        ny1 = 2*y1
        
        #second, rot by -120
        nx2 = x1*cos(radians(-120))-y1*sin(radians(-120));
        ny2 = x1*sin(radians(-120))+y1*cos(radians(-120));
        
        #third, rot by 120
        nx3 = x1*cos(radians(120))-y1*sin(radians(120));
        ny3 = x1*sin(radians(120))+y1*cos(radians(120));

        self.arrRef.append(Asteroid("asteroid_small.png",self.background, self.screen,1, self.arrRef,self.pos,[nx1,ny1],None))
        self.arrRef.append(Asteroid("asteroid_small.png",self.background, self.screen,1, self.arrRef,self.pos,[nx2,ny2],None))
        self.arrRef.append(Asteroid("asteroid_small.png",self.background, self.screen,1, self.arrRef,self.pos,[nx3,ny3],None))
    
    def die(self):
        if self.life > 1:
            self.life = 1
            self.screen.blit(self.background, self.screenRect.topleft)
            self.arrRef.remove(self)
            self.span()
        else:
            self.screen.blit(self.background, self.screenRect.topleft)
            self.arrRef.remove(self)


class aGame:
    GAME_WIDTH=640
    GAME_HEIGHT=490

    def __init__(self):
        pygame.init()
        self.level = 0
        pygame.display.set_mode((aGame.GAME_WIDTH, aGame.GAME_HEIGHT))
        self.screen=pygame.display.get_surface()
        pygame.display.set_caption("Asteroids game")
        bgTile=pygame.image.load("background.jpg")
        bgTile.convert()    
        self.screen.blit(bgTile, (0,0))
        self.Font = pygame.font.SysFont(None,22)
        self.bgSurface=self.drawBackground(bgTile)
        self.player=Player("falcon.png", self.bgSurface, self.screen)
        self.clock = pygame.time.Clock()
        self.levelCnt = 1
        self.asteroids = []
        self.asteroids.append(Asteroid("asteroid_small.png",self.bgSurface, self.screen,1, self.asteroids,0,0,self.player.collideRect))
        self.asteroids.append(Asteroid("big_asteroid.png",self.bgSurface, self.screen,2, self.asteroids,0,0,self.player.collideRect))
        pygame.display.update()
        
    def updateBackground(self, dirtyRects):
        for rect in dirtyRects:
            self.screen.blit(self.bgSurface, rect, rect)
        
        #print debug info to the screen
#        pygame.draw.polygon(self.screen,(0,0,0),[[0,0],[380,0],[380,30],[0,30]])
#        if self.player.fired:
#            LevelText = self.Font.render("Distance: "+str(self.player.shot.distance), True, (255,255,255))
#            self.screen.blit(LevelText,(10,10))

    def nextLevel(self):
        level = self.level+1
        print "Level: ", level
        self=aGame()
        self.level = level
        flipCoin = random.uniform(0,1)
        for lev in range(self.level):
            if flipCoin < 0.5:
                    self.asteroids.append(Asteroid("asteroid_small.png",self.bgSurface, self.screen,1, self.asteroids,0,0,self.player.collideRect))
            else:
                self.asteroids.append(Asteroid("big_asteroid.png",self.bgSurface, self.screen,2, self.asteroids,0,0,self.player.collideRect))
        self.eventLoop()
        
    def checkWin(self):
        if len(self.asteroids) < 1:
            self.nextLevel()
            
    def drawBackground(self, bgTile):
        bgTileRect=bgTile.get_rect()
        tileWidth=bgTileRect.width
        tileHeight=bgTileRect.height

        background=pygame.Surface((aGame.GAME_WIDTH, aGame.GAME_HEIGHT))

        x=0
        while (x<aGame.GAME_WIDTH):
            y=0
            while (y<aGame.GAME_HEIGHT):
                background.blit(bgTile, (x,y))
                y+=tileHeight
            x+=tileWidth
        return background
    
    def GetInput(self):
        keystate = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == QUIT or keystate[K_q]:
                pygame.quit(); sys.exit()
        self.player.speed[0] *= 0.995
        self.player.speed[1] *= 0.995
        if self.player.accel > 0.007:
            self.player.accel *= 0.99
        if keystate[K_LEFT]:
            self.player.rot += 1.0
            if self.player.rot > 360:
                self.player.rot = 0
        if keystate[K_RIGHT]:
            self.player.rot -= 1.0
            if self.player.rot < 0:
                self.player.rot = 359
        if keystate[K_UP]:
            self.player.accel += self.player.accel_append;
            self.player.speed[0] += self.player.accel*sin(radians(self.player.rot))
            self.player.speed[1] += self.player.accel*cos(radians(self.player.rot))
        if keystate[K_DOWN]:
            self.player.accel = 0.007
            self.player.speed[0] *= 0.993
            self.player.speed[1] *= 0.993
        if keystate[K_SPACE]:
            if not self.player.fired and not self.player.dead:
                self.player.shoot()
        if keystate[K_ESCAPE]:
            if not self.player.dead:
                self.teleportPlayer()
        if keystate[K_r]:
            self=aGame()
            self.eventLoop()
            
    def collisionDetect(self, act):
        #asterpid - shot and asteroid - player
        for aster in self.asteroids:
            if self.player.fired:
                if self.player.shot.rect.colliderect(aster.collideRect):
                    if act:
                        aster.die()
                        self.player.fired = False
                        self.player.shot = None
                        myScreen = self.screen.get_rect()
                        self.screen.blit(self.bgSurface, myScreen.topleft)
                    return True
            if self.player.collideRect.colliderect(aster.collideRect):
                if act:
                    self.player.die()
                return True
                
        #player - shot
        if self.player.fired:
            if self.player.collideRect.colliderect(self.player.shot.rect):
                if act and self.player.shot.lethal:
                    self.player.die()
                return True
        
        return False
            
    def teleportPlayer(self):
            
            myScreen = self.screen.get_rect()
            self.screen.blit(self.bgSurface, myScreen.topleft)
            myposx = random.randint(0,myScreen.right)
            myposy = random.randint(0,myScreen.bottom)
            self.player.pos = [myposx,myposy]
            self.player.update()
            dirtyRects=[]
            #print playerRect.colliderect(self.collideRect)
            while self.collisionDetect(False):
                myposx = random.randint(0,myScreen.right)
                myposy = random.randint(0,myScreen.bottom)
                self.player.pos = [myposx,myposy]
                self.screen.blit(self.bgSurface, myScreen.topleft)
                self.player.update()
                pygame.display.update()
                print "collision on teleporting, moving..."
            self.player.pos = [myposx,myposy]

    def eventLoop(self):
        while 1:
            self.GetInput()
            dirtyRects=[]
            if not self.player.dead:
                dirtyRects.extend(self.player.update())
                for aster in self.asteroids:
                    dirtyRects.extend(aster.update())
            if self.player.fired:
                dirtyRects.extend(self.player.shot.update())
            self.updateBackground(dirtyRects)

            self.collisionDetect(True)
            if self.player.fired:
                self.player.shot.draw()
            if not self.player.dead:
                self.player.draw()
                for aster in self.asteroids:
                    aster.draw()
            pygame.display.update()
            self.checkWin()
            self.clock.tick(60)

if __name__ == '__main__':
    myGame=aGame()
    myGame.eventLoop()
