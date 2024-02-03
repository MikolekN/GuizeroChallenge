from guizero import App, Box, Drawing, Text
from random import random
from game_window import GameWindowInterface

NAME = "PONG by 184474"

PADDLE_SPEED = 20


class GameState():
    right = 0
    left = 0


class PongGame(GameWindowInterface):

    def __init__(self):
        super().__init__()

        # Values determining the distance from the edge of the window to the game window
        self.padding_x = self.width // 12
        self.padding_y = self.height // 12

        # Value determining the width of the wall on the edge of the game window
        self.wall_width = 2

        self.game_state = GameState()

        self.app = App(title=NAME, height=self.height, width=self.width, bg="black")
        self.app.tk.resizable(0, 0)  # disables resizing of the application window
        self.app.tk.focus_set()  # sets focus on the application window

        game = Box(self.app, height="fill", width="fill")
        self.game_area = Drawing(game, height="fill", width="fill")


        self.left_paddle = Paddle(self, True)
        self.right_paddle = Paddle(self, False)

        # left_score = Text(left_padding, align="left", text=str(left), color="white")
        # right_score = Text(right_padding, align="right", text=str(right), color="white")

        self.ball = Ball(self)

        self.app.when_key_pressed = self.movePaddle

        self.app.repeat(16, self.moveBall)

        self.app.repeat(1000, self.difficulty)

        self.app.repeat(16, self.updateView)  # refresh rate - 60fps

        self.app.display()

    def gameWindowBeginningX(self):
        return self.padding_x + self.wall_width

    def gameWindowEndingX(self):
        return self.width - self.padding_x - self.wall_width

    def gameWindowBeginningY(self):
        return self.padding_y + self.wall_width

    def gameWindowEndingY(self):
        return self.height - self.padding_y - self.wall_width

    def gameWindowWidth(self):
        return self.gameWindowEndingX() - self.gameWindowEndingX()

    def gameWindowHeight(self):
        return self.gameWindowEndingY() - self.gameWindowBeginningY()

    def checkForCollisionsBetweenPaddleAndBall(self, paddle):
        if (paddle.leftX() < self.ball.rightX() and paddle.rightX() > self.ball.leftX() and
                paddle.upperY() < self.ball.lowerY() and paddle.lowerY() > self.ball.upperY()):
            self.ball.dx *= -1
            self.ball.dy += (self.ball.y - paddle.y) / 10

    def handlePaddleCollisions(self):
        self.checkForCollisionsBetweenPaddleAndBall(self.left_paddle)
        self.checkForCollisionsBetweenPaddleAndBall(self.right_paddle)

    def movePaddle(self, event):
        if event.key == 'w':
            self.left_paddle.move(-PADDLE_SPEED)
        elif event.key == 's':
            self.left_paddle.move(PADDLE_SPEED)
        elif event.key == '8':
            self.right_paddle.move(-PADDLE_SPEED)
        elif event.key == '2':
            self.right_paddle.move(PADDLE_SPEED)

        self.handlePaddleCollisions()

    def moveBall(self):
        self.ball.move()
        if self.ball.leftX() <= self.gameWindowBeginningX():  # The ball touches the left side of the game window
            self.game_state.right += 1
            self.ball = Ball(self)
        elif self.ball.rightX() >= self.gameWindowEndingX():  # The ball touches the right side of the game window
            self.game_state.left += 1
            self.ball = Ball(self)

        self.handlePaddleCollisions()

    def difficulty(self):
        self.ball.dx *= 1 + random() * 0.1
        self.ball.dy *= 1 + random() * 0.1

    def draw_paddles(self):
        self.game_area.rectangle(self.left_paddle.x,
                            self.left_paddle.y,
                            self.left_paddle.x + self.left_paddle.paddle_width,
                            self.left_paddle.y + self.left_paddle.paddle_height, color="white")
        self.game_area.rectangle(self.right_paddle.x,
                            self.right_paddle.y,
                            self.right_paddle.x + self.right_paddle.paddle_width,
                            self.right_paddle.y + self.right_paddle.paddle_height, color="white")

    def draw_ball(self):
        self.game_area.rectangle(self.ball.x, self.ball.y, self.ball.x + self.ball.ball_size, self.ball.y + self.ball.ball_size, color="white")

    # def draw_dividing_line(self):
    #     # TODO
    #     # the line should be dashed
    #     self.game_area.line(x1=game_width / 2, y1=0, x2=game_width / 2, y2=HEIGHT, color="white", width=2)

    # def draw_score(self):
    #     # TODO
    #     # the score should be displayed on the top of the middle of the game area for each player
    #     self.left_score.clear()
    #     self.right_score.clear()
    #     self.left_score.append(str(self.game_state.left))
    #     self.right_score.append(str(self.game_state.right))

    def updateView(self):
        self.game_area.clear()
        self.draw_paddles()
        # self.draw_dividing_line()
        self.draw_ball()
        # self.draw_score()


