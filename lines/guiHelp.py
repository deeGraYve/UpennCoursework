from Tkinter import *

def drawboard(canvas, board):
    (start, end, polygons)=board
    drawPoint(canvas, start, "blue")
    drawPoint(canvas, end, "blue")
    for polygon in polygons:
        for i in range(len(polygon)):
            drawLine(canvas, polygon[i], polygon[(i+1)%len(polygon)], "blue") 

def drawPoint(canvas, point, col):
    (x,y)=point
    canvas.create_oval(((x+5.0)/10.0)*600-2,((y+5.0)/10.0)*600-2,((x+5.0)/10.0)*600+2,((y+5.0)/10.0)*600+2,fill=col)

def drawLine(canvas, point1, point2, col):
    (x1,y1)=point1
    (x2,y2)=point2
    drawPoint(canvas, point1, col)
    drawPoint(canvas, point1, col)
    canvas.create_line(((x1+5.0)/10.0)*600,((y1+5.0)/10.0)*600,((x2+5.0)/10.0)*600,((y2+5.0)/10.0)*600,fill=col)