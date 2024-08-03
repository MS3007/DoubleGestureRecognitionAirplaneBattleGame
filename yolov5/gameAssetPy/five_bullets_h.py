import pygame

def shoot_yellow_bullets(yellow, yellow_bullets, YELLOW_FIVE):
    if YELLOW_FIVE==True:
        bullet = pygame.Rect(
            yellow.x + yellow.width, yellow.y + yellow.height // 2 - 2 + 40, 10, 5)
        yellow_bullets.append(bullet)
        bullet = pygame.Rect(
            yellow.x + yellow.width, yellow.y + yellow.height // 2 - 2 + 80, 10, 5)
        yellow_bullets.append(bullet)
        bullet = pygame.Rect(
            yellow.x + yellow.width, yellow.y + yellow.height // 2 - 2 - 40, 10, 5)
        yellow_bullets.append(bullet)
        bullet = pygame.Rect(
            yellow.x + yellow.width, yellow.y + yellow.height // 2 - 2 - 80, 10, 5)
        yellow_bullets.append(bullet)

def shoot_red_bullets(red, red_bullets, RED_FIVE):
    if RED_FIVE==True:
        bullet=pygame.Rect(
            red.x, red.y + red.height // 2 - 2 + 40, 10, 5)
        red_bullets.append(bullet)
        bullet = pygame.Rect(
            red.x, red.y + red.height // 2 - 2 + 80, 10, 5)
        red_bullets.append(bullet)
        bullet = pygame.Rect(
            red.x, red.y + red.height // 2 - 2 - 40, 10, 5)
        red_bullets.append(bullet)
        bullet = pygame.Rect(
            red.x, red.y + red.height // 2 - 2 - 80, 10, 5)
        red_bullets.append(bullet)
