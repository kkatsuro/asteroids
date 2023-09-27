import pygame

from conf import *

x, y, w, h = MIDDLE_RECT
lost_screen_surface = pygame.Surface((w, h), flags=pygame.SRCALPHA)

score_font = pygame.font.Font(GUI_FONT,  61)
# 'position': , 'text': 'YOUR SCORE:'}

you_lost_render = pygame.font.Font(GUI_FONT, 135).render('YOU LOST', True, OBJECT_COLOR)
press_a_render = pygame.font.Font(GUI_FONT, 53).render('PRESS A TO CONTINUE', True, OBJECT_COLOR)

you_lost_rect = you_lost_render.get_rect(center=(w/2, 140))
press_a_rect  =  press_a_render.get_rect(center=(w/2, 420))  # 545 not visible on 1080p

def draw_lost_screen(surface, score):
    lost_screen_surface.fill((0, 0, 0, 0x44))

    lost_screen_surface.blit(you_lost_render, you_lost_rect)
    lost_screen_surface.blit(press_a_render, press_a_rect)

    score_render = score_font.render(f'YOUR SCORE: {score}', True, OBJECT_COLOR)
    lost_screen_surface.blit(score_render, score_render.get_rect(center=(w/2, 300)))

    surface.blit(lost_screen_surface, (x, y))
