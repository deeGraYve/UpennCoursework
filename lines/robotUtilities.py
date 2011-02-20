import re
from math import sqrt

EPSILON=.0000000001

def read(filename):
    inFile=open(filename, "r")
    startLine=inFile.readline()
    endLine=inFile.readline()
    
    number=re.compile("-?[0-9]+\.[0-9]+")

    (startXStr, startYStr)=number.findall(startLine)
    (endXStr, endYStr)=number.findall(endLine)
    
    polygons=[]
    curPolygon=[]
    
    polygons.append(((-5,-5),(5, -5),(5, 5),(-5, 5)))
    
    for line in inFile.readlines():
        if line.strip()=="":
            polygons.append(tuple(curPolygon))
            curPolygon=[]
        else:
            (curXStr, curYStr)=number.findall(line)
            curPolygon.append((float(curXStr), float(curYStr)))
    return ((float(startXStr), float(startYStr)), (float(endXStr), float(endYStr)), polygons)

                
def pathIntersectsAnyLines(start, end, lines):
    #print "Checking paths in between " + str(start) + " and " + str(end)

    for (one, two) in lines:
        if (linesIntersect((start, end), (one, two))):
            #print "Intersects " + str((one, two))
            return True
    return False

def verticalIntersection(vertical, other):
    if (isVertical(other)):
        ((ax1,ay1), (ax2, ay2))=vertical
        ((bx1,by1),(bx2, by2))=other
        return ((abs(ax1-bx1)<=EPSILON) and (((ay1-by1)*(ay1-by2)<=EPSILON) or ((ay2-by1)*(ay2-by2)<=EPSILON))) 
    else:
        ((x1,y1), (x2,y2))=other
        ((vx1, vy1), (vx2, vy2))=vertical
        slope=(y2-y1)/(x2-x1)
        deltaY=slope*(vx1-x1)
        projectedY=y1+deltaY
        return (projectedY-vy1)*(projectedY-vy2)<=EPSILON

def isVertical(line):
    ((x1,y1),(x2,y2))=line
    return (abs(x1-x2)<=EPSILON)

def linesIntersect(line1, line2):        
    (a, b)=line1
    (c, d)=line2
    
    acd=counterclockwise(a,c,d)
    bcd=counterclockwise(b,c,d)
    abc=counterclockwise(a,b,c)
    abd=counterclockwise(a,b,d)
    
    if (abs(acd)<=EPSILON):
        if (between(d, a, c)):
            return False
    if (abs(bcd)<=EPSILON):
        if (between(b,c,d)):
            return False
    if (abs(abc)<=EPSILON):
        if (between(a,b,c)):
            return False
    if (abs(abd)<=EPSILON):
        if (between(a,b,d)):
            return False
            
    if (abs(acd-bcd)<=EPSILON):
        return False
    if (abs(abc-abd)<=EPSILON):
        return False
    
    if (isVertical(line1)):
        return verticalIntersection(line1, line2)
    elif (isVertical(line2)):
        return verticalIntersection(line2, line1)

    
    return True

def between(a,b,c):
    (a1,a2)=a
    (b1,b2)=b
    (c1,c2)=c
    
    return (((b1-a1)*(c1-a1)<=EPSILON) and ((b2-a2)*(c2-a2)<=EPSILON))
        
def counterclockwise(pt1, pt2, pt3):
    (a,b)=pt1
    (c,d)=pt2
    (e,f)=pt3
    
    det=(c-a)*(f-b)-(d-b)*(e-a)
    
    if (det>=EPSILON):
        return 1
    elif (det<=-EPSILON):
        return -1
    else:
        return 0

def distance(p1, p2):
    (x1,y1)=p1
    (x2,y2)=p2
    
    return sqrt((x1-x2)*(x1-x2)+(y1-y2)*(y1-y2))