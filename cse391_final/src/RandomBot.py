from kingdoms import *

class RandomBot(Player):
    def __init__(self, index, verbose):
        Player.__init__(self, index, "RandomBot"+str(index))
        self.verbose=True
            
    def willDraw(self, board, deck, phase, playerIdx):
        if deck.castlesRemaining(playerIdx)==0:
            if deck.getTilesRemaining()==0:
                return None
            else:
                return DrawCard()
        numTiles=deck.getTilesRemaining()
        numSecretTiles=0
        if (deck.hasSecretTile(playerIdx)):
            numSecretTiles=1
        roll=random.randint(1, deck.castlesRemaining(playerIdx)+numTiles+numSecretTiles)
        
        if (roll<=deck.castlesRemaining(playerIdx)):
            return PlaceCastle(None)
        else:
            return DrawCard()
        
    def getCastle(self, currentTurn, phase, deck):
        roll=random.randint(1, deck.castlesRemaining(currentTurn))
        accum=0
        
        for i in range(0, 4):
            accum=accum+deck.castles[currentTurn][i]
            if (roll<=accum):
                return i+1
        return None
 
                
    def getPosition(self, board, phase):
        roll=random.randint(1, board.emptySpaces())
        count=0
        
        for i in range(0, 6):
            for j in range(0,5):
                if (board[i][j]==None):
                    count+=1
                    if (roll==count):
                        return (i, j)
        
    def getMove(self, board, deck, phase, playerIdx):
        if (deck.hasCards()):
            action=self.willDraw(board, deck, phase, playerIdx)
        else:
            if (deck.castlesRemaining(playerIdx)>0):
                action=PlaceCastle(None)
            elif (deck.hasSecretTile(playerIdx)):
                action=PlaceSecretTile()
            else:
                return None
        
        if (action==None):
            return (None, None, None)
        
        if (isinstance(action, PlaceCastle)):
            castleSize=self.getCastle(playerIdx, phase, deck)
            (row, column)=self.getPosition(board, phase)
            return ((PlaceCastle(castleSize), (row, column)), None)
        else:
            pos=self.getPosition(board, phase)
            if (deck.hasSecretTile(playerIdx)):
                roll=random.randint(1,deck.getTilesRemaining()+1)
                if (roll==1):
                    return ((PlaceSecretTile(), pos), None)
                else:
                    return ((DrawCard(), pos), None)
            else:
                return ((DrawCard(), pos), None)
 
#        if self.verbose:
#            print self.name + " placed " + str(newObj) + " at (" + str(row) + ", " + str(column) + ")" 

#       return (newObj, row, column)
