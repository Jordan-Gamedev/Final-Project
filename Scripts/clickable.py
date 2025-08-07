from pyray import *
from raylib import *

from animation import Animation
from cursor import Cursor
from sprite import Sprite
from transform import Transform2D

class Clickable(Sprite):
    
    def __init__(self, transform:Transform2D, animations:list[Animation], anim_speed:float = 1.0, \
                on_mouse_click = None, on_mouse_enter = None, on_mouse_exit = None, on_mouse_stay = None, on_mouse_absent = None):
        super().__init__(transform, animations, anim_speed)
        # initialize the mouse events, default text, and size
        self.on_mouse_click = on_mouse_click
        self.on_mouse_enter = on_mouse_enter
        self.on_mouse_exit = on_mouse_exit
        self.on_mouse_stay = on_mouse_stay
        self.on_mouse_absent = on_mouse_absent
        self.__is_mouse_in = False
        self.text_over_sprite = ""
        self.text_over_sprite_size = 0

    def update(self, dt):

        super().update(dt)

        # was the mouse within the hitbox last frame?
        was_mouse_in_prev = self.__is_mouse_in

        # get the current texture dimensions to use as a hitbox
        tex_dimensions = Vector2(self.transform.scale * self.get_current_animation().get_current_texture().width, \
                                self.transform.scale * self.get_current_animation().get_current_texture().height)

        # check if the mouse is within the hitbox
        self.__is_mouse_in = self.transform.pos.x < Cursor.global_mouse_position.x < self.transform.pos.x + tex_dimensions.x and \
            self.transform.pos.y < Cursor.global_mouse_position.y < self.transform.pos.y + tex_dimensions.y

        # clicked on hitbox
        if self.on_mouse_click != None and is_mouse_button_pressed(0) and self.__is_mouse_in:
            self.on_mouse_click()
        # mouse just entered hitbox
        elif self.on_mouse_enter != None and not was_mouse_in_prev and self.__is_mouse_in:
            self.on_mouse_enter()
        # mouse just exited hitbox
        elif self.on_mouse_exit != None and was_mouse_in_prev and not self.__is_mouse_in:
            self.on_mouse_exit()
        # mouse is still in hitbox
        elif self.on_mouse_stay != None and was_mouse_in_prev and self.__is_mouse_in:
            self.on_mouse_stay()
        # mouse is still outside of hitbox
        elif self.on_mouse_absent != None and not was_mouse_in_prev and not self.__is_mouse_in:
            self.on_mouse_absent()

    def render(self):
        super().render()
        # calculate the text position in relation to the button sprite
        text_pos_x = int(self.get_center_position_at_self().x)
        text_pos_y = int(self.get_center_position_at_self().y)
        # center the text based on the text length
        text_pos_x -= measure_text(self.text_over_sprite, self.text_over_sprite_size) // 2
        text_pos_y -= self.text_over_sprite_size // 2
        # draw the text over the button
        draw_text(self.text_over_sprite, text_pos_x, text_pos_y, self.text_over_sprite_size, WHITE)