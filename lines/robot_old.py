from robotUtilities import *
from guiHelp import *
import Queue, heapq
import copy



class PriorityQueue(Queue.Queue): 
    
    def _init(self, maxsize):
        self.maxsize = maxsize
        self.cursize = 0
        self.queue = []

    def _full(self):
        return self.maxsize > 0 and len(self.queue) >= self.maxsize

    def __len__(self):
        return self.cursize
    
    def _empty(self):
        return not self.queue

    def _put(self, item):
        heapq.heappush(self.queue, item)
        self.cursize += 1

    def _get(self):
        self.cursize -= 1
        return heapq.heappop(self.queue)
    
    def mpop(self):
        el = heapq.heappop(self.queue)
        retel = copy.deepcopy(el)
        heapq.heappush(self.queue, el)
        return retel

class Node:
    def __init__(self,point):
        self.point = point
        self.visible = []
        self.depth = 0
        self.parent = None
        
    def addVis(self,vis):
        self.visible.append(Node(vis))
        
    def setParent(self,node):
        self.depth = node.depth + 1
        self.parent = node
        
    def getParent(self):
        return self.parent
        
    def __eq__(self, dif):
        if self.point == dif.getPoint():
            return True
        return False
    
    def getPoint(self):
        return self.point
    
    def listVis(self):
        return self.visible
    
    def isIn(self,where):
        pts = []
        for node in where:
            pts.append(node.point)
        if self.point in pts:
            return True
        return False
        
