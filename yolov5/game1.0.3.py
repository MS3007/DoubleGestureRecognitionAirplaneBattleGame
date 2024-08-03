import random
import sys

import pygame
import os
import time
from PIL import Image, ImageEnhance
from gameAssetPy import bullet_counteracting as bc,bgm,record,five_bullets_h,obstacles_nm,initialize_spaceships_h
from gestureDetect import yolo_dec as yd
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("手势识别双人太空飞机大战")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)


# hsz_nm
image_0 = pygame.image.load(os.path.join('Assets', '0.png'))
image_1 = pygame.image.load(os.path.join('Assets', '1.png'))
image_2 = pygame.image.load(os.path.join('Assets', '2.png'))
image_3 = pygame.image.load(os.path.join('Assets', '3.png'))
Flush_Time = 10
#*
protect_img = pygame.image.load(os.path.join('Assets', 'protect.png'))
BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)
BULLET_HIT_SOUND = pygame.mixer.Sound('Assets/Grenade+1.mp3')
BULLET_FIRE_SOUND = pygame.mixer.Sound('Assets/Gun+Silencer.mp3')
FIVE_PLANE_SOUND = pygame.mixer.Sound('Assets/5plane.mp3')
G_BOOM_SOUND = pygame.mixer.Sound('Assets/gboom.mp3')
WIN_SOUND = pygame.mixer.Sound('Assets/win.mp3')
HP_UP_SOUND = pygame.mixer.Sound('Assets/hpup.mp3')
PROTECT_SOUND = pygame.mixer.Sound('Assets/protection.mp3')
UPFIRE_SOUND = pygame.mixer.Sound('Assets/upfire.mp3')

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

FPS = 60
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 3
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2
destination_over = pygame.USEREVENT + 3
boom_over = pygame.USEREVENT + 4
boom_yellow_hit=pygame.USEREVENT + 5
boom_red_hit=pygame.USEREVENT + 6
yellow_cooldown_over = pygame.USEREVENT + 7
red_cooldown_over = pygame.USEREVENT + 8

# hsz_nm
YELLOW_EAT = pygame.USEREVENT + 9  #!黄色吃到血包
RED_EAT = pygame.USEREVENT + 10  #!红色吃到血包
YELLOW_FIVE=False
RED_FIVE = False
#*

# 加载GIF图像并缩放
def load_and_scale_gif(filename, target_size):
    frames = []
    gif = Image.open(filename)
    gif_frames = gif.n_frames
    for frame_number in range(gif_frames):
        gif.seek(frame_number)
        frame_rgba = gif.convert("RGBA")  # 将 GIF 图像转换为 RGBA 模式
        frame_surface = pygame.image.fromstring(frame_rgba.tobytes(), frame_rgba.size, frame_rgba.mode)
        scaled_surface = pygame.transform.scale(frame_surface, target_size)
        frames.append(scaled_surface)

    return frames
#加载并缩放GIF图像到int(SPACESHIP_WIDTH*0.7), int(SPACESHIP_HEIGHT*0.7)像素大小
destination_frames = load_and_scale_gif("Assets/destination.gif", (65, 50))
boom_frames = load_and_scale_gif("Assets/boom.gif", (55, 40))

YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

SPACE = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'space.jpg')), (WIDTH, HEIGHT))

