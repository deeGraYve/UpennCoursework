import copy
import sets
import sys
import random

class Sudoku:
    def __init__(self,tmpbrd):
        self.board = []
        vls = []
        for row in tmpbrd:
            retrow = []
            for i in range(9):
                if row[i] != "*":
                    retrow.append(int(row[i]))
                    vls.append(int(row[i]))
                else:
                    retrow.append(row[i])
                    vls.append(row[i])
            self.board.append(retrow)
        #self.prt()
        digs = '012345678'
        cells = [x+y for x in digs for y in digs]
        #print cells
        self.vals = dict((cell,[1,2,3,4,5,6,7,8,9]) for cell in cells)
        ks = self.vals.keys()
        for k in ks:
            xk = (int(k))/10
            yk = (int(k))%10
            preset = self.board[xk][yk]
            if preset != '*':
                self.vals[k] = [preset]
        self.arcqueue = self.makeQueueArcs(self.vals)
        self.boardt = []
        i = 0
        while (i<9):
            self.boardt.append([])
            i+=1
        m = 0
        while m < 9:
            n = 0
            while n < 9:
                (self.boardt[n]).append(self.board[m][n])
                n+=1
            m+=1
                
        
        
    def prt(self):
        print self.board
    
    def __str__(self):
        pict = []
        horLine = ('/' * 37)
        separator = ('/' + ('-' * 11)) * 3
        pict.append(horLine)
        cmt = 1
        for row in self.board:
            nrow = "/ "
            cnt = 1
            for el in row:
                if (cnt%3) == 0:
                    nrow = nrow + el.__str__() + " / "
                    cnt = 1
                else:
                    nrow = nrow + el.__str__() + " | "
                    cnt+=1
            pict.append(nrow)
            if (cmt%3) == 0:
                pict.append(horLine)
                cmt = 1
            else:
                pict.append(separator)
                cmt += 1
        return '\n'.join(pict)
    
    def inRow(self,num,x,y):
        vector = []
        i = 0
        while (i<9):
            nm = self.board[x][i]
            if(nm != '*'):
                vector.append(nm)
            i+=1
        #print vector
        if num in vector:
            return False
        return True
    
    def inCol(self,num,x,y):
        vector = []
        i = 0
        while (i<9):
            nm = self.board[i][y]
            if(nm != '*'):
                vector.append(nm)
            i+=1
        #print vector
        if num in vector:
            return False
        return True
    
    def inSqr(self,num,x,y):
        uprigx = 3*(x/3)
        uprigy = 3*(y/3)
        uprig = [uprigx,uprigy]
        #print "up right corner coord is ", uprig, " with val = ", self.board[uprigx][uprigy]
        vector = []
        i = j = 0
        while (i < 3):
            cy = uprigy + i
            while (j <3):
                cx = uprigx+j
                nm = self.board[cx][cy]
                if (nm != '*'):
                    vector.append(nm)
                j+=1
            i+=1
            j = 0
        #print vector
        if num in vector:
            return False
        return True
    
    def canPut(self,num,x,y):
        if( (self.inCol(num,x,y)) and (self.inRow(num,x,y)) and (self.inSqr(num,x,y))):
            return True
        return False
    
    def makeQueueArcs(self,vals):
        prequeue = []
        for key in vals.keys():
            if vals[key] == [1,2,3,4,5,6,7,8,9]:
                prequeue.append(key)
        queue = []
        for every in prequeue:
            for other in prequeue:
                if other != every:
                    str = every+"->"+other
                    queue.append(str)
        return queue
    
    def removeFirst(self):
        res = self.arcqueue.pop(0)
        ret = res.split('->')
        return ret
    
    def enqueue(self,xk,xi):
        xkstr = xk.__str__()
        xistr = xi.__str__()
        join = xkstr+"->"+xistr
        self.arcqueue.append(join)
        
    def domain(self,x):
        xstr = x.__str__()
        return self.vals[xstr]
    
    def deleteFromDomain(self,val,x):
        k = self.domain(x)
        ki = k.index(val)
        k.pop(ki)
        xstr = x.__str__()
        self.vals[xstr] = k
        return k
    
    def test(self,posx,posy,x,y):
        x1 = (int(posx))/10
        y1 = (int(posx))%10
        x2 = (int(posy))/10
        y2 = (int(posy))%10
        curry = self.board[x2][y2]
        self.board[x2][y2] = y
        #print "trying ", y, " in y and ", x, " in x"
        res = self.canPut(x, x1, y1)
        #print "result of putting ", x, " to ", x1, y1, "with ", y, "in", x2, y2, " is ", res
        self.board[x2][y2] = curry
        return res
    
    def neighbors(self,xi,xj):
        neighbors = []
        allxi = []
        for arc in self.arcqueue:
            start = arc.split("->")
            if(start[0] == xi and start[1] != xj):
                neighbors.append(start[1])
        #print xj in neighbors
        return neighbors
    
    def removeIncVals(self,xi,xj, verb):
        removed = False
        #print "domain xi is ", self.domain(xi)
        if verb == True:
            print "comparing ",xi, " with domain ", self.domain(xi), " and ", xj, " with domain", self.domain(xj)
        removeCand = []
        for x in self.domain(xi):
            cnt = 0
            for y in self.domain(xj):
                out = self.test(xi,xj,x,y)
                if out == False:
                    cnt+=1
            if cnt == len(self.domain(xj)):
                if verb:
                    print x, " is not consistent"
                removeCand.append(x)
                removed = True
        if removed == True:
            for val in removeCand:
                if verb:
                    print "deleting ", val, "from domain"
                self.deleteFromDomain(val, xi)
        #print self.domain(xi), xi
        #print self.domain(xj), xj
        return removed
    
    def isCons(self):
        if [] in self.vals.values():
            return False
        return True
    
    def isConsistent(self):
        if (self.diffRows() and self.diffCols() and self.diffSqrs() and self.isCons()):
            return True
        #print "rows", self.diffRows()
        #print "cols", self.diffCols()
        #print "sqrs", self.diffSqrs()
        #print "cons", self.isCons()
        return False
    
    def diffRows(self):
        for row in self.board:
            if not self.alldif(row):
                #print row
                return False
        return True
    
    def diffCols(self):
        for col in self.boardt:
            if not self.alldif(col):
                #print col
                return False
        return True
    
    def diffSqrs(self):
        i = 0
        while i < 3:
            j = 0
            while j < 3:
                sqrs = []
                m = 0
                while m < 3:
                    n = 0
                    while n < 3:
                        num = self.board[i*3+m][j*3+n]
                        if num != '*':
                            sqrs.append(num)
                        n+=1
                    m+=1
                if not self.alldif(sqrs):
                    return False
                j+=1
            i+=1
        return True
    
    def alldif(self,arr):
        for sm in arr:
            if arr.count(sm) != 1 and sm != '*':
                #print "count for", sm, " is ", arr.count(sm)
                return False
        return True
    
    def nakedPair(self,ar,crnum,which):
        reduced = False
        if which == 'col':
            if len(ar) > 0:
                i = 0
                while i < 9:
                    nm = i.__str__()+crnum.__str__()
                    #print nm
                    old = copy.copy(self.vals[nm])
                    #print copy.copy(self.vals[nm]), "before"
                    #print "remove", ar
                    new = []
                    if not old in ar:
                        for ev in ar:
                            for dig in ev:
                                if dig in old:
                                    old.remove(dig)
                                    #print "removing ", dig, " from ", old
                                    #print "yay col"
                                    reduced = True
                    self.vals[nm] = old
                    #print self.vals[nm], " after"
                    i+=1
        if which == 'row':
            if len(ar) > 0:
                i = 0
                while i < 9:
                    nm = crnum.__str__()+i.__str__()
                    #print nm
                    old = copy.copy(self.vals[nm])
                    print copy.copy(self.vals[nm]), "before, in", nm
                    print "remove", ar
                    new = []
                    if not old in ar:
                        for ev in ar:
                            for dig in ev:
                                if dig in old:
                                    old.remove(dig)
                                    print "removing ", dig, " from ", old
                                    print "yay row"
                                    reduced = True
                    self.vals[nm] = old
                    print self.vals[nm], " after"
                    i+=1
        return reduced
    
    def nakedPairElim(self):
        #cols
        rmd = False
        i = 0
        while i < 9:
            j = 0
            vals = []
            npairs = []
            while j < 9:
                nm = j.__str__()+i.__str__()
                
                vals.append(self.vals[nm])
                j+=1
            for any in vals:
                if (len(any) == vals.count(any)) and len(any) > 1:
                    #print any, "already here! in column", i
                    if not any in npairs:
                        npairs.append(any)
                    #print "eliminating ", npairs
                    res = self.nakedPair(npairs,i,'col')
                    #print "res is ", res
                    if res:
                        return [True,self.formOut()]
                    #    rmd = True
            i+=1
