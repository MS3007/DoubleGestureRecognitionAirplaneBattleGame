import os
import pygame
import random

# 障碍物
OBSTACLES_TIMER = 0
MAX_OBSTACLES = 4
THE_OBSTACLES_IMAGE = pygame.image.load(os.path.join("Assets", "main_meteorite_1.png"))
STONE_CRACK_SOUND = pygame.mixer.Sound(os.path.join("Assets", "stone_crack.mp3"))

def default_obstacles_nm(obstacles):
    global OBSTACLES_TIMER
    current_time = pygame.time.get_ticks()
    # 障碍物的生成
    if current_time - OBSTACLES_TIMER >= 10000 and len(obstacles) < MAX_OBSTACLES:
        obstacle_width = random.randint(20, 100)
        obstacle_height = random.randint(20, 100)

        the_obstacle = pygame.transform.scale(THE_OBSTACLES_IMAGE, (obstacle_width, obstacle_height))

        obstacle_rect = the_obstacle.get_rect()
        obstacle_rect.x = random.randint(50, 850)
        obstacle_rect.y = random.randint(50, 450)
        obstacles.append((obstacle_rect, the_obstacle))
        OBSTACLES_TIMER = current_time


def handle_collisions_nm(obstacles, yellow, red, yellow_bullets, red_bullets, yellow_health, red_health, yellow_state, red_state):

    for obstacle in obstacles:
        # 飞船碰到障碍物会受到一点伤害
        # 因为我（hsz）有个无敌状态，所以碰到障碍物不会掉血，我给诺木这改了
        if yellow_state==1:
            if yellow.colliderect(obstacle[0]):
                obstacles.remove(obstacle)
                yellow_health -= 0
                STONE_CRACK_SOUND.play()
        else:
            if yellow.colliderect(obstacle[0]):
                obstacles.remove(obstacle)
                yellow_health -= 1
                STONE_CRACK_SOUND.play()
        if red_state == 1:
            if red.colliderect(obstacle[0]):
               obstacles.remove(obstacle)
               red_health -= 0
               STONE_CRACK_SOUND.play()
        else:
            if red.colliderect(obstacle[0]):
               obstacles.remove(obstacle)
               red_health -= 1
               STONE_CRACK_SOUND.play()
        # 障碍物被击中就会消失
        for bullet in yellow_bullets:
            if bullet.colliderect(obstacle[0]):
                obstacles.remove(obstacle)
                yellow_bullets.remove(bullet)
                STONE_CRACK_SOUND.play()
                break
        for bullet in red_bullets:
            if bullet.colliderect(obstacle[0]):
                obstacles.remove(obstacle)
                red_bullets.remove(bullet)
                STONE_CRACK_SOUND.play()
                break
    return yellow_health, red_health
