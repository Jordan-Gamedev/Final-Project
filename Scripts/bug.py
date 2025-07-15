import os
from pyray import *
from raylib import *
from dynamic_sprite import *

class Bug(DynamicSprite):
    
    all_bugs:list = []

    def __init__(self, transform:Transform2D, animations:list, damage_size:float, max_hp:float, points:int, speed:float, anim_speed:float = 1.0):
        self.damage_size:float = damage_size
        self.hp:float = max_hp
        self.points = points
        Bug.all_bugs.append(self)
        super().__init__(transform, animations, speed, anim_speed)
        print("Bug Created")
    
    def update(self, dt):
        super().update(dt)

        if file_exists("Data\Player_Data.txt"):
            file = open("Data\Player_Data.txt", "r")
            values = file.readline().split(',')
            file_data = [value for value in values]
            file.close()
            
            if file_data[0] == '':
                return

            # centered player position
            player_pos = Vector2(float(file_data[0]) + (float(file_data[3]) * float(file_data[2]) / 2.0), float(file_data[1]) + (float(file_data[4]) * float(file_data[2]) / 2.0))
                
            window_pos = get_window_position()

            player_is_in_window = window_pos.x < player_pos.x < window_pos.x + get_screen_width() and \
            window_pos.y < player_pos.y < window_pos.y + get_screen_height()

            if player_is_in_window and vector2_distance(self.get_center_position_at_self(), player_pos) <= self.damage_size:
                self.hp = max(0.0, self.hp - dt)
            
            world_edge_x = (-400, get_monitor_width(get_current_monitor()) + 400)
            world_edge_y = (-400, get_monitor_height(get_current_monitor()) + 400)
            
            # reward points to the player when a bug dies from health loss
            if self.hp == 0.0:
                
                # make this process wait for the saving process to finish
                while not file_exists("PersistentData\Save_Data.txt"):
                    pass
                
                # open and get file data
                os.rename("PersistentData\Save_Data.txt", "PersistentData\Save_Data.saving")
                file = open("PersistentData\Save_Data.saving", "r+")
                file_data = [value for value in file.readline().split(',', 1)]
                file.seek(0)
                file.truncate()
                
                # add points
                points = int(file_data[0])
                points += self.points
                file_data[0] = points
                
                # finalize change
                file.write(f"{file_data[0]},{file_data[1]}")
                file.close()
                os.rename("PersistentData\Save_Data.saving", "PersistentData\Save_Data.txt")
            
            pos = self.transform.pos
            if self.hp == 0.0 or pos.x < world_edge_x[0] or pos.x > world_edge_x[1] or pos.y < world_edge_y[0] or pos.y > world_edge_y[1]:
                Sprite.all_sprites.remove(self)
                Bug.all_bugs.remove(self)
                print("Bug Destroyed")