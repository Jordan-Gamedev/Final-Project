import os
from os.path import join
from pyray import *
from raylib import *
import shutil

from bug import *
from hopping_bug import *
from cursor import *
from dynamic_sprite import *
from player import *
from sprite import *
import subprocess

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

############################ import assets ############################

os.makedirs("Data", exist_ok=True)
open(join("Data", "Shared_Main_Process_Sprite_Data.txt"), "w").close()

player_textures = [join("Assets", "Bat_1.png"), join("Assets", "Bat_2.png")]
cursor_textures = [join("Assets", "Cursor_Idle_1.png"), join("Assets", "Cursor_Idle_2.png"), join("Assets", "Cursor_Idle_3.png")]
gnat_textures = [join("Assets", "Gnat_1.png"), join("Assets", "Gnat_2.png")]
grass_texture = [join("Assets", "Grass_1.png")]

############################## game loop ##############################

player = Player(player_textures, 10.0, Vector2(), rot = 0.0, scale=4.9)
player.speed = 1000

cursor = Cursor(cursor_textures, 5.0, get_mouse_position())

gnat = Bug(gnat_textures, 15.0, 1.0, 50.0, Vector2(200, 200), 0, 2)

hop_strength = (Vector2(2, 2), Vector2(6, 12))
grasshopper = HoppingBug(gnat_textures, 15.0, 1.0, 50.0, hop_strength=hop_strength, \
                          idle_time=Vector2(3, 6), pos=Vector2(400, 500), rot=0, scale=2)
grasshopper.speed = 100

grass = Sprite(grass_texture, 0.0, Vector2(0, get_monitor_height(current_monitor) - (27 * 5)), 0.0, 2.5)

process = subprocess.Popen(["python", join("Scripts", "sub.py")])

while not window_should_close():

    # updating

    delta_time = get_frame_time()

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
    file = open(join("Data", "Shared_Main_Process_Sprite_Data.txt"), "w")
    file.truncate()
    
    new_file_contents = f"{player.get_current_texture_path()},{player.pos.x:.2f},{player.pos.y:.2f},{player.rot:.2f},{player.scale:.2f}\n"

    little_bug:Bug = None
    for little_bug in Bug.all_bugs:
        new_file_contents += f"{little_bug.get_current_texture_path()},{little_bug.pos.x:.2f},{little_bug.pos.y:.2f},{little_bug.rot:.2f},{little_bug.scale:.2f}\n"

    file.write(new_file_contents)
    file.close()

process.kill()

while os.path.exists("Data"):
    shutil.rmtree("Data", ignore_errors=True)

close_window()