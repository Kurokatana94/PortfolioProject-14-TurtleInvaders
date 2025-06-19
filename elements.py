from turtle import Turtle

size_modifier = .8

# ==================================== ENEMY ====================================

class Enemy(Turtle):
    def __init__(self, color: str, initial_pos: list[float]):
        super().__init__()
        self.SPEED = 10
        self.shape('turtle')
        self.shapesize(.8*size_modifier,.8*size_modifier)
        self.right(90)
        self.enemy_color = color
        self.color(color)
        self.speed(0)
        self.penup()
        self.goto(tuple(initial_pos))

    def move(self, direction):
        if direction == 'right':
            target_pos = tuple([self.pos()[0] + self.SPEED, self.pos()[1]])
        elif direction == 'left':
            target_pos = tuple([self.pos()[0] - self.SPEED, self.pos()[1]])
        elif direction == 'down':
            target_pos = tuple([self.pos()[0], self.pos()[1] - self.SPEED])
        self.goto(target_pos)

    def destroy(self):
        self.hideturtle()
        self.clear()

# ==================================== PLAYER ====================================

class Player(Turtle):
    def __init__(self):
        super().__init__()
        self._INITIAL_POS = (0, -230)
        self.SPEED = 5
        self.LEFT = 180
        self.RIGHT = 0
        self.lives = 2
        self.shape('triangle')
        self.shapesize(2*size_modifier, 1*size_modifier)
        self.left(90)
        self.color('white')
        self.speed(0)
        self.penup()
        self.goto(self._INITIAL_POS)

    def move(self, speed):
        target_pos = tuple([self.pos()[0]+speed, self._INITIAL_POS[1]])
        self.goto(target_pos)

    def go_right(self):
        if self.pos()[0] < 350:
            self.move(self.SPEED)

    def go_left(self):
        if self.pos()[0] > -350:
            self.move(self.SPEED*-1)

    def death(self):
        if self.lives >= 1:
            self.lives -= 1
            self.goto(self._INITIAL_POS)
            return False
        else:
            return True

# ==================================== PROJECTILE | ENEMY & PLAYER ====================================

class Projectile(Turtle):
    def __init__(self, starting_pos):
        super().__init__()
        self.SPEED = 10
        self.shape('square')
        self.shapesize(1*size_modifier, .1*size_modifier)
        self.color('white')
        self.penup()
        self.goto(starting_pos)

    def move(self, direction_mod=1):
        self.goto(self.pos()[0], self.pos()[1] + self.SPEED*direction_mod)
        self.screen.ontimer(lambda: self.move(direction_mod=direction_mod), 100)

    def destroy(self):
        self.hideturtle()
        self.clear()

# ==================================== UI ====================================
class Score(Turtle):
    def __init__(self,screen_width, screen_height, high_score=0, score=0):
        super().__init__()
        self.score = score
        self.high_score = high_score
        self.hideturtle()
        self.penup()
        self.color('white')
        self.goto(screen_width//2-20, screen_height//2-20)
        self.write_score()

    def write_score(self):
        return self.write(f'SCORE: {self.score}  |  HIGH SCORE: {self.high_score}', align='right', font=("Arial", 10, "bold"))

    def update_score(self):
        self.clear()
        self.write_score()

class PlayerLife(Turtle):
    def __init__(self, initial_pos):
        super().__init__()
        self._INITIAL_POS = initial_pos
        self.penup()
        self.shape('triangle')
        self.shapesize(2*size_modifier, 1*size_modifier)
        self.color('white')
        self.left(90)
        self.goto(initial_pos)

    def lose_life(self):
        self.hideturtle()
        self.clear()