#===============================================================================
#        i = 0
#        while i < 9:
#            j = 0
#            vals = []
#            npairs = []
#            while j < 9:
#                nm = i.__str__()+j.__str__()                
#                vals.append(self.vals[nm])
#                j+=1
#            for any in vals:
#                if (len(any) == vals.count(any)) and len(any) > 1:
#                    print any, "already here! in column", i
#                    if not any in npairs:
#                        npairs.append(any)
#                    res = self.nakedPair(npairs,i,'row')
#                    if res:
#                        return [True,self.formOut()]
#            i+=1
#===============================================================================
        #print "rmd is ", rmd
        return [rmd,self.formOut()]
    
    def reduceSqr(self,sx,sy):
        reduced = False
        i = sx*3
        aldef = []
        hypoth = dict()
        while i<((sx*3)+3):
            j = sy*3
            while j<((sy*3)+3):
                #print self.board[i][j]
                nm = i.__str__()+j.__str__()
                if self.board[i][j] != '*':
                    aldef.append(self.board[i][j])
                    hypoth[nm] = [self.board[i][j]]
                else:
                    hypoth[nm] = []
                j+=1
            i+=1
        #print aldef
        #print hypoth
        for n in [1,2,3,4,5,6,7,8,9]:
            if (not n in aldef):
                #print "fitting ", n
                whcrow = []
                whccol = []
                #print "looking at rows"
                rws = []
                cls = []
                m = 0
                while m<3:
                    if n in self.board[sx*3+m]:
                        rws.append(self.canGo(n,sx,m))
                    if n in self.boardt[sy*3+m]:
                        #print n, "is in", self.boardt[sy*3+m], " with col# ", sy*3+m
                        cls.append(self.canGo(n,sy,m))
                        #print "cls here is", cls
                    m+=1
                #print cls
                if len(rws) == 2:
                    for tst in rws[0]:
                        if tst in rws[1]:
                            whcrow.append(tst)
                    #print n, " can only go into row ", whcrow 
                else:
                    if len(rws) == 0:
                        whcrow = [sx*3, sx*3+1, sx*3+2]
                    else:
                        whcrow = rws[0]
                    #print n, " can go into rows ", whcrow 
                if len(cls) == 2:
                    for cst in cls[0]:
                        if cst in cls[1]:
                            whccol.append(cst)
                    #print n, " can only go into col ", whccol
                else:
                    if len(cls) == 0:
                        whccol = [sy*3, sy*3+1, sy*3+2]
                    else:
                        whccol = cls[0]
                    #print n, " can go into cols ", whccol
                posssqr = []
                for q in whcrow:
                    for w in whccol:
                        if self.board[q][w] == '*':
                            posssqr.append(q.__str__()+w.__str__())
                #print n, "can only go to squares ", posssqr
                if len(posssqr) == 1:
                    xw = (int(posssqr[0]))/10
                    yw = (int(posssqr[0]))%10
                    #print "assigning ", n, " to square", posssqr[0]
                    reduced = True
                    self.board[xw][yw] = n
        #for sq,vl in hypoth.items():
            #if len(vl) == 0:
                #self.analyze(sq,aldef)
        return reduced
    
    def canGo(self,num,cpos,nt):
        vt = [cpos*3,cpos*3+1,cpos*3+2]
        #print vt
        nm = []
        for v in vt:
            #print "checking ", v, " against ", cpos*3+nt
            if v != cpos*3+nt:
                nm.append(v)
        #print "nm is ",nm
        return nm
    
    def analyze(self,sq,constr):
        print "analyzing ", sq, " with constr ", constr
        return True
    
    
    def reduce(self):
        red = False
        i = 0
        while i < 3:
            j = 0
            while j < 3:
                interm = self.reduceSqr(i,j)
                if interm:
                    red = True
                j+=1
            i+=1
        return [red,self.formOut()]
    
    def ac3(self):
        verb = False
        while len(self.arcqueue) > 0:
            (Xi, Xj) = self.removeFirst()
            rem = self.removeIncVals(Xi, Xj, verb)
            if rem == True:
                neigh = self.neighbors(Xi, Xj)
                if verb:
                    print neigh, " are neighbors"
                for n in neigh:
                    mk = n.__str__()+"->"+Xi
                    if mk not in self.arcqueue:
                        self.arcqueue.append(mk)
        #for kj,kl in self.vals.items():
        #print kj, " --> ", kl
        return self.isConsistent()
    
    def formOut(self):
        for kj,kl in self.vals.items():
            if len(kl) == 1:
                xn = (int(kj))/10
                yn = (int(kj))%10
                self.board[xn][yn] = kl[0]
        out = []
        for row in self.board:
            str = ''
            for it in row:
                str+=it.__str__()
            str+='\n'
            out.append(str)
        return out
    
    def solve(self):
        self.ac3()
        out = self.formOut()
        return out
        
