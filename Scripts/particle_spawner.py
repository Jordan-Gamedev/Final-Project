from pyray import *
import random
from particle import Particle
from animation import Animation
from transform import Transform2D

class SpawnParticles:
    def __init__(self, spawn_particle:bool, spawn_rate, particle_anim:Animation):
        self.spawn_particle = spawn_particle
        self.spawn_rate = spawn_rate
        self.spawn_pos = Vector2()
        self.particle_anim = particle_anim

    def update(self, dt):
        if not self.spawn_particle:
            self.current_time = self.spawn_rate
            return

        self.current_time -= dt

        # Exit early if the spawn timer has not yet reached zero
        if (self.current_time > 0):
            return

        self.current_time = self.spawn_rate

        spawn_bounds_x = (self.spawn_pos.x - 30, self.spawn_pos.x + 30)

        spawn_pos_x = random.uniform(spawn_bounds_x[0], spawn_bounds_x[1])

        particle_transform = Transform2D(Vector2(spawn_pos_x, self.spawn_pos.y), 0, 1)
                
        particle = Particle(particle_transform, self.particle_anim, speed=10, anim_speed=2)
        particle.vel.x = random.uniform(-1, 1) * 50
        particle.vel.y = -32