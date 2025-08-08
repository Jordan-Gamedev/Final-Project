from pyray import *
from raylib import *
from bug import *
import random

class CrawlingBug(Bug):
    def __init__(self, transform:Transform2D, animations:list, damage_size:float, max_hp:float, points:int, idle_fall_prob_per_sec:float, \
                walk_fall_prob_per_sec:float, on_ceiling:bool, idle_time:Vector2, walk_time:Vector2, speed:float, anim_speed:float = 1.0, blood_color=GREEN):
        
        super().__init__(transform, animations, damage_size, max_hp, points, speed, anim_speed, blood_color)
        
        # Probability of falling off of ceiling every second while standing still
        self.idle_fall_prob_per_sec = idle_fall_prob_per_sec
        # Probability of falling off of ceiling every second while walking
        self.walk_fall_prob_per_sec = walk_fall_prob_per_sec
        # A Vector2 timer that lets the bug rest between walks with some random jitter between x and y
        self.idle_time = idle_time
        # A Vector2 timer that determines how long the bug walks with some random jitter between x and y
        self.walk_time = walk_time
        # The current time in between walks
        self.current_idle_time:float = idle_time.y
        # The current time to walk
        self.current_walk_time:float = 0.0
        # The time until the next fall probability check
        self.current_fall_check_time = 0.0
        
        # flip the sprite horizontally if it is facing the wrong direction
        if self.transform.pos.x > Bug.SCREEN_WIDTH / 2:
            self.flip_sprite_horiz()

        bug_height = self.get_current_animation().get_current_texture().height * self.transform.scale

        # the ground and ceiling positions
        ground_pos = int(Bug.SCREEN_HEIGHT * 0.97 - bug_height)
        ceil_pos = int(Bug.SCREEN_HEIGHT * 0.03 + bug_height)

        # flip the sprite vertically to cling to ceiling
        if on_ceiling:
            self.flip_sprite_vert()
            self.transform.pos.y = ceil_pos
        else:
            self.transform.pos.y = ground_pos

    def update(self, dt):

        super().update(dt)

        bug_height = self.get_current_animation().get_current_texture().height * self.transform.scale

        # the ground and ceiling positions
        ground_pos = int(Bug.SCREEN_HEIGHT * 0.97 - bug_height)
        ceil_pos = int(Bug.SCREEN_HEIGHT * 0.03 + bug_height)
        
        # checks if the bug is grounded or clinging to the ceiling
        is_grounded = True if self.transform.pos.y >= ground_pos else False
        is_on_ceiling = True if self.transform.pos.y <= ceil_pos else False
        
        self.current_fall_check_time += dt
        if is_on_ceiling and self.current_fall_check_time >= 1:
            self.current_fall_check_time -= 1

            # generate fall probability
            rand = random.uniform(0.0, 1.0)
            prob = self.walk_fall_prob_per_sec if self.current_walk_time > 0.0 else self.idle_fall_prob_per_sec
            
            # the probability to fall happened, so make the bug fall
            if rand < prob:
                self.vel.y = 1

        # collide with ground
        if is_grounded and self.vel.y >= 0:
            self.vel.y = 0
            self.transform.pos.y = ground_pos
        # gravity
        elif not is_on_ceiling or self.vel.y > 0:
            
            # the bug will be idle the maximum time after falling
            self.current_idle_time = self.idle_time.y
            self.current_walk_time = 0.0
            self.vel.x = lerp(self.vel.x, 0, dt)

            # have gravity affect the bug
            self.vel.y += 4 * dt
        
        # the bug is currently idle
        if self.current_idle_time > 0:
            self.current_idle_time -= dt

            # the idle time is up, so set up walking
            if self.current_idle_time <= 0:
                self.current_walk_time = random.uniform(self.walk_time.x, self.walk_time.y)

        # the bug is currently walking
        if self.current_walk_time > 0:
            self.current_walk_time -= dt
            self.vel.x = self.facing_direction_x

            # the walk time is up, so set up resting
            if self.current_walk_time <= 0:
                self.current_idle_time = random.uniform(self.idle_time.x, self.idle_time.y)
                self.vel.x = 0

        # flip the sprite upright if it is on its back while on the ground and trying to move
        if is_grounded and self.facing_direction_y == -1:
            self.vel.x = 0
            if self.current_walk_time > 0:
                self.flip_sprite_vert()
                self.current_walk_time = 0
                self.current_idle_time = random.uniform(self.idle_time.x, self.idle_time.y)

        # play fall animation
        if not is_on_ceiling and self.facing_direction_y == -1:
            if self.anim_index != 2:
                self.play_animation(2)
        # play idle animation
        elif self.current_idle_time > 0:
            if self.anim_index != 0:
                self.play_animation(0)
        # play walk animation
        elif self.current_walk_time > 0:
            if self.anim_index != 1:
                self.play_animation(1)