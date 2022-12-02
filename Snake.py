from guizero import App, Waffle
from random import randint

NAME = "Snake by 184474"
HEIGHT = 20
WIDTH = 20

chosenMove = 0
gameOver = False

class apple():
    def __init__(self):
        self.position = (randint(0, WIDTH - 1), randint(0, HEIGHT - 1))

class snake():
    def __init__(self):
        self.direction = (0, 1) # UP (0, -1), DOWN (0, 1), LEFT (-1, 0), RIGHT (1, 0)
        self.position = [(WIDTH // 2, HEIGHT // 2)]

    def moveSnake(self):
        global gameOver
        new = (self.position[0][0] + self.direction[0], self.position[0][1] + self.direction[1])
        if new[0] < 0 or new[0] > WIDTH - 1 or new[1] < 0 or new[1] > HEIGHT - 1:
            gameOver = True
        elif new in s.position and len(s.position) > 2:
            gameOver = True
        elif new in getApplesPositions():
            self.position = [new] + self.position
            rem = []
            for a in apples:
                if a.position == new:
                    rem.append(a)
            for r in rem:
                apples.remove(r)
                addApple()
        else:
            self.position = [new] + self.position
            self.position.pop()

    def turnUp(self):
        if self.direction != (0, 1) or len(self.position) < 3:
            self.direction = (0, -1)

    def turnDown(self):
        if self.direction != (0, -1) or len(self.position) < 3:
            self.direction = (0, 1)

    def turnRight(self):
        if self.direction != (-1, 0) or len(self.position) < 3:
            self.direction = (1, 0)

    def turnLeft(self):
        if self.direction != (1, 0) or len(self.position) < 3:
            self.direction = (-1, 0)

def cleanBoard():
    for x in range(WIDTH):
        for y in range(HEIGHT):
            waffle.pixel(x, y).color = "white"

def drawSnake():
    for p in s.position:
        waffle.pixel(p[0], p[1]).color = "green"

def drawApples():
    for a in apples:
        waffle.pixel(a.position[0], a.position[1]).color = "red"

def gameLoop():
    s.turnUp() if chosenMove == 0 else s.turnDown() if chosenMove == 1 else s.turnLeft() if chosenMove == 2 else s.turnRight()
    s.moveSnake()
    if gameOver:
        exit(1)
    cleanBoard()
    drawSnake()
    drawApples()

def addApple():
    new = apple()
    while new.position in getApplesPositions() or new.position in s.position:
        new = apple()
    apples.append(new)

def getApplesPositions():
    ret = []
    for a in apples:
        ret.append(a.position)
    return ret

app = App(title=NAME, bg="black")
waffle = Waffle(app, height=HEIGHT, width=WIDTH)
s = snake()
apples = [apple()]
app.repeat(100, gameLoop)
app.repeat(150000, addApple)
def keyboardPressed(e):
    global chosenMove
    if e.key == "w":
        chosenMove = 0
    elif e.key == "s":
        chosenMove = 1
    elif e.key == "a":
        chosenMove = 2
    elif e.key == "d":
        chosenMove = 3
app.when_key_pressed = keyboardPressed

app.display()