from guizero import App, Waffle
from random import randint

NAME = "Tetris by 184474"
HEIGHT = 20
WIDTH = 10

fallenTetrominoes = []

class tetromino():
    def __init__(self, id = None, turn = None):
        self.identity = randint(0,6) if id == None else id
        #self.identity = 0
        self.turn = randint(0,3) if turn == None else turn
        self.position = (randint(0, WIDTH - 4), -4)
        if self.identity == 0:
            self.teal()
        elif self.identity == 1:
            self.blue()
        elif self.identity == 2:
            self.orange()
        elif self.identity == 3:
            self.yellow()
        elif self.identity == 4:
            self.lime()
        elif self.identity == 5:
            self.purple()
        else:
            self.red()

    def getTurn(self):
        if self.turn == 0:
            return self.turn1
        elif self.turn == 1:
            return self.turn2
        elif self.turn == 2:
            return self.turn3
        else:
            return self.turn4

    def makeTurn(self, direction = 1):
        temp = self.turn
        self.turn += direction
        self.turn = self.turn % 4
        flag = False
        for i in self.getTurn():
            if i[0] + self.position[0] >= WIDTH or i[0] + self.position[0] < 0:
                flag = True
                break
            if i[1] + self.position[1] >= HEIGHT:
                flag = True
                break
            for f in fallenTetrominoes:
                for t in self.getTurn():
                    if f[0] == t[0] + self.position[0] and f[1] == t[1] + self.position[1]:
                        flag = True
                        break
        if flag:
            self.turn = temp

    def move(self, direction = 1):
        flag = True
        for i in self.getTurn():
            if i[0] + self.position[0] + direction >= WIDTH or i[0] + self.position[0] + direction < 0:
                flag = False
                break
            for j in fallenTetrominoes:
                if i[0] + self.position[0] + direction == j[0] and i[1] + self.position[1] + 1 == j[1]:
                    flag = False
                    break
        if flag:
            self.position = (self.position[0] + direction,self.position[1])

    def fall(self):
        flag = True
        for i in self.getTurn():
            if i[1] + self.position[1] + 1 >= HEIGHT:
                flag = False
                break
            for j in fallenTetrominoes:
                if i[0] + self.position[0] == j[0] and i[1] + self.position[1] + 1 == j[1]:
                    flag = False
                    break
        if flag:
            self.position = (self.position[0], self.position[1] + 1)

    def isOnFloor(self):
        for i in self.getTurn():
            if i[1] + self.position[1] + 1 >= HEIGHT:
                return True
            for j in fallenTetrominoes:
                if i[0] + self.position[0] == j[0] and i[1] + self.position[1] + 1 == j[1]:
                    return True

    def addToFallen(self):
        for i in self.getTurn():
            fallenTetrominoes.append((i[0] + self.position[0], i[1] + self.position[1], self.color))

    def teal(self):
        self.turn1 = [(0, 2), (1, 2), (2, 2), (3, 2)]
        self.turn2 = [(2, 0), (2, 1), (2, 2), (2, 3)]
        self.turn3 = [(0, 1), (1, 1), (2, 1), (3, 1)]
        self.turn4 = [(1, 0), (1, 1), (1, 2), (1, 3)]
        self.color = "teal"

    def blue(self):
        self.turn3 = [(0, 1), (1, 1), (2, 1), (2, 2)]
        self.turn2 = [(1, 2), (2, 0), (2, 1), (2, 2)]
        self.turn1 = [(1, 1), (1, 2), (2, 2), (3, 2)]
        self.turn4 = [(1, 1), (1, 2), (1, 3), (2, 1)]
        self.color = "blue"

    def orange(self):
        self.turn3 = [(1, 2), (1, 1), (2, 1), (3, 1)]
        self.turn2 = [(1, 1), (2, 1), (2, 2), (2, 3)]
        self.turn1 = [(0, 2), (1, 2), (2, 2), (2, 1)]
        self.turn4 = [(1, 0), (1, 1), (1, 2), (2, 2)]
        self.color = "orange"

    def yellow(self):
        self.turn1 = [(1, 1), (2, 1), (1, 2), (2, 2)]
        self.turn2 = [(1, 1), (2, 1), (1, 2), (2, 2)]
        self.turn3 = [(1, 1), (2, 1), (1, 2), (2, 2)]
        self.turn4 = [(1, 1), (2, 1), (1, 2), (2, 2)]
        self.color = "yellow"

    def lime(self):
        self.turn1 = [(0, 2), (1, 2), (1, 1), (2, 1)]
        self.turn2 = [(1, 1), (1, 2), (2, 2), (2, 3)]
        self.turn3 = [(1, 2), (2, 2), (2, 1), (3, 1)]
        self.turn4 = [(1, 0), (1, 1), (2, 1), (2, 2)]
        self.color = "lime"

    def purple(self):
        self.turn1 = [(1, 2), (2, 2), (2, 1), (3, 2)]
        self.turn2 = [(1, 1), (2, 0), (2, 1), (2, 2)]
        self.turn3 = [(0, 1), (1, 1), (1, 2), (2, 1)]
        self.turn4 = [(1, 1), (1, 2), (1, 3), (2, 2)]
        self.color = "purple"

    def red(self):
        self.turn1 = [(1, 1), (2, 1), (2, 2), (3, 2)]
        self.turn2 = [(1, 1), (1, 2), (2, 0), (2, 1)]
        self.turn3 = [(0, 1), (1, 1), (1, 2), (2, 2)]
        self.turn4 = [(1, 2), (1, 3), (2, 1), (2, 2)]
        self.color = "red"

