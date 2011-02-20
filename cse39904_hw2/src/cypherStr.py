import string

def toCypher(clue):
    alphabet = string.lowercase[:26]
    code = string.lowercase[2:26] + 'ab'
    
    trans = string.maketrans(alphabet, code)
    clue = clue.translate(trans)
    
    return clue
    
#toCypher("fcjjm rfcpc")