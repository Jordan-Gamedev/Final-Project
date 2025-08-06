from os import path
from pyray import *
from raylib import *
from cursor import Cursor
from dynamic_sprite import *
from particle_spawner import SpawnParticles
import save_data_handler

class Bug(DynamicSprite):
    all_bugs:list[Sprite] = []
    blood_anim = None

    def create_particle_anim():
        Bug.blood_anim = Animation("Assets\\Sprites\\Liquid_Drop", 50)

    def __init__(self, transform:Transform2D, animations:list, damage_size:float, max_hp:float, points:int, speed:float, anim_speed:float = 1.0, blood_color=GREEN):
        super().__init__(transform, animations, speed, anim_speed)
        
        if not Bug.blood_anim:
            Bug.create_particle_anim()

        self.particle_spawner = SpawnParticles(.05, Bug.blood_anim, load_sound("Assets\\Sounds\\Plop_Sound.wav"), blood_color)
        self.damage_size:float = damage_size
        self.hp:float = max_hp
        self.points = points
        Bug.all_bugs.append(self)
    
    def try_capture(self) -> bool:
        bug_pos = vector2_add(self.get_center_position_at_self(), Vector2(-get_window_position().x, -get_window_position().y))        
        if vector2_distance(Cursor.global_mouse_position, bug_pos) <= self.damage_size and Cursor.is_global_mouse_left_pressed:
            file, file_data = save_data_handler.open_save_file("r+")
            
            num_jars_restored = int(file_data[1])
            num_jars_holding_bugs = len(file_data) - 4

            success = num_jars_holding_bugs < num_jars_restored

            if success:
                file_data.append(f"{path.dirname(self.animations[0].get_current_texture_path())},{self.animations[0].frame_duration},{self.points},{self.transform.scale:.2f}")
                
            for data in file_data:
                file.write(f"{data}\n")
            
            save_data_handler.close_save_file(file)
            return success

    def update(self, dt):
        super().update(dt)

        self.particle_spawner.update(dt)

        if file_exists("Data\\Player_Data.txt"):
            file = open("Data\\Player_Data.txt", "r")
            values = file.readline().split(',')
            file_data = [value for value in values]
            file.close()
            
            if file_data[0] == '':
                return

            # centered player position
            player_pos = Vector2(float(file_data[0]) + (float(file_data[3]) * float(file_data[2]) / 2.0), float(file_data[1]) + (float(file_data[4]) * float(file_data[2]) / 2.0))
                
            window_pos = get_window_position()

            if self.try_capture():
                Sprite.all_sprites.remove(self)
                Bug.all_bugs.remove(self)
                return
            
            player_is_in_window = window_pos.x < player_pos.x < window_pos.x + get_screen_width() and \
            window_pos.y < player_pos.y < window_pos.y + get_screen_height()

            if player_is_in_window and vector2_distance(self.get_center_position_at_self(), player_pos) <= self.damage_size:
                self.hp = max(0.0, self.hp - dt)
                self.particle_spawner.spawn_pos = self.get_center_position_at_self()
                self.particle_spawner.spawn_particle = True
            else:
                self.particle_spawner.spawn_particle = False
            
            world_edge_x = (-400, get_monitor_width(get_current_monitor()) + 400)
            world_edge_y = (-400, get_monitor_height(get_current_monitor()) + 400)
            
            # reward points to the player when a bug dies from health loss
            if self.hp == 0.0:
                fx = load_sound("Assets\\Sounds\\Eating_Bug.wav")
                set_sound_volume(fx, .5)
                play_sound(fx)
                
                file, file_data = save_data_handler.open_save_file("r+")
                
                # add points
                points = int(file_data[0])
                points += self.points
                file_data[0] = str(points)
                
                # finalize change
                for data in file_data:
                    file.write(f"{data}\n")
                
                save_data_handler.close_save_file(file)

            pos = self.transform.pos
            if self.hp == 0.0 or pos.x < world_edge_x[0] or pos.x > world_edge_x[1] or pos.y < world_edge_y[0] or pos.y > world_edge_y[1]:
                Sprite.all_sprites.remove(self)
                Bug.all_bugs.remove(self)