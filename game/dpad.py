from conf import *


def shrink_rect(rect, delta):
    x, y, w, h = rect
    return x + delta, y + delta, w - delta*2, h - delta*2

position, length, width, border = Vector2(106, 204), 76, 108, 10

actual_length = width + 2*length

rh = (position.x, length+position.y, actual_length, width)
rv = (length+position.x, position.y, width, actual_length)

upper_left  = Vector2(length+border, length+border) + position
upper_right = Vector2(length+width-border, length+border) + position
down_left   = Vector2(length+border, length+width-border) + position
down_right  = Vector2(length+width-border, length+width-border) + position

center = Vector2(actual_length/2, actual_length/2) + position

rh_left = (border + position.x, length + position.y, length, width)
rh_right = (width+length-border + position.x, length + position.y, length, width)
rv_up = (length + position.x, border + position.y, width, length)
rv_down = (length + position.x, length+width-border + position.y, width, length)

def draw_dpad_background(surface):
    pygame.draw.rect(surface, WHITE, rh)
    pygame.draw.rect(surface, WHITE, rv)
    pygame.draw.rect(surface, BLACK, shrink_rect(rh, border))
    pygame.draw.rect(surface, BLACK, shrink_rect(rv, border))

def draw_dpad_left(surface): 
    pygame.draw.rect(surface, WHITE, rh_left)
    pygame.draw.polygon(surface, WHITE, (center, upper_left, down_left))

def draw_dpad_right(surface): 
    pygame.draw.rect(surface, WHITE, rh_right)
    pygame.draw.polygon(surface, WHITE, (center, upper_right, down_right))

def draw_dpad_up(surface): 
    pygame.draw.rect(surface, WHITE, rv_up)
    pygame.draw.polygon(surface, WHITE, (center, upper_left, upper_right))

def draw_dpad_down(surface): 
    pygame.draw.rect(surface, WHITE, rv_down)
    pygame.draw.polygon(surface, WHITE, (center, down_left, down_right))