class SudokuSolve:
    
    def __init__(self,filename):
        self.guess = dict()
        self.needguess = False
        self.solved = False
        fileHandle = open(filename, "r")
        line=fileHandle.readline()
        tmpbrd = []
        while line != "":
            tmpbrd.append(line)
            line=fileHandle.readline()
        self.old = copy.copy(tmpbrd)
        self.sudoku = Sudoku(tmpbrd)
        
    def slv(self):
        self.sudoku = Sudoku(self.old)
        self.new = self.sudoku.solve()
        if self.new != self.old:
            self.old = copy.copy(self.new)
            return True
        return False
    
    def ret(self):
        for key, val in self.sudoku.vals.items():
                if len(val) > 1:
                    print "picking", val, " from ", key
                    return [key,val]
    
    def guessSol(self):
        [v1,v2] = self.ret()
        self.guess[v1]                        
        return False
    
    def psolve(self):
        slvred = True
        while slvred == True and self.sudoku.isConsistent():
            slvres = True
            while slvres == True and self.sudoku.isConsistent():
                print "ac-3ing..."
                slvres = self.slv()
            print "reducing..."
            [slvred, self.old] = self.sudoku.reduce()
            if slvred == False:
                print "eliminating..."
                [rs,self.old] = self.sudoku.nakedPairElim()
                if rs == False:
                    slvred = False
                else:
                    if self.sudoku.isConsistent():
                        slvred = True
        if self.sudoku.isConsistent():
            for thn in self.sudoku.board:
                if '*' in thn:
                    self.solved = False
                    self.needguess = True
                    return [True,False]
                else:
                    self.solved = True
                    return [True, True]
        return [False,False]
        
    def myOut(self,dct):
        for kj,kl in self.sudoku.vals.items():
            if len(kl) == 1:
                xn = (int(kj))/10
                yn = (int(kj))%10
                self.sudoku.board[xn][yn] = kl[0]
            if kj in dct.keys():
                xn = (int(kj))/10
                yn = (int(kj))%10
                #print "guessing ", dct[kj], " in ", kj
                self.sudoku.board[xn][yn] = dct[kj]
                self.sudoku.vals[kj] = dct[kj]
        out = []
        for row in self.sudoku.board:
            str = ''
            for it in row:
                str+=it.__str__()
            str+='\n'
            out.append(str)
        return out
       
      
    def solve(self):
        [cons,solvd] = self.psolve()
        if not solvd:
            print "guessing time"
            #steps = dict((f,g) for (f,g) in self.sudoku.vals.items())
            #print steps
            #return None
            stepstaken = dict((f,g) for (f,g) in self.sudoku.vals.items())
            lim = 2
            guessed = dict()
            while lim < 4:
                guess = dict()
                rot = True
                cnt = 0
                while rot:
                    guess.clear()
                    for dm in range(lim):
                        rnkey = random.randint(0,len(stepstaken.keys())-1)
                        kkey = stepstaken.keys()[rnkey]
                        rnval = random.randint(0,len(stepstaken.values())-1)
                        kv = stepstaken.values()[rnval]
                        kvl = random.randint(0,len(kv)-1)
                        kval = kv[kvl]
                        guess[kkey] = kval
                    hashstr = ''
                    for gk,gv in guess.items():
                        hashstr +=gk+'-'+gv.__str__()+'.'
                    if not hashstr in guessed.values():
                        oldsudoku = copy.deepcopy(self.sudoku)
                        tmp = self.myOut(guess)
                        self.sudoku = Sudoku(tmp)
                        #print self.sudoku
                        [cns,slv] = self.psolve()
                        if slv:
                            print "Solution found!"
                            print self.sudoku
                            return self.sudoku.formOut()
                        #print cns, slv 
                        self.sudoku = Sudoku(oldsudoku.formOut()) #TODO: if consistent - guess further with these vals 
                        #guessed[len(guessed)+1] = hashstr
                        #print hashstr in guessed.values()
                        cnt+=1
                    if cnt > 10:
                        rot = False
                lim+=1
            print "not found"
            return self.sudoku
        else:
            print "Solution found!"
            print self.sudoku
            return self.sudoku.formOut()
        
            
sdk = SudokuSolve('test/gentle_sudoku.test')
print sdk.solve()
#sdk.sudoku.reduceSqr
#print sdk.sudoku.isConsistent()
#print sdk.sudoku.isConsistent()
#print sdk.removeIncVals('58','38')
#print sdk.inCol(3,2,6)
#print sdk.inRow(3,2,6)
#print sdk.inSqr(3,2,6)
#print sdk.sudoku
#print sdk.removeIncVals('22','03')
#===============================================================================
#print sdk.removeFirst(), sdk.domain(58)
#sdk.deleteFromDomain(4,58)
#print sdk.domain(58)
#print sdk.removeFirst()
#print sdk.neighbors('58','30')
#print sdk.removeFirst()
#sdk.enqueue(81, 48)
#sdk.enqueue(81, 50)
#print sdk.removeFirst()
#print sdk.test(58,17,2,7)
#===============================================================================