import os
import pygame as pg
import random


# pgの初期化
pg.init()
# ファイルパスについて
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# 色をRGBで定義。RGB: Red, Green, Blueの値を0~255の256段階で表す
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (0,0,255)
GREEN = (0,255,0)
RED = (255,0,0)


def check_bound(obj_rct: pg.Rect) -> tuple[bool, bool]:
    """
    オブジェクトが画面内or画面外を判定し，真理値タプルを返す関数
    引数：こうかとんや爆弾，ビームなどのRect
    戻り値：横方向，縦方向のはみ出し判定結果（画面内：True／画面外：False）
    """
    yoko, tate = True, True
    if obj_rct.left < 0 or width < obj_rct.right:
        yoko = False
    if obj_rct.top < 0 or height < obj_rct.bottom:
        tate = False
    return yoko, tate

class Enemy(pg.sprite.Sprite):
    """
    敵（ゴースト）
    """
    def __init__(self):
        """
        敵初期化。Surfaceを作成
        引数無し
        """
        super().__init__()
        self.image = pg.transform.rotozoom(pg.image.load("fig/ghost.png"),0,0.1)
        self.rect = self.image.get_rect()
        self.rect.centerx = random.randint(0, width - enemy_size)
        self.rect.centery = random.randint(0, height - enemy_size)        
        
    def update(self):
        """
        ゴーストの位置を更新
        引数 screen :画面Surface
        """
        if self.rect.centerx < bird.rect.centerx:
            self.rect.centerx += enemy_speed
        elif self.rect.centerx > bird.rect.centerx:
            self.rect.centerx -= enemy_speed
        if self.rect.centery < bird.rect.centery:
            self.rect.centery += enemy_speed
        elif self.rect.centery > bird.rect.centery:
            self.rect.centery -= enemy_speed
        # self.rect = self.imgs.get_rect()
        # screen.blit(self.image,self.rect)
        

class Bird(pg.sprite.Sprite):
    """
    ゲームキャラクター（こうかとん）に関するクラス
    """
    delta = {  # 押下キーと移動量の辞書
        pg.K_UP: (0, -1),
        pg.K_DOWN: (0, +1),
        pg.K_LEFT: (-1, 0),
        pg.K_RIGHT: (+1, 0),
    }

    def __init__(self, num: int, xy: tuple[int, int]):
        """
        こうかとん画像Surfaceを生成する
        引数1 num：こうかとん画像ファイル名の番号
        引数2 xy：こうかとん画像の位置座標タプル
        """
        super().__init__()
        img0 = pg.transform.rotozoom(pg.image.load(f"fig/{num}.png"), 0, 0.9)
        img = pg.transform.flip(img0, True, False)  # デフォルトのこうかとん
        self.imgs = {
            (+1, 0): img,  # 右
            (+1, -1): pg.transform.rotozoom(img, 45, 0.9),  # 右上
            (0, -1): pg.transform.rotozoom(img, 90, 0.9),  # 上
            (-1, -1): pg.transform.rotozoom(img0, -45, 0.9),  # 左上
            (-1, 0): img0,  # 左
            (-1, +1): pg.transform.rotozoom(img0, 45, 0.9),  # 左下
            (0, +1): pg.transform.rotozoom(img, -90, 0.9),  # 下
            (+1, +1): pg.transform.rotozoom(img, -45, 0.9),  # 右下
        }
        self.dire = (+1, 0)
        self.image = self.imgs[self.dire]
        self.rect = self.image.get_rect()
        self.rect.center = xy
        self.speed = 5

    def change_img(self, num: int, screen: pg.Surface):
        """
        こうかとん画像を切り替え，画面に転送する
        引数1 num：こうかとん画像ファイル名の番号
        引数2 screen：画面Surface
        """
        self.image = pg.transform.rotozoom(pg.image.load(f"fig/{num}.png"), 0, 0.9)
        screen.blit(self.image, self.rect)

    def update(self, key_lst: list[bool], screen: pg.Surface):
        """
        押下キーに応じてこうかとんを移動させる
        引数1 key_lst：押下キーの真理値リスト
        引数2 screen：画面Surface
        """
        sum_mv = [0, 0]
        for k, mv in __class__.delta.items():
            if key_lst[k]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
    
        self.rect.move_ip(self.speed*sum_mv[0], self.speed*sum_mv[1])
        if check_bound(self.rect) != (True, True):
            self.rect.move_ip(-self.speed*sum_mv[0], -self.speed*sum_mv[1])
        if not (sum_mv[0] == 0 and sum_mv[1] == 0):
            self.dire = tuple(sum_mv)
            self.image = self.imgs[self.dire]
        screen.blit(self.image, self.rect)



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
                pg.draw.line(screen, BLUE , [j*32, i*32], [j*32+32,i*32], 3)
                pg.draw.line(screen, BLUE , [j*32, i*32+32], [j*32+32,i*32+32], 3)
            elif item == 2:
                pg.draw.line(screen, BLUE , [j*32, i*32], [j*32,i*32+32], 3)
                pg.draw.line(screen, BLUE , [j*32+32, i*32], [j*32+32,i*32+32], 3)