def draw_window(red,reds, yellow,yellows, red_bullets, yellow_bullets, red_health, yellow_health, health_packages,tag,yellow_state,special_areas,red_state,obstacles, current_frame,yellow_skill_ready, red_skill_ready,username1,username2):
    """
    :param yellows:
    :param reds:
    :param red:
    :param yellow:
    :param red_bullets:
    :param yellow_bullets:
    :param red_health: 生命值
    :param yellow_health: 生命值
    :param health_packages:
    :param tag: 是画哪种类型的血包，0血包加血，1加强伤害，2无敌血包
    :param yellow_state:  左边状态，0普通，1加强伤害，2有盾牌
    :param red_state:   右边状态，0普通，1加强伤害，2有盾牌
    :return:
    """
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)

    red_health_text = HEALTH_FONT.render(
        f"{username2}"+"HP: " + str(round(red_health, 2)) , 1, WHITE)  # ！ 左边血，状态
        # "Health: " + str(red_health), 1, WHITE)    #zby原来的
    yellow_health_text = HEALTH_FONT.render(
        f"{username1}"+"HP: " + str(round(yellow_health, 2)) , 1, WHITE)  # ！ 右边血，状态
        # "Health: " + str(yellow_health), 1, WHITE) #zby原来的
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 50, 10))    #zby原来的是10
    WIN.blit(yellow_health_text, (10, 10))

    # 显示技能冷却状态
    yellow_skill_text = HEALTH_FONT.render(
        "State: " + str(yellow_state)+" Skill: " + ("Ready" if yellow_skill_ready else "Cooldown"), 1, WHITE)
    red_skill_text = HEALTH_FONT.render(
        "State: " + str(red_state)+" Skill: " + ("Ready" if red_skill_ready else "Cooldown"), 1, WHITE)
    WIN.blit(yellow_skill_text, (10, 50))
    WIN.blit(red_skill_text, (WIDTH - red_skill_text.get_width() - 10, 50))

    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    if yellow_state == 1:
        WIN.blit(pygame.transform.scale(protect_img, (55, 55)), (yellow.x-10, yellow.y))


    #hsz_nm
    if YELLOW_FIVE:
        for temp in yellows:
            WIN.blit(YELLOW_SPACESHIP, (temp.x, temp.y))
    #*
    WIN.blit(RED_SPACESHIP, (red.x, red.y))
    if red_state == 1:
        WIN.blit(pygame.transform.scale(protect_img, (55, 55)), (red.x, red.y))
    #hsz_nm
    if RED_FIVE:
        for temp in reds:
            WIN.blit(RED_SPACESHIP, (temp.x, temp.y))

    for package in health_packages:  # 假如血包有元素，就画出来
        # pygame.draw.rect(WIN, colors[tag], package)
        if tag == 0:
            WIN.blit(pygame.transform.scale(image_2, (40, 40)), package)
        elif tag == 1:
            WIN.blit(pygame.transform.scale(image_1, (40, 40)), package)
        elif tag == 2:
            WIN.blit(pygame.transform.scale(image_0, (40, 40)), package)
        else:
            WIN.blit(pygame.transform.scale(image_3, (40, 40)), package)
    #*
    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)
    #hsz_nm
    for obstacle in obstacles:
        WIN.blit(obstacle[1], obstacle[0])
    #*
    if special_areas:
        for area in special_areas:
            if 'destination' in area['state']:
                WIN.blit(destination_frames[current_frame], (area['x'], area['y']))
            elif 'boom' in area['state']:
                WIN.blit(boom_frames[current_frame], (area['x'], area['y']))  # 使用 BLEND_ADD 来正确处理透明度信息

    pygame.display.update()
def handle_special_skill(special_areas,active_range):
    player_range_y = (0, HEIGHT - 15)
    for _ in range(10):
        area_x = random.randint(active_range[0], active_range[1])
        area_y = random.randint(player_range_y[0], player_range_y[1])
        area = {
            'x': area_x,
            'y': area_y,
            'state': 'destination'
        }
        # print(area)
        special_areas.append(area)
def handle_movement(keys_pressed, yellow, red, yellows, reds):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0:  # LEFT
        yellow.x -= VEL
        for temp in yellows:
            temp.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x:  # RIGHT
        yellow.x += VEL
        for temp in yellows:
            temp.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0:  # UP
        yellow.y -= VEL
        for temp in yellows:
            temp.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 15:  # DOWN
        yellow.y += VEL
        for temp in yellows:
            temp.y += VEL

    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width:  # LEFT
        red.x -= VEL
        for temp in reds:
            temp.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH:  # RIGHT
        red.x += VEL
        for temp in reds:
            temp.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0:  # UP
        red.y -= VEL
        for temp in reds:
            temp.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 15:  # DOWN
        red.y += VEL
        for temp in reds:
            temp.y += VEL

