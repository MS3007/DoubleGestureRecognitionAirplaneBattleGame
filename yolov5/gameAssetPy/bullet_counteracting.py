import pygame
pygame.font.init()
pygame.mixer.init()
def bullet_counteracting(yellow_bullets, red_bullets, yellow, red):
    for yellow_bullet in yellow_bullets:
        for red_bullet in red_bullets:
            if yellow_bullet.colliderect(red_bullet):
                yellow_bullets.remove(yellow_bullet)
                red_bullets.remove(red_bullet)


