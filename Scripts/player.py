from pyray import *
from raylib import *

import cursor
from dynamic_sprite import *

class Player(DynamicSprite):
    
    def __init__(self, transform:Transform2D, animations:list, speed:float, anim_speed:float = 1.0):
        self.speed = speed
        self.target_pos = transform.pos
        super().__init__(transform, animations, speed, anim_speed)

    def update(self, dt):

        if cursor.Cursor.is_global_mouse_clicking:
            self.target_pos = self.center_position_at_other(cursor.Cursor.global_mouse_position)

        if vector2_distance(self.target_pos, self.transform.pos) > self.speed * dt:
            self.vel = vector2_subtract(self.target_pos, self.transform.pos)
            self.vel = vector2_normalize(self.vel)
        else:
            self.vel = Vector2()
            self.transform.pos = self.target_pos
        
        super().update(dt)

        file = open("Data\Player_Data.txt", "w")
        curr_tex:Texture2D = self.get_current_animation().get_current_texture()
        file.write(f"{self.transform.pos.x:.4f},{self.transform.pos.y:.4f},{self.transform.scale:.4f},{curr_tex.width},{curr_tex.height}")
        file.close()