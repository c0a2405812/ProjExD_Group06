import pygame
import random

# Pygameの初期化
pygame.init()

# 色をRGBで定義。RGB: Red, Green, Blueの値を0~255の256段階で表す
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (0,0,255)
GREEN = (0,255,0)
RED = (255,0,0)

def enviroment():
    """
    ステージを定義
    """
    grid = ((0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,2,0),
            (0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,2,0),
            (1,3,1,1,1,1,1,1,1,3,1,1,1,1,1,1,1,3,1,1,1,1,1,3,1),
            (0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,2,0),
            (0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,2,0),
            (0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,2,0),
            (1,3,1,1,1,1,1,1,1,3,1,1,1,1,1,1,1,3,1,1,1,1,1,3,1),
            (0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,2,0),
            (0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,2,0),
            (0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,2,0),
            (1,3,1,1,1,1,1,1,1,3,1,1,1,1,1,1,1,3,1,1,1,1,1,3,1),
            (0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,2,0),
            (0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,2,0),
            (0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,2,0),
            (1,3,1,1,1,1,1,1,1,3,1,1,1,1,1,1,1,3,1,1,1,1,1,3,1),
            (0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,2,0),
            (0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,2,0),
            (0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,2,0))

    return grid

def draw_enviroment(screen):
    for i,row in enumerate(enviroment()):
        for j,item in enumerate(row):
            # ステージで「1」「2」と定義されている場所に線を描画
            if item == 1:
                pygame.draw.line(screen, BLUE , [j*32, i*32], [j*32+32,i*32], 3)
                pygame.draw.line(screen, BLUE , [j*32, i*32+32], [j*32+32,i*32+32], 3)
            elif item == 2:
                pygame.draw.line(screen, BLUE , [j*32, i*32], [j*32,i*32+32], 3)
                pygame.draw.line(screen, BLUE , [j*32+32, i*32], [j*32+32,i*32+32], 3)

# ウィンドウの設定
width, height = 640, 480
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pac-Man")

# 色の定義
black = (0, 0, 0)
white = (255, 255, 255)
yellow = (255, 255, 0)
red = (255, 0, 0)
blue = (0, 0, 255)

# フォントの設定
font = pygame.font.Font(None, 74)

# フレームレート
clock = pygame.time.Clock()
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

# ゲームループ
running = True
game_clear = False
game_over = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        pacman_x -= pacman_speed
    if keys[pygame.K_RIGHT]:
        pacman_x += pacman_speed
    if keys[pygame.K_UP]:
        pacman_y -= pacman_speed
    if keys[pygame.K_DOWN]:
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

    # 画面の描画
    win.fill(black)
    pygame.draw.rect(win, yellow, (pacman_x, pacman_y, pacman_size, pacman_size))
    for enemy in enemies:
        pygame.draw.rect(win, red, (enemy["x"], enemy["y"], enemy_size, enemy_size))
    for coin in coins:
        pygame.draw.rect(win, blue, (coin["x"], coin["y"], coin_size, coin_size))

    pygame.display.update()
    clock.tick(fps)

# ゲームクリアの表示
if game_clear:
    win.fill(black)
    text = font.render("Game Clear", True, white)
    text_rect = text.get_rect(center=(width / 2, height / 2))
    win.blit(text, text_rect)
    pygame.display.update()
    pygame.time.wait(3000)

# ゲームオーバーの表示
if game_over:
    win.fill(black)
    text = font.render("Game Over", True, white)
    text_rect = text.get_rect(center=(width / 2, height / 2))
    win.blit(text, text_rect)
    pygame.display.update()
    pygame.time.wait(3000)

pygame.quit()
