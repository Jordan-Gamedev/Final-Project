import os
from pyray import *
from raylib import *
import shutil
import subprocess

from animation import *
from bug import *
from bug_spawner import SpawnBugs
from cursor import *
from dynamic_sprite import *
from hopping_bug import *
from player import *
from sprite import *

########################## create data files ##########################
def set_up_data_files():

    # delete data files in case the program crashed last time and the corrupted files are still there
    if os.path.exists("Data"):
        shutil.rmtree("Data", ignore_errors=True)

    # create temporary and persistent data folders if they do not exist
    os.makedirs("Data", exist_ok=True)
    os.makedirs("PersistentData", exist_ok=True)

    # create temporary data files
    open("Data\\Shared_Main_Process_Sprite_Data.txt", "x").close()
    open("Data\\Player_Data.txt", "x").close()
    open("Data\\Mouse_Data.txt", "x").close()

    # delete corrupt backup save (worse case scenario for the user)
    if file_exists("PersistentData\\Backup_Save_Data.saving"):
        os.remove("PersistentData\\Backup_Save_Data.saving")

    # recover corrupt save data from backup save, or delete it if there is no backup
    if file_exists("PersistentData\\Save_Data.saving"):
        
        # backup save exists, so recover data
        if file_exists("PersistentData\\Backup_Save_Data.txt"):
            os.rename("PersistentData\\Save_Data.saving", "PersistentData\\Save_Data.txt")
            shutil.copyfile("PersistentData\\Backup_Save_Data.txt", "PersistentData\\Save_Data.txt")
        # backup save was somehow also corrupted and now does not exist, so delete corrupt data
        else:
            os.remove("PersistentData\\Save_Data.saving")

    # create save data file if it does not exist
    if not file_exists("PersistentData\\Save_Data.txt"):
        with open("PersistentData\\Save_Data.txt", "w") as file:
            # Points, Size of Desert
            file.write(f"{0},{0}")
    
    # create backup save data file
    open("PersistentData\\Backup_Save_Data.txt", "w").close()
    shutil.copyfile("PersistentData\\Save_Data.txt", "PersistentData\\Backup_Save_Data.txt")
#######################################################################

######################## set window properties ########################
def set_up_window():
    # create maximized window
    set_config_flags(FLAG_WINDOW_TRANSPARENT | FLAG_WINDOW_UNDECORATED | FLAG_WINDOW_ALWAYS_RUN | FLAG_WINDOW_RESIZABLE)
    init_window(1920, 1080, 'Game')
    maximize_window()
    
    # make Window's default cursor invisible
    hide_cursor()

    # set the maximum frame rate to the maximum refresh rate of the monitor 
    set_target_fps(get_monitor_refresh_rate(get_current_monitor()))
#######################################################################

############################ import assets ############################

def create_asset_instances():
    # set up player
    player_idle_anim = Animation("Assets\\Sprites\\Bat", (100.0, 100.0))
    player = Player(Transform2D(scale=4.9), [player_idle_anim], speed=1000)

    # set up grass which hangs out at the bottom of the screen
    grass_idle_anim = Animation("Assets\\Sprites\\Background", (250.0,))
    Sprite(Transform2D(Vector2(0, get_monitor_height(get_current_monitor()) - (27 * 5)), rot=0, scale=2.5), [grass_idle_anim])

    # set up spawner which spawns bugs over time
    gnat_idle_anim = Animation("Assets\\Sprites\\Gnat", (300.0, 300.0))
    spawner = SpawnBugs(max_capacity=12, spawn_rate=3, fly_anims=[gnat_idle_anim], hopper_anims=[gnat_idle_anim], crawler_anims=[gnat_idle_anim])

    # set up custom cursor
    cursor_idle_anim = Animation("Assets\\Sprites\\Cursor", (50.0, 50.0, 50.0))
    Cursor(Transform2D(get_mouse_position(), rot=0, scale=2), [cursor_idle_anim])

    return (player, spawner)

#######################################################################

def main():

    set_up_data_files()
    set_up_window()
    player, spawner = create_asset_instances()

    ############################## game loop ##############################

    process = subprocess.Popen(["python", "Scripts\\sub.py"])

    while not window_should_close():

        # updating
        delta_time = get_frame_time()
        spawner.update(delta_time)
        for sprite in Sprite.all_sprites:
            sprite.update(delta_time)
    
        # drawing
        begin_drawing()
        clear_background(Color(0, 0, 0, 0))

        monitor = get_current_monitor()
        draw_text("Press 'Esc' to close game", get_monitor_width(monitor) // 2 - 350, int(get_monitor_height(monitor) * 0.05), 50, WHITE)

        for sprite in Sprite.all_sprites:
            sprite.render()
    
        draw_fps(0, 0)
        end_drawing()

        # sync visuals to subprocesses
        file = open("Data\\Shared_Main_Process_Sprite_Data.txt", "w")
    
        new_file_contents = f"{player.get_current_animation().get_current_texture_path()},{player.transform.pos.x:.2f},{player.transform.pos.y:.2f},{player.transform.rot:.2f},{player.transform.scale:.2f}\n"

        for little_bug in Bug.all_bugs:
            new_file_contents += f"{little_bug.get_current_animation().get_current_texture_path()},{little_bug.transform.pos.x:.2f},{little_bug.transform.pos.y:.2f},{little_bug.transform.rot:.2f},{little_bug.transform.scale:.2f}\n"

        file.write(new_file_contents)
        file.close()

    process.kill()

    # delete temporary data
    while os.path.exists("Data"):
        shutil.rmtree("Data", ignore_errors=True)

    # update backup savefile
    if file_exists("PersistentData\\Save_Data.txt") and file_exists("PersistentData\\Backup_Save_Data.txt"):
        shutil.copyfile("PersistentData\\Save_Data.txt", "PersistentData\\Backup_Save_Data.txt")

    # close the game
    close_window()

if __name__ == "__main__":
    main()