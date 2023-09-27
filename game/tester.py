#!/usr/bin/python3

import pygame
import pygame._sdl2.controller
import sys

from conf import *

from dpad import draw_dpad_background, draw_dpad_left, draw_dpad_right, draw_dpad_up, draw_dpad_down

Vector2 = pygame.math.Vector2

# proportion: 123.4 / 53.2 = 2.32

CONTROLLER_WIDTH  = 1318
CONTROLLER_HEIGHT = int(CONTROLLER_WIDTH / 2.32)

# colors
white = 240, 240, 240
grey = 72,72,72
light_grey = 189,174,173

black = 24, 24, 24
black_pressed = 124, 124, 124

red = 238, 21, 21
red_pressed = 140, 21, 21

BORDER_WIDTH = 40

pygame.init()

middle_font = pygame.font.SysFont('sourcecodepro', 29)

pygame.font.init()

button_font_small = pygame.font.Font('fonts/Need Every Sound.ttf', 29)
button_font_big   = pygame.font.Font('fonts/Need Every Sound.ttf', 41)
logo_font         = pygame.font.Font('fonts/NintendBoldRM8E.ttf', 50)
trademark_font    = pygame.font.SysFont('sourcecodepro', 50)

select_render = button_font_small.render('SELECT', True, red)
start_render  = button_font_small.render( 'START', True, red)

a_render = button_font_big.render('A', True, red)
b_render = button_font_big.render('B', True, red)

ast_render = logo_font.render('Asteroids', True, red)
trademark_render = trademark_font.render('®', True, red)

# @todo: change it to percent of CONTROLLER_WIDTH value
def make_controller_surface(buttons):
    controller_bg = pygame.Surface((CONTROLLER_WIDTH, CONTROLLER_HEIGHT), flags=pygame.SRCALPHA)

    # actual controller rect
    pygame.draw.rect(controller_bg, white, (0,0,CONTROLLER_WIDTH,CONTROLLER_HEIGHT), border_radius=24)
    pygame.draw.rect(controller_bg, grey, (BORDER_WIDTH, 80, CONTROLLER_WIDTH-2*BORDER_WIDTH, CONTROLLER_HEIGHT-80-BORDER_WIDTH), border_radius=18)

    draw_dpad_background(controller_bg)
    if buttons[DPAD_UP]: # or left_stick.y < 0:
        draw_dpad_up(controller_bg)
    if buttons[DPAD_DOWN]: # or left_stick.y > 0:
        draw_dpad_down(controller_bg)
    if buttons[DPAD_LEFT]: # or left_stick.x < 0:
        draw_dpad_left(controller_bg)
    if buttons[DPAD_RIGHT]: # or left_stick.x > 0:
        draw_dpad_right(controller_bg)

    # middle
    pygame.draw.rect(controller_bg, light_grey, (440,      80, 360, 66), border_bottom_left_radius=18, border_bottom_right_radius=18)
    pygame.draw.rect(controller_bg, light_grey, (440,   80+86, 360, 66), border_radius=18)
    pygame.draw.rect(controller_bg, light_grey, (440, 80+86*2, 360, 66), border_radius=18)
    pygame.draw.rect(controller_bg, light_grey, (440, CONTROLLER_HEIGHT-BORDER_WIDTH-33, 360, 33),
                                           border_top_left_radius=18, border_top_right_radius=18)

    pygame.draw.rect(controller_bg, white, (440, 80+86*3, 360, 2*66), border_radius=18)

    if buttons[BUTTON_SELECT]:
        pygame.draw.rect(controller_bg, black_pressed, (440+40, 80+86*3 + 45, 100, 38), border_radius=18)
    else:
        pygame.draw.rect(controller_bg, black,      (440+40, 80+86*3 + 45, 100, 38), border_radius=18)

    if buttons[BUTTON_START]:
        pygame.draw.rect(controller_bg, black_pressed, (440+120+90, 80+86*3 + 45, 100, 38), border_radius=18)
    else:
        pygame.draw.rect(controller_bg, black, (440+120+90, 80+86*3 + 45, 100, 38), border_radius=18)

    controller_bg.blit(select_render, (455, 270) )
    controller_bg.blit( start_render, (640, 270) )

    # right side buttons
    pygame.draw.rect(controller_bg, white, ( 860, 329, 141, 141), border_radius=12)
    pygame.draw.rect(controller_bg, white, (1035, 329, 141, 141), border_radius=12)
    
    if buttons[BUTTON_X]:
        pygame.draw.circle(controller_bg, red_pressed, ( 860 + 141/2, 329 + 141/2), 60 )
    else:
        pygame.draw.circle(controller_bg, red, ( 860 + 141/2, 329 + 141/2), 60 )

    if buttons[BUTTON_A]:
        pygame.draw.circle(controller_bg, red_pressed, (1030 + 141/2, 329 + 141/2), 60 )
    else:
        pygame.draw.circle(controller_bg, red, (1030 + 141/2, 329 + 141/2), 60 )

    controller_bg.blit(ast_render, (883, 168))
    controller_bg.blit(trademark_render, (1153, 153) )

    controller_bg.blit(a_render, (1142, 480) )
    controller_bg.blit(b_render, ( 975, 480) )

    return controller_bg

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    running = True

    pygame._sdl2.controller.init()
    controllers = [ pygame._sdl2.controller.Controller(x)
                    for x in range(pygame.joystick.get_count())
                    if pygame._sdl2.controller.is_controller(x) ]

    left_stick = Vector2()
    right_stick = Vector2()
    left_trigger, right_trigger = 0, 0
    trigger_value = 50

    dpad_position, dpad_length, dpad_width = Vector2(106, 204), 76, 0
    setting_width = True
    stick_value = Vector2(1015.68, 194.142)

    buttons = [ False ] * 32

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.CONTROLLERBUTTONDOWN or event.type == pygame.CONTROLLERBUTTONUP:
                buttons[event.button] = (event.type == pygame.CONTROLLERBUTTONDOWN)
                print(event.button)
                
            elif event.type == pygame.CONTROLLERAXISMOTION:
                axis = event.axis

                if axis == LEFT_STICK_X:
                    left_stick.x = event.value if abs(event.value) > CONTROLLER_DEAD_ZONE else 0

                elif axis == LEFT_STICK_Y:
                    left_stick.y = event.value if abs(event.value) > CONTROLLER_DEAD_ZONE else 0

                elif axis == RIGHT_STICK_X:
                    right_stick.x = event.value if abs(event.value) > CONTROLLER_DEAD_ZONE else 0

                elif axis == RIGHT_STICK_Y:
                    right_stick.y = event.value if abs(event.value) > CONTROLLER_DEAD_ZONE else 0

                elif axis == LEFT_TRIGGER:
                    left_trigger = event.value if abs(event.value) > CONTROLLER_DEAD_ZONE else 0

                elif axis == RIGHT_TRIGGER:
                    right_trigger = event.value if abs(event.value) > CONTROLLER_DEAD_ZONE else 0

                print(f'size: {trigger_value}, position: {stick_value}')


        stick_value += left_stick / (32767 / 4)
        trigger_value += right_trigger / (32767 * 1)
        trigger_value -= left_trigger / (32767 * 1)
        controller_bg = make_controller_surface(buttons)

        screen.fill(black)
        screen.blit(controller_bg, (0,0))
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == '__main__':
    main()
