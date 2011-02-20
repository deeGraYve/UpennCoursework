import random
import sys
import random
import time

from copy import deepcopy

class Board:
    verbose=False
    
    def __init__(self):
        self.board=[]
        self.numEmptySpaces=30
        self.phase=1
    
        for i in range(0, 6):
            self.board.append([None, None, None, None, None])
    def __str__(self):
        s = "     0   1   2   3   4\n";
        for i in range(0,6):
            s+=str(i)+"  "
            for j in range(0,5):
                if (self.board[i][j]==None):
                    s=s+"  * ";
                else:
                    s=s+ str(self.board[i][j]);
            s=s+"\n";
        return s
    def __getitem__(self, row):
        return self.board[row]
    
    def placeTile(self, row, column, obj):
        self.board[row][column]=obj
        self.numEmptySpaces-=1
        
    def score(self):
        scores=[0,0]
        
        for i in range(0,6):
            for j in range(0,5):
                if (isinstance(self.board[i][j], Castle)):
                    self.updateScoresForCastle(scores, self.board[i][j],i,j)
        
        return scores
    
    def emptySpaces(self):
        return self.numEmptySpaces
    
    def updateScoresForCastle(self, scores, castle, i, j):
        player=castle.owner
        multiplier=castle.value
        
        score=multiplier*(self.scoreColumn(i,j)+self.scoreRow(i,j))
        
#        print player
#        print str((i,j))
        scores[player]+=score
        
        #if (self.verbose):
        #    print "Scored castle " + str(castle) + "at " + str(i) + ", " + str(j) + " for " + str(score) + "  points"
        
    def scoreRow(self, i, j):
        posAccum=0
        negAccum=0
        seenMine=False
        seenDragon=False
        
        start=0
        end=4

        cur=j

        while (cur>-1):
            if (isinstance(self.board[i][cur], MountainTile)):
                start=cur+1
                break
            cur=cur-1;
    
        cur=j

        while (cur<5):
            if (isinstance(self.board[i][cur], MountainTile)):
                end=cur-1
                break
            cur=cur+1;

        
        for cur in range(start, end+1):
            if (isinstance(self.board[i][cur], DragonTile)):
                seenDragon=True
            elif (isinstance(self.board[i][cur], MineTile)):
                seenMine=True
            elif (isinstance(self.board[i][cur], Castle)):
                pass
            elif (isinstance(self.board[i][cur], NumberedTile)):
                value=self.board[i][cur].value;
                if (value>0):
                    posAccum=posAccum+value
                else:
                    negAccum=negAccum+value
            elif (self.board[i][cur]==None):
                pass
            else:
                print self.board[i][cur]
                raise ValueError()
                
        if (seenDragon):
            accum=negAccum
        else:
            accum=posAccum+negAccum
        
        if (seenMine):
            accum=accum*2
            
        return accum
        
    def scoreColumn(self, i, j):
        posAccum=0
        negAccum=0
        seenMine=False
        seenDragon=False
        
        start=0
        end=5

        cur=i

        while (cur>-1):
            if (isinstance(self.board[cur][j], MountainTile)):
                start=cur+1
                break
            cur=cur-1;
    
        cur=i

        while (cur<6):
            if (isinstance(self.board[cur][j], MountainTile)):
                end=cur-1
                break
            cur=cur+1;

        
        for cur in range(start, end+1):
            if (isinstance(self.board[cur][j], DragonTile)):
                seenDragon=True
            elif (isinstance(self.board[cur][j], MineTile)):
                seenMine=True
                
            elif (isinstance(self.board[cur][j], NumberedTile)):
                value=self.board[cur][j].value;
                if (value>0):
                    posAccum=posAccum+value
                else:
                    negAccum=negAccum+value
            elif (isinstance(self.board[cur][j], Castle)):
                pass
            elif (self.board[cur][j]==None):
                pass
            else:
                raise ValueError()
                 
        if (seenDragon):
            accum=negAccum
        else:
            accum=posAccum+negAccum
        
        if (seenMine):
            accum=accum*2
            
        return accum  
    
class Tie:
    def __str__(self):
        return "Tie"
    
