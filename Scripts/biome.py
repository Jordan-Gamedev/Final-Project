from animation import Animation
from clickable import Clickable
from pyray import *
from subprocess import Popen
from transform import Transform2D

class Biome:

    def __init__(self, name:str, initial_price:int, starting_expand_price:int, expand_price_hike_mult:int, starting_size:int, size_increment:int, \
                max_size:int, button_price_hidden_path:str, button_size_price_hidden_path:str, button_price_revealed_path:str, button_pos:Vector2):
        
        # biome pricing
        self.initial_price = initial_price
        self.starting_expand_price = starting_expand_price
        self.expand_price_hike_mult = expand_price_hike_mult
        self.times_purchased = 0
        
        # biome stats
        self.name = name
        self.starting_size = starting_size
        self.size_increment = size_increment
        self.max_size = max_size
        self.subprocess:Popen = None

        # create a biome purchase button
        self.purchase_button = Clickable(Transform2D(scale=2.5),\
            [Animation(button_price_hidden_path, (100,)),\
            Animation(button_size_price_hidden_path, (100,)),\
            Animation(button_price_revealed_path, (100,))], anim_speed=0)
        self.purchase_button.transform.pos = self.purchase_button.center_position_at_other(button_pos)
        self.purchase_button.on_mouse_enter = self.__reveal_pricing
        self.purchase_button.on_mouse_exit = self.__hide_pricing
        self.purchase_button.text_over_sprite_size = 32

    def __del__(self):
        self.close_biome()

    def get_price(self) -> int:
        if self.times_purchased == 0:
            return self.initial_price
        else:
            return int(self.starting_expand_price * (self.expand_price_hike_mult ** (self.times_purchased - 1)))
    
    def can_obtain(self) -> bool:
        # only obtain if it still has room to expand
        return self.get_size() < self.max_size
    
    def obtain(self):

        # purchase biome
        self.times_purchased += 1

        # open the biome on first purchase
        if self.times_purchased == 1:
            self.open_biome()

        self.__reveal_pricing()

    def get_size(self):
        return min(self.starting_size + (self.size_increment * (self.times_purchased - 1)), self.max_size)
    
    def open_biome(self):
        if self.subprocess == None and self.times_purchased > 0:
            self.subprocess = Popen(["python", "Scripts\\biome_process.py", self.name])

    def close_biome(self):
        if self.subprocess != None:
            self.subprocess = self.subprocess.kill()

    def __reveal_pricing(self):
        self.purchase_button.play_animation(2)
        if self.get_size() < self.max_size:
            self.purchase_button.text_over_sprite = str(self.get_price())
        else:
            self.purchase_button.text_over_sprite = "MAX"

    def __hide_pricing(self):
        self.purchase_button.text_over_sprite = ""
        if self.times_purchased == 0:
            self.purchase_button.play_animation(0)
        else:
            self.purchase_button.play_animation(1)