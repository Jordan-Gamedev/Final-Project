import math
from pyray import *
import random
from raylib import *
from bug import *


class FlyingBug(Bug):
    def __init__(self, transform:Transform2D, animations:list, damage_size:float, max_hp:float, points:int, rot_speed:Vector2, min_move_speed_mult:float, speed:float, anim_speed:float = 1.0, blood_color=GREEN):
        
        super().__init__(transform, animations, damage_size, max_hp, points, speed, anim_speed, blood_color)
        
        # the min/max speed to rotate towards a target rotation
        self.potential_rot_speed:Vector2 = rot_speed

        # the current rotation speed
        self.rot_speed:float = 0.0

        self.target_rot_speed:float = 0.0

        # the previous target rotation
        self.prev_target_rot:float = 0.0

        # the target rotation to rotate towards
        self.target_rot:float = 0.0
        
        # the slowest it can go
        self.min_move_speed_mult = min_move_speed_mult

    def update(self, dt):
        
        super().update(dt)

        if abs(self.transform.rot - self.target_rot) < 1.0:
            
            # save the previous target rotation
            self.prev_target_rot = self.target_rot

            # get a new random target rotation
            self.target_rot = random.uniform(0.0, 360.0)
            
            # get a new random rotation speed
            self.rot_speed = -self.rot_speed
            self.target_rot_speed = random.uniform(float(self.potential_rot_speed.x), float(self.potential_rot_speed.y))

            # shorter angle wrap-around path
            if self.target_rot - self.transform.rot > 180:
                self.target_rot -= 360
            elif self.target_rot - self.transform.rot < -180:
                self.target_rot += 360

        # lerp the current rotation speed to the new rotation speed
        self.rot_speed = lerp(self.rot_speed, self.target_rot_speed, dt)

        # move towards target rotation
        rot_delta = max(0, self.rot_speed) * dt
        #self.transform.rot = lerp(self.transform.rot, self.target_rot, rot_delta)
        new_rot = lerp(self.transform.rot, self.target_rot, rot_delta)
        self.rotate_around_center(new_rot)

        # set the velocity to the facing direction
        move_speed = lerp(vector2_length(self.vel), max(self.min_move_speed_mult, self.target_rot_speed), dt)
        self.vel = vector2_rotate(Vector2(move_speed, 0), math.radians(self.transform.rot))