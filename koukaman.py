import pygame as pg
import random
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))
import pygame.time
import pygame.mixer

# Pygameの初期化
pg.init()
# pgの初期化
pg.init()

# 色をRGBで定義。RGB: Red, Green, Blueの値を0~255の256段階で表す
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (0,0,255)
GREEN = (0,255,0)
RED = (255,0,0)
YELLOW = (255,255,0)

class Score:
    """
    コイン取ったらスコア加算
    """
    def __init__(self):
        self.font = pg.font.Font(None, 35)
        self.color = (255, 255, 255)
        self.value = 0
        self.image = self.font.render(f"SCORE: {self.value}", 0, self.color)
        self.rect = self.image.get_rect()
        self.rect.center = width/2, 15

    def update(self, screen: pg.Surface):
        self.image = self.font.render(f"SCORE: {self.value}", 0, self.color)
        screen.blit(self.image, self.rect)


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
        self.image.set_colorkey((0,0,0))
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
        self.hyper = 0

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




class MusicPlayer:
    """
    BGMを追加するクラス
    """
    def __init__(self, intro_file, loop_file):  
        """
        BGMをロード、追加する関数
        """
        self.intro_file = intro_file
        self.loop_file = loop_file
        pygame.mixer.init()
        pygame.mixer.music.load(self.intro_file)
        pygame.mixer.music.play()

    def update(self):
        """
        BGMをループさせる関数
        """
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load(self.loop_file)
            pygame.mixer.music.play(-1)

    def stop(self):
        """
        BGMを止める関数
        """
        pygame.mixer.music.stop()

    def play_once(self, filename):
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()


def enviroment():
    """
    ステージを定義
    """
    grid = (
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
        (0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,2,0),
        (1,3,1,1,1,1,1,1,1,3,1,1,1,1,1,1,1,3,1,1,1,1,1,3,1),
        (0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,2,0),
        (0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,2,0),
        (0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,2,0)
    )
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

# ウィンドウ設定
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

# アイテムの設定
item_size = 15
item_frame = 0
items = [{"x": random.randint(0, width - item_size), "y": random.randint(0, height - item_size)} for _ in range(1)]

# ゲームループ
running = True
game_clear = False
game_over = False
score = Score()

class Life:
    """
    残機を表示させるクラス
    """  
    def __init__(self):
        self.value = 3
        self.count = 0  # 無敵時間（フレーム）
        self.image = pg.image.load("fig/heart.png")
        self.image = pg.transform.scale(self.image, (20, 20))

    def update(self, screen):
        for i in range(self.value):
            screen.blit(self.image, (10 + i * 35, height - 40))

life = Life()

# メインループ
bgm = MusicPlayer("fig/levelintro.wav", "fig/default.wav")
pygame.time.wait(5000)
bgm.update()
while running:

    key_lst = pg.key.get_pressed()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

   

    # 無敵時間カウント
    if life.count > 0:
        life.count -= 1


    # コインの収集
    for coin in coins[:]:
        if abs(bird.rect.centerx - coin["x"]) < coin_size and abs(bird.rect.centery - coin["y"]) < coin_size:
            coins.remove(coin)
            score.value += 10


    # アイテムの収集
    for item in items[:]:
        if abs(bird.rect.centerx - item["x"]) < item_size and abs(bird.rect.centery - item["y"]) < item_size:
            items.remove(item)
            bird.hyper = 1
            bird.speed = 10
            item_frame = 500

    # 敵との衝突判定
    for enemy in pg.sprite.spritecollide(bird, emys, True): 
            if bird.hyper == 1:
                emys.remove(enemy)
            if bird.hyper == 0:
                #---------ライフを１減らし、０になったらゲームオーバー---------
                if life.count == 0:
                    life.value -= 1
                    life.count = fps  # 無敵時間1秒
                    if life.value == 0:
                        game_over = True
                        running = False
                #------------------------------------------------------------

    # コインがすべて収集された場合
    if not coins:
        game_clear = True
        running = False
    
    # アイテムの効果時間
    if bird.hyper == 1:
        item_frame -= 1
    if item_frame == 0:
        bird.hyper = 0
        bird.speed = 5



    # 画面の描画
    win.fill(black)
    #pg.draw.rect(win, yellow, (bird.rect.centerx, bird.rect.centery, bird.size, bird.size))
    for coin in coins:
        pg.draw.rect(win, blue, (coin["x"], coin["y"], coin_size, coin_size))
    for item in items:
        pg.draw.rect(win, red, (item["x"], item["y"], item_size, item_size))
    
    # こうかとんのupdate
    bird.update(key_lst,win)
    # 敵のupdate
    emys.update()
    emys.draw(win)
    score.update(win)
    life.update(win)
    pg.display.update()
    clock.tick(fps)

# ゲームクリアの表示
if game_clear:
    bgm.stop()
    bgm.play_once("fig/death.wav") 
    win.fill(black)
    text = font.render("Game Clear", True, white)
    text_rect = text.get_rect(center=(width / 2, height / 2))
    win.blit(text, text_rect)
    pg.display.update()
    pg.time.wait(3000)

# ゲームオーバーの表示
if game_over:
    bgm.stop()  # 通常BGMを止める
    bgm.play_once("fig/death.wav")  # ゲームオーバーBGMを1回だけ再生
    win.fill(black)
    text = font.render("Game Over", True, white)
    text_rect = text.get_rect(center=(width / 2, height / 2))
    win.blit(text, text_rect)
    pg.display.update()
    pg.time.wait(3000)


pg.quit()
pg.quit()
