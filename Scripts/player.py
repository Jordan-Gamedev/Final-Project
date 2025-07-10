from os.path import join
from pyray import *
from raylib import *

import cursor
from dynamic_sprite import *

class Player(DynamicSprite):
    
    def __init__(self, textures, anim_speed, pos = Vector2(), rot = 0.0, scale = 1.0):
        super().__init__(textures, anim_speed, pos, rot, scale)
        self.target_pos = pos

    def update(self, dt):

        if cursor.Cursor.is_global_mouse_clicking:
            self.target_pos = self.center_position_at_other(cursor.Cursor.global_mouse_position)

        if vector2_distance(self.target_pos, self.pos) > self.speed * dt:
            self.dir = vector2_subtract(self.target_pos, self.pos)
            self.dir = vector2_normalize(self.dir)
        else:
            self.dir = Vector2()
            self.pos = self.target_pos
        
        super().update(dt)

        with open(join("Data", "Player_Data.txt"), "w") as file:
                file.write(f"PosX: {self.pos.x:.4f}\nPosY: {self.pos.y:.4f}\nRot: {self.rot}\nScale: {self.scale:.4f}\n")
                file.close()