import os
import random
import sys
import time
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA ={
    pg.K_UP:(0, -5),
    pg.K_DOWN:(0, +5),
    pg.K_LEFT:(-5, 0),
    pg.K_RIGHT:(+5, 0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとんRectかばくだんRect
    戻り値：タプル（横方向判定結果, 縦方向判定結果）
    画面内ならTrue, 画面外ならFalse
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:  # 横方向にはみ出ていたら
        yoko = False
    if rct.top < 0 or HEIGHT <rct.bottom:  # 縦方向にはみ出ていたら
        tate = False
    return yoko, tate


def gameover(screen: pg.Surface) ->None:
    """
    ゲームオーバー画面を表示し、5秒待機する
    """
    black_sfc = pg.Surface((WIDTH, HEIGHT))
    black_sfc.fill((0, 0, 0))
    black_sfc.set_alpha(200)
    screen.blit(black_sfc, (0, 0))
    font = pg.font.Font(None, 120)
    text_sfc = font.render("Game Over", True, (255, 255, 255))
    text_rct = text_sfc.get_rect(center=(WIDTH/2, HEIGHT/2))
    screen.blit(text_sfc, text_rct)
    cry_img = pg.image.load("fig/8.png")
    cry_img = pg.transform.rotozoom(cry_img, 0, 1.2)
    cry_rct1 = cry_img.get_rect(center = (WIDTH/2 -270, HEIGHT/2))
    cry_rct2 = cry_img.get_rect(center = (WIDTH/2 + 270, HEIGHT/2))
    screen.blit(cry_img, cry_rct1)
    screen.blit(cry_img, cry_rct2)
    pg.display.update()
    time.sleep(5)


def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    """
    時間とともに爆弾が拡大、加速する
    爆弾は10段階
    """
    bb_imgs = []
    bb_accs = [a for a in range(1,11)]
    for r in range(1,11):
        bb_img = pg.Surface((20*r, 20*r))
        bb_img.set_colorkey((0, 0, 0))
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
        bb_imgs.append(bb_img)
    return bb_imgs, bb_accs


def get_kk_imgs() -> dict[tuple[int, int], pg.Surface]:
    """
    移動量タプルをキー
    rotozoomしたこうかとん画像Surfaceを値とする辞書を返す
    """
    kk_img0 = pg.image.load("fig/3.png")
    kk_img1 = pg.transform.flip(kk_img0, True, False)
    kk_imgs = {
        (0, 0):kk_img0,
        (0, -5):pg.transform.rotozoom(kk_img1, 90, 0.9),
        (0, +5):pg.transform.rotozoom(kk_img0, 90, 0.9),
        (-5, 0):kk_img0,
        (+5, 0):kk_img1,
        (+5, -5):pg.transform.rotozoom(kk_img1, 45, 0.9),
        (-5, -5):pg.transform.rotozoom(kk_img0, -45, 0.9),
        (-5, +5):pg.transform.rotozoom(kk_img0, 45, 0.9),
        (+5, +5):pg.transform.rotozoom(kk_img1, -45, 0.9),
    }
    return kk_imgs


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    kk_imgs = get_kk_imgs()
    bb_img = pg.Surface((20,20))    
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    bb_img.set_colorkey((0, 0, 0))
    bb_imgs, bb_accs = init_bb_imgs()
    bb_rct = bb_img.get_rect()
    bb_rct.centerx = random.randint(0, WIDTH)
    bb_rct.centery = random.randint(0, HEIGHT)
    vx, vy = +5, +5
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0])
        if kk_rct.colliderect(bb_rct):
            gameover(screen)
            return  # ゲームオーバー

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5
        kk_rct.move_ip(sum_mv)
        kk_img = kk_imgs.get(tuple(sum_mv), kk_imgs[(0, 0)])
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)
        avx = vx*bb_accs[min(tmr//500, 9)]
        avy = vy*bb_accs[min(tmr//500, 9)]
        bb_img = bb_imgs[min(tmr//500, 9)]
        bb_rct.move_ip(avx, avy)
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
