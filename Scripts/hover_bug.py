from pyray import *
import random
from raylib import *
from bug import *


class HoverBug(Bug):
    def __init__(self, transform:Transform2D, animations:list, damage_size:float, max_hp:float, points:int, \
                  jitter:float, jitter_speed_mult:float, max_move_dist:float, idle_time:Vector2, speed:float, anim_speed:float = 1.0, blood_color=GREEN):
        
        super().__init__(transform, animations, damage_size, max_hp, points, speed, anim_speed, blood_color)
        
        # the distance around the idle point that it make small movements towards
        self.jitter = jitter
        # the movement at which the bug jitters
        self.jitter_speed_mult = jitter_speed_mult
        # a Vector2 timer that lets the bug rest between hops with some random jitter between x and y
        self.idle_time:Vector2 = idle_time
        # the current time in between moving to the next idle point
        self.current_idle_time:float = idle_time.y
        # the max distance to place the idle point
        self.max_move_dist:float = max_move_dist
        # the target position to move towards
        self.target_position:Vector2 = Vector2(transform.pos.x, transform.pos.y)
        # the position where the bug chills and hovers about
        self.idle_position:Vector2 = Vector2(transform.pos.x, transform.pos.y)
        
    def update(self, dt):
        
        super().update(dt)

        self.vel = vector2_normalize(vector2_subtract(self.target_position, self.transform.pos))

        if self.current_idle_time > 0:

            self.current_idle_time -= dt

            self.vel.x *= self.jitter_speed_mult
            self.vel.y *= self.jitter_speed_mult

            if vector2_distance(self.transform.pos, self.target_position) < 3:
                # compute new random jitter position
                self.target_position.x = random.uniform(self.idle_position.x - self.jitter, self.idle_position.x + self.jitter)
                self.target_position.y = random.uniform(self.idle_position.y - self.jitter, self.idle_position.y + self.jitter)

            if self.current_idle_time <= 0:

                # compute new random idle position
                min_x = self.idle_position.x - (self.max_move_dist * 0.5) if self.facing_direction_x == 1 else self.idle_position.x - self.max_move_dist
                max_x = self.idle_position.x + self.max_move_dist if self.facing_direction_x == 1 else self.idle_position.x + (self.max_move_dist * 0.5)
                self.target_position.x = random.uniform(min_x, max_x)
                min_y = self.idle_position.y - (self.max_move_dist * 0.5)
                max_y = self.idle_position.y + (self.max_move_dist * 0.5)
                self.target_position.y = random.uniform(min_y, max_y)
                self.idle_position = Vector2(self.target_position.x, self.target_position.y)

                if (self.target_position.x < self.transform.pos.x and self.facing_direction_x > 0) or (self.target_position.x > self.transform.pos.x and self.facing_direction_x < 0):
                    self.flip_sprite_horiz()

        elif vector2_distance(self.transform.pos, self.target_position) < self.speed * dt:
            # reset idle time
            self.current_idle_time = random.uniform(self.idle_time.x, self.idle_time.y)