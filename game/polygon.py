import random
import pygame

from misc import coords_to_points
from separation_axis_theorem import separating_axis_theorem
from conf import *

Vector2 = pygame.math.Vector2

# polygon is basically list of points and one middle point
# @todo: shouldnt middle point be equal to position?
class Polygon:
    def __init__(self, position=None, points=None):
        if position:
            position = Vector2(position)
        else:
            position = Vector2(0,0)

        if not points:
            points = [ Vector2(position) ]
            start = Vector2(1, 0)

            x_sum = points[0].x
            y_sum = points[0].y

            for _ in range(9):
                start = start.normalize() * random.randint(400, 2000) / 50
                start = start.rotate(random.randint(80, 600)/10)
                points.append(points[-1] + start)
                x_sum += points[-1].x
                y_sum += points[-1].y

            self.points = points

            length = len(points)
            self.middle = Vector2(x_sum/length, y_sum/length)

        else:
            self.points = points
            self.update_middle_point()

        self.update_rect_hitbox()

        # move it so middle is in position(input)
        if position:
            self.move(position - self.middle)


    def update_middle_point(self):
        x_sum = y_sum = 0
        for x, y in self.points:
            x_sum += x
            y_sum += y
        length = len(self.points)
        self.middle = Vector2(x_sum/length, y_sum/length)

    def maybe_collides(self, polygon):
        x1, x2, y1, y2 = self.rect_coords
        for x, y in polygon.rect_points:
            if x1 <= x <= x2 and y1 <= y <= y2:
                return True
        return False

    def collides(self, polygon):
        # if not maybe_collides(self, polygon):
        #     return
        return separating_axis_theorem(self.points, polygon.points)

    def update_rect_hitbox(self):
        self.rect_coords = self.get_min_max_x_y()
        self.rect_points = coords_to_points(*self.rect_coords)

    def rotate(self, angle):
        self.points = [ (p - self.middle).rotate(angle) + self.middle for p in self.points ]
        self.update_rect_hitbox()

    def move(self, vec):
        self.points = [ p + vec for p in self.points ]
        self.middle += vec

        # move rect hitbox
        # this is a little bit more efficient than running self.update_rect_hitbox() here
        # but can it be even more?
        x1, x2, y1, y2 = self.rect_coords
        self.rect_coords = x1+vec.x, x2+vec.x, y1+vec.y, y2+vec.y
        self.rect_points = [ p + vec for p in self.rect_points ]

    def move_to(self, position):
        self.move(position - self.middle)

    def get_min_max_x_y(self):
        x1, y1 = self.points[0]  # just choose 'random' points
        x2, y2 = x1, y1
        for x, y in self.points:
            if x < x1:
                x1 = x
            elif x > x2:
                x2 = x
            if y < y1:
                y1 = y
            elif y > y2:
                y2 = y
        return x1, x2, y1, y2

    def get_dimensions(self):
        x1, x2, y1, y2 = self.rect_coords
        return x2 - x1, y2 - y1
