from animation import Animation
from clickable import Clickable
from pyray import *
from raylib import *
from transform import Transform2D

class Button(Clickable):
    def __init__(self, transform:Transform2D, animations:list[Animation], pos:Vector2, event):
        super().__init__(transform, animations)

        # initialize the position of the button and current animation speed
        transform.pos = self.center_position_at_other(pos)
        self.curr_anim_speed = 0
        # initialize mouse events to play animations and run functions
        self.on_mouse_enter = lambda : self.play_animation(0)
        self.on_mouse_exit = lambda : self.stop_animation(0)
        self.on_mouse_click = lambda : self.__event(event)
    
    def __event(self, event):
        # run the function provided and play the sound
        event()
        play_sound(load_sound("Assets\\Sounds\\Menu_Click.wav"))