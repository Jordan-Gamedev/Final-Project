from pyray import *
from raylib import *
from cursor import Cursor
from dynamic_sprite import *
from particle_spawner import SpawnParticles
import save_data_handler
from shop import Shop

class Bug(DynamicSprite):
    all_bugs:list[Sprite] = []
    blood_anim = None

    def create_particle_anim():
        Bug.blood_anim = Animation("Assets\\Sprites\\Liquid_Drop", (50, 50, 50, 50, 50, 50))

    def __init__(self, transform:Transform2D, animations:list, damage_size:float, max_hp:float, points:int, speed:float, anim_speed:float = 1.0):
        super().__init__(transform, animations, speed, anim_speed)
        
        if not Bug.blood_anim:
            Bug.create_particle_anim()

        self.particle_spawner = SpawnParticles(.05, Bug.blood_anim, load_sound("Assets\\Sounds\\Plop_Sound.wav"))
        self.damage_size:float = damage_size
        self.hp:float = max_hp
        self.points = points
        Bug.all_bugs.append(self)
    
    def is_captured(self) -> bool:
        if vector2_distance(Cursor.global_mouse_position, self.get_center_position_at_self()) <= self.damage_size and Cursor.is_global_mouse_left_pressed:
            for jar in Shop.jars:
                if not jar.bug_anim:
                    jar.bug_anim = self.animations[0]
                    jar.bug_scale = self.transform.scale
                    jar.points = self.points
                    return True
        return False

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

            if self.is_captured():
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
                points = file_data[0]
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