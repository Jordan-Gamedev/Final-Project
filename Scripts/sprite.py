from pyray import *
from raylib import *

class Sprite:

    all_sprites:list = []

    def __init__(self, textures, anim_speed, pos = Vector2(), rot = 0.0, scale = 1.0):
        self.textures = textures
        self.curr_tex_index = 0.0
        self.anim_speed = anim_speed
        self.pos = pos
        self.rot = rot
        self.scale = scale
        Sprite.all_sprites.append(self)
    
    def update(self, dt):
        self.curr_tex_index += (self.anim_speed * dt)
        self.curr_tex_index %= len(self.textures)
        
    def render(self):
        draw_texture_ex(self.get_current_texture(), self.pos, self.rot, self.scale, WHITE)

    def get_current_texture(self):
        return self.textures[int(self.curr_tex_index)]

    def get_center_position_at_self(self):
        texture = self.get_current_texture()
        return Vector2(self.pos.x + (texture.width * self.scale / 2.0), self.pos.y + (texture.height * self.scale / 2.0))

    def center_position_at_other(self, pos):
        texture = self.get_current_texture()
        return Vector2(pos.x - (texture.width * self.scale / 2.0), pos.y - (texture.height * self.scale / 2.0))