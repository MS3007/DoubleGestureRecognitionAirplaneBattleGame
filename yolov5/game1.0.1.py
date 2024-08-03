import random
import pygame
import os
from PIL import Image, ImageEnhance
from gestureDetect import yolo_dec as yd
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("First Game!")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)
BULLET_HIT_SOUND = pygame.mixer.Sound('Assets/Grenade+1.mp3')
BULLET_FIRE_SOUND = pygame.mixer.Sound('Assets/Gun+Silencer.mp3')

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
    os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))

def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health, special_areas, current_frame,yellow_skill_ready, red_skill_ready):
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)

    red_health_text = HEALTH_FONT.render(
        "Health: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render(
        "Health: " + str(yellow_health), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))

    # 显示技能冷却状态
    yellow_skill_text = HEALTH_FONT.render(
        "Skill: " + ("Ready" if yellow_skill_ready else "Cooldown"), 1, WHITE)
    red_skill_text = HEALTH_FONT.render(
        "Skill: " + ("Ready" if red_skill_ready else "Cooldown"), 1, WHITE)
    WIN.blit(yellow_skill_text, (10, 50))
    WIN.blit(red_skill_text, (WIDTH - red_skill_text.get_width() - 10, 50))

    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

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
        print(area)
        special_areas.append(area)
def handle_movement(keys_pressed, yellow, red):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0:  # LEFT
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x:  # RIGHT
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0:  # UP
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 15:  # DOWN
        yellow.y += VEL

    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width:  # LEFT
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH:  # RIGHT
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0:  # UP
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 15:  # DOWN
        red.y += VEL

def yollow_gesture(label,confidence,yellow):
    if float(confidence) > 0.60:
        if label == "left" and yellow.x - VEL > 0:  # LEFT
            yellow.x -= VEL
        if label == "right" and yellow.x + VEL + yellow.width < BORDER.x:  # RIGHT
            yellow.x += VEL
        if label == "up" and yellow.y - VEL > 0:  # UP
            yellow.y -= VEL
        if label == "down" and yellow.y + VEL + yellow.height < HEIGHT - 15:  # DOWN
            yellow.y += VEL

def red_gesture(label,confidence,red):
    if float(confidence) > 0.60:
        if label == "left" and red.x - VEL > BORDER.x + BORDER.width:  # LEFT
            red.x -= VEL
        if label == "right" and red.x + VEL + red.width < WIDTH:  # RIGHT
            red.x += VEL
        if label == "up" and red.y - VEL > 0:  # UP
            red.y -= VEL
        if label == "down" and red.y + VEL + red.height < HEIGHT - 15:  # DOWN
            red.y += VEL
def handle_bullets(yellow_bullets, red_bullets, yellow, red):
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
    while True:
        red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
        yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
        yellow_active_range=[0, 410]
        red_active_range=[485, WIDTH-30]
        red_bullets = []
        yellow_bullets = []
        special_areas = []
        current_frame = 0
        red_health = 10
        yellow_health = 10

        yellow_skill_ready = True
        red_skill_ready = True



        clock = pygame.time.Clock()
        run = True

        while run:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                        bullet = pygame.Rect(
                            yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                        yellow_bullets.append(bullet)

                    if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                        bullet = pygame.Rect(
                            red.x, red.y + red.height//2 - 2, 10, 5)
                        red_bullets.append(bullet)

                if event.type == destination_over:
                    print("event.type == destination_ver")
                    if special_areas:
                        for area in special_areas:
                            area['state'] = 'boom'

                if event.type == boom_over:
                    print("event.type == boom_over")
                    special_areas.clear()

                if event.type == boom_red_hit:
                    red_health = round(red_health - 0.01, 2)

                if event.type == boom_yellow_hit:
                    yellow_health = round(yellow_health - 0.01, 2)

                if event.type == RED_HIT:
                    red_health -= 1

                if event.type == YELLOW_HIT:
                    yellow_health -= 1

                if event.type == yellow_cooldown_over:
                     yellow_skill_ready = True

                if event.type == red_cooldown_over:
                      red_skill_ready = True
            winner_text = ""
            if red_health <= 0:
                winner_text = "Yellow Wins!"

            if yellow_health <= 0:
                winner_text = "Red Wins!"

            if winner_text != "":
                draw_winner(winner_text)
                break

            keys_pressed = pygame.key.get_pressed()
            # handle_movement(keys_pressed, yellow, red)

            gestureL, gestureR = detector.get_latest_result()
            print("GestureL: ", gestureL)
            print("GestureR: ", gestureR)
            if gestureL:
                Llabel, Lconfidence = gestureL
                yollow_gesture(Llabel, Lconfidence, yellow)
            if gestureR:
                Rlabel, Rconfidence = gestureR
                red_gesture(Rlabel, Rconfidence, red)

            if keys_pressed[pygame.K_g] and not special_areas and yellow_skill_ready:
                handle_special_skill(special_areas,red_active_range)
                pygame.time.set_timer(destination_over, 1080)
                pygame.time.set_timer(boom_over, 2500)
                current_frame = 0  # 重置当前帧索引
                yellow_skill_ready = False
                pygame.time.set_timer(yellow_cooldown_over, 15000)  # 设置黄色玩家技能冷却时间
            if keys_pressed[pygame.K_PERIOD] and not special_areas and red_skill_ready:
                handle_special_skill(special_areas,yellow_active_range)
                pygame.time.set_timer(destination_over, 1080)
                pygame.time.set_timer(boom_over, 2500)
                current_frame = 0  # 重置当前帧索引
                red_skill_ready = False
                pygame.time.set_timer(red_cooldown_over, 15000)  # 设置红色玩家技能冷却时间

            handle_bullets(yellow_bullets, red_bullets, yellow, red)
            if special_areas:check_collision(special_areas,yellow,red)
            draw_window(red, yellow, red_bullets,
                        yellow_bullets, red_health, yellow_health, special_areas,current_frame,yellow_skill_ready, red_skill_ready)
            current_frame = (current_frame + 1) % len(destination_frames)  # 更新当前帧索引


if __name__ == "__main__":
    main()
