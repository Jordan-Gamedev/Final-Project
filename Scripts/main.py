import os
from pyray import *
from raylib import *
import shutil
import subprocess

from bug import *
from bug_spawner import SpawnBugs
from cursor import *
from dynamic_sprite import *
from hopping_bug import *
from player import *
from sprite import *

def main():

    ######################## set window properties ########################

    # delete data files in case the program crashed last time and the corrupted files are still there
    while os.path.exists("Data"):
        shutil.rmtree("Data", ignore_errors=True)

    # get currently used monitor
    current_monitor = get_current_monitor()

    # create maximized window
    set_config_flags(FLAG_WINDOW_TRANSPARENT | FLAG_WINDOW_UNDECORATED | FLAG_WINDOW_ALWAYS_RUN | FLAG_WINDOW_RESIZABLE)
    init_window(1920, 1080, 'Game')
    maximize_window()
    hide_cursor()

    # set the maximum frame rate to the maximum refresh rate of the monitor 
    set_target_fps(get_monitor_refresh_rate(current_monitor))

    ########################## create data files ##########################

    os.makedirs("Data", exist_ok=True)
    os.makedirs("PersistentData", exist_ok=True)
    open("Data\Shared_Main_Process_Sprite_Data.txt", "w").close()

    # delete corrupt backup save (worse case scenario for the user)
    if file_exists("PersistentData\Backup_Save_Data.saving"):
        os.remove("PersistentData\Backup_Save_Data.saving")

    # recover corrupt save data from backup save, or delete it if there is no backup
    if file_exists("PersistentData\Save_Data.saving"):
        
        # backup save exists, so recover data
        if file_exists("PersistentData\Backup_Save_Data.txt"):
            os.rename("PersistentData\Save_Data.saving", "PersistentData\Save_Data.txt")
            shutil.copyfile("PersistentData\Backup_Save_Data.txt", "PersistentData\Save_Data.txt")
        # backup save was somehow also corrupted and now does not exist, so delete corrupt data
        else:
            os.remove("PersistentData\Save_Data.saving")

    # create save data file if it does not exist
    if not file_exists("PersistentData\Save_Data.txt"):
        file = open("PersistentData\Save_Data.txt", "w")
        # Points, Size of Desert
        file.write(f"{0},{0}")
        file.close()
    
    # create backup save data file
    open("PersistentData\Backup_Save_Data.txt", "w").close()
    shutil.copyfile("PersistentData\Save_Data.txt", "PersistentData\Backup_Save_Data.txt")
    
    ############################ import assets ############################

    player_textures_paths = ["Assets\Bat_1.png", "Assets\Bat_2.png"]
    player_loaded_textures = [load_texture(player_textures_paths[0]), load_texture(player_textures_paths[1])]

    cursor_textures_paths = ["Assets\Cursor_Idle_1.png", "Assets\Cursor_Idle_2.png", "Assets\Cursor_Idle_3.png"]
    cursor_loaded_textures = [load_texture(cursor_textures_paths[0]), load_texture(cursor_textures_paths[1]), load_texture(cursor_textures_paths[2])]

    grass_textures_paths = ["Assets\Grass_1.png"]
    grass_loaded_textures = [load_texture(grass_textures_paths[0])]

    gnat_textures_paths = ["Assets\Gnat_1.png", "Assets\Gnat_2.png"]

    ############################## game loop ##############################

    player = Player(player_textures_paths, player_loaded_textures, 10.0, Vector2(), rot = 0.0, scale=4.9)
    player.speed = 1000

    Cursor(cursor_textures_paths, cursor_loaded_textures, 5.0, get_mouse_position())

    Sprite(grass_textures_paths, grass_loaded_textures, 0.0, Vector2(0, get_monitor_height(current_monitor) - (27 * 5)), 0.0, 2.5)

    spawner = SpawnBugs(max_capacity=12, spawn_rate=3, fly_tex_paths=gnat_textures_paths, hopper_tex_paths=gnat_textures_paths, crawler_tex_paths=gnat_textures_paths)

    process = subprocess.Popen(["python", "Scripts\sub.py"])

    while not window_should_close():

        # updating

        delta_time = get_frame_time()

        spawner.update(delta_time)

        for sprite in Sprite.all_sprites:
            sprite.update(delta_time)
    
        # drawing
    
        begin_drawing()

        clear_background(Color(0, 0, 0, 0))
    
        draw_text("Press 'Esc' to close game", get_monitor_width(current_monitor) // 2 - 350, int(get_monitor_height(current_monitor) * 0.05), 50, WHITE)

        for sprite in Sprite.all_sprites:
            sprite.render()
    
        draw_fps(0, 0)
    
        end_drawing()

        # sync visuals to subprocesses
        file = open("Data\Shared_Main_Process_Sprite_Data.txt", "w")
        file.truncate()
    
        new_file_contents = f"{player.get_current_texture_path()},{player.pos.x:.2f},{player.pos.y:.2f},{player.rot:.2f},{player.scale:.2f}\n"

        little_bug:Bug = None
        for little_bug in Bug.all_bugs:
            new_file_contents += f"{little_bug.get_current_texture_path()},{little_bug.pos.x:.2f},{little_bug.pos.y:.2f},{little_bug.rot:.2f},{little_bug.scale:.2f}\n"

        file.write(new_file_contents)
        file.close()

    process.kill()

    # delete temporary data
    while os.path.exists("Data"):
        shutil.rmtree("Data", ignore_errors=True)

    # update backup savefile
    if file_exists("PersistentData\Save_Data.txt") and file_exists("PersistentData\Backup_Save_Data.txt"):
        shutil.copyfile("PersistentData\Save_Data.txt", "PersistentData\Backup_Save_Data.txt")

    # close the game
    close_window()

if __name__ == "__main__":
    main()