def cleanTetromino():
    for i in T.getTurn():
        if i[1] + T.position[1] >= 0:
            waffle.pixel(i[0] + T.position[0], i[1] + T.position[1]).color = "white"
def drawTetromino():
    for i in T.getTurn():
        if i[1] + T.position[1] >= 0:
            waffle.pixel(i[0] + T.position[0], i[1] + T.position[1]).color = T.color

def fall():
    cleanTetromino()
    T.fall()
    drawTetromino()

app = App(title=NAME, bg="black")
waffle = Waffle(app, height=HEIGHT, width=WIDTH)
T = tetromino(0, 0)

def checkBoard():
    def findFull():
        full = []
        for i in range(0, HEIGHT):
            filled = True
            for j in range(0, WIDTH):
                if not (j, i, waffle.pixel(j, i).color) in fallenTetrominoes:
                    filled = False
                    break
            if filled:
                full.append(i)
        return full
    full = findFull()
    print(str(full))
    def removeFull():
        for y in full:
            for x in range(0, WIDTH):
                delete = []
                for f in fallenTetrominoes:
                    if f[0] == x and f[1] == y:
                        print("ERASING: " + str(f))
                        delete.append(f)
                        waffle.pixel(x,y).color = "white"
                for d in delete:
                    fallenTetrominoes.remove(d)
    removeFull()

    def fallFull():
        print(str(fallenTetrominoes))
        full.sort()
        for i in full:
            new = []
            delete = []
            print(str(i))
            for f in fallenTetrominoes:
                print("before: " + str(f))
                if f[1] < i:
                    print("DELETING: " + str(f))
                    print("APPENDING: (" + str(f[0]) + ", " + str(f[1] + 1) + ", " + f[2] + ")")
                    new.append((f[0], f[1] + 1, f[2]))
                    delete.append(f)
            for d in delete:
                fallenTetrominoes.remove(d)
            for n in new:
                fallenTetrominoes.append(n)
    fallFull()

def clearBoard():
    for y in range(0, HEIGHT):
        for x in range(0, WIDTH):
            waffle.pixel(x, y).color = "white"
def drawFallen():
    for i in fallenTetrominoes:
        waffle.pixel(i[0], i[1]).color = i[2]

def func():
    global T
    clearBoard()
    drawTetromino()
    drawFallen()
    fall()
    if T.isOnFloor():
        T.addToFallen()
        T = tetromino()
    checkBoard()
    print(str(fallenTetrominoes))
app.repeat(500, func)

def turnLeft():
    cleanTetromino()
    T.makeTurn()
    drawTetromino()
app.when_left_button_pressed = turnLeft
def turnRight():
    cleanTetromino()
    T.makeTurn(-1)
    drawTetromino()
app.when_right_button_pressed = turnRight

def moveRight():
    cleanTetromino()
    T.move()
    drawTetromino()
def moveLeft():
    cleanTetromino()
    T.move(-1)
    drawTetromino()
def move(e):
    if e.key == "a":
        moveLeft()
    elif e.key == "d":
        moveRight()
    elif e.key == "s":
        fall()
app.when_key_pressed = move

app.display()