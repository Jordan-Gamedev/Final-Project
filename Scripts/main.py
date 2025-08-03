import os
from pyray import *
from raylib import *
import shutil
import subprocess

from animation import Animation
from bug import Bug
from bug_spawner import SpawnBugs
from clickable import Clickable
from cursor import Cursor
from particle import Particle
from player import Player
from sprite import Sprite
from transform import Transform2D

######################### globals #####################################
background_art = None
process = None
game_started:bool = False
player = None
cursor = None
grass = None
spawner = None
#######################################################################

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
    set_config_flags(FLAG_WINDOW_UNDECORATED | FLAG_WINDOW_ALWAYS_RUN | FLAG_WINDOW_RESIZABLE)
    init_window(1920, 1080, 'Game')
    maximize_window()
    
    # make Window's default cursor invisible
    hide_cursor()

    # set the maximum frame rate to the maximum refresh rate of the monitor 
    set_target_fps(get_monitor_refresh_rate(get_current_monitor()))

    global background_art ; background_art = load_texture("Assets\\Sprites\\Background\\Main_Background.jpg")
#######################################################################

def start_game():
    global game_started ; game_started = True
    Sprite.all_sprites.clear()
    create_asset_instances()
    global process ; process = subprocess.Popen(["python", "Scripts\\sub.py"])

############################ import assets ############################
def create_asset_instances():
    # set up player
    player_idle_anim = Animation("Assets\\Sprites\\Bat", (100.0, 100.0))
    global player ; player = Player(Transform2D(scale=4.9), [player_idle_anim], speed=1000)

    # set up spawner which spawns bugs over time
    gnat_idle_anim = Animation("Assets\\Sprites\\Gnat", (300.0, 300.0))
    hoverer_idle_anim = Animation("Assets\\Sprites\\Hoverer", (50, 50))
    hopper_idle_anim = Animation("Assets\\Sprites\\Hopper\\Idle", (50, 50, 50, 50, 50, 50))
    hopper_jump_anim = Animation("Assets\\Sprites\\Hopper\\Jump", (50, 50, 50, 50, 50, 50), is_loop=False)
    crawler_idle_anim = Animation("Assets\\Sprites\\Crawler\\Idle", (50, 50, 50, 50, 50, 50, 50, 50))
    crawler_walk_anim = Animation("Assets\\Sprites\\Crawler\\Walk", (50, 50, 50, 50, 50, 50))
    crawler_fall_anim = Animation("Assets\\Sprites\\Crawler\\Fall", (25, 25, 25, 25, 25, 25))
    global spawner ; spawner = SpawnBugs(max_capacity=15, spawn_rate=1, fly_anims=[gnat_idle_anim], hover_anims=[hoverer_idle_anim], \
                    hopper_anims=[hopper_idle_anim, hopper_jump_anim], crawler_anims=[crawler_idle_anim, crawler_walk_anim, crawler_fall_anim])

    # set up custom cursor
    cursor_idle_anim = Animation("Assets\\Sprites\\Cursor", (50.0, 50.0, 50.0))
    global cursor ; cursor = Cursor(Transform2D(get_mouse_position(), rot=0, scale=2), [cursor_idle_anim])

    # set up grass which hangs out at the bottom of the screen
    grass_idle_anim = Animation("Assets\\Sprites\\Background", (250.0,))
    global grass ; grass = Sprite(Transform2D(Vector2(0, get_monitor_height(get_current_monitor()) - (27 * 5)), rot=0, scale=2.5), [grass_idle_anim])
#######################################################################

