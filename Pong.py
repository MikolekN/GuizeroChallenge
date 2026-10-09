import time

from guizero import App, Box, Drawing
from game_window import GameWindowInterface, ResolutionNotChosen
from center_window import center_window

NAME = "PONG by 184474"

# The original was locked to the 60Hz video field rate, so the game advances in fixed
# steps of a sixtieth of a second however often the screen actually gets redrawn
TICK_SECONDS = 1 / 60

# Once the game falls this far behind there is nothing to gain from replaying the gap
MAX_CATCHUP_TICKS = 4

# The original cabinet had a switch to end the game at 11 points or at 15
WINNING_SCORE = 11

# A 555 timer on the original board held the ball back between points
SERVE_DELAY = 1000

# The board read the paddle as three bits, so the ball came back at one of eight fixed
# angles depending on which segment of the paddle it struck. Top segment to bottom
# segment, in units of the ball's vertical step
SEGMENT_DY = (-4, -3, -2, -1, 1, 2, 3, 4)

# A four bit counter counted the hits in a rally and sped the ball up in response. Each
# tier is a fraction of the fastest speed at which a paddle can still catch the ball
SPEED_TIERS = ((12, 0.8), (4, 0.6), (0, 0.4))

# Which bars of a seven segment digit are lit: "a" is the top bar, "b" to "f" carry on
# clockwise from the top right, and "g" is the middle bar
DIGIT_SEGMENTS = ("abcdef", "bc", "abdeg", "abcdg", "bcfg",
                  "acdfg", "acdefg", "abc", "abcdefg", "abcdfg")

# Which paddle a key drives, and in which direction. Keys are named by tk's keysym
PADDLE_KEYS = {
    "w": ("left", -1), "s": ("left", 1),
    "8": ("right", -1), "2": ("right", 1),
    "KP_8": ("right", -1), "KP_2": ("right", 1),
    "Up": ("right", -1), "Down": ("right", 1),
    "KP_Up": ("right", -1), "KP_Down": ("right", 1),
}

RESTART_KEY = "space"


def keyName(event):
    """guizero reports the character that was typed, which is empty for keys like the
    arrows, so take the name of the key from the tk event underneath instead."""
    return event.tk_event.keysym


class GameState():
    def __init__(self):
        self.right = 0
        self.left = 0
        self.hits = 0  # the length of the current rally, which sets the ball's speed
        self.ball_in_play = False
        # Flipped on every serve, so that they do not all set off the same way
        self.serve_downward = False

    def isOver(self):
        return self.left >= WINNING_SCORE or self.right >= WINNING_SCORE


