import os
from pyray import *
from raylib import *
from dynamic_sprite import *
from particle_spawner import SpawnParticles

class Bug(DynamicSprite):
    all_bugs:list[Sprite] = []
    blood_anim = None

    def create_particle_anim():
        Bug.blood_anim = Animation("Assets\\Sprites\\Blood", (50, 50, 50, 50, 50, 50))

    def __init__(self, transform:Transform2D, animations:list, damage_size:float, max_hp:float, points:int, speed:float, anim_speed:float = 1.0):
        if not Bug.blood_anim:
            Bug.create_particle_anim()

        self.particle_spawner = SpawnParticles(False, .05, Bug.blood_anim)
        self.damage_size:float = damage_size
        self.hp:float = max_hp
        self.points = points
        Bug.all_bugs.append(self)
        super().__init__(transform, animations, speed, anim_speed)
        print("Bug Created")
    
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
                
                # make this process wait for the saving process to finish
                while not file_exists("PersistentData\\Save_Data.txt"):
                    pass
                
                # renaming a file can sometimes cause permission errors for a few frames, so keep trying until success
                while True:
                    
                    try:
                        # open and get file data
                        os.rename("PersistentData\\Save_Data.txt", "PersistentData\\Save_Data.saving")
                        file = open("PersistentData\\Save_Data.saving", "r+")
                        break

                    except:
                        pass

                file_data = [line.strip() for line in file.readlines()]
                file.seek(0)
                file.truncate()
                
                # add points
                points = int(file_data[0])
                points += self.points
                file_data[0] = f"{points}"
                
                # finalize change
                for data in file_data:
                    file.write(f"{data}\n")
                file.close()
                os.rename("PersistentData\\Save_Data.saving", "PersistentData\\Save_Data.txt")
            
            pos = self.transform.pos
            if self.hp == 0.0 or pos.x < world_edge_x[0] or pos.x > world_edge_x[1] or pos.y < world_edge_y[0] or pos.y > world_edge_y[1]:
                Sprite.all_sprites.remove(self)
                Bug.all_bugs.remove(self)
                print("Bug Destroyed")