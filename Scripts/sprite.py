from animation import Animation
from transform import Transform2D
import math
from pyray import *
from raylib import *

class Sprite:

    all_sprites:list = []

    def __init__(self, transform:Transform2D, animations:list[Animation], anim_speed:float = 1.0):
        self.transform = transform
        self.animations = animations
        self.anim_speed = anim_speed
        self.anim_index = 0
        self.facing_direction_x = 1
        self.facing_direction_y = 1
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

        hypotenuse = math.sqrt(texture.width**2 + texture.height**2)
        angle = math.atan(float(texture.height) / float(texture.width)) + math.radians(self.transform.rot)

        return Vector2(self.transform.pos.x + (hypotenuse * math.cos(angle) * self.transform.scale * 0.5), self.transform.pos.y + (hypotenuse * math.sin(angle) * self.transform.scale * 0.5))

    def center_position_at_other(self, pos):
        texture = self.get_current_animation().get_current_texture()

        hypotenuse = math.sqrt(texture.width**2 + texture.height**2)
        angle = math.atan(float(texture.height) / float(texture.width)) + math.radians(self.transform.rot)

        return Vector2(pos.x - (hypotenuse * math.cos(angle) * self.transform.scale * 0.5), pos.y - (hypotenuse * math.sin(angle) * self.transform.scale * 0.5))

    
    def rotate_around_center(self, rotation:float):
        prev_centered_position = self.get_center_position_at_self()
        self.transform.rot = rotation
        new_centered_position = self.get_center_position_at_self()
        diff = vector2_subtract(prev_centered_position, new_centered_position)
        self.transform.pos = vector2_add(self.transform.pos, diff)

    def flip_sprite_horiz(self):
        self.facing_direction_x = -self.facing_direction_x
        for anim in self.animations:
            for i, tex in enumerate(anim.loaded_textures):
                image_to_flip = load_image_from_texture(tex)
                image_flip_horizontal(image_to_flip)
                unload_texture(tex)
                anim.loaded_textures[i] = load_texture_from_image(image_to_flip)

    def flip_sprite_vert(self):
        self.facing_direction_y = -self.facing_direction_y
        for anim in self.animations:
            for i, tex in enumerate(anim.loaded_textures):
                image_to_flip = load_image_from_texture(tex)
                image_flip_vertical(image_to_flip)
                unload_texture(tex)
                anim.loaded_textures[i] = load_texture_from_image(image_to_flip)