class Game:
    def __init__(self, player1, player2):
        self.round=1
        self.scores=[0,0];
        self.currentTurn=0
        self.players=(player1, player2);
        self.board=Board()
        self.deck=Deck()
        
    def play(self):
        scores=[0, 0]
        times=[0.0, 0.0]
        for phase in range(0,3):
            self.deck.reset()
            self.board=Board()
            self.currentTurn=0
            self.deck.resetCastlesForNewRound(0)
            self.deck.resetCastlesForNewRound(1)
            if (scores[1]>scores[0]):
                self.currentTurn=1
            while(self.board.emptySpaces()>0):
                print str(self.board.emptySpaces()) + " spaces left; " + str(self.deck.getTilesRemaining()) + " cards left; " + str(self.deck.castlesRemaining(0)) + " P0 castles; " + str(self.deck.castlesRemaining(1)) + " P1 castles."
                print "P0 secret tile: " + str(self.deck.viewSecretTile(0)) + "; P1 secret tile: " + str(self.deck.viewSecretTile((1))) 
                curPlayer=self.players[self.currentTurn]
     
                startTime=time.time()
                action=curPlayer.getMove(deepcopy(self.board), deepcopy(self.deck), phase, self.currentTurn)
                if (action==None):
                    print "Can't move; must pass"
                    self.currentTurn=(self.currentTurn+1)%2
                    continue
                ((moveType, (row, column)), expectedScore)=action
                endTime=time.time()
                print 'Chose move in %0.3f ms' % ((endTime-startTime)*1000.0)  
                times[self.currentTurn]+=endTime-startTime                                   
                
                newObj=None
                
                #print "MT: " + str(moveType)
                #print isinstance(moveType, DrawCard)
                #print isinstance(moveType, PlaceSecretTile)
                #print isinstance(moveType, PlaceCastle)
                
                if (isinstance(moveType, DrawCard)):
                    newObj=self.deck.draw()
                elif (isinstance(moveType, PlaceSecretTile)):
                    #print "Chose PlaceSecretTile"
                    newObj=self.deck.useSecretTile(self.currentTurn)
                elif (isinstance(moveType, PlaceCastle)):
                    #print "Placing castle of moveType.castleSize " + str(moveType.castleSize)
                    #print self.players[self.currentTurn].castles
                    newObj=self.deck.consumeCastle(self.currentTurn, moveType.castleSize)
                elif (isinstance(moveType, PassMove)):
                    if ((not self.deck.hasCards()) and (not self.deck.hasSecretTile(self.currentTurn)) and self.deck.castlesRemaining(self.currentTurn)==0):
                        newObj=None
                    else:
                        newObj=IllegalMove()
                
                print "Chose to place " + str(newObj) + " at (" + str(row) + ", " + str(column) + ") with expected score of " + str(expectedScore)
                
                if (isinstance(newObj, IllegalMove)):
                    print "Illegal move!"
                    return (self.currentTurn+1)%2
                
                if (newObj==None):
                    self.currentTurn=(self.currentTurn+1) % 2
                    continue
    
                if (self.board[row][column]!=None):
                    print "Illegal move!"
                    return (self.currentTurn+1)%2

                self.currentTurn=(self.currentTurn+1) % 2
    
                self.board.placeTile(row, column, newObj)
                
                print "\n\n"
            print "Final board for phase " + str(phase) + ": "
            print str(self.board)
            Board.verbose=True
            tmpScores=self.board.score()
            scores[0]+=tmpScores[0]
            scores[1]+=tmpScores[1]
            
            print "Scores after phase " + str(phase) + ": " + str(scores)
            print "Time Elapsed " + str(times)
        if (scores[0]<scores[1]):
            return 1;
        elif (scores[0]>scores[1]):
            return 0;
        else:
            return Tie();
        
class Tile:
    pass

class DragonTile:
    def __str__(self):
        return "  D "
    
class MineTile:
    def __str__(self):
        return "  G "

    
class MountainTile:
    def __str__(self):
        return "  M "

    
class NumberedTile:
    def __init__(self, value):
        self.value=value

    def __str__(self):
        if (self.value<0):
            return " "+str(self.value)+" ";
        else:
            return "  "+str(self.value)+" "

class Castle:
    def __init__(self, value, owner):
        self.value=value
        self.owner=owner
    def __str__(self):
        return str(self.owner) + "C" + str(self.value) + " ";

class Deck:
    def __init__(self):
        self.reset()
        self.castles=[[4,3,2,1],[4,3,2,1]]
        self.numCastleSizes=[4,4]
        
    def useSecretTile(self,playerIdx):
        tmp=self.secretCards[playerIdx]
        self.secretCards[playerIdx]=None
        return tmp
        
    def hasSecretTile(self, playerIdx):
        return not (self.secretCards[playerIdx]==None)
    
    def viewSecretTile(self, playerIdx):
        return self.secretCards[playerIdx]
    def hasCards(self):
        return len(self.deck)>0
    
    def numberRemaining(self, TileType, value):
        if (TileType == MountainTile):
            return self.mountainsRemaining
        elif (TileType == MineTile):
            return self.minesRemaining
        elif (TileType == DragonTile):
            return self.dragonsRemaining
        elif (TileType == NumberedTile):
            if (value>0):
                return self.positiveRemaining[value-1]
            else:
                return self.negativeRemaining[-value-1]
        else:
            raise ValueError
        
    def getTilesRemaining(self):
        return len(self.deck)

    def shuffle(self):
        random.shuffle(self.deck)
        
    def draw(self):
