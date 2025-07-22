from transform import Transform2D
from pyray import *
from raylib import *

class Sprite:

    all_sprites:list = []

    def __init__(self, transform:Transform2D, animations:list, anim_speed:float = 1.0):
        self.transform = transform
        self.animations = animations
        self.anim_speed = anim_speed
        self.anim_index = 0
        Sprite.all_sprites.append(self)
    
    def update(self, dt):
        self.get_current_animation().update(self.anim_speed * dt)
        
    def render(self, offset=Vector2()):
        draw_texture_ex(self.get_current_animation().get_current_texture(), vector2_add(self.transform.pos, offset), self.transform.rot, self.transform.scale, WHITE)

    def play_animation(self, anim_index):
        curr_anim = self.get_current_animation()
        curr_anim.curr_frame = 0
        curr_anim.curr_frame_time = 0.0
        self.anim_index = anim_index

    def get_current_animation(self):
        return self.animations[self.anim_index]

    def get_center_position_at_self(self):
        texture = self.get_current_animation().get_current_texture()
        return Vector2(self.transform.pos.x + (texture.width * self.transform.scale / 2.0), self.transform.pos.y + (texture.height * self.transform.scale / 2.0))

    def center_position_at_other(self, pos):
        texture = self.get_current_animation().get_current_texture()
        return Vector2(pos.x - (texture.width * self.transform.scale / 2.0), pos.y - (texture.height * self.transform.scale / 2.0))