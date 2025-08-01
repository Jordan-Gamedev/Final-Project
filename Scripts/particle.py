from pyray import *
from raylib import *
from dynamic_sprite import *

class Particle(DynamicSprite):
    all_particles:list[Sprite] = []

    def __init__(self, transform:Transform2D, animation:Animation, speed:float, anim_speed = 1.0):
        Particle.all_particles.append(self)
        super().__init__(transform, [animation], speed, anim_speed)
    
    def update(self, dt):
        super().update(dt)

        self.vel.y += 64 * dt
        self.vel.x = lerp(self.vel.x, 0, 2 * dt)
        self.rotate_around_center(math.degrees(vector2_angle(Vector2(1,0), self.vel)))
        
        # destroy the particle if it falls on grass
        if self.transform.pos.y < -100:
            Sprite.all_sprites.remove(self)
            Particle.all_particles.remove(self)