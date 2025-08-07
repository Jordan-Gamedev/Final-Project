from os import path
from pyray import *
from raylib import *
from cursor import Cursor
from dynamic_sprite import *
from particle_spawner import SpawnParticles
import save_data_handler

class Bug(DynamicSprite):
    # keep track of all bug instances
    all_bugs:list[Sprite] = []
    blood_anim = None

    def create_particle_anim():
        # get the particle animation
        Bug.blood_anim = Animation("Assets\\Sprites\\Liquid_Drop", 50)

    def __init__(self, transform:Transform2D, animations:list, damage_size:float, max_hp:float, points:int, speed:float, anim_speed:float = 1.0, blood_color=GREEN):
        super().__init__(transform, animations, speed, anim_speed)
        # cache the particle textures when the first bug is spawned
        if not Bug.blood_anim:
            Bug.create_particle_anim()

        # create a particle spawner instance per bug and provide the animation, sound, color, and spawn rate
        self.particle_spawner = SpawnParticles(.05, Bug.blood_anim, load_sound("Assets\\Sounds\\Plop_Sound.wav"), blood_color)
        # set the zone to damage the bug, the max hp, and the point value
        self.damage_size:float = damage_size
        self.hp:float = max_hp
        self.points = points
        Bug.all_bugs.append(self)
    
    def try_capture(self) -> bool:
        
        # find the bug's current position
        bug_pos = vector2_add(self.get_center_position_at_self(), Vector2(-get_window_position().x, -get_window_position().y))        
        
        # checks if the bug is in its biome window
        window_pos = get_window_position()
        bug_is_in_window = window_pos.x < self.get_center_position_at_self().x < window_pos.x + get_screen_width() and \
            window_pos.y < self.get_center_position_at_self().y < window_pos.y + get_screen_height()
        
        # check if the bug is visible for capture, the left click button is pressed, and whether the bug is within capture distance
        if bug_is_in_window and Cursor.is_global_mouse_left_pressed and vector2_distance(Cursor.global_mouse_position, bug_pos) <= self.damage_size:
            
            # get the save file and data with read/write permissions
            file, file_data = save_data_handler.open_save_file("r+")
            # get the number of jars available and the number of captured jars
            num_jars_restored = int(file_data[1])
            num_jars_holding_bugs = len(file_data) - 4
            # determine if the capture is a success
            success = num_jars_holding_bugs < num_jars_restored
            # append the animation folder, frame duration, point worth, and scale of the bug to the save file
            if success:
                file_data.append(f"{path.dirname(self.animations[0].get_current_texture_path())},{self.animations[0].frame_duration},{self.points},{self.transform.scale:.2f}")
                # play the capture sound
                play_sound(load_sound("Assets\\Sounds\\Jar_Clink.wav"))
            # write the new data to the file
            for data in file_data:
                file.write(f"{data}\n")
            #close the save data
            save_data_handler.close_save_file(file)

            return success

    def update(self, dt):
        super().update(dt)
        # call the particle spawner update method
        self.particle_spawner.update(dt)

        # get the shared player data file to get the player position
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

            # destroy the bugs if captured and early exit
            if self.try_capture():
                Sprite.all_sprites.remove(self)
                Bug.all_bugs.remove(self)
                return
            
            # check if the player is within the window bounds
            player_is_in_window = window_pos.x < player_pos.x < window_pos.x + get_screen_width() and \
                window_pos.y < player_pos.y < window_pos.y + get_screen_height()

            # check if the player is in bug damaging range
            if player_is_in_window and vector2_distance(self.get_center_position_at_self(), player_pos) <= self.damage_size:
                # clamp the bug's health to zero and decrease health over time
                self.hp = max(0.0, self.hp - dt)
                # update the particle spawner position
                self.particle_spawner.spawn_pos = self.get_center_position_at_self()
                # tell the particle spawner to spawn particles
                self.particle_spawner.spawn_particle = True
            else:
                self.particle_spawner.spawn_particle = False
            
            # get the world edges
            world_edge_x = (-400, get_monitor_width(get_current_monitor()) + 400)
            world_edge_y = (-400, get_monitor_height(get_current_monitor()) + 400)
            
            # reward points to the player when a bug dies from health loss
            if self.hp == 0.0:
                # load and play the bug eat sound
                fx = load_sound("Assets\\Sounds\\Eating_Bug.wav")
                set_sound_volume(fx, .5)
                play_sound(fx)
                
                # open the save file in read/write mode
                file, file_data = save_data_handler.open_save_file("r+")
                
                # add points
                points = int(file_data[0])
                points += self.points
                file_data[0] = str(points)
                
                # finalize change
                for data in file_data:
                    file.write(f"{data}\n")
                
                save_data_handler.close_save_file(file)

            # destroy the bug if it ever strays too far from the game world
            pos = self.transform.pos
            if self.hp == 0.0 or pos.x < world_edge_x[0] or pos.x > world_edge_x[1] or pos.y < world_edge_y[0] or pos.y > world_edge_y[1]:
                Sprite.all_sprites.remove(self)
                Bug.all_bugs.remove(self)