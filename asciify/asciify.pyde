import random as r
import string as s

IMAGE_NAME = "tom.png"
SHOW_ORIGINAL = 1

""":
    CLICK TO SWITCH MODE
"""

def settings():
    global Image, ImageColor
    Image = loadImage(IMAGE_NAME)
    ImageColor = loadImage(IMAGE_NAME)
    size(Image.width, Image.height)
    
def setup():
    global font, Image
    background(255)
    font = createFont("Courier", 10)
    textFont(font)
    fill(0)
    Image.filter(GRAY)
    
symbols = ['.',',',':',';','+','*','?','%','S','#','@']
symbols = symbols[::-1]
    
def pickSymbol(bright):
    return  symbols[ int( ( len(symbols) - 1) * bright / 255)]

def mouseClicked():
    global SHOW_ORIGINAL
    SHOW_ORIGINAL = ~SHOW_ORIGINAL
        
def draw():
    background(255)
    global SHOW_ORIGINAL
    if SHOW_ORIGINAL == 1:
        image(ImageColor,0,0)
    else:
        for y in range(0, height, 10):
            for x in range(0, width, 10):
                b = brightness(Image.get(x,y))
                text( pickSymbol(b), x, y)
