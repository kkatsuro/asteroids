import pygame
import random

from polygon import Polygon
from misc import coords_to_points
from tester import make_controller_surface

from conf import *

# each entity is game object with position, velocity and rotation
# it has way to be drawn and a hitbox make out of polygon
class Entity:
    def __init__(self):
        self.velocity = Vector2()
        self.acceleration = Vector2()
        self.rotation = 0
        self.rotation_velocity = 0
        self.max_velocity = 2

        self.color = OBJECT_COLOR

        self.shield_timeout = 1  # code to make this decrease is necessary in new entities

    def get_direction(self):
        return Vector2(0, -1).rotate(-self.rotation)

    def maybe_collides(self, entity):
        return self.hitbox.maybe_collides(entity.hitbox)

    def collides(self, entity):
        return self.hitbox.collides(entity.hitbox)

    def update(self, dt):
        self.velocity += self.acceleration * dt
        if self.velocity.length() > self.max_velocity:
            self.velocity = self.velocity.normalize() * self.max_velocity
        self.hitbox.move(self.velocity * dt)

        # @todo: should we have position *and* hitbox?
        if self.rotation_velocity != 0:
            self.rotation += self.rotation_velocity * dt
            self.hitbox.rotate(self.rotation_velocity * dt)

        left, right, up, down = self.hitbox.rect_coords
        if right < 0:
            delta = right - left + WIDTH
            self.hitbox.move(Vector2(delta, 0))
            if self.shield_timeout <= 0:
                self.shield = 2000
                self.shield_timeout = 10_000

        elif left > WIDTH:
            delta = left - right - WIDTH
            self.hitbox.move(Vector2(delta, 0))
            if self.shield_timeout <= 0:
                self.shield = 2000
                self.shield_timeout = 10_000

        if down < 0:
            delta = down - up + HEIGHT
            self.hitbox.move(Vector2(0, delta))
            if self.shield_timeout <= 0:
                self.shield = 2000
                self.shield_timeout = 10_000

        elif up > HEIGHT:
            delta = up - down - HEIGHT
            self.hitbox.move(Vector2(0, delta))
            if self.shield_timeout <= 0:
                self.shield = 2000
                self.shield_timeout = 10_000

    def move_to(self, position):
        self.hitbox.move_to(Vector2(position))

    # in standard entity hitbox is actual object we draw
    def draw(self, surface):
        pygame.draw.polygon(surface, self.color, self.hitbox.points) 
        # self.draw_boundry(surface)

    def draw_boundry(self, surface):
        b, a, c, d = self.hitbox.rect_points
        pygame.draw.line(surface, BORDER_COLOR, a, b)
        pygame.draw.line(surface, BORDER_COLOR, b, c)
        pygame.draw.line(surface, BORDER_COLOR, c, d)
        pygame.draw.line(surface, BORDER_COLOR, d, a)

class Projectile(Entity):
    def __init__(self, position, direction):
        Entity.__init__(self)
        self.velocity = direction * 20  # @todo: speed
        self.lifetime = 800 
        self.max_velocity = 3
        
        # make position be in the middle here
        position = Vector2(position)
        a, b, c, d = [ position.copy() for _ in range(4) ]
        b.x += 5
        c.y += 5
        d.x += 5
        d.y += 5
        self.hitbox = Polygon(points=[a, b, d, c])

    def update(self, dt):
        Entity.update(self, dt)
        self.lifetime -= 1 * dt


class Asteroid(Entity):
    def __init__(self, position=None, direction=None, size=None, player=None):
        Entity.__init__(self)  # @verify

        self.hitbox = Polygon()

        if size != None:
            self.size = size
        else:
            self.size = random.randint(10, 100)

        self.lifetime = 1

        if player != None:
            # spawn it beside screen but not too far away so it won't teleport
            # and not too close to player
            pos_x, pos_y = player.hitbox.middle
            x, y = self.hitbox.get_dimensions()
            while Vector2(pos_x, pos_y).distance_to(player.hitbox.middle) < 300:
                r = random.randint(0, 3)
                if r == 0:
                    pos_x = -x
                    pos_y = random.randint(-200, HEIGHT+200)
                elif r == 1:
                    pos_x = WIDTH + x
                    pos_y = random.randint(-200, HEIGHT+200)
                elif r == 2:
                    pos_x = random.randint(-200, WIDTH+200)
                    pos_y = -y
                elif r == 3:
                    pos_x = random.randint(-200, WIDTH+200)
                    pos_y = HEIGHT + y

            self.hitbox.move_to(Vector2(pos_x, pos_y))

            direction = (self.hitbox.middle - player.hitbox.middle).rotate( random.randint(-30, 30) )
            self.velocity = direction.normalize() * random.randint(1, 4) / 10

        else:
            if direction != None:
                self.velocity = direction.normalize() * random.randint(1, 4) / 10
            else:
                self.velocity.x = random.randint(-2, 2) / 15 
                self.velocity.y = random.randint(-2, 2) / 15 

            if position != None:
                offset = position
            else:
                offset = Vector2(random.randint(100, WIDTH-100), random.randint(100, HEIGHT-100))

            self.rotation_velocity = random.randint(-2, 2) / 10
            self.hitbox = Polygon(offset)

