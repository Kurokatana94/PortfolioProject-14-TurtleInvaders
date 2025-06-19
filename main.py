from turtle import Screen
from tkinter import Tk, messagebox
from elements import Player, Projectile, Enemy, Score, PlayerLife, size_modifier
from random import randint

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

def get_high_score():
    return None

high_score = get_high_score()

game_level = 1
score = Score(SCREEN_WIDTH, SCREEN_HEIGHT, high_score)

#Window init
screen = Screen()
screen.bgcolor("black")
screen.title("Turtle Invaders")
screen.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
screen.tracer(0)
screen.listen()

# ======================================== PLAYER ========================================

player = Player()
player.lives = 2

projectiles = []

enemies_projectiles = []

# ======================================== ENEMIES SECTION ========================================

def get_rand_color() -> str:
    while True:
        rgb = tuple(randint(0,255) for _ in range(3))
        if rgb != (0,0,0):
            return '#%02x%02x%02x' % rgb

def init_enemies(level):
    starting_y = SCREEN_HEIGHT//4 - ((level + 2) // 2 * 20)
    enemies = []
    for n in range(level+2):
        color = get_rand_color()
        enemies_line = [Enemy(color, [j * (SCREEN_WIDTH / 2) // 11, n * 30 + starting_y]) for j in range(-5, 6)]
        enemies.append(enemies_line)
    return enemies

def enemies_movement(direction: str, enemies):
    if any(enemy.pos()[0] >= 350 for row in enemies for enemy in row) and direction == 'down':
        enemies_direction['dir'] = 'left'
    elif any(enemy.pos()[0] <= -350 for row in enemies for enemy in row) and direction == 'down':
        enemies_direction['dir'] = 'right'
    elif any(enemy.pos()[0] >= 350 for row in enemies for enemy in row) or any(enemy.pos()[0] <= -350 for row in enemies for enemy in row):
        enemies_direction['dir'] = 'down'

    # If any enemy reaches the player ycor, it's a game over
    if any(enemy.pos()[1] <= player.pos()[1] for row in enemies_list for enemy in row):
        game_over_popup()

    [enemy.move(enemies_direction['dir']) for row in enemies for enemy in row]
    screen.ontimer(lambda:enemies_movement(enemies_direction['dir'], enemies), 200)

# Enemies init
enemies_list = init_enemies(game_level//3+1)

enemies_direction = {'dir': 'right'}

def destroy_enemy(row, enemy, projectile):
    global score
    score.score += 100
    score.update_score()
    projectile.destroy()
    projectiles.remove(projectile)
    enemy.destroy()
    enemies_list[enemies_list.index(row)].remove(enemy)
    print(score)

enemies_shot_cd = 3000

def enemy_shot(enemies):
    rows = [row for row in enemies if len(row) > 0]
    if rows:
        rand_n = randint(0, len(rows)-1) if len(rows) > 1 else 0
        rand_row = rows[rand_n]
        rand_n = randint(0, len(rand_row)-1) if len(rand_row) > 1 else 0
        enemy = rand_row[rand_n]
        print(enemies)

        init_projectile(source='enemy', enemy=enemy)

        screen.ontimer(lambda: enemy_shot(enemies), enemies_shot_cd)

# ======================================== UI & POPUPS ========================================

ui_lives = []

def init_lives():
    [ui_lives.append(PlayerLife(initial_pos=(SCREEN_WIDTH*-1//2+40*(n*1), SCREEN_HEIGHT*-1//2+20))) for n in range(player.lives+1)]
    try:
        ui_lives[0].lose_life()
    except Exception as e:
        print("Error: ", e)

init_lives()

# Create a window for the game start
def start_game_popup():
    root = Tk()
    root.withdraw()
    root.attributes("-topmost", True)

    # Ask the user whether they want to play again or quit
    start = messagebox.askyesno(
        title="Welcome to Turtle Invaders",
        message="Are you ready to Play?\n\nPress Yes to start\n\nMove the Player with '↔' or 'a' & 'd'"
    )
    root.destroy()

    if not start:
        screen.bye()

def game_over_popup():
    root = Tk()
    root.withdraw()
    root.attributes("-topmost", True)

    play_again = messagebox.askyesno(
        title="Game Over",
        message=f"Score: {score}\n\nDo you want to play again?"
    )

    root.destroy()

    if not play_again:
        screen.bye()

    restart()

# ======================================== PROJECTILE ========================================

def init_projectile(source: str, enemy=None):
    if len(projectiles) < 1 and source == 'player':
        projectile = Projectile(player.pos())
        projectile.move()
        projectiles.append(projectile)
    elif len(enemies_projectiles) < game_level + 2 and source == 'enemy':
        projectile = Projectile(enemy.pos())
        projectile.color(enemy.enemy_color)
        projectile.move(direction_mod=-1)
        enemies_projectiles.append(projectile)

def check_out_of_bounds(projectile):
    if projectile.ycor() > SCREEN_HEIGHT // 2:
        projectile.destroy()
        projectiles.remove(projectile)
    elif projectile.ycor() < SCREEN_HEIGHT // 2 * -1:
        projectile.destroy()
        enemies_projectiles.remove(projectile)
        print('removed')

def check_player_hit():
    for projectile in enemies_projectiles:
        if projectile.distance(player) < (20*size_modifier):
            ui_lives[-1].lose_life()
            ui_lives.remove(ui_lives[-1])
            enemies_projectiles.remove(projectile)
            projectile.destroy()
            if player.death():
                game_over_popup()
                print('player hit')

def check_enemy_hit(projectile):
    [destroy_enemy(row, enemy, projectile) for row in enemies_list for enemy in row if projectile.distance(enemy) < (20*.8*size_modifier)]

    if all(len(row) == 0 for row in enemies_list):
        restart(game_level+1)

def check_projectiles_pos():
    for projectile in projectiles:
        check_out_of_bounds(projectile)
        check_enemy_hit(projectile)
    for projectile in enemies_projectiles:
        check_out_of_bounds(projectile)
        check_player_hit()

# ======================================== GAME RESET/RESTART ========================================

def restart(level=1):
    global score
    global player
    global enemies_list
    global game_level
    global enemies_direction
    global enemies_shot_cd
    global ui_lives

    game_level = level

    # - PLAYER RESET
    player.hideturtle()
    player.clear()
    player = Player()

    player.lives = 2

    screen.onkeypress(key="Right", fun=player.go_right)
    screen.onkeypress(key="d", fun=player.go_right)
    screen.onkeypress(key="Left", fun=player.go_left)
    screen.onkeypress(key="a", fun=player.go_left)

    # Shoots the player projectiles
    screen.onkeypress(key="space", fun=lambda: init_projectile('player'))

    # - ENEMIES RESET
    [enemy.destroy() for row in enemies_list for enemy in row]
    enemies_list.clear()

    enemies_list = init_enemies(game_level // 3 + 1)

    enemies_direction = {'dir': 'right'}

    # - PROJECTILES RESET
    [projectile.destroy() for projectile in enemies_projectiles]
    enemies_projectiles.clear()

    try:
        projectiles[0].destroy()
        projectiles.clear()
    except Exception as e:
        print('Error: ', e)


    # - UI RESET
    updated_score = 0

    if level > 1:
        enemies_shot_cd = int(enemies_shot_cd * .8)
        updated_score = score.score
    score = Score(SCREEN_WIDTH, SCREEN_HEIGHT, high_score, score=updated_score)

    ui_lives = []

    init_lives()

    enemy_shot(enemies_list)
    enemies_movement(enemies_direction['dir'], enemies_list)

# ======================================== PLAYER INPUTS ========================================

screen.onkeypress(key="Right", fun=player.go_right)
screen.onkeypress(key="d", fun=player.go_right)
screen.onkeypress(key="Left", fun=player.go_left)
screen.onkeypress(key="a", fun=player.go_left)

# Shoots the player projectiles
screen.onkeypress(key="space", fun=lambda: init_projectile('player'))

def destroy_enemies():
    for row in enemies_list:
        for enemy in row:
            if enemy != enemies_list[0][0]:
                enemy.destroy()
                enemies_list[enemies_list.index(row)].remove(enemy)

screen.onkeypress(key='l', fun=destroy_enemies)

# ======================================== MAIN ========================================

def main():
    is_running = True

    start_game_popup()

    enemy_shot(enemies_list)
    enemies_movement(enemies_direction['dir'], enemies_list)

    while is_running:
        check_projectiles_pos()
        screen.update()

if __name__ == '__main__':
    main()