from guizero import App, Box, Drawing, Text
from random import random

HEIGHT = 600
WIDTH = 1200
NAME = "PONG by 184440 & 184474"
PADDLE_SPEED = 20

paddle_width = 20 if WIDTH > 1000 else 10 if WIDTH > 100 else 4
paddle_height = 160 if WIDTH > 1000 else 80 if WIDTH > 100 else 10
padding_width = 2 * paddle_width
game_width = WIDTH - 2 * padding_width - 2 * paddle_width
ball_size = 20 if WIDTH > 1000 else 10 if WIDTH > 100 else 4

right = 0
left = 0

"""def pressed(event):
    print("pressed: {}".format(event.key))
app.when_key_pressed = pressed"""

class Paddle():
    def __init__(self):
        self.x1 = 0
        self.y1 = int(HEIGHT / 2 - paddle_height / 2)
        self.x2 = paddle_width - 1
        self.y2 = int(HEIGHT / 2 + paddle_height / 2)
    def move(self, speed):
        if self.y1 + speed < 0:
            self.y1 = 0
            self.y2 = paddle_height
        elif self.y2 + speed > HEIGHT:
            self.y1 = HEIGHT - paddle_height
            self.y2 = HEIGHT
        else:
            self.y1 += speed
            self.y2 += speed

class Ball():
    def __init__(self):
        self.x = int(game_width/2)
        self.y = int(HEIGHT/2)

        self.x1 = self.x - ball_size
        self.y1 = self.y - ball_size
        self.x2 = self.x + ball_size
        self.y2 = self.y + ball_size

        self.dx = -3
        self.dy = 1
    def move(self):
        if self.x1 + self.dx < 0:
            self.x1 = 0
            self.x = ball_size
            self.x2 = 2 * ball_size
            self.dx *= -1
        elif self.x2 + self.dx > game_width:
            self.x1 = game_width - 2 * ball_size
            self.x = game_width - ball_size
            self.x2 = game_width
            self.dx *= -1
        else:
            self.x1 += self.dx
            self.x += self.dx
            self.x2 += self.dx

        if self.y1 + self.dy < 0:
            self.y1 = 0
            self.y = ball_size
            self.y2 = 2 * ball_size
            self.dy *= -1
        elif self.y2 + self.dy > HEIGHT:
            self.y1 = HEIGHT - 2 * ball_size
            self.y = HEIGHT - ball_size
            self.y2 = HEIGHT
            self.dy *= -1
        else:
            self.y1 += self.dy
            self.y += self.dy
            self.y2 += self.dy
    def start(self):
        self.x = int(game_width/2)
        self.y = int(HEIGHT/2)

        self.x1 = self.x - ball_size
        self.y1 = self.y - ball_size
        self.x2 = self.x + ball_size
        self.y2 = self.y + ball_size

        rand = random()
        self.dx = -3 if rand < 0.125 else -3 if rand < 0.25 else 3 if rand < 0.375 else 3 if rand < 0.5 else -1 if rand < 0.625 else -1 if rand < 0.75 else 1 if rand < 0.875 else 1
        self.dy = -1 if rand < 0.125 else 1 if rand < 0.25 else -1 if rand < 0.375 else 1 if rand < 0.5 else -3 if rand < 0.625 else 3 if rand < 0.75 else -3 if rand < 0.875 else 3


app = App(title=NAME, height=HEIGHT, width=WIDTH, bg="black")
app.tk.resizable(0, 0)
app.tk.focus_set()

left_padding = Box(app, height=HEIGHT, width=padding_width, align="left")
right_padding = Box(app, height=HEIGHT, width=padding_width, align="right")
game_box = Box(app, height="fill", width="fill")

left_score = Text(left_padding, align="left", text=str(left), color="white")
right_score = Text(right_padding, align="right", text=str(right), color="white")

left_paddle_area =  Drawing(game_box, height=HEIGHT, width=paddle_width, align="left")
#left_paddle_area.rectangle(x1=0, y1=-1, x2=paddle_width-1, y2=HEIGHT, color="white", outline=1, outline_color="black")
left_paddle = Paddle()
left_paddle_area.rectangle(left_paddle.x1, left_paddle.y1, left_paddle.x2, left_paddle.y2, color="white")

right_paddle_area = Drawing(game_box, height=HEIGHT, width=paddle_width, align="right")
#right_paddle_area.rectangle(x1=0, y1=-1, x2=paddle_width-1, y2=HEIGHT, color="white", outline=1, outline_color="black")
right_paddle = Paddle()
right_paddle_area.rectangle(right_paddle.x1, right_paddle.y1, right_paddle.x2, right_paddle.y2, color="white")

game_area = Drawing(game_box, height=HEIGHT, width="fill")
ball = Ball()
game_area.rectangle(ball.x1, ball.y1, ball.x2, ball.y2, color="white")

def move_paddle(event):
    if event.key == 'w':
        left_paddle.move(-PADDLE_SPEED)
    elif event.key == 's':
        left_paddle.move(PADDLE_SPEED)
    elif event.key == '8':
        right_paddle.move(-PADDLE_SPEED)
    elif event.key == '2':
        right_paddle.move(PADDLE_SPEED)
app.when_key_pressed = move_paddle

def update_view():
    left_paddle_area.clear()
    left_paddle_area.rectangle(left_paddle.x1, left_paddle.y1, left_paddle.x2, left_paddle.y2, color="white")
    right_paddle_area.clear()
    right_paddle_area.rectangle(right_paddle.x1, right_paddle.y1, right_paddle.x2, right_paddle.y2, color="white")
    game_area.clear()
    game_area.rectangle(x1=-3, y1=0, x2=game_width+3, y2=HEIGHT, color="black", outline=6, outline_color="white")
    game_area.line(x1=game_width/2, y1=0, x2=game_width/2, y2=HEIGHT, color="white", width=3)
    game_area.rectangle(ball.x1, ball.y1, ball.x2, ball.y2, color="white")
    left_score.clear()
    right_score.clear()
    left_score.append(str(left))
    right_score.append(str(right))
app.repeat(16, update_view) #refresh rate - 60fps

def move_ball():
    global right, left
    ball.move()
    if ball.x1 == 0:
        if left_paddle.y2 < ball.y1 or left_paddle.y1 > ball.y2:
            right += 1
            ball.start()
            #print("Right wins!")
            #app.destroy()
        else:
            if ball.y1 < left_paddle.y2 < ball.y2:
                ball.dy = abs(ball.dy) + 0.1
            elif ball.y1 < left_paddle.y1 < ball.y2:
                ball.dy = -abs(ball.dy) - 0.1
    elif ball.x2 == game_width:
        if right_paddle.y2 < ball.y1 or right_paddle.y1 > ball.y2:
            left += 1
            ball.start()
            #print("Left wins!")
            #app.destroy()
        else:
            if ball.y1 < right_paddle.y2 < ball.y2:
                ball.dy = abs(ball.dy) + 0.05
            elif ball.y1 < right_paddle.y1 < ball.y2:
                ball.dy = -abs(ball.dy) - 0.05
app.repeat(16, move_ball)

def difficulty():
    ball.dx *= 1 + random()*0.1
    ball.dy *= 1 + random()*0.1
app.repeat(1000, difficulty)
app.display()