# ウィンドウの設定
width, height = 640, 480
win = pg.display.set_mode((width, height))
pg.display.set_caption("Pac-Man")

# 色の定義
black = (0, 0, 0)
white = (255, 255, 255)
yellow = (255, 255, 0)
red = (255, 0, 0)
blue = (0, 0, 255)

# フォントの設定
font = pg.font.Font(None, 74)

# フレームレート
clock = pg.time.Clock()
fps = 30

# パックマンの設定
bird = Bird(3,(width//2,height//2))
# pacman_size = 20
# pacman_x = width // 2
# pacman_y = height // 2
# pacman_speed = 5

# 敵のグループ作成
emys = pg.sprite.Group()
# 敵の設定
enemy_size = 20
enemy_speed = 2
for _ in range(3):
    emys.add(Enemy())

# コインの設定
coin_size = 10
coins = [{"x": random.randint(0, width - coin_size), "y": random.randint(0, height - coin_size)} for _ in range(10)]

# ゲームループ
running = True
game_clear = False
game_over = False



while running:

    key_lst = pg.key.get_pressed()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    # keys = pg.key.get_pressed()
    # if keys[pg.K_LEFT]:
    #     pacman_x -= pacman_speed
    # if keys[pg.K_RIGHT]:
    #     pacman_x += pacman_speed
    # if keys[pg.K_UP]:
    #     pacman_y -= pacman_speed
    # if keys[pg.K_DOWN]:
    #     pacman_y += pacman_speed

    # パックマンの画面外移動制限
    # pacman_x = max(0, min(width - pacman_size, pacman_x))
    # pacman_y = max(0, min(height - pacman_size, pacman_y))

    # 敵の移動
    # for enemy in enemies:
    #     if enemy["x"] < pacman_x:
    #         enemy["x"] += enemy_speed
    #     elif enemy["x"] > pacman_x:
    #         enemy["x"] -= enemy_speed
    #     if enemy["y"] < pacman_y:
    #         enemy["y"] += enemy_speed
    #     elif enemy["y"] > pacman_y:
    #         enemy["y"] -= enemy_speed

    # コインの収集
    for coin in coins[:]:
        if abs(bird.rect.centerx - coin["x"]) < coin_size and abs(bird.rect.centery - coin["y"]) < coin_size:
            coins.remove(coin)

    # 敵との衝突判定
    for enemy in pg.sprite.spritecollide(bird, emys, True):        
        game_over = True
        running = False


    # コインがすべて収集された場合
    if not coins:
        game_clear = True
        running = False

    # 画面の描画
    win.fill(black)
    # pg.draw.rect(win, yellow, (pacman_x, pacman_y, pacman_size, pacman_size))
    for coin in coins:
        pg.draw.rect(win, blue, (coin["x"], coin["y"], coin_size, coin_size))

    # こうかとんのupdate
    bird.update(key_lst,win)
    # 敵のupdate
    emys.update()
    emys.draw(win)
    pg.display.update()
    clock.tick(fps)

# ゲームクリアの表示
if game_clear:
    win.fill(black)
    text = font.render("Game Clear", True, white)
    text_rect = text.get_rect(center=(width / 2, height / 2))
    win.blit(text, text_rect)
    pg.display.update()
    pg.time.wait(3000)

# ゲームオーバーの表示
if game_over:
    win.fill(black)
    text = font.render("Game Over", True, white)
    text_rect = text.get_rect(center=(width / 2, height / 2))
    win.blit(text, text_rect)
    pg.display.update()
    pg.time.wait(3000)

pg.quit()
