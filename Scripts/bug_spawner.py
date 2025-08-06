from pyray import *
import random

from animation import Animation
from bug import Bug
from crawling_bug import CrawlingBug
from flying_bug import FlyingBug
from hopping_bug import HoppingBug
from hover_bug import HoverBug
from transform import Transform2D

class SpawnBugs:
    def __init__(self, max_capacity, spawn_rate, fly_anims:list[Animation], hover_anims:list[Animation], \
            hopper_anims:list[Animation], crawler_anims:list[Animation], fly_pnts, hover_pnts, hop_pnts, crawl_pnts, blood_color=GREEN):
        self.max_capacity = max_capacity

        self.spawn_rate = spawn_rate
        
        self.fly_anims = fly_anims
        self.hover_anims = hover_anims
        self.hopper_anims = hopper_anims
        self.crawler_anims = crawler_anims
        
        self.fly_pnts = fly_pnts
        self.hover_pnts = hover_pnts
        self.hop_pnts = hop_pnts
        self.crawl_pnts = crawl_pnts

        self.current_time = spawn_rate
        self.spawn_bounds_x = (-100, get_monitor_width(get_current_monitor()) + 100)
        self.spawn_bounds_y = (0, get_monitor_height(get_current_monitor()) - 100)

        self.blood_color = blood_color

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

        choices = []
        if self.fly_anims:
            choices.append('fly')
        if self.hover_anims:
            choices.append('hover')
        if self.hopper_anims:
            choices.append('hop')
        if self.crawler_anims:
            choices.append('crawl')
        
        choice = random.choice(choices)

        bug_transform = Transform2D(Vector2(spawn_pos_x, spawn_pos_y), 0, 2)
        match choice:
            case 'fly':
                
                anims = [Animation(animation.folder_path, animation.frame_duration, animation.is_loop, animation.on_finish_event) for animation in self.fly_anims]                
                FlyingBug(bug_transform, anims, damage_size=70.0, max_hp=1.0, points=self.fly_pnts, rot_speed=Vector2(.75, 2), min_move_speed_mult=1, speed=100, anim_speed=5, blood_color=self.blood_color)
            
            case 'hover':

                anims = [Animation(animation.folder_path, animation.frame_duration, animation.is_loop, animation.on_finish_event) for animation in self.hover_anims]
                HoverBug(bug_transform, anims, damage_size=50.0, max_hp=0.5, points=self.hover_pnts, jitter=10.0, jitter_speed_mult=.15, max_move_dist=700.0, idle_time=Vector2(3, 6), speed=1200, blood_color=self.blood_color)

            case 'hop':
                
                anims = [Animation(animation.folder_path, animation.frame_duration, animation.is_loop, animation.on_finish_event) for animation in self.hopper_anims]
                hop_strength = (Vector2(2, 2), Vector2(6, 12))
                HoppingBug(bug_transform, anims, damage_size=70.0, max_hp=1.5, points=self.hop_pnts, hop_strength=hop_strength, idle_time=Vector2(3, 6), speed=100, blood_color=self.blood_color)

            case 'crawl':

                anims = [Animation(animation.folder_path, animation.frame_duration, animation.is_loop, animation.on_finish_event) for animation in self.crawler_anims]
                on_ceiling = random.choice([True, False])
                CrawlingBug(bug_transform, anims, damage_size=50.0, max_hp=0.65, points=self.crawl_pnts, idle_fall_prob_per_sec=0.01, walk_fall_prob_per_sec=0.025, on_ceiling=on_ceiling, \
                            idle_time=Vector2(1.5, 5), walk_time=Vector2(1.5, 4), speed=100, blood_color=self.blood_color)