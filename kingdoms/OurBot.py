from kingdoms import *
#modified RandomBot, some properties not needed

#UPDATE
#one ply is the same but with hPlyDepth 2 and in choosing the best outcome it should be hPlyDepth-1 
#as an argument to chooseAction routine
#Lacking implementation of special cases and weights

class OurBot(Player):
    
    def __init__(self, index):
        Player.__init__(self, index, "OurBot"+str(index))
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
        hPlyDepth = 2
        if(board.emptySpaces() < 3):
            hPlyDepth = 5
        elif(board.emptySpaces() < 6):
            hPlyDepth = 4
        elif(board.emptySpaces() < 9):
            hPlyDepth = 3
        else:
            hPlyDepth = 2
        return self.chooseAction(playerIdx, board, deck, phase, hPlyDepth, self.verbose)
    
    def whereCMove(self, whosMove, board, deck, phase, hPlyDepth): #determine score of placing castles
        favSoFarMove = favSoFarScore = favSoFarSize = None
        opponent = ((whosMove + 1) % 2)
        for hypCastles in range(0, 4):
            if (deck.castles[whosMove][hypCastles] > 0):
                castleSize = (hypCastles + 1)
                existEmptySquares = False
                castle = Castle(castleSize, whosMove)
                for i in range(0, 6):
                    for j in range(0, 5):
                        if (board[i][j] == None):#empty space
                            existEmptySquares = True
                            hypBoard = deepcopy(board) #need copying procedure!
                            hypBoard[i][j] = castle
                            hypDeck = deepcopy(deck)
                            hypDeck.castles[whosMove][hypCastles] -= 1
                            (mv, score,) = self.chooseAction(opponent, hypBoard, hypDeck, phase, (hPlyDepth - 1), False)
                            #why score is None???
                            try:
                                score = -score #determine if score returned by best action is > then so far best score
                            except TypeError:
                                print 'silly move of nothingness: None'
                            if (score > favSoFarScore):
                                favSoFarScore = score
                                favSoFarSize = (hypCastles + 1)
                                favSoFarMove = (i, j)
                #what if no empty squares???
        if (favSoFarScore > None):
            return ((PlaceCastle(favSoFarSize), favSoFarMove), (favSoFarScore - 0.1))
            # I implemented it becauseRyan's HalfPlySearchBot does that sometimes - it expects score of -0.1 or X.9 sometimes, so I did the same 
        else:
            return (None, None)
        
    def getDScore(self, whosMove, board, deck, phase, hPlyDepth):
        opponent = ((whosMove + 1) % 2)
        if (board.emptySpaces() == 0 or deck.getTilesRemaining() == 0):
            return (None, None)
        favSoFarScore = favSoFarMove = None
        hypTile = deck.deck[0]    
        for i in range(0, 6):
            for j in range(0, 5):
                if (board[i][j] == None):
                    hypBoard = deepcopy(board)
                    hypBoard.placeTile(i, j, hypTile)
                    hypDeck = deepcopy(deck)
                    hypDeck.draw()
                    #crashes here sometimes - find out why??
                    (mv, score,) = self.chooseAction(opponent, hypBoard, hypDeck, phase, (hPlyDepth - 1), False)
                    try:
                        score = -score
                    except TypeError:
                        #score is None, so cannot apply negation
                        print 'weird move of nothingness: None'
                    if (score > favSoFarScore):
                        favSoFarScore = score
                        favSoFarMove = (i,j)
        return ((DrawCard(), favSoFarMove), favSoFarScore)
    
    def getSScore(self, whosMove, board, deck, phase, hPlyDepth):
        opponent = ((whosMove + 1) % 2)
        if (not deck.hasSecretTile(whosMove)):
            return (None, None)
        favSoFarScore = favSoFarMove = None
        hypDeck = deepcopy(deck)
        secret = hypDeck.useSecretTile(whosMove)
        for i in range(0, 6):
            for j in range(0, 5):
                if (board[i][j] == None):
                    hypBoard = deepcopy(board)
                    hypBoard[i][j] = secret
                    (mv, score,) = self.chooseAction(opponent, hypBoard, hypDeck, phase, (hPlyDepth - 1), False)
                    try:
                        score = -score
                    except TypeError:
                        print 'weird move of None'
                    if (score > favSoFarScore):
                        favSoFarScore = score
                        favSoFarMove = (i,j)
        return ((PlaceSecretTile(),favSoFarMove),favSoFarScore    )
    
    def chooseAction(self, whosMove, board, deck, phase, hPlyDepth, verbose):
        #here should be different weights and special cases scenarios
        #like castle and secret tile weights for diff epochs
        #weights of tiles - Dragon, Mountain...NOT IMPLEMENTED
        if ((hPlyDepth == 0) or (board.emptySpaces() == 0)): #no spaces to move - return scores
            scores = board.score()
            diff = scores[0] - scores[1]
            if (whosMove == 0):
                return (None,(diff))
            else:
                return (None,(-diff))
        if ((deck.castlesRemaining(whosMove) == 0) and ((deck.getTilesRemaining() == 0) and (not deck.hasSecretTile(whosMove)))):
            return None # nothing else to do
        (cMove, cScore,) = self.whereCMove(whosMove, board, deck, phase, hPlyDepth)
        (dMove, dScore,) = self.getDScore(whosMove, board, deck, phase, hPlyDepth)
        (sMove, sScore,) = self.getSScore(whosMove, board, deck, phase, hPlyDepth)
        outDraw = outCastle = outSecret = False #all false originally, determine which score is greater
        if (dScore >= cScore):
            if (dScore >= sScore):
                outDraw = True
            else:
                outSecret = True
        elif (cScore >= sScore):
            outCastle = True
        else:
            outSecret = True
        if outDraw:
            if verbose:
                print (((((self.name + ' draws a card with expected score of ') + str(dScore)) + ' over ') + str(hPlyDepth)) + ' half-plys')
            return (dMove, dScore)
        elif outCastle:
            if verbose:
                print (((((self.name + ' places a castle with expected score of ') + str(cScore)) + ' over ') + str(hPlyDepth)) + ' half-plys')
            return (cMove, cScore)
        elif outSecret:
            if verbose:
                print (((((self.name + ' plays secret tile with expected score of ') + str(cScore)) + ' over ') + str(hPlyDepth)) + ' half-plys')
            return (sMove, sScore)