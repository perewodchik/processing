import math as m
import random as r
backgroundColor = "#FFFFFFF"
windowWidth = 900
windowHeight = 900
offset = 0.33
depth = 50
redValue = 255
greenValue = 255
blueValue = 255

""":
    Sigma of -5 = 0
    Sigma of  5 = 255
"""
rSigma = -3
gSigma = -3
bSigma = -3
rAdd = 3
gAdd = 1
bAdd = 2
coeff = 0.1

a = PVector(0,0)
b = PVector(windowWidth, 0)
c = PVector(windowWidth, windowHeight)
d = PVector(0, windowHeight)

def sigmoid(x):
    try:
        return 1 / (1 + m.exp(-x))
    except:
        print(x)
        return 1 / (1 + x)

finished = 1
def drawFractal(a,b,c,d, rS, gS, bS, deep):
    if deep >= depth:
        global finished
        finished = 1
        return
    
    a1 = PVector(a.x * (1-offset) + b.x * offset, a.y*(1-offset) + b.y * offset)
    b1 = PVector(b.x * (1-offset) + c.x * offset, b.y*(1-offset) + c.y * offset)
    c1 = PVector(c.x * (1-offset) + d.x * offset, c.y*(1-offset) + d.y * offset)
    d1 = PVector(d.x * (1-offset) + a.x * offset, d.y*(1-offset) + a.y * offset)
        
    for m,n,k in (a1,b,b1), (b1,c,c1), (c1,d,d1), (d1,a,a1):
        rS += rAdd * coeff
        gS += gAdd * coeff
        bS += bAdd * coeff
    
        newColor = (sigmoid(rS) * 255, sigmoid(gS) * 255, sigmoid(bS) * 255)
        stroke(*newColor)
        strokeWeight(2)
        fill(*newColor)
        triangle(m.x, m.y, n.x, n.y, k.x, k.y)
    
    drawFractal(a1, b1, c1, d1, rS, gS, bS, deep + 1)


def setup():
    size(windowWidth, windowHeight)
    
def draw():
    background(sigmoid(rSigma + 4*rAdd*coeff*depth) * 255, sigmoid(gSigma + 4*gAdd*coeff*depth) * 255, sigmoid(bSigma + 4*bAdd*coeff*depth) * 255)
    global offset, depth, finished, coeff
    if finished == 1:
        finished = 0
        drawFractal(a,b,c,d, rSigma, gSigma, bSigma, 0)
    offset = float(mouseX) / windowWidth
    coeff = sigmoid( (float(mouseY) / windowHeight - 0.5) * 5)
    

def mouseClicked():
    global rSigma, gSigma, bSigma, rAdd, bAdd, gAdd
    if mouseButton == LEFT:
        rSigma =  (r.random() - 0.5) * 10
        gSigma = (r.random() - 0.5) * 10
        bSigma = (r.random() - 0.5) * 10
        rAdd = (r.random() - 0.5) * 5
        bAdd = (r.random() - 0.5) * 5
        gAdd = (r.random() - 0.5) * 5
        
        
    
