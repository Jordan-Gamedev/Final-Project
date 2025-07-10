from os.path import join
from pyray import *
from raylib import *
from dynamic_sprite import *
import sprite

class Bug(DynamicSprite):
    
    def __init__(self, textures, anim_speed, max_hp, damage_size, pos = Vector2(), rot = 0.0, scale = 1.0):
        self.damage_size = damage_size
        self.hp:float = max_hp
        super().__init__(textures, anim_speed, pos, rot, scale)
    
    def update(self, dt):
        super().update(dt)

        if file_exists(join("Data", "Player_Data.txt")):
            file_data = []
            file = open(join("Data", "Player_Data.txt"), "r")
            
            for line in file:
                if ':' in line:
                    value = line.split(': ', 1)[1].strip()
                    file_data.append(value)
            
            file.close()

            if len(file_data) > 1:
                
                # centered player position
                player_pos = Vector2(float(file_data[0]) + (float(file_data[4]) * float(file_data[3]) / 2.0), float(file_data[1]) + (float(file_data[5]) * float(file_data[3]) / 2.0))
                
                if vector2_distance(self.get_center_position_at_self(), player_pos) <= self.damage_size:
                    self.hp = max(0.0, self.hp - dt)
                    if self.hp == 0.0:
                        sprite.Sprite.all_sprites.remove(self)
            print(f"Bug pos: ({self.pos.x:.2f}, {self.pos.y:.2f})  Player pos: ({player_pos.x:.2f}, {player_pos.y:.2f}  hp: {self.hp:.2f})")