def gesture_movement(gestureL,gestureR,yellow, red, yellows, reds):
    # if gestureL:
    #     Llabel, Lconfidence = gestureL
    # else:
    #     Llabel, Lconfidence = None, 0
    # if gestureR:
    #     Rlabel, Rconfidence = gestureR
    # else:
    #     Rlabel, Rconfidence = None, 0



        if gestureL == "left" and yellow.x - VEL > 0:  # LEFT
            yellow.x -= VEL
            for temp in yellows:
                temp.x -= VEL
        if gestureL == "right" and yellow.x + VEL + yellow.width < BORDER.x:  # RIGHT
            yellow.x += VEL
            for temp in yellows:
                temp.x += VEL
        if gestureL == "up" and yellow.y - VEL > 0:  # UP
            yellow.y -= VEL
            for temp in yellows:
                temp.y -= VEL
        if gestureL == "down" and yellow.y + VEL + yellow.height < HEIGHT - 15:  # DOWN
            yellow.y += VEL
            for temp in yellows:
                temp.y += VEL

        if gestureR == "left" and red.x - VEL > BORDER.x + BORDER.width:  # LEFT
            red.x -= VEL
            for temp in reds:
                temp.x -= VEL
        if gestureR == "right" and red.x + VEL + red.width < WIDTH:  # RIGHT
            red.x += VEL
            for temp in reds:
                temp.x += VEL
        if gestureR == "up" and red.y - VEL > 0:  # UP
            red.y -= VEL
            for temp in reds:
                temp.y -= VEL
        if gestureR == "down" and red.y + VEL + red.height < HEIGHT - 15:  # DOWN
            red.y += VEL
            for temp in reds:
                temp.y += VEL
def handle_bullets(yellow_bullets, red_bullets,health_packages, yellow, red):
    #hsz_nm
    if len(health_packages):
        if yellow.colliderect(health_packages[0]):  #colliderect为pygame中的函数，两个元素有重叠时就会返回1，否则返回0.重叠也就是飞船吃到血包
            pygame.event.post(pygame.event.Event(YELLOW_EAT))   # 发送黄色吃到血包的信号
            health_packages.clear()  # 屏幕上的血包被吃了，也就不要显示在屏幕
        else:
            if red.colliderect(health_packages[1]):
                pygame.event.post(pygame.event.Event(RED_EAT))
                health_packages.clear()
    #*
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)
def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() /
                         2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    #jdj_yll
    pygame.mixer.music.stop()  # 停止播放背景音乐
    #*
    pygame.time.delay(5000)


def check_collision(special_areas, yellow, red):
    # 用于记录是否已经发送过碰撞事件的标志
    red_hit_sent = False
    yellow_hit_sent = False

    for area in special_areas:
        if area['state'] == 'boom':
            # 检测红色玩家与特殊区域的碰撞
            if red.colliderect(pygame.Rect(area['x'], area['y'], 40, 25)) and not red_hit_sent:
                pygame.event.post(pygame.event.Event(boom_red_hit))
                red_hit_sent = True

            # 检测黄色玩家与特殊区域的碰撞
            if yellow.colliderect(pygame.Rect(area['x'], area['y'], 40, 25)) and not yellow_hit_sent:
                pygame.event.post(pygame.event.Event(boom_yellow_hit))
                yellow_hit_sent = True



