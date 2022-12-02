from guizero import App, PushButton, Waffle, Box
from datetime import datetime
# recommended dimensions of a window are: a square
DIM = 20
FILE = "map"
NAME = "MapMaker by 184474"

app = App(title=NAME, bg="black")
size = 0
def func(x, y):
    map[x, y].color = "grey" if map[x, y].color == "white" else "red" if map[x, y].color == "grey" else "blue" if \
        map[x, y].color == "red" else "green" if map[x, y].color == "blue" else "white"
map = Waffle(app, color="white", height=size, width=size, dim=DIM, pad=1, command=func)

def askSize():
    global size
    app.hide()
    size = app.question(title="Size", question="Enter the size of map you want to create.", initial_value=10)
    if size is None:
        exit(69)
    if not size == str(int(size)):
        size = 10
    size = int(size)
    app.width = size * (DIM + 2)
    app.show()
    app.hide()
    app.height = size * (DIM + 2)
    app.show()

    map.width = size
    map.height = size
askSize()

box = Box(app, align="bottom")
resize = PushButton(box, text="New", command=askSize, align="left")
resize.bg = "white"

def saveFile():
    with open(FILE+datetime.now().strftime("%d_%m_%H_%M_%S")+".txt", "w") as f:
        f.write(str(size) + '\n')
        for i in range(size):
            for j in range(size):
                f.write("0\n" if map.pixel(i,j).color == "white" else "1\n" if map.pixel(i,j).color == "grey" else "2\n" if map.pixel(i,j).color == "red" else "3\n" if map.pixel(i,j).color == "blue" else "4\n")
save = PushButton(box, text="Save", command=saveFile, align="right")
save.bg = "white"

app.display()