class Paddle:
    def __init__(self, game_window, position):
        self.game_window = game_window

        self.paddle_width = self.game_window.width // 120
        self.paddle_height = self.game_window.height // 6

        if position:
            self.x = self.game_window.padding_x
            self.y = self.game_window.gameWindowBeginningY()
        else:
            self.x = self.game_window.width - self.game_window.padding_x - self.paddle_width
            self.y = self.game_window.gameWindowBeginningY()

        self.upper_boundary = self.game_window.gameWindowBeginningY()
        self.lower_boundary = self.game_window.gameWindowEndingY()

    def upperY(self):
        return self.y

    def lowerY(self):
        return self.y + self.paddle_height

    def leftX(self):
        return self.x

    def rightX(self):
        return self.x + self.paddle_width

    def move(self, speed):
        if self.upperY() + speed < self.upper_boundary:
            self.y = self.upper_boundary
        elif self.lowerY() + speed > self.lower_boundary:
            self.y = self.lower_boundary - self.paddle_height
        else:
            self.y += speed


class Ball:

    def __init__(self, game_window):
        self.game_window = game_window

        self.ball_size = 20 if self.game_window.width > 1000 else 10 if self.game_window.width > 100 else 4
        self.x = self.game_window.width // 2 - self.ball_size // 2
        self.y = self.game_window.height // 2 - self.ball_size // 2

        self.upper_boundary = self.game_window.gameWindowBeginningY()
        self.lower_boundary = self.game_window.gameWindowEndingY()
        self.left_boundary = self.game_window.gameWindowBeginningX()
        self.right_boundary = self.game_window.gameWindowEndingX()

        rand = random()
        self.dx = -3 if rand < 0.125 else -3 if rand < 0.25 else 3 if rand < 0.375 else 3 if rand < 0.5 else -1 if rand < 0.625 else -1 if rand < 0.75 else 1 if rand < 0.875 else 1
        self.dy = -1 if rand < 0.125 else 1 if rand < 0.25 else -1 if rand < 0.375 else 1 if rand < 0.5 else -3 if rand < 0.625 else 3 if rand < 0.75 else -3 if rand < 0.875 else 3

    def upperY(self):
        return self.y

    def lowerY(self):
        return self.y + self.ball_size

    def leftX(self):
        return self.x

    def rightX(self):
        return self.x + self.ball_size

    def move(self):
        # The movement in the X axis
        if self.leftX() + self.dx < self.left_boundary:
            self.x = self.left_boundary
            self.dx *= -1
        elif self.rightX() + self.dx > self.right_boundary:
            self.x = self.right_boundary - self.ball_size
            self.dx *= -1
        else:
            self.x += self.dx

        # The movement in the Y axis
        if self.upperY() + self.dy < self.upper_boundary:
            self.y = self.upper_boundary
            self.dy *= -1
        elif self.lowerY() + self.dy > self.lower_boundary:
            self.y = self.lower_boundary - self.ball_size
            self.dy *= -1
        else:
            self.y += self.dy


pong_game = PongGame()
pong_game.app.display()

"""
EXAMPLE: HOW TO DETERMINE WHAT KEY IS BEING PRESSED
def pressed(event):
    print("pressed: {}".format(event.key))
app.when_key_pressed = pressed
"""