#        self.shuffle()
        ret=self.deck[0]
        
        self.decrementCounts(ret)
        
        self.deck=self.deck[1:]
        return ret
    
    def decrementCounts(self, ret):
        if (isinstance(ret, MountainTile)):
            self.mountainsRemaining-=1
        elif (isinstance(ret, MineTile)):
            self.minesRemaining-=1
        elif (isinstance(ret, DragonTile)):
            self.dragonsRemaining-=1
        elif (isinstance(ret, NumberedTile)):
            v=ret.value
            if (v>0):
                self.positiveRemaining[v-1]-=1
            else:
                self.negativeRemaining[-v-1]-=1
        else:
            raise ValueError

    def castlesRemaining(self, idx):
        return sum(self.castles[idx])

    def resetCastlesForNewRound(self, idx):
#        castlesAdded=4-self.castles[0]
        self.castles[idx][0]=4
        self.numCastleSizes=[4,4]
        #self.numCastles+=castlesAdded
   
    def consumeCastle(self, idx, castleSize):
        if (self.castles[idx][castleSize-1]>0):
            self.castles[idx][castleSize-1]-=1
            if (self.castles[idx][castleSize-1]==0):
                self.numCastleSizes[idx]-=1
            #self.numCastles-=1
#            print "Consuming castle " + str(self.index)
            return Castle(castleSize, idx)
        else:
            return IllegalMove()

    def reset(self):
        self.deck=[]
        self.deck.append(MountainTile())
        self.deck.append(MountainTile())
        self.deck.append(MineTile())
        self.deck.append(DragonTile())
        
        self.mountainsRemaining=2
        self.minesRemaining=1
        self.dragonsRemaining=1
        self.positiveRemaining=[2,2,2,2,2,2]
        self.negativeRemaining=[1,1,1,1,1,1]
        
        for value in range(1, 7):
            self.deck.append(NumberedTile(value))
            self.deck.append(NumberedTile(value)) 
            self.deck.append(NumberedTile(-value))

        self.shuffle()
        self.secretCards=[]
        self.secretCards.append(self.draw())
        self.secretCards.append(self.draw())
        

class Player:
    def __init__(self, index, name):
        self.score=0
        self.name=name
#        self.numCastles=10
        self.index=index    
        
    def getMove(self, board, deck, phase, playerIdx):
        return None   
    
class IllegalMove:
    pass

class PlaceCastle:
    def __init__(self, size):
        self.castleSize=size

class DrawCard:
    pass

class PlaceSecretTile:
    pass

class PassMove:
    pass

class HumanPlayer(Player):
    def __init__(self, name):
        Player.__init__(self)
        self.name=name
    
    def printStatus(self, board):
        print "Your turn, " + self.name
        print "The current board state is:"
        print board
        print "Your castles are " + str(self.castles[0]) + \
        " ones, " + str(self.castles[1]) + " twos, " + str(self.castles[2]) + " threes, " + \
        str(self.castles[3]) + " fours." 
        
    def willDraw(self, board):
        try:
            print "Will you draw (1) or place a castle (2)?"
            decision=int(sys.stdin.readline())
            if (decision==2):
                return PlaceCastle()
            else:
                return DrawCard()
        except ValueError:
            return self.willDraw(board)
        
    def getCastle(self, currentTurn):
        try:
            print "What size castle?"    
            castleType=int(sys.stdin.readline())
            self.castles[castleType-1]=self.castles[castleType-1]-1;
            return Castle(castleType, currentTurn)
        except ValueError:
            return self.getCastle(currentTurn)
        
    def getTilePosition(self, board, tile):
        print "The tile you drew is:"
        print tile
        return self.getPosition(board)
        
    def getPosition(self, board):
        try:
            print "What row to place (0-indexed)?"
            row = int(sys.stdin.readline())
            print "What column to place (0-indexed)?"
            column = int(sys.stdin.readline())
            if (board[row][column]!=None):
                raise ValueError()
        except ValueError:
            return self.getPosition(board)
        return (row, column)
    
    def getMove(self, board, deck, playerIdx):
        self.printStatus(board)

        if (deck.hasCards()):
            action=self.willDraw(board)
        else:
            action=PlaceCastle()
                
        if (isinstance(action, PlaceCastle)):
            newObj=self.getCastle(playerIdx)
            (row, column)=self.getPosition(board)
        else:
            newObj=deck.draw()
            (row, column)=self.getTilePosition(board, newObj)

        return (newObj, row, column)
