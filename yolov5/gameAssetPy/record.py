
import pygame
import sys
# 初始化pygame
pygame.init()
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("First Game!")
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)
HEALTH_FONT = pygame.font.SysFont('SimSun', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)
INPUT_FONT = pygame.font.Font(None, 32)
# 开始界面

# record.py
def draw_text(surface, text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_surface, text_rect)
def save_username(username1, username2):
    # 打开文本文件以附加模式
    with open("usernames.txt", "a") as file:
        # 将用户名写入文件，每个用户名占一行
        if username1:
            file.write(username1 + "\n")
        if username2:
            file.write(username2 + "\n")

# record.py

def handle_input(events,username1, username2,active_box):
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                # 切换活动文本框
                active_box = 1 if active_box == 2 else 2
            # elif event.key == pygame.K_RETURN:
            #     # 按下回车键保存用户名并清空文本框
            #     save_username(username1, username2)
            #     username1 = ""
            #     username2 = ""
            elif event.key == pygame.K_BACKSPACE:
                # 按下退格键删除字符
                if active_box == 1:
                    username1 = username1[:-1]
                elif active_box == 2:
                    username2 = username2[:-1]
            elif pygame.K_0 <= event.key <= pygame.K_9:
                # 捕获数字键事件
                if active_box == 1:
                    username1 += chr(event.key)
                elif active_box == 2:
                    username2 += chr(event.key)
            else:
                # 捕获其他字符，但排除回车键和Tab键
                if event.key not in [pygame.K_RETURN, pygame.K_TAB, pygame.K_SPACE]:
                    if active_box == 1:
                        username1 += event.unicode
                    elif active_box == 2:
                        username2 += event.unicode

    return username1, username2, active_box

# 其他函数和代码继续写在下面

def draw_start_screen_jdj(username1="", username2="",fg=0):
    WIN.fill(WHITE)
    if fg==1:
        alert_text = HEALTH_FONT.render("保存成功，请开始游戏！", 1, GREEN)
    elif fg==2:
        alert_text = HEALTH_FONT.render("请输入另一玩家用户名！", 1, RED)
    elif fg==3:
        alert_text = HEALTH_FONT.render("请输入用户名！", 1, RED)
    start_text = HEALTH_FONT.render("开始游戏", 1, BLACK)
    start_text2 = HEALTH_FONT.render("（按回车键保存用户名，按空格键开始游戏）", 1, BLACK)
    start_text_width = start_text.get_width()
    screen_center_x = WIDTH // 2
    screen_center_y = HEIGHT // 2

    WIN.blit(start_text, (screen_center_x - start_text_width // 2, screen_center_y - start_text.get_height() // 2-150))
    vertical_distance = start_text.get_height() - start_text2.get_height() + 50
    if fg!=0:
        WIN.blit(alert_text, (screen_center_x - alert_text.get_width() // 2, screen_center_y + vertical_distance // 2+30))
    WIN.blit(start_text2, (screen_center_x - start_text2.get_width() // 2, screen_center_y + vertical_distance // 2+80))

    # 绘制两个输入框
    pygame.draw.rect(WIN, BLACK, (screen_center_x - 150, screen_center_y - 100, 300, 50), 2)
    # 第二个输入框
    pygame.draw.rect(WIN, BLACK, (screen_center_x - 150, screen_center_y - 30, 300, 50), 2)

    player1_text = HEALTH_FONT.render("Player 1:", 1, BLACK)
    player2_text = HEALTH_FONT.render("Player 2:", 1, BLACK)

    # 设置文本框的位置，使其在输入框前方并与输入框的顶部对齐
    player1_text_pos = (screen_center_x - 150 - player1_text.get_width(), screen_center_y - 100)
    player2_text_pos = (screen_center_x - 150 - player2_text.get_width(), screen_center_y - 30)

    WIN.blit(player1_text, player1_text_pos)
    WIN.blit(player2_text, player2_text_pos)

    # 绘制已输入的用户名
    draw_text(WIN, username1, HEALTH_FONT, BLACK, screen_center_x - 145, screen_center_y - 95)
    draw_text(WIN, username2, HEALTH_FONT, BLACK, screen_center_x - 145, screen_center_y - 25)

    pygame.display.update()


def save_game_result(winner_text, username1, username2, red_health, yellow_health):
    # 读取整个文件
    with open("usernames.txt", "r") as f:
        user_scores = f.readlines()

    # 追加本次玩家的分数
    if winner_text == f"{username1} Wins!":
        user_scores.append(f"{username1},{yellow_health}\n")
        user_scores.append(f"{username2},{red_health}\n")
    else:
        user_scores.append(f"{username2},{red_health}\n")
        user_scores.append(f"{username1},{yellow_health}\n")

    # 过滤出包含有效分数的行，并按照分数排序
    valid_scores = [line for line in user_scores if "," in line]
    # valid_scores.sort(key=lambda x: int(x.split(",")[1]), reverse=True)
    valid_scores.sort(key=lambda x: float(x.split(",")[1]), reverse=True)
    # 将更新后的数据写回文件
    with open("usernames.txt", "w") as f:
        f.writelines(valid_scores)
#结束界面
def draw_end_screen_jdj(winner_text, red_health, yellow_health,username1,username2):
    WIN.fill(BLACK)
    winner_font = pygame.font.SysFont(None, 100)
    text = winner_font.render(winner_text, True, WHITE)
    WIN.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/2 - text.get_height()/2))
    continue_text = HEALTH_FONT.render("继续游戏（按C键）", 1, WHITE)
    quit_text = HEALTH_FONT.render("退出游戏（按Q键）", 1, WHITE)
    top_text = HEALTH_FONT.render("查看排行榜（按A键）", 1, WHITE)
    WIN.blit(continue_text, (WIDTH/2 - continue_text.get_width()/2, HEIGHT/2 + 50))
    WIN.blit(quit_text, (WIDTH/2 - quit_text.get_width()/2, HEIGHT/2 + 100))
    WIN.blit(top_text, (WIDTH / 2 - top_text.get_width() / 2, HEIGHT / 2 + 150))
    print(red_health)
    print(yellow_health)
    # 保存游戏结果
    save_game_result(winner_text, username1, username2, red_health, yellow_health)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    return 1;
                elif event.key == pygame.K_q:
                    return 2;
                elif event.key == pygame.K_a:
                    # 读取并显示前十名分数
                    draw_leaderboard()

def draw_leaderboard():
    WIN.fill(WHITE)
    screen_center_x = WIDTH // 2
    screen_center_y = HEIGHT // 2
    title = HEALTH_FONT.render("历史玩家排行", 1, BLACK)
    WIN.blit(title, (screen_center_x - title.get_width() // 2, screen_center_y - title.get_height() // 2-200))
    # 从 usernames.txt 文件中读取用户名和分数
    with open("usernames.txt", "r") as f:
        user_scores = f.readlines()

    # 显示前十名玩家的用户名和分数
    y = 80
    for i in range(min(10, len(user_scores))):
        username, score = user_scores[i].strip().split(",")
        name_text = INPUT_FONT.render(f"{i + 1}. {username} - {score}", True, BLACK)
        name_rect = name_text.get_rect()
        name_rect.midtop = (WIDTH // 2, y)
        WIN.blit(name_text, name_rect)
        y += 40

    pygame.display.update()

# 运行绘制开始屏幕的函数
draw_start_screen_jdj()