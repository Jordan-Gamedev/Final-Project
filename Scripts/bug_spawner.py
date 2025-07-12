from pyray import *
from bug import Bug
from hopping_bug import HoppingBug
import random

class SpawnBugs:
    def __init__(self, max_capacity, spawn_rate, fly_tex_paths, hopper_tex_paths, crawler_tex_paths):
        self.max_capacity = max_capacity

        self.spawn_rate = spawn_rate
        
        self.fly_tex_paths = fly_tex_paths
        self.hopper_tex_paths = hopper_tex_paths
        self.crawler_tex_paths = crawler_tex_paths
        self.fly_tex = []
        self.hopper_tex = []
        self.crawler_tex = []

        for path in self.fly_tex_paths:
            self.fly_tex.append(load_texture(path))
        for path in self.hopper_tex_paths:
            self.hopper_tex.append(load_texture(path))
        for path in self.crawler_tex_paths:
            self.crawler_tex.append(load_texture(path))
        
        self.current_time = spawn_rate
        self.spawn_bounds_x = (-100, get_monitor_width(get_current_monitor()) + 100)
        self.spawn_bounds_y = (0, get_monitor_height(get_current_monitor()) - 100)

    def update(self, dt):
        # If a maximum number of bugs are already spawned, perform an early exit
        if (len(Bug.all_bugs) >= self.max_capacity):
            self.current_time = self.spawn_rate
            return

        self.current_time -= dt

        # Exit early if the spawn timer has not yet reached zero
        if (self.current_time > 0):
            return

        self.current_time = self.spawn_rate

        spawn_pos_x = random.choice([self.spawn_bounds_x[0], self.spawn_bounds_x[1]])
        spawn_pos_y = random.uniform(self.spawn_bounds_y[0], self.spawn_bounds_y[1])

        choice = random.choice(['fly', 'grasshopper'])

        match choice:
            case 'fly':
                flyer = Bug(self.fly_tex_paths, self.fly_tex, 15.0, 1.0, 50.0, Vector2(spawn_pos_x, spawn_pos_y), 0, 2)
            case 'grasshopper':
                hop_strength = (Vector2(2, 2), Vector2(6, 12))

                grasshopper = HoppingBug(self.hopper_tex_paths, self.hopper_tex, 15.0, 1.0, 50.0, hop_strength=hop_strength, \
                idle_time=Vector2(3, 6), pos=Vector2(spawn_pos_x, spawn_pos_y), rot=0, scale=2)
        
                grasshopper.speed = 100