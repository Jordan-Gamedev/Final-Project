from pyray import *
from raylib import *

class Sprite:

    all_sprites:list = []

    def __init__(self, textures_paths:list, loaded_textures:list, anim_speed, pos = Vector2(), rot = 0.0, scale = 1.0):
        self.textures_paths = textures_paths
        self.loaded_textures = loaded_textures
        self.curr_tex_index = 0.0
        self.anim_speed = anim_speed
        self.pos = pos
        self.rot = rot
        self.scale = scale
        Sprite.all_sprites.append(self)
    
    def update(self, dt):
        self.curr_tex_index += (self.anim_speed * dt)
        self.curr_tex_index %= len(self.loaded_textures)
        
    def render(self, offset=Vector2()):
        draw_texture_ex(self.get_current_texture(), vector2_add(self.pos, offset), self.rot, self.scale, WHITE)

    def get_current_texture(self):
        return self.loaded_textures[int(self.curr_tex_index)]
    
    def get_current_texture_path(self):
        return self.textures_paths[int(self.curr_tex_index)]

    def get_center_position_at_self(self):
        texture = self.get_current_texture()
        return Vector2(self.pos.x + (texture.width * self.scale / 2.0), self.pos.y + (texture.height * self.scale / 2.0))

    def center_position_at_other(self, pos):
        texture = self.get_current_texture()
        return Vector2(pos.x - (texture.width * self.scale / 2.0), pos.y - (texture.height * self.scale / 2.0))