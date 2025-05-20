import pygame as pg
import random

# Pygameの初期化
pg.init()

# 色の定義
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (0,0,255)
GREEN = (0,255,0)
RED = (255,0,0)
YELLOW = (255, 255, 0)
GRAY = (100, 100, 100)

# Fix用
black = (0, 0, 0)
white = (255, 255, 255)
yellow = (255, 255, 0)
red = (255, 0, 0)
blue = (0, 0, 255)

# ウィンドウの設定
width, height = 640, 480
win = pg.display.set_mode((width, height))
pg.display.set_caption("Pac-Man")

# フォントの設定
font = pg.font.Font(None, 74)

# フレームレート
clock = pg.time.Clock()
fps = 30

# パックマンの設定
pacman_size = 20
pacman_x = width // 2
pacman_y = height // 2
pacman_speed = 5

# 敵の設定
enemy_size = 20
enemy_speed = 2
enemies = [{"x": random.randint(0, width - enemy_size), "y": random.randint(0, height - enemy_size)} for _ in range(3)]

# コインの設定
coin_size = 10
coins = [{"x": random.randint(0, width - coin_size), "y": random.randint(0, height - coin_size)} for _ in range(10)]

# WorldSettings
GRID_SIZE = 32 # (16 = 30*40)
grid = [[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,],
        [1,0,1,1,1,1,1,0,1,1,1,1,0,1,1,1,1,1,0,1,],
        [1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,],
        [1,0,0,0,1,1,1,0,1,1,1,1,0,1,1,1,0,0,0,1,],
        [1,0,1,0,1,0,0,0,0,0,0,1,0,0,0,1,0,1,0,1,],
        [1,0,1,0,1,0,1,1,1,0,1,1,0,1,0,1,0,1,0,1,],
        [0,0,0,0,1,0,1,0,0,0,0,0,0,1,0,1,0,0,0,0,],
        [1,0,1,0,1,0,1,0,1,1,0,1,1,1,0,1,0,1,0,1,],
        [1,0,1,0,1,0,0,0,1,0,0,0,0,0,0,1,0,1,0,1,],
        [1,0,0,0,1,1,1,0,1,1,1,1,0,1,1,1,0,0,0,1,],
        [1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,],
        [1,0,1,1,1,1,1,0,1,1,1,1,0,1,1,1,1,1,0,1,],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,],]

# Grid構成
def draw_enviroment(screen,grid):
    for index, row in enumerate(grid):
        for j, item in enumerate(row):
            if item == 1:
                rect = pg.Rect(j* GRID_SIZE, index * GRID_SIZE, GRID_SIZE, GRID_SIZE)
                pg.draw.rect(screen, WHITE, rect)

def draw_grid(screen):
    for x in range(0, width, GRID_SIZE):
        pg.draw.line(screen, GRAY, (x, 0), (x, height))
    for y in range(0, height, GRID_SIZE):
        pg.draw.line(screen, GRAY, (0, y), (width, y))

# ゲームループ
running = True
game_clear = False
game_over = False

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    keys = pg.key.get_pressed()
    if keys[pg.K_LEFT]:
        pacman_x -= pacman_speed
    if keys[pg.K_RIGHT]:
        pacman_x += pacman_speed
    if keys[pg.K_UP]:
        pacman_y -= pacman_speed
    if keys[pg.K_DOWN]:
        pacman_y += pacman_speed

    # パックマンの画面外移動制限
    pacman_x = max(0, min(width - pacman_size, pacman_x))
    pacman_y = max(0, min(height - pacman_size, pacman_y))

    # 敵の移動
    for enemy in enemies:
        if enemy["x"] < pacman_x:
            enemy["x"] += enemy_speed
        elif enemy["x"] > pacman_x:
            enemy["x"] -= enemy_speed
        if enemy["y"] < pacman_y:
            enemy["y"] += enemy_speed
        elif enemy["y"] > pacman_y:
            enemy["y"] -= enemy_speed

    # コインの収集
    for coin in coins[:]:
        if abs(pacman_x - coin["x"]) < coin_size and abs(pacman_y - coin["y"]) < coin_size:
            coins.remove(coin)

    # 敵との衝突判定
    for enemy in enemies:
        if abs(pacman_x - enemy["x"]) < enemy_size and abs(pacman_y - enemy["y"]) < enemy_size:
            game_over = True
            running = False

    # コインがすべて収集された場合
    if not coins:
        game_clear = True
        running = False

    # ScreenGrid
    win.fill(BLACK)
    draw_grid(win) 
    pg.draw.rect(win, YELLOW, (pacman_x, pacman_y, pacman_size, pacman_size))
    for enemy in enemies:
        pg.draw.rect(win, RED, (enemy["x"], enemy["y"], enemy_size, enemy_size))
    for coin in coins:
        pg.draw.rect(win, BLUE, (coin["x"], coin["y"], coin_size, coin_size))

    draw_enviroment(win, grid) #　壁描画
    pg.display.flip()
    pg.display.update()
    clock.tick(fps)





# ゲームクリアの表示
if game_clear:
    win.fill(BLACK)
    text = font.render("Game Clear", True, WHITE)
    text_rect = text.get_rect(center=(width / 2, height / 2))
    win.blit(text, text_rect)
    pg.display.update()
    pg.time.wait(3000)

# ゲームオーバーの表示
if game_over:
    win.fill(BLACK)
    text = font.render("Game Over", True, WHITE)
    text_rect = text.get_rect(center=(width / 2, height / 2))
    win.blit(text, text_rect)
    pg.display.update()
    pg.time.wait(3000)

pg.quit()