# def move_paddle(event):
#     if event.key == 'w':  # If the left paddle is moving upwards
#         if ball.x1 < left_paddle.x2 and ball.x2 > left_paddle.x1:  # If the ball is in line with the left paddle
#             if left_paddle.y1 >= ball.y2 and left_paddle.y1 - PADDLE_SPEED < ball.y2:  # If the left paddle hits the ball
#                 # Push the top of the left paddle to the bottom of the ball
#                 left_paddle.y1 = ball.y2
#                 left_paddle.y2 = ball.y2 + paddle_height
#                 # Move the kinetic enegry of the collision into the movement of the ball
#                 if ball.dy == 0:  # If the ball wasn't moving in the Y dimension start the movement
#                     ball.dy = -1
#                 elif ball.dy < 0:  # If the ball was moving up in the Y dimension make the movement faster
#                     ball.dy -= random() * 0.1
#                 else:  # If the ball was moving down in the Y dimension bounce the ball from the paddle
#                     ball.dy *= -1
#             else:
#                 left_paddle.move(-PADDLE_SPEED)
#         else:
#             left_paddle.move(-PADDLE_SPEED)
#     elif event.key == 's':  # If the left paddle is moving downwards
#         if ball.x1 < left_paddle.x2 and ball.x2 > left_paddle.x1:  # If the ball is in line with the left paddle
#             if left_paddle.y2 <= ball.y1 and left_paddle.y2 + PADDLE_SPEED > ball.y1:  # If the left paddle hits the ball
#                 # Push the bottom of the left paddle to the top of the ball
#                 left_paddle.y2 = ball.y1 - paddle_height
#                 left_paddle.y2 = ball.y1
#                 # Move the kinetic enegry of the collision into the movement of the ball
#                 if ball.dy == 0:  # If the ball wasn't moving in the Y dimension start the movement
#                     ball.dy = 1
#                 elif ball.dy < 0:  # If the ball was moving up in the Y dimension bounce the ball from the paddle
#                     ball.dy *= -1
#                 else:  # If the ball was moving down in the Y dimension make the movement faster
#                     ball.dy += random() * 0.1
#             else:
#                 left_paddle.move(PADDLE_SPEED)
#         else:
#             left_paddle.move(PADDLE_SPEED)
#
#         if event.key == '8':  # If the right paddle is moving upwards
#             if ball.x1 < right_paddle.x2 and ball.x2 > right_paddle.x1:  # If the ball is in line with the right paddle
#                 if right_paddle.y1 >= ball.y2 and right_paddle.y1 - PADDLE_SPEED < ball.y2:  # If the right paddle hits the ball
#                     # Push the top of the right paddle to the bottom of the ball
#                     right_paddle.y1 = ball.y2
#                     right_paddle.y2 = ball.y2 + paddle_height
#                     # Move the kinetic enegry of the collision into the movement of the ball
#                     if ball.dy == 0:  # If the ball wasn't moving in the Y dimension start the movement
#                         ball.dy = -1
#                     elif ball.dy < 0:  # If the ball was moving up in the Y dimension make the movement faster
#                         ball.dy -= random() * 0.1
#                     else:  # If the ball was moving down in the Y dimension bounce the ball from the paddle
#                         ball.dy *= -1
#                 else:
#                     right_paddle.move(-PADDLE_SPEED)
#             else:
#                 right_paddle.move(-PADDLE_SPEED)
#         elif event.key == '2':  # If the right paddle is moving downwards
#             if ball.x1 < right_paddle.x2 and ball.x2 > right_paddle.x1:  # If the ball is in line with the right paddle
#                 if right_paddle.y2 <= ball.y1 and right_paddle.y2 + PADDLE_SPEED > ball.y1:  # If the right paddle hits the ball
#                     # Push the bottom of the right paddle to the top of the ball
#                     right_paddle.y2 = ball.y1 - paddle_height
#                     right_paddle.y2 = ball.y1
#                     # Move the kinetic enegry of the collision into the movement of the ball
#                     if ball.dy == 0:  # If the ball wasn't moving in the Y dimension start the movement
#                         ball.dy = 1
#                     elif ball.dy < 0:  # If the ball was moving up in the Y dimension bounce the ball from the paddle
#                         ball.dy *= -1
#                     else:  # If the ball was moving down in the Y dimension make the movement faster
#                         ball.dy += random() * 0.1
#                 else:
#                     right_paddle.move(PADDLE_SPEED)
#             else:
#                 right_paddle.move(PADDLE_SPEED)

# def move_ball():
#     global right, left
#     # ball.move()
#     if ball.x1 + ball.dx <= 0:  # The ball touches the left side of the screen
#         right += 1
#         # ball.start()
#     elif ball.x2 + ball.dx >= WIDTH:  # The ball touches the right side of the screen
#         left += 1
#         # ball.start()
#     elif (ball.x1 + ball.dx > left_paddle.x2 and ball.x2 + ball.dx > left_paddle.x1) and (
#             left_paddle.y1 < ball.y2 + ball.dy < left_paddle.y2):  # If after the move the ball hits the left paddle
#         ball.x1 = left_paddle.x2
#         ball.y1 += ball.dy
#         ball.x2 = left_paddle.x2 + ball_size
#         ball.y2 += ball.dy
#         ball.dx *= -1
#     elif right_paddle.x1 < ball.x1 + ball.dx < right_paddle.x2 and right_paddle.y1 < ball.y2 + ball.dy < right_paddle.y2:  # If after the move the ball hits the right paddle
#         ball.x1 = right_paddle.x1 - ball_size
#         ball.y1 += ball.dy
#         ball.x2 = right_paddle.x1
#         ball.y2 += ball.dy
#         ball.dx *= -1
#     else:
#         ball.move()
