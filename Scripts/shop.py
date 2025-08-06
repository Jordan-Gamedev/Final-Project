from io import TextIOWrapper
import os
from pyray import *

from animation import Animation
from biome import Biome
from clickable import Clickable
from sprite import Sprite
from transform import Transform2D

def open_save_file() -> TextIOWrapper:
        
        # make this process wait for the saving process to finish
        while not file_exists("PersistentData\\Save_Data.txt"):
            pass
        
        # renaming a file can sometimes cause permission errors for a few frames, so keep trying until success
        while True:
            
            try:
                # open and get file data
                os.rename("PersistentData\\Save_Data.txt", "PersistentData\\Save_Data.saving")
                file = open("PersistentData\\Save_Data.saving", "r+")
                return file
            except:
                pass

def close_save_file(file:TextIOWrapper):
    file.close()
    os.rename("PersistentData\\Save_Data.saving", "PersistentData\\Save_Data.txt")

class Shop:

    def __init__(self, max_jars = 5, starting_jar_cost = 250, jar_price_hike_mult = 2, purchaseable_biomes:list[Biome] = []):
        
        # jar economy
        self.max_jars = max_jars
        self.starting_jar_cost = starting_jar_cost
        self.jar_price_hike_mult = jar_price_hike_mult

        # get data from the save file
        file = open_save_file()
        file_data = [line for line in file]
        close_save_file(file)
        
        # get the number of jars already purchased from the save file
        self.num_jars = int(file_data[1])

        # set the times purchased for the biomes to the save data's purchase values
        self.purchaseable_biomes = purchaseable_biomes
        for i in range(len(self.purchaseable_biomes)):
            self.purchaseable_biomes[i].times_purchased = int(file_data[2 + i])
            self.purchaseable_biomes[i]._Biome__hide_pricing()

        # make the biome purchase buttons able to purchase their respective biomes
        for i in range(len(self.purchaseable_biomes)):
            self.purchaseable_biomes[i].purchase_button.on_mouse_click = lambda i=i : self.buy_biome(i)

        # create a jar purchase button
        self.jar_button = Clickable(Transform2D(scale=2.5), [Animation("Assets\\Sprites\\Shop_Buttons\\Jar_Price_Hidden", (100,)),\
            Animation("Assets\\Sprites\\Shop_Buttons\\Jar_Price_Revealed", (100,))], anim_speed=0)
        self.jar_button.transform.pos = self.jar_button.center_position_at_other(Vector2(get_monitor_width(get_current_monitor()) * 0.45, get_monitor_height(get_current_monitor()) * 0.56))
        self.jar_button.on_mouse_enter = self.__reveal_jar_pricing
        self.jar_button.on_mouse_exit = self.__hide_jar_pricing
        self.jar_button.on_mouse_click = self.buy_jar
        self.jar_button.text_over_sprite_size = 32

        # load jar textures
        self.restored_jar_texture = load_texture("Assets\\Sprites\\Bug_Bottle\\Bug_Bottle_1.png")
        self.broken_jar_texture = load_texture("Assets\\Sprites\\Bug_Bottle\\Bug_Bottle_2.png")

    def get_jar_price(self) -> int:
        return int(self.starting_jar_cost * (self.jar_price_hike_mult ** self.num_jars))

    def buy_jar(self) -> bool:

        # safely open the save file for reading and writing
        file:TextIOWrapper = open_save_file()

        # get the data from the file and wipe the file
        file_data = [line.strip() for line in file.readlines()]
        file.seek(0)
        file.truncate()
        
        # get the points and number of jars
        points = int(file_data[0])
        
        # current jar cost
        jar_cost = self.get_jar_price()

        # player has all the jars or is too broke to buy a jar
        if self.num_jars == self.max_jars or points < jar_cost:
            # unsuccessful purchase
            for data in file_data:
                file.write(f"{data}\n")
            close_save_file(file)
            return False

        # spend the points
        points -= jar_cost
        file_data[0] = f"{points}"
        
        # add the jar
        self.num_jars += 1
        self.__reveal_jar_pricing()
        file_data[1] = self.num_jars

        # finalize the change
        for data in file_data:
            file.write(f"{data}\n")
        close_save_file(file)

        play_sound(load_sound("Assets\\Sounds\\Purchase_FX.wav"))

        # successfully purchased
        return True

    def buy_biome(self, biome_index:int) -> bool:

        # safely open the save file for reading and writing
        file:TextIOWrapper = open_save_file()

        # get the data from the file and wipe the file
        file_data = [line.strip() for line in file.readlines()]
        file.seek(0)
        file.truncate()
        
        # get the points
        points = int(file_data[0])

        # player is too broke to buy this biome or the biome is maxed
        if points < self.purchaseable_biomes[biome_index].get_price() or not self.purchaseable_biomes[biome_index].can_obtain():
            # unsuccessful purchase
            for data in file_data:
                file.write(f"{data}\n")
            close_save_file(file)
            return False

        # spend the points
        points -= self.purchaseable_biomes[biome_index].get_price()
        file_data[0] = str(points)

        # obtain the biome
        self.purchaseable_biomes[biome_index].obtain()

        # save the biome purchase
        file_data[biome_index + 2] = str(self.purchaseable_biomes[biome_index].times_purchased)

        # finalize the change
        for data in file_data:
            file.write(f"{data}\n")
        close_save_file(file)
        
        play_sound(load_sound("Assets\\Sounds\\Purchase_FX.wav"))

        # successfully purchased
        return True

    def close_shop(self):
        for biome in self.purchaseable_biomes:
            biome.close_biome()
        try:
            Sprite.all_sprites.remove(self.jar_button)
        except:
            pass

    def render(self):

        monitor_width = get_monitor_width(get_current_monitor())
        pos = Vector2(monitor_width * 0.42, get_monitor_height(get_current_monitor()) * 0.43)

        for i in range(self.num_jars):
            draw_texture_ex(self.restored_jar_texture, Vector2(pos.x + (monitor_width * i * 0.07), pos.y), 0, 3, WHITE)

        for i in range(self.max_jars - self.num_jars):
            draw_texture_ex(self.broken_jar_texture, Vector2(pos.x + (monitor_width * (i + self.num_jars) * 0.07), pos.y), 0, 3, WHITE)

    def __reveal_jar_pricing(self):
        self.jar_button.play_animation(1)

        if self.num_jars < self.max_jars:
            self.jar_button.text_over_sprite = str(self.get_jar_price())
        else:
            self.jar_button.text_over_sprite = "MAX"
    
    def __hide_jar_pricing(self):
        self.jar_button.play_animation(0)
        self.jar_button.text_over_sprite = ""