############################# start menu ##############################
def start_menu():
    # updating
    delta_time = get_frame_time()
    
    for sprite in Sprite.all_sprites:
        sprite.update(delta_time)

    # drawing
    begin_drawing()
    clear_background(Color(0, 0, 0, 0))
    source_rect = Rectangle(0, 0, background_art.width, background_art.height)
    dest_rect = Rectangle(0, 0, GetScreenWidth(), GetScreenHeight())
    draw_texture_pro(background_art, source_rect, dest_rect, Vector2(), 0, WHITE)
    monitor = get_current_monitor()
    draw_text("Press 'Esc' to close game", get_monitor_width(monitor) // 2 - 350, int(get_monitor_height(monitor) * 0.05), 50, WHITE)

    # render all sprites except the cursor
    for sprite in Sprite.all_sprites:
        if sprite is not cursor and sprite is not grass:
            sprite.render()

    # render cursor over everything
    cursor.render()

    draw_fps(0, 0)
    end_drawing()
#######################################################################

############################## game loop ##############################
def game_loop():
    # updating
    delta_time = get_frame_time()
    spawner.update(delta_time)
    for sprite in Sprite.all_sprites:
        sprite.update(delta_time)

    # drawing
    begin_drawing()
    clear_background(Color(0, 0, 0, 0))

    source_rect = Rectangle(0, 0, background_art.width, background_art.height)
    dest_rect = Rectangle(0, 0, GetScreenWidth(), GetScreenHeight())
    draw_texture_pro(background_art, source_rect, dest_rect, Vector2(), 0, WHITE)

    monitor = get_current_monitor()
    draw_text("Press 'Esc' to close game", get_monitor_width(monitor) // 2 - 350, int(get_monitor_height(monitor) * 0.05), 50, WHITE)

    # render all sprites except the cursor
    for sprite in Sprite.all_sprites:
        if sprite is not cursor and sprite is not grass:
            sprite.render()

    # render grass over bugs
    grass.render()

    # render cursor over everything
    cursor.render()

    draw_fps(0, 0)
    end_drawing()

    # sync visuals to subprocesses
    file = open("Data\\Shared_Main_Process_Sprite_Data.txt", "w")

    new_file_contents = f"{player.get_current_animation().get_current_texture_path()},{player.transform.pos.x:.2f},{player.transform.pos.y:.2f},{player.transform.rot:.2f},{player.transform.scale:.2f}\n"

    for little_bug in Bug.all_bugs:
        new_file_contents += f"{little_bug.get_current_animation().get_current_texture_path()},{little_bug.transform.pos.x:.2f},{little_bug.transform.pos.y:.2f},{little_bug.transform.rot:.2f},{little_bug.transform.scale:.2f}\n"
    for particle in Particle.all_particles:
        new_file_contents += f"{particle.get_current_animation().get_current_texture_path()},{particle.transform.pos.x:.2f},{particle.transform.pos.y:.2f},{particle.transform.rot:.2f},{particle.transform.scale:.2f}\n"
    file.write(new_file_contents)
    file.close()
#######################################################################

def main():
    set_up_data_files()
    set_up_window()
    
    # set up custom cursor
    cursor_idle_anim = Animation("Assets\\Sprites\\Cursor", (50.0, 50.0, 50.0))
    global cursor ; cursor = Cursor(Transform2D(get_mouse_position(), rot=0, scale=2), [cursor_idle_anim])

    button_transform = Transform2D(pos=Vector2(), rot=0, scale=5)
    
    start_button_idle_anim = Animation("Assets\\Sprites\\Start_Button", (100, 100, 100, 100))
    start_button = Clickable(button_transform, [start_button_idle_anim])

    button_transform.pos = start_button.center_position_at_other(Vector2(get_monitor_width(get_current_monitor()) * 0.5, get_monitor_height(get_current_monitor()) * 0.5))
    start_button.transform.pos = button_transform.pos

    start_button.curr_anim_speed = 0
    start_button.on_mouse_enter = lambda : start_button.play_animation(0)
    start_button.on_mouse_exit = lambda : start_button.stop_animation(0)
    start_button.on_mouse_click = lambda : start_game()

    while not window_should_close():

        if game_started:
            game_loop()
        else:
            start_menu()

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