class navigateSolution:
    
    def __init__(self):
        #triangle_in_the_middle.test
        #square_in_the_middle.test
        #big_triangles.test
        #tall_triangle_in_the_middle.test
        self.board = read('big_triangles.test')
        (self.start, self.end, preobst) = self.board
        self.obstacles = []
        self.lines = []
        self.fringe = []
        self.visited = []
        self.queue = PriorityQueue()
        range = 0
        for obstacle in preobst:
            if range == 0:
                range = 1
            else:
                self.obstacles.append(obstacle)
                self.lines.extend(self.makeLines(obstacle))
    
    def drawMe(self):
        self.root = Tk()
        #offsetc = Canvas(self.root, width = 100, height = 100)
        #offsetc.pack()
        self.mycanvas = Canvas(self.root, width = 600, height = 600)
        self.mycanvas.pack()
        drawboard(self.mycanvas,self.board)
        drawPoint(self.mycanvas,self.start,"red")
        drawPoint(self.mycanvas,self.end,"green")
        
    def startDraw(self):
        self.root.mainloop()
        
    def drawOrigin(self):
        drawPoint(self.mycanvas,(0,0),"yellow")
    
    def makeLines(self,obst):
        lns = []
        for i in range(len(obst)-1):
            lns.append((obst[i], obst[i+1]))
        lns.append((obst[len(obst)-1], obst[0]))
        return lns
    
    def isInsidePoly(self,poly,node):
        cross = 0
        pt = node.point
        lns = self.makeLines(poly)
        ray = ((99.2,101.3),pt) #TODO: check that the line segment doesn't cross the vertex
        for ln in lns:
            if linesIntersect(ray, ln) == True:
                cross += 1
        if cross % 2 == 1:
            return True
        return False
    
    def findVisible(self,curnode):
        #print self.obstacles
        for obstacle in self.obstacles:
            polylines = self.makeLines(obstacle)
            for point in obstacle:
                if pathIntersectsAnyLines(curnode.point, point, self.lines) == False:
                    testnode = Node(self.getMiddle(((curnode.point),(point))))
                    if self.isInsidePoly(obstacle, testnode) == False:
                        #print testnode.point, "is not in", obstacle
                        #avoid redundancy
                        if Node(point) not in curnode.visible and curnode.point != point:
                            curnode.addVis(point)
                    else:
                        #get adjacent edges end-points that are missing
                        #because isInsidePoly returns True on them, but they have to be added
                        acc = []
                        for polyline in polylines:
                            if curnode.point in polyline:
                                (p1,p2) = polyline
                                if p1 != curnode.point:
                                    acc.append(p1)
                                else:
                                    acc.append(p2)
                        #print "acc is ", acc, "curnode is", curnode.point
                        for pt in acc:
                            if Node(pt) not in curnode.visible  and curnode.point != point:
                                curnode.addVis(pt)
                    #drawLine(self.mycanvas,curnode.point,point,"orange")
        if pathIntersectsAnyLines(curnode.point, self.end, self.lines) == False:
            curnode.addVis(self.end)
        return curnode.visible
    
    def getStart(self):
        return Node(self.start)
    
    def isGoal(self,node):
        if node.point == self.end:
            return True
        return False
    
    def getMiddle(self, line):
        """returns floor of center of line segment"""
        ((x1, y1), (x2,y2)) = line
        (x, y) = (((x1+x2)/2), ((y1+y2)/2))
        return (x, y)
    
    def successor(self,node):
        succ = []
        for vis in self.findVisible(node):
            if vis.isIn(self.visited) == False and vis.isIn(self.fringe) == False:
                succ.append(vis)
        return succ 
    
    def dfs(self):
        self.fringe.append(self.getStart())
        while len(self.fringe) > 0:
            node = self.fringe.pop()
            if node.getParent() != None:
                drawLine(self.mycanvas,node.getParent().point,node.point,"red")
            self.visited.append(node)
            if self.isGoal(node):
                return node
            successors = self.successor(node) 
            for sc in successors:
                sc.setParent(node)
            self.fringe.extend(successors)
        return None 
    
    def bfs(self):
        self.fringe.append(self.getStart())
        while len(self.fringe) > 0:
            node = self.fringe.pop(0)
            if node.getParent() != None:
                drawLine(self.mycanvas,node.getParent().point,node.point,"red")
            self.visited.append(node)
            if self.isGoal(node):
                return node
            successors = self.successor(node) 
            for sc in successors:
                sc.setParent(node)
            self.fringe.extend(successors)
        return None 
    
    def h(self,node):
        return distance(node.point,self.end)
    
    def g(self,node):
        sofar = 0
        child = node.point
        parent = node.getParent()
        while parent != None:
            sofar += distance(child,parent.point)
            child = parent.point
            parent = parent.getParent()
        return sofar
    
    def f(self,node):
        h = self.h(node)
        g = self.g(node)
        #print "h: ", h, " g: ",g
        val = h + g
        #print "val: ", val
        return val
    
    def myQueue(self,node):
        priority = self.f(node)
        return (priority, node)
    
    def printQueue(self):
        testq = self.queue.queue
        for ret in testq:
            print ret[0], " = ", self.g(ret[1]), " (g) + ", self.h(ret[1]), "(h) at ", ret[1].point
    
    def extendQueue(self,node):
        successors = self.findVisible(node)
        for succ in successors:
            succ.setParent(node)
            self.queue.put((self.f(succ),succ))
        
    
    def aStar(self):
        self.queue.put(self.myQueue(self.getStart()))
        #self.visited.append(self.getStart())
        closed = {}
        cntr = 1
        while self.queue.cursize > 0 and cntr < 1001:
            if cntr % 100 == 0:
                print (cntr/1000)*100, "% done"
            #self.prt(self.queue)
            cntr += 1
            exp = self.queue.get()
            node = exp[1]
            #self.findVisible(node)
            #print "expanding ", node.point, " with ", exp[0], " vis: "
            #for vs in node.listVis():
                #print vs.point
            #print "---------------------"
            if self.isGoal(node):
                print "found it!"
                return node
            else:
                """extend queue here"""
                self.extendQueue(node)
            #self.printQueue()
            #print self.queue.cursize
        if cntr <= 0:
            print "exceeded # of loops"
        return None
    
    def drawPath(self,res):
        path = []
        path.append(res.point)
        while res.getParent() != None:
            path.append(res.getParent().point)
            res = res.getParent()
        for i in range(len(path)-1):
            drawLine(self.mycanvas,path[i],path[i+1],"green")
        drawPoint(self.mycanvas,self.end,"green")
        #ret = []
        #length = len(path)
        #for i in range(length):
        #ret.append(path[length-i-1])
        #TODO: reverse path???
        #print path
        path.reverse()
        print path
        return path
    
    def prt(self,prqueue):
        testq = []
        while prqueue.queue:
            ret = prqueue.get()
            testq.append(copy.copy(ret))
            print ret[0], " <-> ", ret[1].point
        for it in testq:
            prqueue.put(it)
        #sm = prqueue.get()
        #print "expand ", sm[1].point, " with ", sm[0]
        
    
    def test(self):
        pq = PriorityQueue(1000)    
        pq.put((366, 'arad'))
        self.prt(pq)
        pq.put((393, 'sibiu'))
        pq.put((447, 'timisoara'))
        pq.put((449, 'zerind'))
        self.prt(pq)
        pq.put((646, 'arad'))
        pq.put((415, 'fagaras'))
        pq.put((671, 'oradea'))
        pq.put((413, 'rimniau'))
        self.prt(pq)
        pq.put((526, 'ciaiova'))
        pq.put((417, 'pitesti'))
        pq.put((553, 'sibiu'))
        self.prt(pq)
        pq.put((591, 'sibiu'))
        pq.put((450, 'bucharest'))
        self.prt(pq)
        pq.put((418, 'bucharest'))
        pq.put((615, 'ciaiova'))
        pq.put((607, 'rimniau'))
        self.prt(pq)
        #while not pq.empty():
        #print pq.get()[1], 
            
        
t = navigateSolution()
#t.drawMe()
#t.test()
#t.drawOrigin()
#st = t.getStart()
#t.findVisible(st)
#t.startDraw()
#print st.listVis()


###t.drawPath(t.dfs())
###t.startDraw()

t.aStar()
#t.drawPath(t.aStar())
#t.startDraw()

#===============================================================================
#ln = ((7,-5),(2,9))
#print t.getMiddle(ln)
#pol = [(-1.0, -1.0), (-1.0, 0.0), (0.0, 1.0), (1.0, 1.0)]
#pol2 = [(-4.0, -1.0), (-4.0, 0.0), (-3.0, 1.0), (-2.0, 1.0)]
#pol3 = ((-0.5, -0.5), (-0.5, 0.5), (0.5, 0.5), (0.5, -0.5))
#pol4 = [(-0.5, -0.5), (-0.5, 0.5), (0.5, 0.5), (0.5, -0.5)]
#pol = [(-1,0),(1,0),(0,4)]
#tst = Node((0,0))
#print t.isInsidePoly(pol, tst)
#print t.isInsidePoly(pol2, tst)
#print t.isInsidePoly(pol3, tst)
#print t.isInsidePoly(pol4, tst)
#===============================================================================

        
#test()