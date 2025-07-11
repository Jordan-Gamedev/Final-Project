from pyray import *
from raylib import *
from bug import *
import random

class HoppingBug(Bug):
    def __init__(self, textures, anim_speed, max_hp, damage_size, hop_strength, idle_time:Vector2, pos = Vector2(), rot = 0.0, scale = 1.0):
        # A Vector2 that indicates the direction and strength of the initial velocity
        self.hop_strength = hop_strength
        # A Vector2 timer that lets the bug rest between hops with some random jitter between x and y
        self.idle_time = idle_time
        # The current time in between hops
        self.current_idle_time:float = idle_time.y
        
        super().__init__(textures, anim_speed, max_hp, damage_size, pos, rot, scale)
    
    def update(self, dt):
        super().update(dt)

        ground_pos = get_monitor_height(get_current_monitor()) - 200
        is_grounded = True if self.pos.y >= ground_pos else False

        if is_grounded:
            self.vel.y = 0
            self.vel.x = 0
            self.pos.y = ground_pos
            self.current_idle_time -= dt
        else:
            self.vel.y += 16 * dt
        
        if self.current_idle_time <= 0:
            rest_timer = random.uniform(self.idle_time.x, self.idle_time.y)
            self.current_idle_time = rest_timer
            self.vel.x = random.choice([-1, 1]) * random.uniform(self.hop_strength[0].x, self.hop_strength[1].x)
            self.vel.y = random.uniform(-self.hop_strength[0].y, -self.hop_strength[1].y)