SIZE = 80
class Player(Entity):
    def __init__(self):
        Entity.__init__(self)
        self.acceleration_value = 0
        self.dimensions = Vector2(SIZE * 2.32, SIZE)

        middle = Vector2(WIDTH/2, HEIGHT/2)
        x1, y1 = middle - self.dimensions / 2
        x2, y2 = middle + self.dimensions / 2

        self.hitbox = Polygon(points=coords_to_points(x1, x2, y1, y2))
        self.lifetime = 3

        self.alpha = 255
        self.shield = 0
        self.shield_timeout = 0

        self.max_velocity = 0.5

        self.controller_surface_cache = {}

        self.texture = None
        self.last_rotation = 0
        self.key = tuple()
        self.last_key = tuple()

        self.break_acceleration = Vector2()

    def set_acceleration(self, value):
        self.acceleration_value = value 
        self.update_acceleration()

    def set_rotation(self, value):
        if abs(value) > CONTROLLER_DEAD_ZONE:
            self.rotation_velocity = -value / (32767*4)
        else:
            self.rotation_velocity = 0
        self.update_acceleration()

    def update_acceleration(self):
        if self.acceleration_value < CONTROLLER_DEAD_ZONE:
            self.acceleration = Vector2()
        self.acceleration = self.acceleration_value * Vector2(0, 1).rotate(-self.rotation) / -7000000

    def update(self, dt, buttons):
        self.last_rotation = self.rotation

        if buttons[DPAD_UP]:
            self.acceleration = Vector2(0, 1).rotate(-self.rotation) / -900
        elif buttons[DPAD_DOWN]:
            self.acceleration = Vector2(0, 1).rotate(-self.rotation) / 1900
        else:
            self.acceleration = Vector2(0)

        if buttons[DPAD_LEFT]:
            self.rotation_velocity =  0.25
        elif buttons[DPAD_RIGHT]:
            self.rotation_velocity = -0.25
        else:
            self.rotation_velocity = 0

        Entity.update(self, dt)

        if self.shield > 0:
            self.shield -= dt
            alpha = abs((self.shield % 1000) - 500)+500  # this is my weird way to increasing/decreasing number
            self.alpha = alpha / (1000 / 255)
        else:
            self.shield_timeout -= dt
            

        self.last_key = self.key
        self.key = tuple(buttons)


    def draw(self, surface):
        width, height = self.hitbox.get_dimensions()

        if self.key != self.last_key or self.rotation != self.last_rotation:  # regenerate self.texture
            controller_surface = self.controller_surface_cache.get(self.key)
            if controller_surface == None:
                controller_surface = make_controller_surface(self.key)
                self.controller_surface_cache[self.key] = controller_surface

            rotated = pygame.transform.rotate(controller_surface, self.rotation)
            self.texture = pygame.transform.smoothscale(rotated, (width, height))

        if self.shield > 0:
            self.texture.set_alpha(self.alpha)

        self.draw_position = Vector2(self.hitbox.middle.x-width/2, self.hitbox.middle.y-height/2)
        surface.blit(self.texture, self.draw_position)

        # self.draw_boundry(surface)


# generation test
def main():
    WIDTH, HEGIHT = 1000, 1000

    example = env_default('EX', 0)

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEGIHT))
    clock = pygame.time.Clock()
    running = True

    middle = Vector2(WIDTH/2, HEGIHT/2)

    a = Asteroid(middle)
    a.velocity = Vector2()
    a.rotation_velocity = 0.1

    if example == 2:
        a2 = Asteroid(middle)
        a2.velocity = Vector2()
        a2.rotation_velocity = -0.15

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if example == 1:
            a.acceleration = (pygame.mouse.get_pos() - a.hitbox.middle).normalize() / 300
        elif example == 2:
            a2.move_to(pygame.mouse.get_pos())
            if a.maybe_collides(a2):
                a.color = BLUE
                a2.color = BLUE

                if a.collides(a2):
                    a.color = RED
                    a2.color = RED

            else:
                a.color = OBJECT_COLOR
                a2.color = OBJECT_COLOR
            

        a.update(5)

        screen.fill(BACKGROUND)
        a.draw(screen)
        if example == 2:
            a.draw_boundry(screen)
            a2.draw_boundry(screen)

        pygame.display.flip()

        clock.tick(165)


if __name__ == "__main__":
    main()
