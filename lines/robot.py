from robotUtilities import *
from guiHelp import *
import heapq

class PriorityQueue:
    def __init__(self):
        """heap: A binomial heap storing [priority,item] lists."""
        self.heap = []
        self.dict = {}
      
    def setPriority(self,stuff,priority):
        """inserts element into the queue and sets up its priority"""
        if stuff in self.dict:
            self.dict[stuff][0] = priority
            heapq.heapify(self.heap)
        else:
            pair = [priority,stuff]
            heapq.heappush(self.heap,pair)
            self.dict[stuff] = pair
      
    def getPriority(self,stuff):
        """returns the priority of a given element in the queue"""
        if not stuff in self.dict:
            return None
        return self.dict[stuff][0]
      
    def dequeue(self):
        """dequeues the element with the highest priority"""
        if self.isEmpty():
            return None
        (priority,stuff) = heapq.heappop(self.heap)
        del self.dict[stuff]
        return stuff  
  
    def isEmpty(self):
        """checks whether or not the queue is empty"""
        return len(self.heap) == 0


class Node:
    """Node structure to use for DFS and BFS searches"""
    def __init__(self,point):
        self.point = point
        self.visible = []
        self.depth = 0
        self.parent = None
        
    def addVis(self,vis):
        """adds visible points to the list"""
        self.visible.append(Node(vis))
        
    def setParent(self,node):
        """sets parent of the node"""
        self.depth = node.depth + 1
        self.parent = node
        
    def getParent(self):
        """returns the parent of the node"""
        return self.parent
        
    def __eq__(self, dif):
        """operation of node comparison"""
        if self.point == dif.getPoint():
            return True
        return False
    
    def getPoint(self):
        """returns the point of the node"""
        return self.point
    
    def listVis(self):
        """lists all visible nodes"""
        return self.visible
    
    def isIn(self,where):
        """checks if node is in some node's array"""
        pts = []
        for node in where:
            pts.append(node.point)
        if self.point in pts:
            return True
        return False
    
class aStartNode:
    """node structure to be used with A* search (added it late, didn't want to
    modify the existing Node structure)"""
    def __init__(self, state, parent, pathcost):
        self.state = state
        self.parent = parent
        self.pathcost = pathcost
        
