from pyray import *
import random

from animation import Animation
from bug import Bug
from flying_bug import FlyingBug
from hopping_bug import HoppingBug
from hover_bug import HoverBug
from transform import Transform2D

class SpawnBugs:
    def __init__(self, max_capacity, spawn_rate, fly_anims:list[Animation], hopper_anims:list[Animation], crawler_anims:list[Animation]):
        self.max_capacity = max_capacity

        self.spawn_rate = spawn_rate
        
        self.fly_anims = fly_anims
        self.hopper_anims = hopper_anims
        self.crawler_anims = crawler_anims
        
        self.current_time = spawn_rate
        self.spawn_bounds_x = (-100, get_monitor_width(get_current_monitor()) + 100)
        #self.spawn_bounds_x = (100, get_monitor_width(get_current_monitor()) - 100)
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

        #choice = random.choice(['fly', 'fly'])
        choice = random.choice(['hover', 'hop', 'fly'])

        bug_transform = Transform2D(Vector2(spawn_pos_x, spawn_pos_y), 0, 2)
        match choice:
            case 'fly':
                
                anims = [Animation(animation.folder_path, animation.frame_durations, animation.is_loop, animation.on_finish_event) for animation in self.fly_anims]                
                FlyingBug(bug_transform, anims, damage_size=60.0, max_hp=1.0, points=10, rot_speed=Vector2(.75, 2), min_move_speed_mult=1, speed=100, anim_speed=5)
            case 'hop':
                
                anims = [Animation(animation.folder_path, animation.frame_durations, animation.is_loop, animation.on_finish_event) for animation in self.hopper_anims]
                hop_strength = (Vector2(2, 2), Vector2(6, 12))
                HoppingBug(bug_transform, anims, damage_size=60.0, max_hp=1.0, points=10, hop_strength=hop_strength, idle_time=Vector2(3, 6), speed=100)
            case 'hover':

                anims = [Animation(animation.folder_path, animation.frame_durations, animation.is_loop, animation.on_finish_event) for animation in self.fly_anims]
                HoverBug(bug_transform, anims, damage_size=60.0, max_hp=1.0, points=10, jitter=10.0, max_move_dist=200.0, idle_time=Vector2(3, 6), speed=250)