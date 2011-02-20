from kingdoms import *
from HalfPlySearchBot import *
from RandomBot import *
from OnePlySearchBot import *
from AdaptiveSearchBot import *
from OurBot import *
from Agent2 import Agent2
from Agent11a import Agent11a
from CleverBot import *

#p1=HumanPlayer("Ryan")
#p1=HalfPlyMaxScoreSearchBot(0, True)
#p2=RandomBot(1, True)
#p1=OurBot(0, True)
p2=AdaptiveSearchBot(1)
p1=CleverBot(0)

g=Game(p1, p2)
result=g.play()

print result