class navigateSolution:
    """solution class"""
    def __init__(self,num):
        files = []
        files.append('triangle_in_the_middle.test')
        files.append('square_in_the_middle.test')
        files.append('big_triangles.test')
        files.append('tall_triangle_in_the_middle.test')
        files.append('mine.test')
        self.board = read(files[num])
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
                
    def tracepath(self,node):
        """traces path back to the parent"""
        if node.parent:
            return self.tracepath(node.parent) + [node.state]
        else:
            return [node.state]
    
    def drawMe(self):
        """draws the board with the obstacles"""
        self.root = Tk()
        self.mycanvas = Canvas(self.root, width = 600, height = 600)
        self.mycanvas.pack()
        drawboard(self.mycanvas,self.board)
        drawPoint(self.mycanvas,self.start,"red")
        drawPoint(self.mycanvas,self.end,"green")
        
    def startDraw(self):
        """starts displaying the canvas"""
        self.root.mainloop()
        
    def drawOrigin(self):
        """draws origin"""
        drawPoint(self.mycanvas,(0,0),"yellow")
    
    def makeLines(self,obst):
        """returns an array of lines that an obstacle consists of"""
        lns = []
        for i in range(len(obst)-1):
            lns.append((obst[i], obst[i+1]))
        lns.append((obst[len(obst)-1], obst[0]))
        return lns
    
    def isInsidePoly(self,poly,node):
        """checks if a point is inside of a given polygon"""
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
        """finds nodes visible from a given one"""
        for obstacle in self.obstacles:
            polylines = self.makeLines(obstacle)
            for point in obstacle:
                if pathIntersectsAnyLines(curnode.point, point, self.lines) == False:
                    testnode = Node(self.getMiddle(((curnode.point),(point))))
                    if self.isInsidePoly(obstacle, testnode) == False:
                        if Node(point) not in curnode.visible and curnode.point != point:
                            curnode.addVis(point)
                    else:
                        acc = []
                        for polyline in polylines:
                            if curnode.point in polyline:
                                (p1,p2) = polyline
                                if p1 != curnode.point:
                                    acc.append(p1)
                                else:
                                    acc.append(p2)
                        for pt in acc:
                            if Node(pt) not in curnode.visible  and curnode.point != pt:
                                curnode.addVis(pt)
        if pathIntersectsAnyLines(curnode.point, self.end, self.lines) == False:
            curnode.addVis(self.end)
        return curnode.visible
    
    def getStart(self):
        """returns Node with start point"""
        return Node(self.start)
    
    def isGoal(self,node):
        """checks if node is a goal state"""
        if node.point == self.end:
            return True
        return False
    
    def isGoalState(self,pt):
        """checks if point is a goal state"""
        if pt == self.end:
            return True
        return False
    
    def getMiddle(self, line):
        """returns floor of center of line segment"""
        ((x1, y1), (x2,y2)) = line
        (x, y) = (((x1+x2)/2), ((y1+y2)/2))
        return (x, y)
    
    def successor(self,node):
        """returns successors of the node"""
        succ = []
        for vis in self.findVisible(node):
            if vis.isIn(self.visited) == False and vis.isIn(self.fringe) == False:
                succ.append(vis)
        return succ 
    
    def dfs(self):
        """DFS search"""
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
        """BFS search"""
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
    
    def h(self,pnt):
        """returns a value of h needed for heuristic function, namely a distance to the end point"""
        return distance(pnt,self.end)
        
        
    def getSuccessors(self,pt):
        """returns node's successors used in A* search(slightly different from successors function)"""
        visible = []
        for obstacle in self.obstacles:
            polylines = self.makeLines(obstacle)
            for point in obstacle:
                if pathIntersectsAnyLines(pt, point, self.lines) == False:
                    testnode = Node(self.getMiddle(((pt),(point))))
                    if self.isInsidePoly(obstacle, testnode) == False:
                        if point not in visible and pt != point:
                            visible.append((point,distance(pt,point)))
                    else:
                        acc = []
                        for polyline in polylines:
                            if pt in polyline:
                                (p1,p2) = polyline
                                if p1 != pt:
                                    acc.append(p1)
                                else:
                                    acc.append(p2)
                        for pnt in acc:
                            if pnt not in visible  and pt != pnt:
                                visible.append((pnt,distance(pt,pnt)))
        if pathIntersectsAnyLines(pt, self.end, self.lines) == False:
            visible.append((self.end,distance(pt,self.end)))
        return visible
        
    def aStar(self):
        """A* search"""
        fringe = PriorityQueue()      
        fringe.setPriority(aStartNode(self.getStart().point, None, 0.0), self.h(self.start))
        closed = set()
        while not fringe.isEmpty():
            node = fringe.dequeue()
            if self.isGoalState(node.state):
                return (self.tracepath(node), node.pathcost)
            elif node.state not in closed:
                closed.add(node.state)
                for (nextstate, nextcost) in self.getSuccessors(node.state):
                    g = node.pathcost + nextcost
                    f = self.h(nextstate) + g
                    fringe.setPriority(aStartNode(nextstate, node, g), f)
        return (None, 0.0)
    
    def aStarSolve(self):
        """returns A* solution path"""
        (seq, len) = self.aStar()
        print "A* solution: ", seq
        print "A* solution length: ", len
        seq.reverse()
        return seq
    
    def aStartDrawPath(self,path):
        """draws A* solution path"""
        for i in range(len(path)-1):
            drawLine(self.mycanvas,path[i],path[i+1],"green")
        drawPoint(self.mycanvas,self.end,"green")
    
    def drawPath(self,res,methodname):
        """draws a path"""
        path = []
        path.append(res.point)
        while res.getParent() != None:
            path.append(res.getParent().point)
            res = res.getParent()
        for i in range(len(path)-1):
            drawLine(self.mycanvas,path[i],path[i+1],"green")
        drawPoint(self.mycanvas,self.end,"green")
        path.reverse()
        print methodname, " solution: ", path
        return path

class Demo:
    """demo class demonstrating 3 search types"""
    def __init__(self,nm):
        self.num = nm
        
    def showSolutions(self):
        """displays 3 solutions"""
        t = navigateSolution(self.num)
        t.drawMe()
        t.drawPath(t.bfs(), "BFS")
        t.startDraw()
        
        t2 = navigateSolution(self.num)
        t2.drawMe()
        t2.drawPath(t2.dfs(), "DFS")
        t2.startDraw()
        
        t3 = navigateSolution(self.num)
        t3.drawMe()
        t3.aStartDrawPath(t3.aStarSolve())
        t3.startDraw()


"""Enter number from 0 to 4 in Demo(NUMBER)"""
x = Demo(2)
x.showSolutions()