def main():
    detector = yd()
    detector.open_cam("list.streams")
    run = False
    while True:
        #jdj_yll
        show_username1 = ""
        show_username2 = ""
        username1 = ""  # 在这里初始化 username1 和 username2
        username2 = ""

        #*

        # jdj_yll
        active_box = 1
        text_fg = 0
        while not run:
            events = pygame.event.get()  # 获取事件列表

            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    run = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if show_username1 != "" and show_username2 != "":
                            run = True
                        elif show_username1 == "" and show_username2 == "":
                            text_fg = 3
                    # 用户名输入部分
                    if event.key == pygame.K_RETURN:
                        if username1 != "" and username2 != "":
                            record.save_username(username1, username2)
                            show_username1 = username1
                            show_username2 = username2
                            text_fg = 1
                            # username1 = ""
                            # username2 = ""
                        elif username1 != "" or username2 != "":
                            text_fg = 2
            username1, username2, active_box = record.handle_input(events, username1, username2, active_box)
            record.draw_start_screen_jdj(username1, username2, text_fg)

            pygame.display.update()
        #hsz_nm
        global YELLOW_FIVE
        global RED_FIVE
        red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
        yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
        reds, yellows = initialize_spaceships_h.initialize_spaceships()
        #*
        # red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
        # yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
        yellow_active_range=[0, 410]
        red_active_range=[485, WIDTH-30]
        red_bullets = []
        yellow_bullets = []
        special_areas = []
        current_frame = 0
        #hsz_nm
        obstacles = []
        health_packages = []
        #*
        red_health = 10
        yellow_health = 10

        yellow_skill_ready = True
        red_skill_ready = True

        #hsz_nm
        red_state = 0  # 红色当前状态，0普通，1加强，2无敌
        yellow_state = 0
        #*

        # 背景音乐
        bgm.bgm()
        #*
        clock = pygame.time.Clock()

        #hsz_nm
        last_flash_time = time.time()  # 获取上一次跟新的时间
        last_flash_time_2 = last_flash_time
        tag = random.choice([0, 1, 2, 3])  # 随机选择一种状态
        health_packages.append(
            pygame.Rect(random.randint(100, 400), random.randint(100, 400), 20, 20))  # 将血包加入到血包数组，这个血包在左边随机位置出现
        health_packages.append(pygame.Rect(random.randint(500, 800), random.randint(100, 400), 20, 20))  # 右边随机位置出现
        #*
        # rms
        last_yellow_bullet_time = time.time()
        last_red_bullet_time = time.time()
        bullet_interval = 3
        #*
        detector.clear_latest_result()
        while run:
            gestureL, gestureR, skill= detector.get_latest_result()
            #hsz_nm
            if time.time() - last_flash_time_2 > 10:  # 加强/无敌取消(10s)
                last_flash_time_2 = time.time()
                yellow_state = 0
                red_state = 0
            if time.time() - last_flash_time > Flush_Time:  # ！血包刷新一次
                last_flash_time = time.time()  # ！
                health_packages.clear()  # ！就算没吃到，上一次的血包也要消失
                YELLOW_FIVE = False
                RED_FIVE = False
                tag = random.choice([0, 1, 2, 3])
                # tag=3
                health_packages.append(pygame.Rect(random.randint(100, 400), random.randint(100, 400), 20, 20))
                health_packages.append(pygame.Rect(random.randint(500, 800), random.randint(100, 400), 20, 20))
            #*
            clock.tick(FPS)
            if gestureL == "fire" and len(yellow_bullets) < MAX_BULLETS :
                if yellow_state == 2:
                    bullet = pygame.Rect(
                        yellow.x + yellow.width, yellow.y + yellow.height // 2 - 2, 15, 10)
                else:
                    bullet = pygame.Rect(
                        yellow.x + yellow.width, yellow.y + yellow.height // 2 - 2, 10, 5)
                yellow_bullets.append(bullet)
                # hsz_nm
                yellow_health -= 0  # ! 一颗子弹掉0.5滴血
                BULLET_FIRE_SOUND.play()
                five_bullets_h.shoot_yellow_bullets(yellow, yellow_bullets, YELLOW_FIVE)
                detector.clear_latest_result()
                # *

            if gestureR == "fire" and len(red_bullets) < MAX_BULLETS :
                if red_state == 2:
                    bullet = pygame.Rect(
                        red.x, red.y + red.height // 2 - 2, 15, 10)
                else:
                    bullet = pygame.Rect(
                        red.x, red.y + red.height // 2 - 2, 10, 5)
                red_bullets.append(bullet)
                # hsz_nm
                red_health -= 0  # !0.5血
                BULLET_FIRE_SOUND.play()
                five_bullets_h.shoot_red_bullets(red, red_bullets, RED_FIVE)
                detector.clear_latest_result()
                # *
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                    #jdj_yll
                    BULLET_FIRE_SOUND.play()
                    #*
                # if event.type == pygame.KEYDOWN:
                #     if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                #         if yellow_state == 2:
                #             bullet = pygame.Rect(
                #                 yellow.x + yellow.width, yellow.y + yellow.height // 2 - 2, 15, 10)
                #         else:
                #             bullet = pygame.Rect(
                #                 yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                #         yellow_bullets.append(bullet)
                #         #hsz_nm
                #         yellow_health -= 0.5  # ! 一颗子弹掉0.5滴血
                #         BULLET_FIRE_SOUND.play()
                #         five_bullets_h.shoot_yellow_bullets(yellow, yellow_bullets, YELLOW_FIVE)
                #         #*
                #
                #     if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                #         if red_state == 2:
                #             bullet = pygame.Rect(
                #                 red.x, red.y + red.height // 2 - 2, 15, 10)
                #         else:
                #             bullet = pygame.Rect(
                #                 red.x, red.y + red.height//2 - 2, 10, 5)
                #         red_bullets.append(bullet)
                #         #hsz_nm
                #         red_health -= 0.5  # !0.5血
                #         BULLET_FIRE_SOUND.play()
                #         five_bullets_h.shoot_red_bullets(red, red_bullets, RED_FIVE)
                #         #*

                if event.type == destination_over:
                    # print("event.type == destination_ver")
                    if special_areas:
                        for area in special_areas:
                            area['state'] = 'boom'

                if event.type == boom_over:
                    # print("event.type == boom_over")
                    G_BOOM_SOUND.stop()
                    special_areas.clear()

                if event.type == boom_red_hit:
                    red_health = round(red_health - 0.01, 2)

                if event.type == boom_yellow_hit:
                    yellow_health = round(yellow_health - 0.01, 2)

                if event.type == RED_HIT:
                    # red_health -= 1
                    BULLET_HIT_SOUND.play()
                    #hsz_nm
                    if red_state != 1:  # 假如红色状态不是1，也就是没用加强，就会有伤害
                        if yellow_state == 0:  # 黄色普通状态，攻击伤害1
                            red_health -= 1
                        else:
                            red_health -= 2  # 伤害2，加强状态
                    yellow_health += 0.5  # ! 打中再+0.5滴
                    #*

                if event.type == YELLOW_HIT:
                    BULLET_HIT_SOUND.play()
                    # yellow_health -= 1
                    #hsz_nm
                    if yellow_state != 1:
                        if red_state == 0:
                            yellow_health -= 1
                        else:
                            yellow_health -= 2
                    red_health += 0.5  # ! 打中再+0.5滴
                    #*
                #hsz_nm
                if event.type == RED_EAT:
                    if tag == 0:
                        HP_UP_SOUND.play()
                        red_health += 1
                    elif tag == 3:
                        FIVE_PLANE_SOUND.play()
                        RED_FIVE = True
                    else:
                        red_state = tag
                        yellow_state = 0
                        if tag == 1:
                            PROTECT_SOUND.play()
                        elif tag == 2:
                            UPFIRE_SOUND.play()

                if event.type == YELLOW_EAT:
                    if tag == 0:
                        HP_UP_SOUND.play()
                        yellow_health += 1
                    elif tag == 3:
                        FIVE_PLANE_SOUND.play()
                        YELLOW_FIVE = True
                    else:
                        yellow_state = tag
                        red_state = 0
                        if tag == 1:
                            PROTECT_SOUND.play()
                        elif tag == 2:
                            UPFIRE_SOUND.play()
                #*

                if event.type == yellow_cooldown_over:
                     yellow_skill_ready = True

                if event.type == red_cooldown_over:
                      red_skill_ready = True
            #jdj_yll
            winner_text = ""
            if red_health <= 0:
                winner_text = show_username1 + " Wins!"
                bgm.close_bgm()
                WIN_SOUND.play()


            if yellow_health <= 0:
                winner_text = show_username2 + " Wins!"
                bgm.close_bgm()
                WIN_SOUND.play()

            if winner_text != "":
                tp_fg=record.draw_end_screen_jdj(winner_text, red_health, yellow_health, show_username1, show_username2)
                if tp_fg==1:
                    # run= False
                    break
                elif tp_fg==2:
                    pygame.quit()
                    detector.close_cam()
                    sys.exit(0)

            #*

            keys_pressed = pygame.key.get_pressed()
            # handle_movement(keys_pressed, yellow, red, yellows, reds)


            # print("GestureL: ", gestureL)
            # print("GestureR: ", gestureR)
            gesture_movement(gestureL,gestureR, yellow, red, yellows, reds)


            # if keys_pressed[pygame.K_g] and not special_areas and yellow_skill_ready:
            if skill==1 and not special_areas and yellow_skill_ready:
                G_BOOM_SOUND.play()
                handle_special_skill(special_areas,red_active_range)
                pygame.time.set_timer(destination_over, 1080)
                pygame.time.set_timer(boom_over, 2500)
                current_frame = 0  # 重置当前帧索引
                yellow_skill_ready = False
                pygame.time.set_timer(yellow_cooldown_over, 15000)  # 设置黄色玩家技能冷却时间
                detector.clear_latest_result()
            # if keys_pressed[pygame.K_PERIOD] and not special_areas and red_skill_ready:
            if skill==2 and not special_areas and red_skill_ready:
                G_BOOM_SOUND.play()
                handle_special_skill(special_areas,yellow_active_range)
                pygame.time.set_timer(destination_over, 1080)
                pygame.time.set_timer(boom_over, 2500)
                current_frame = 0  # 重置当前帧索引
                red_skill_ready = False
                pygame.time.set_timer(red_cooldown_over, 15000)  # 设置红色玩家技能冷却时间
                detector.clear_latest_result()

            handle_bullets(yellow_bullets, red_bullets,health_packages, yellow, red)
            if special_areas:check_collision(special_areas,yellow,red)
            # draw_window(red, yellow, red_bullets,
            #             yellow_bullets, red_health, yellow_health, special_areas,current_frame,yellow_skill_ready, red_skill_ready)


            #hsz_nm
            # 障碍物相关的判定以及更新血量
            yellow_health, red_health = obstacles_nm.handle_collisions_nm(obstacles, yellow, red, yellow_bullets,
                                                                          red_bullets, yellow_health, red_health,
                                                                          yellow_state, red_state)
            # 生成障碍物
            obstacles_nm.default_obstacles_nm(obstacles)
            # draw_window(red, reds, yellow, yellows, red_bullets, yellow_bullets,
            #             red_health, yellow_health, health_packages, tag, yellow_state, red_state, obstacles)
            draw_window(red, reds, yellow, yellows, red_bullets,
                        yellow_bullets, red_health, yellow_health, health_packages, tag, yellow_state, special_areas,
                        red_state, obstacles, current_frame, yellow_skill_ready, red_skill_ready,username1,username2)
            #*
            current_frame = (current_frame + 1) % len(destination_frames)  # 更新当前帧索引

if __name__ == "__main__":

    main()
