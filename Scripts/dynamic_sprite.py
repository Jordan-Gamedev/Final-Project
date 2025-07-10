from pyray import *
from raylib import *
from sprite import *

class DynamicSprite(Sprite):
    
    def __init__(self, textures, anim_speed, pos = Vector2(), rot = 0.0, scale = 1.0):
        super().__init__(textures, anim_speed, pos, rot, scale)
        self.dir = Vector2()
        self.speed = 0.0
    
    def update(self, dt):
        self.pos.x += self.dir.x * self.speed * dt
        self.pos.y += self.dir.y * self.speed * dt
        super().update(dt)