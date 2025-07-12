from pyray import *
from raylib import *
from dynamic_sprite import *

class Bug(DynamicSprite):
    
    all_bugs:list = []

    def __init__(self, textures_paths, loaded_textures, anim_speed, max_hp, damage_size, pos = Vector2(), rot = 0.0, scale = 1.0):
        self.damage_size = damage_size
        self.hp:float = max_hp
        Bug.all_bugs.append(self)
        super().__init__(textures_paths, loaded_textures, anim_speed, pos, rot, scale)
    
    def update(self, dt):
        super().update(dt)

        if file_exists("Data\Player_Data.txt"):
            file_data = []
            file = open("Data\Player_Data.txt", "r")
            
            for line in file:
                if ':' in line:
                    value = line.split(': ', 1)[1].strip()
                    file_data.append(value)
            
            file.close()

            if len(file_data) > 4:
                
                # centered player position
                player_pos = Vector2(float(file_data[0]) + (float(file_data[3]) * float(file_data[2]) / 2.0), float(file_data[1]) + (float(file_data[4]) * float(file_data[2]) / 2.0))
                if vector2_distance(self.get_center_position_at_self(), player_pos) <= self.damage_size:
                    self.hp = max(0.0, self.hp - dt)
            
            world_edge = (-400, get_monitor_width(get_current_monitor()) + 400)

            if self.hp == 0.0 or self.pos.x < world_edge[0] or self.pos.x > world_edge[1]:
                Sprite.all_sprites.remove(self)
                Bug.all_bugs.remove(self)
                print("Bug Destroyed")