import os
import random
import pygame as pg
import pygame.time
import pygame.mixer

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
YELLOW = (255,255,0)
GRAY = (100,100,100)

def check_bound(obj_rct: pg.Rect, ) -> bool:
    """
    オブジェクトが壁に接しているかどうか判定し，真理値を返す関数
    引数：こうかとんのRect
    戻り値：オブジェクトの中心座標が白いかどうかの判定、もしくは
    横方向，縦方向のはみ出し判定結果（画面外、壁：False）
    """
    # ↓ここに衝突判定を追加↓
    hantei =  True
    if screen.get_at((obj_rct.centerx,obj_rct.centery)) == (255,255,255,255):
        hantei = False

    if obj_rct.left < 0 :
        hantei = False
        # Collision = 0
    if width < obj_rct.right:
        hantei = False
        # Collision = 1
    if obj_rct.top < 0 :
        hantei = False
        # Collision = 2
    if height < obj_rct.bottom:
        hantei = False
        # Collision = 3
    return hantei # Collision

    # ↑ここに衝突判定を追加↑

def check_bound2(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数：ゴーストrect
    戻り値：判定結果タプル、（横、縦）
    画面内ならTrue、画面外ならFlase
    """
    yoko, tate = True, True  # 横、縦方向用の変数
    #横方向判定
    if rct.left < 0 or width < rct.right:  # 画面外だったら
        yoko = False
    if rct.top < 0 or height < rct.bottom:  # 画面外だったら
        tate = False
    return yoko, tate

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
        self.image = pg.transform.rotozoom(pg.image.load("fig/ghost.png"),0,0.08)
        self.rect = self.image.get_rect()
        self.rect.centerx = random.randint(0,640)
        self.rect.centery = random.randint(0,480)
        self.vx = 4
        self.vy = 4
        
    def update(self):
        """
        ゴーストの位置を更新
        引数 screen :画面Surface
        """
        self.rect.move_ip(self.vx, self.vy)  # 爆弾の移動
        yoko, tate = check_bound2(self.rect)
        if not yoko:  # 左右どちらかにはみ出ていたら
            self.vx *= -1
        if not tate:  # 上下どちらかにはみ出ていたら
            self.vy *= -1
        screen.blit(self.image, self.rect)  # 爆弾の描画
        

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
        img0 = pg.transform.rotozoom(pg.image.load(f"fig/{num}.png"), 0, 0.6)
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
        self.speed = 4
        self.hyper = 0

    def change_img(self, num: int, screen: pg.Surface):
        """
        こうかとん画像を切り替え，画面に転送する
        引数1 num：こうかとん画像ファイル名の番号
        引数2 screen：画面Surface
        """
        self.image = pg.transform.rotozoom(pg.image.load(f"fig/{num}.png"), 0, 0.9)
        screen.blit(self.image, self.rect)

    def update(self, key_lst: list[bool], screen: pg.Surface): # Collision
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
        if check_bound(self.rect) != True: # 衝突判定による停止(False)
            self.rect.move_ip(-self.speed*sum_mv[0], -self.speed*sum_mv[1])

        if not (sum_mv[0] == 0 and sum_mv[1] == 0):
            self.dire = tuple(sum_mv)
            self.image = self.imgs[self.dire]
        screen.blit(self.image, self.rect)

class World(pg.sprite.Sprite):
    """
    マップについてのクラス
    """
    # WorldSettings
    def __init__(self):
        """
        マップの初期化
        引数無し
        """
        super().__init__()
        self.GRID_SIZE = 32 # (16 = 30*40)
        self.rect_list = [] # マップのrectを入れるリスト
        self.grid = [[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,],
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
        # コイン配置用のrect.center座標リスト作成
        for index, row in enumerate(self.grid):
            for j, item in enumerate(row):
                if item == 0:
                    rect = pg.Rect(j* self.GRID_SIZE, index * self.GRID_SIZE, self.GRID_SIZE, self.GRID_SIZE)
                    self.rect_list.append([rect.centerx-6,rect.centery-6])

    def draw(self, screen :pg.Surface):
        """
        壁とGridを作成
        引数 screen :画面Surface
        """
        for x in range(0, width, self.GRID_SIZE):
            pg.draw.line(screen, GRAY, (x, 0), (x, height))
        for y in range(0, height, self.GRID_SIZE):
            pg.draw.line(screen, GRAY, (0, y), (width, y)) 
        # Grid構成
        for index, row in enumerate(self.grid):
            for j, item in enumerate(row):
                if item == 1:
                    rect = pg.Rect(j* self.GRID_SIZE, index * self.GRID_SIZE, self.GRID_SIZE, self.GRID_SIZE)
                    pg.draw.rect(screen, WHITE, rect)

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
        pg.mixer.init() 
        pg.mixer.music.load(self.intro_file) 
        pg.mixer.music.play() 
 
    def update(self): 
        """ 
        BGMをループさせる関数 
        """ 
        if not pg.mixer.music.get_busy(): 
            pg.mixer.music.load(self.loop_file) 
            pg.mixer.music.play(-1) 
 
    def stop(self): 
        """ 
        BGMを止める関数 
        """ 
        pg.mixer.music.stop() 
 
    def play_once(self, filename): 
        pg.mixer.music.load(filename) 
        pg.mixer.music.play() 

class Score:
    """
    コイン取ったらスコア加算
    """
    def __init__(self):
        self.font = pg.font.Font(None, 35)
        self.color = (0, 0, 0)
        self.value = 0
        self.image = self.font.render(f"SCORE: {self.value}", 0, self.color)
        self.rect = self.image.get_rect()
        self.rect.center = width/2, 15

    def update(self, screen: pg.Surface):
        self.image = self.font.render(f"SCORE: {self.value}", 0, self.color)
        screen.blit(self.image, self.rect)

class Life:
    """
    残機を表示させるクラス
    """  
    def __init__(self):
        """
        残機の初期化と表示
        引数無し
        """
        self.value = 3
        self.count = 0  # 無敵時間（フレーム）
        self.image = pg.image.load("fig/heart.jpg")
        self.image = pg.transform.scale(self.image, (20, 20))

    def update(self, screen :pg.Surface):
        """
        残機の更新
        引数 screen :画面Surface
        """
        for i in range(self.value):
            screen.blit(self.image, (10 + i * 35, height - 30))

# ウィンドウ設定
width, height = 640, 480
screen = pg.display.set_mode((width, height))
pg.display.set_caption("Pac-Man")

# フォントの設定
font = pg.font.Font(None, 74)

# フレームレート
clock = pg.time.Clock()
fps = 30

# マップ作成
world = World()
worlds = pg.sprite.Group()
worlds.draw(screen)

# こうかとんインスタンス作成
bird = Bird(3,(width//2,height//2))

# 敵のグループ作成
# 敵人数設定
emys = pg.sprite.Group()
for _ in range(5):
    emys.add(Enemy())

# コインとアイテムの設定
coin_size = 15
coins = []
item_size = 15
item_frame = 0
items = []
Grid = [[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,],
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
for i in world.rect_list:
    coins.append({"x": i[0], "y": i[1]})
for _ in range(3):
    result = random.choice(coins)
    coins.remove(result)
    items.append(result)

# ゲームループ
running = True
game_clear = False
game_over = False

# BGMの設定
bgm = MusicPlayer("fig/levelintro.wav", "fig/default.wav") 
pg.time.wait(5000) 
bgm.update() 

# スコアの設定
score = Score()
# 残機の設定
life = Life()

# メインの処理
while running:

    key_lst = pg.key.get_pressed()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

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
            bird.speed = 6
            item_frame = 500

    if life.count > 0:
        life.count -= 1

    # 敵との衝突判定
    for enemy in pg.sprite.spritecollide(bird, emys, False):            
        if bird.hyper == 0:
            #---------ライフを１減らし、０になったらゲームオーバー---------
            if life.count == 0:
                life.value -= 1
                life.count = fps  # 無敵時間1秒
                if life.value == 0:
                    game_over = True
                    running = False
            #------------------------------------------------------------
        if bird.hyper == 1:
            enemy.kill()
            score.value += 50

    # コインがすべて収集された場合
    if not coins:
        game_clear = True
        running = False


    # 画面の描画
    screen.fill(BLACK)
    world.draw(screen)
    
    for coin in coins:
        pg.draw.rect(screen, YELLOW, (coin["x"], coin["y"], coin_size, coin_size))
    for item in items:
        pg.draw.rect(screen, RED, (item["x"], item["y"], item_size, item_size))
    
    # アイテムの効果時間
    if bird.hyper == 1:
        item_frame -= 1
    if item_frame == 0:
        bird.hyper = 0
        bird.speed = 4

    # こうかとんのupdate
    bird.update(key_lst,screen)
    # 敵のupdate
    emys.update()
    emys.draw(screen)
    # スコアのupdate
    score.update(screen)
    # 残機のupdate
    life.update(screen)
    pg.display.update()
    clock.tick(fps)

# ゲームクリアの表示
if game_clear:
    bgm.stop()  # 通常BGMを止める 
    bgm.play_once("fig/death.wav")  # ゲームオーバーBGMを1回だけ再生 
    screen.fill(BLACK)
    text = font.render("Game Clear", True, WHITE)
    text_rect = text.get_rect(center=(width / 2, height / 2))
    screen.blit(text, text_rect)
    pg.display.update()
    pg.time.wait(3000)

# ゲームオーバーの表示
if game_over:
    bgm.stop()  # 通常BGMを止める 
    bgm.play_once("fig/death.wav")  # ゲームオーバーBGMを1回だけ再生 
    screen.fill(BLACK)
    text = font.render("Game Over", True, WHITE)
    text_rect = text.get_rect(center=(width / 2, height / 2))
    screen.blit(text, text_rect)
    pg.display.update()
    pg.time.wait(3000)

pg.quit()