class PongGame(GameWindowInterface):

    def __init__(self):
        super().__init__()

        # How far the paddles sit in from the sides of the screen
        self.paddle_inset = self.width // 20

        # How far a paddle travels in a single frame while its key is held
        self.paddle_speed = max(2, self.height // 60)

        self.digit_height = self.height // 8
        self.digit_stroke = max(2, self.digit_height // 6)

        self.game_state = GameState()

        self.app = App(title=NAME, height=self.height, width=self.width, bg="black")

        game = Box(self.app, height="fill", width="fill")
        # Sized explicitly rather than filled, so that the canvas is exactly the space
        # everything is positioned in. A filled canvas is only measured once the window
        # has been drawn, which would leave the coordinates guessing
        self.game_area = Drawing(game, height=self.height, width=self.width)

        self.left_paddle = Paddle(self, True)
        self.right_paddle = Paddle(self, False)

        self.ball = Ball(self)

        self.app.when_key_pressed = self.keyPressed
        self.app.when_key_released = self.keyReleased

        # Placed once the widgets exist, so that the window sits in the middle of the
        # screen at exactly the size the game is drawn at. This also stops it resizing
        self.app.tk.update_idletasks()
        center_window(self.app, self.width, self.height)

        # Take the keyboard rather than merely asking for it. The resolution dialog held
        # focus a moment ago, and closing it hands focus back to whatever was behind, not
        # on to this window. Without this the player presses keys at a window that is not
        # listening until they think to click on it first
        self.app.tk.lift()
        self.app.tk.focus_force()

        # Bookkeeping for the fixed step taken in updateGame
        self.last_tick = time.perf_counter()
        self.owed_time = 0.0

        # Windows rounds timers to about 15.6ms, so asking for 8 lands on a single one of
        # those while asking for 16 overshoots to nearer 24. This only decides how often
        # the game gets drawn - it advances in TICK_SECONDS steps whatever is chosen here
        self.app.repeat(8, self.updateGame)

        self.serveAfterDelay(toward_left=True)

    def gameWindowBeginningX(self):
        return 0

    def gameWindowEndingX(self):
        return self.width

    def gameWindowBeginningY(self):
        return 0

    def gameWindowEndingY(self):
        return self.height

    def paddleFor(self, side):
        return self.left_paddle if side == "left" else self.right_paddle

    def checkForCollisionsBetweenPaddleAndBall(self, paddle):
        if not (paddle.leftX() < self.ball.rightX() and paddle.rightX() > self.ball.leftX() and
                paddle.upperY() < self.ball.lowerY() and paddle.lowerY() > self.ball.upperY()):
            return

        # Bounce only a ball that is moving into the paddle. Without this the ball is
        # turned around again on every frame it still overlaps and sticks to the paddle
        approaching = self.ball.dx < 0 if paddle.is_left else self.ball.dx > 0
        if not approaching:
            return

        # Put the ball back against the face of the paddle so it can never end up inside it
        self.ball.x = paddle.rightX() if paddle.is_left else paddle.leftX() - self.ball.ball_size

        # Which of the eight segments of the paddle was struck picks the return angle
        segment = int((self.ball.centerY() - paddle.upperY()) / paddle.paddle_height * len(SEGMENT_DY))
        segment = max(0, min(len(SEGMENT_DY) - 1, segment))

        self.game_state.hits += 1
        speed = self.ball.speedFor(self.game_state.hits)
        self.ball.dx = speed if paddle.is_left else -speed
        self.ball.dy = SEGMENT_DY[segment] * self.ball.dy_unit

    def handlePaddleCollisions(self):
        self.checkForCollisionsBetweenPaddleAndBall(self.left_paddle)
        self.checkForCollisionsBetweenPaddleAndBall(self.right_paddle)

    def keyPressed(self, event):
        key = keyName(event)

        if key == RESTART_KEY and self.game_state.isOver():
            self.restart()
            return

        if key in PADDLE_KEYS:
            side, direction = PADDLE_KEYS[key]
            self.paddleFor(side).direction = direction

    def keyReleased(self, event):
        key = keyName(event)
        if key not in PADDLE_KEYS:
            return

        side, direction = PADDLE_KEYS[key]
        paddle = self.paddleFor(side)
        # Stop only if this is the key the paddle is currently moving on, so that letting
        # go of one key while still holding the opposite one does not halt the paddle
        if paddle.direction == direction:
            paddle.direction = 0

    def movePaddles(self):
        if self.game_state.isOver():
            return

        for paddle in (self.left_paddle, self.right_paddle):
            if paddle.direction != 0:
                paddle.move(paddle.direction * self.paddle_speed)

    def moveBall(self):
        if not self.game_state.ball_in_play:
            return

        self.ball.move()
        self.handlePaddleCollisions()

        if self.ball.rightX() < self.gameWindowBeginningX():  # past the left paddle
            self.score(scorer_is_left=False)
        elif self.ball.leftX() > self.gameWindowEndingX():  # past the right paddle
            self.score(scorer_is_left=True)

    def score(self, scorer_is_left):
        if scorer_is_left:
            self.game_state.left += 1
        else:
            self.game_state.right += 1

        self.game_state.ball_in_play = False

        if not self.game_state.isOver():
            # The ball is served towards whoever just gave the point away
            self.serveAfterDelay(toward_left=not scorer_is_left)

    def serveAfterDelay(self, toward_left):
        self.game_state.ball_in_play = False
        self.game_state.hits = 0
        self.app.after(SERVE_DELAY, lambda: self.serve(toward_left))

    def serve(self, toward_left):
        if self.game_state.isOver():
            return

        self.game_state.serve_downward = not self.game_state.serve_downward
        self.ball.serve(toward_left, self.game_state.serve_downward)
        self.game_state.ball_in_play = True

    def restart(self):
        self.game_state = GameState()
        self.left_paddle.reset()
        self.right_paddle.reset()
        self.serveAfterDelay(toward_left=True)

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

    def draw_net(self):
        # A dashed line down the middle of the screen, equal lengths on and off, which is
        # decoration only and does not take any part in the game
        net_width = max(2, self.width // 300)
        dash = max(4, self.height // 56)
        x = (self.gameWindowBeginningX() + self.gameWindowEndingX()) // 2 - net_width // 2

        y = self.gameWindowBeginningY()
        while y < self.gameWindowEndingY():
            self.game_area.rectangle(x, y, x + net_width, min(y + dash, self.gameWindowEndingY()), color="white")
            y += dash * 2

    def drawDigit(self, digit, left, top):
        height = self.digit_height
        width = height * 3 // 5
        stroke = self.digit_stroke
        middle = top + height // 2

        bars = {
            "a": (left, top, left + width, top + stroke),
            "b": (left + width - stroke, top, left + width, middle),
            "c": (left + width - stroke, middle, left + width, top + height),
            "d": (left, top + height - stroke, left + width, top + height),
            "e": (left, middle, left + stroke, top + height),
            "f": (left, top, left + stroke, middle),
            "g": (left, middle - stroke // 2, left + width, middle - stroke // 2 + stroke),
        }

        for bar in DIGIT_SEGMENTS[digit]:
            x1, y1, x2, y2 = bars[bar]
            self.game_area.rectangle(x1, y1, x2, y2, color="white")

    def drawScore(self, score, edge, top, towards_left):
        digits = [int(character) for character in str(score)]
        step = self.digit_height * 3 // 5 + self.digit_stroke
        # The left player's score is laid out backwards from the net, the right one's
        # forwards from it, so that both sit alongside the middle of the screen
        start = edge - len(digits) * step if towards_left else edge

        for position, digit in enumerate(digits):
            self.drawDigit(digit, start + position * step, top)

    def draw_scores(self):
        middle = (self.gameWindowBeginningX() + self.gameWindowEndingX()) // 2
        gap = self.width // 10
        top = self.height // 12

        self.drawScore(self.game_state.left, middle - gap, top, towards_left=True)
        self.drawScore(self.game_state.right, middle + gap, top, towards_left=False)

    def draw_game_over(self):
        size = max(8, self.height // 30)
        message = "PRESS SPACE TO PLAY AGAIN"
        # Drawing places text by its top left corner, so the width has to be guessed at
        # from the size of the font to get the message near the middle of the screen
        x = self.width // 2 - len(message) * size * 3 // 10
        self.game_area.text(x, self.height * 3 // 4, message, color="white", size=size)

    def updateView(self):
        self.game_area.clear()
        self.draw_net()
        self.draw_scores()
        self.draw_paddles()

        if self.game_state.ball_in_play:
            self.draw_ball()

        if self.game_state.isOver():
            self.draw_game_over()

    def updateGame(self):
        # The game moves on in fixed steps rather than once per drawn frame, so that it
        # runs at the same speed whatever rate the timer actually manages to deliver
        now = time.perf_counter()
        self.owed_time += now - self.last_tick
        self.last_tick = now

        ticks = int(self.owed_time / TICK_SECONDS)
        if ticks > MAX_CATCHUP_TICKS:
            # Something held the program up. Replaying the whole gap would throw the ball
            # across the screen, so the missed time is given up on instead of caught up
            ticks = MAX_CATCHUP_TICKS
            self.owed_time = 0.0
        else:
            # Whatever is left over is less than a whole step, and is carried into the
            # next frame rather than thrown away, so no time is lost as the game runs
            self.owed_time -= ticks * TICK_SECONDS

        for _ in range(ticks):
            self.movePaddles()
            self.moveBall()

        self.updateView()


class Paddle:
    def __init__(self, game_window, position):
        self.game_window = game_window
        self.is_left = position

        self.paddle_width = self.game_window.width // 120
        self.paddle_height = self.game_window.height // 6

        if self.is_left:
            self.x = self.game_window.paddle_inset
        else:
            self.x = self.game_window.width - self.game_window.paddle_inset - self.paddle_width

        self.upper_boundary = self.game_window.gameWindowBeginningY()
        self.lower_boundary = self.game_window.gameWindowEndingY()

        # -1 while the player holds up, 1 while they hold down, 0 while they hold neither
        self.direction = 0
        self.y = 0
        self.reset()

    def reset(self):
        self.y = (self.lower_boundary + self.upper_boundary - self.paddle_height) // 2
        self.direction = 0

    def upperY(self):
        return self.y

    def lowerY(self):
        return self.y + self.paddle_height

    def centerY(self):
        return self.y + self.paddle_height / 2

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

        self.upper_boundary = self.game_window.gameWindowBeginningY()
        self.lower_boundary = self.game_window.gameWindowEndingY()

        # The furthest the ball may travel in one frame and still be certain to overlap a
        # paddle it crosses. Any faster and it would jump straight over one, so every
        # speed the ball is ever given is a fraction of this
        self.safe_dx = self.ball_size + self.game_window.left_paddle.paddle_width

        # One step of the eight fixed return angles
        self.dy_unit = self.game_window.left_paddle.paddle_height / 24

        self.x = 0
        self.y = 0
        self.dx = 0
        self.dy = 0
        self.serve(True)

    def speedFor(self, hits):
        for threshold, fraction in SPEED_TIERS:
            if hits >= threshold:
                return self.safe_dx * fraction

    def serve(self, toward_left, downward=True):
        self.x = self.game_window.width // 2 - self.ball_size // 2
        self.y = self.game_window.height // 2 - self.ball_size // 2

        speed = self.speedFor(0)
        self.dx = -speed if toward_left else speed
        self.dy = self.dy_unit if downward else -self.dy_unit

    def upperY(self):
        return self.y

    def lowerY(self):
        return self.y + self.ball_size

    def centerY(self):
        return self.y + self.ball_size / 2

    def leftX(self):
        return self.x

    def rightX(self):
        return self.x + self.ball_size

    def move(self):
        # The movement in the X axis - the ball is not stopped here, running off the left
        # or the right edge of the screen is what scores a point
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


if __name__ == "__main__":
    try:
        pong_game = PongGame()
    except ResolutionNotChosen:
        # The player closed the resolution dialog instead of picking a size, so there is
        # no game to play. That is an answer, not a fault, so it leaves without a fuss
        raise SystemExit(0)

    pong_game.app.display()
