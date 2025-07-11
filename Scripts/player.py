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
            self.vel = vector2_subtract(self.target_pos, self.pos)
            self.vel = vector2_normalize(self.vel)
        else:
            self.vel = Vector2()
            self.pos = self.target_pos
        
        super().update(dt)

        file = open(join("Data", "Player_Data.txt"), "w")
        curr_tex:Texture2D = self.get_current_texture()
        file.truncate()
        file.write(f"PosX: {self.pos.x:.4f}\nPosY: {self.pos.y:.4f}\nScale: {self.scale:.4f}\nTexWidth: {curr_tex.width}\nTexHeight: {curr_tex.height}")
        file.close()