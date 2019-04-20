from random import *
backgroundColor = "#B0E19B"
startColor = "#37BA004"
endColor =  "#2B8F00"
wayColor = "#41DB00"
wallColor = "#CB0024"
windowWidth = 900
windowHeight = 900
mazeSize = 10

""":
    This is a maze generator using DSU with a possible solution
    There is also BFS for finding path from start to finish.
    CONTROLS:
        LEFT MOUSE - set starting position
        RIGHT MOUSE - set ending position
        D - create a maze or generate a new one
        S - show/hide solution
        C - clear current maze
        
    So, i didn't play for it initially, but you can also draw a maze of your own!
    In order to do that, simply hold MIDDLE MOUSE and hover over the cells
    that should become the walls. It will automatically generate the solution
    once you're finished building the walls
"""

class Point:
    def __init__(self, x_, y_):
        self.x = x_
        self.y = y_
        
startPoint = Point(0,0)
endPoint = Point(mazeSize - 1, mazeSize - 1)


#We will keep the connections as one dimensional arra, 
#where row is defined using // operator, 
#and column is defines using % operator

dirx = [-1, 0, 0, 1]
diry = [ 0,-1, 1, 0]
unionLink = [i for i in range(mazeSize * mazeSize)]
unionSize = [1 for i in range(mazeSize * mazeSize)]
Maze = [[0 for i in range(mazeSize)] for i in range(mazeSize)]
showPath = 0
pathFound = 0

def unionFind(x):
    x = int(x)
    while x != unionLink[x]:
        x = unionLink[x]
    return x

def unionSame(f, s):
    return unionFind(f) == unionFind(s)

def unionUnite(f, s):
    f = unionFind(f)
    s = unionFind(s)
    if f == s:
        return
    if unionSize[f] < unionSize[s]:
        f, s = s, f
    unionSize[f] += unionSize[s]
    unionLink[s] = f


""":
    The core of the program, the function program has been written for!
    It uses disjoint set union to build a maze in such a way so there will
    always be a solution. The way it works is it fills the maze with walls
    except for start and finish. Then it chooses a random cell and removes
    the wall. If there are other non-wall cells, then they are joined. This
    process repeats until a solution is found.
"""
def createMaze():
    global unionLink
    global unionSize
    global Maze
    Maze = [[1 for i in range(mazeSize)] for i in range(mazeSize)]
    unionLink = [i for i in range(mazeSize * mazeSize)]
    unionSize = [1 for i in range(mazeSize * mazeSize)]
    
    Maze[startPoint.y][startPoint.x] = 0
    Maze[endPoint.y][endPoint.x] = 0
    start = startPoint.y * mazeSize + startPoint.x
    finish = endPoint.y * mazeSize + endPoint.x
    
    while unionFind(start) != unionFind(finish):
        curPoint = randint(0, mazeSize * mazeSize - 1)
        while(curPoint == start or curPoint == finish):
            curPoint = randint(0, mazeSize * mazeSize - 1)
        
        curX = curPoint % mazeSize
        curY = curPoint // mazeSize
        Maze[curY][curX] = 0
        for i in range(4):
            newY = curY + diry[i]
            newX = curX + dirx[i]
            newPoint = newY * mazeSize + newX
            if(newX >= 0 and newX < mazeSize and newY >= 0 and newY < mazeSize and
               Maze[newY][newX] == 0 and unionFind(newPoint) != unionFind(curPoint)):
                   unionUnite(newPoint, curPoint)

""":
    An implementation of breadth-first search to find
    shortest path. The solution is stored in the Maze
    array it has a value of 2
"""

def createPath():
    global Maze
    used = {}
    distance = {}
    parent = {}
    start = (startPoint.x, startPoint.y)
    used[start] = 1
    parent[start] = start
    queue = [start]
    while queue:
        curPoint = queue.pop(0)
        curX = curPoint[0]
        curY = curPoint[1]
        if curPoint == (endPoint.x, endPoint.y):
            break
        for i in range(4):
            newX = curX + dirx[i]
            newY = curY + diry[i]
            if(newX >= 0 and newX < mazeSize and newY >= 0 and newY < mazeSize and not used.has_key((newX,newY)) and Maze[newY][newX] != 1):
                queue.append((newX,newY))
                used[(newX,newY)] = 1
                parent[(newX,newY)] = curPoint
    
    if not parent.has_key((endPoint.x,endPoint.y)):
        return
    
    wayBack = []
    curNode = parent[(endPoint.x,endPoint.y)]
    while curNode != start:
        wayBack.append(curNode)
        curNode = parent[curNode]
        
    for cell in wayBack:
        curX = cell[0]
        curY = cell[1]
        Maze[curY][curX] = 2
                   
            
def drawGrid():
    stroke(0)
    for i in range(1,mazeSize):
        line(i * windowWidth / mazeSize, 0, i * windowWidth / mazeSize, windowHeight)
    for j in range(1, mazeSize):
        line(0, j * windowHeight / mazeSize, windowWidth, j * windowHeight / mazeSize)
        
    fill(startColor)
    rect(startPoint.x * windowWidth / mazeSize , startPoint.y * windowHeight / mazeSize, windowWidth / mazeSize, windowHeight / mazeSize)
    fill(endColor)
    rect(endPoint.x * windowWidth / mazeSize , endPoint.y * windowHeight / mazeSize, windowWidth / mazeSize, windowHeight / mazeSize)
        
def drawMaze():
    fill(wallColor)
    for i in range(mazeSize):
        for j in range(mazeSize):
            if Maze[i][j] == 1:
                rect(j * windowWidth / mazeSize, i * windowHeight / mazeSize, windowWidth / mazeSize, windowHeight / mazeSize)
            
def drawPath():
    global showPath
    if showPath == 0:
        return
    fill(wayColor)
    for i in range(mazeSize):
        for j in range(mazeSize):
            if Maze[i][j] == 2:
                rect(j * windowWidth / mazeSize, i * windowHeight / mazeSize, windowWidth / mazeSize, windowHeight / mazeSize)
            
def clearMaze():
    global Maze
    Maze = [[0 for i in range(mazeSize)] for i in range(mazeSize)]
    
def clearPath():
    global Maze
    for i in range(mazeSize):
        for j in range(mazeSize):
            if Maze[i][j] == 2:
                Maze[i][j] = 0

def setup():
    size(windowWidth, windowHeight)
    stroke(255)
    background(backgroundColor)
    createPath()

def draw():
    background(backgroundColor)
    drawGrid()
    drawMaze()
    drawPath()

def mousePressed():
    clearPath()
    if mouseButton == LEFT:
        global startPoint
        startPoint = Point( int( (mouseX % windowWidth) * mazeSize / windowWidth), int( (mouseY % windowHeight) * mazeSize / windowHeight))
    
    if mouseButton == RIGHT:
        global endPoint
        endPoint = Point( int( (mouseX % windowWidth) * mazeSize / windowWidth), int( (mouseY % windowHeight) * mazeSize / windowHeight))
        
def mouseDragged():
    global Maze
    if mouseButton == CENTER:
        wallX = int( (mouseX % windowWidth) * mazeSize / windowWidth)
        wallY = int( (mouseY % windowHeight) * mazeSize / windowHeight)
        Maze[wallY][wallX] = 1
        
def mouseReleased():
    createPath()
        
def keyPressed():
    global showPath
    if key == 'c' or key == 'C':
        clearMaze()
        createPath()
    if key == 's' or key == 'S':
        showPath = ~showPath
    if key == 'd' or key == 'D':
        createMaze()
        createPath()
