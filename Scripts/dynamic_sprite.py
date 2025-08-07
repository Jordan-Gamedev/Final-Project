from pyray import *
from raylib import *
from sprite import *

class DynamicSprite(Sprite):
    
    def __init__(self, transform:Transform2D, animations:list, speed:float, anim_speed:float = 1.0):
        super().__init__(transform, animations, anim_speed)
        # create velocity and speed variable to control sprite movement
        self.vel = Vector2()
        self.speed = speed
    
    def update(self, dt):
        # update sprite position based on velocity, speed, and frame timing
        self.transform.pos.x += self.vel.x * self.speed * dt
        self.transform.pos.y += self.vel.y * self.speed * dt
        super().update(dt)