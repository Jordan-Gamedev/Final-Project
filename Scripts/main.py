import os
from pyray import *
from raylib import *
import shutil

from animation import Animation
from biome import Biome
from bug import Bug
from bug_spawner import SpawnBugs
from clickable import Clickable
from cursor import Cursor
from particle import Particle
from player import Player
from shop import Shop
from sprite import Sprite
from transform import Transform2D

############################# globals #################################
background_art = None
game_started:bool = False
player = None
grass_texture = None
cursor = None
spawner = None
last_known_points = 0
shop:Shop = None
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
            # points, number of jars, cave biome purchases, mountain biome purchases
            file.write(f"{0}\n{0}\n{0}\n{0}")
    
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

    # set the maximum frame rate to 60 because the optimization sucks 
    set_target_fps(60)
    
    # make it so you can't exit with a key press
    set_exit_key(KEY_NULL)
    
    # load background art into gpu vram
    global background_art ; background_art = load_texture("Assets\\Sprites\\Background\\Main_Background.jpg")
#######################################################################

def start_game():
    global game_started ; game_started = True
    Sprite.all_sprites.clear()
    create_asset_instances()

def quit_game():
    
    # end the process if it is active
    if shop != None:
        shop.close_shop()

    # delete temporary data
    while os.path.exists("Data"):
        shutil.rmtree("Data", ignore_errors=True)

    # update backup savefile
    if file_exists("PersistentData\\Save_Data.txt") and file_exists("PersistentData\\Backup_Save_Data.txt"):
        shutil.copyfile("PersistentData\\Save_Data.txt", "PersistentData\\Backup_Save_Data.txt")

    # close the game
    close_window()

    # close the application
    exit(0)

############################ import assets ############################
def create_asset_instances():
    
    # cave biome button details
    cave_biome_button_paths = ["Assets\\Sprites\\Shop_Buttons\\Cave_Price_Hidden", "Assets\\Sprites\\Shop_Buttons\\Cave_Size_Price_Hidden", "Assets\\Sprites\\Shop_Buttons\\Cave_Price_Revealed", "Assets\\Sprites\\Background\\Cave_Background.jpg"]
    cave_biome_button_pos = Vector2(get_monitor_width(get_current_monitor()) * 0.57, get_monitor_height(get_current_monitor()) * 0.57)
    cave_biome = Biome("Cave", 1500, 250, 1.5, 100, 100, 1000, cave_biome_button_paths[0], cave_biome_button_paths[1], cave_biome_button_paths[2], cave_biome_button_paths[3], cave_biome_button_pos)

    # mountain biome button details
    mountain_biome_button_paths = ["Assets\\Sprites\\Shop_Buttons\\Mountain_Price_Hidden", "Assets\\Sprites\\Shop_Buttons\\Mountain_Size_Price_Hidden", "Assets\\Sprites\\Shop_Buttons\\Mountain_Price_Revealed", "Assets\\Sprites\\Background\\Mountain_Background.jpg"]
    mountain_biome_button_pos = Vector2(get_monitor_width(get_current_monitor()) * 0.7, get_monitor_height(get_current_monitor()) * 0.57)
    mountain_biome = Biome("Mountain", 2000, 250, 1.5, 100, 100, 1000, mountain_biome_button_paths[0], mountain_biome_button_paths[1], mountain_biome_button_paths[2], mountain_biome_button_paths[3], mountain_biome_button_pos)

    # set up shop
    global shop ; shop = Shop(starting_jar_cost=10, purchaseable_biomes=[cave_biome, mountain_biome])

    # set up player
    player_idle_anim = Animation("Assets\\Sprites\\Bat", (100.0, 100.0))
    global player ; player = Player(Transform2D(scale=4.9), [player_idle_anim], speed=1000)
    player.transform.pos = player.center_position_at_other(Cursor.global_mouse_position)
    
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

#######################################################################

def go_to_start_menu():
    # remove previous scene
    Sprite.all_sprites.clear()
    Bug.all_bugs.clear()

    global grass_texture ; grass_texture = load_texture("Assets\\Sprites\\Background\\Grass_1.png")

    if shop != None:
        shop.close_shop()

    # set up custom cursor
    cursor_idle_anim = Animation("Assets\\Sprites\\Cursor", (50.0, 50.0, 50.0))
    global cursor ; cursor = Cursor(Transform2D(get_mouse_position(), rot=0, scale=2), [cursor_idle_anim])

    start_button_hover_anim = Animation("Assets\\Sprites\\Start_Button", (150, 150, 150, 150))
    start_button = Clickable(Transform2D(scale=5), [start_button_hover_anim])

    start_button.transform.pos = start_button.center_position_at_other(Vector2(get_monitor_width(get_current_monitor()) * 0.5, get_monitor_height(get_current_monitor()) * 0.3))
    start_button.curr_anim_speed = 0
    start_button.on_mouse_enter = lambda : start_button.play_animation(0)
    start_button.on_mouse_exit = lambda : start_button.stop_animation(0)
    start_button.on_mouse_click = start_game

    quit_button_hover_anim = Animation("Assets\\Sprites\\Quit_Button", (150, 150, 150, 150))
    quit_button = Clickable(Transform2D(scale=5), [quit_button_hover_anim])
    
    quit_button.transform.pos = quit_button.center_position_at_other(Vector2(get_monitor_width(get_current_monitor()) * 0.5, get_monitor_height(get_current_monitor()) * 0.6))
    quit_button.curr_anim_speed = 0
    quit_button.on_mouse_enter = lambda : quit_button.play_animation(0)
    quit_button.on_mouse_exit = lambda : quit_button.stop_animation(0)
    quit_button.on_mouse_click = quit_game

    settings_button_hover_anim = Animation("Assets\\Sprites\\Settings_Icon", (50, 50, 50, 50), is_loop=False)
    settings_button = Clickable(Transform2D(scale=2.5), [settings_button_hover_anim])
    settings_button_hover_anim.on_finish_event = lambda : settings_button.stop_animation(0)
    settings_button.transform.pos = settings_button.center_position_at_other(Vector2(get_monitor_width(get_current_monitor()) * 0.5 + 300, get_monitor_height(get_current_monitor()) * 0.3))
    settings_button.curr_anim_speed = 0
    settings_button.on_mouse_enter = lambda : settings_button.play_animation(0)
    settings_button.on_mouse_click = go_to_settings_menu

def go_to_settings_menu():

    # remove previous scene
    Sprite.all_sprites.clear()
    Bug.all_bugs.clear()
    if shop != None:
        shop.close_shop()

    # set up custom cursor
    cursor_idle_anim = Animation("Assets\\Sprites\\Cursor", (50.0, 50.0, 50.0))
    global cursor ; cursor = Cursor(Transform2D(get_mouse_position(), rot=0, scale=2), [cursor_idle_anim])

    # clear save button
    clear_save_button_hover_anim = Animation("Assets\\Sprites\\Delete_Button", (150, 150, 150, 150), is_loop=True)
    clear_save_button = Clickable(Transform2D(scale=5), [clear_save_button_hover_anim])
    clear_save_button.transform.pos = clear_save_button.center_position_at_other(Vector2(get_monitor_width(get_current_monitor()) * 0.5, get_monitor_height(get_current_monitor()) * 0.5))
    clear_save_button.curr_anim_speed = 0
    clear_save_button.on_mouse_enter = lambda : clear_save_button.play_animation(0)
    clear_save_button.on_mouse_exit = lambda : clear_save_button.stop_animation(0)
    clear_save_button.on_mouse_click = delete_save

    # back button
    back_button_hover_anim = Animation("Assets\\Sprites\\Back_Button", (150, 150, 150, 150), is_loop=True)
    back_button = Clickable(Transform2D(scale=2.5), [back_button_hover_anim])
    back_button.transform.pos = back_button.center_position_at_other(Vector2(get_monitor_width(get_current_monitor()) * 0.5, get_monitor_height(get_current_monitor()) * 0.7))
    back_button.curr_anim_speed = 0
    back_button.on_mouse_enter = lambda : back_button.play_animation(0)
    back_button.on_mouse_exit = lambda : back_button.stop_animation(0)
    back_button.on_mouse_click = go_to_start_menu
    
def delete_save():
    # delete data files in case the program crashed last time and the corrupted files are still there
    if os.path.exists("PersistentData"):
        shutil.rmtree("PersistentData", ignore_errors=True)
    set_up_data_files()

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
    
    # render all sprites except the cursor
    for sprite in Sprite.all_sprites:
        if sprite is not cursor:
            sprite.render()

    draw_texture_ex(grass_texture, Vector2(0, get_monitor_height(get_current_monitor()) - (27 * 5)), 0, 2.5, WHITE)

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

    # get points from save data
    if file_exists("PersistentData\\Save_Data.txt"):
        with open("PersistentData\\Save_Data.txt", "r") as save_data_file:
            global last_known_points ; last_known_points = int(save_data_file.readline())

    # drawing
    begin_drawing()
    clear_background(Color(0, 0, 0, 0))

    source_rect = Rectangle(0, 0, background_art.width, background_art.height)
    dest_rect = Rectangle(0, 0, GetScreenWidth(), GetScreenHeight())
    draw_texture_pro(background_art, source_rect, dest_rect, Vector2(), 0, WHITE)

    # go back to start menu if the escape key is pressed
    if is_key_pressed(KEY_ESCAPE):
        global game_started ; game_started = False
        go_to_start_menu()

    # render the shop's glass jars
    shop.render()

    # show how many points the player has
    points_render_pos_x = int(get_monitor_width(get_current_monitor()) * 0.58)
    points_render_pos_y = int(get_monitor_height(get_current_monitor()) * 0.38)
    points_text = f"Points: {last_known_points}"
    points_render_pos_x -= measure_text(points_text, 64) // 2
    points_render_pos_y -= 32
    draw_text(points_text, points_render_pos_x, points_render_pos_y, 64, WHITE)

    # render all sprites except the cursor
    for sprite in Sprite.all_sprites:
        if sprite is not cursor:
            sprite.render()

    # render grass over bugs
    draw_texture_ex(grass_texture, Vector2(0, get_monitor_height(get_current_monitor()) - (27 * 5)), 0, 2.5, WHITE)

    # render cursor over everything
    cursor.render()

    draw_fps(0, 0)
    end_drawing()

    # sync visuals to subprocesses

    with open("Data\\Shared_Main_Process_Sprite_Data.txt", "w") as file:

        new_file_contents = f"{player.get_current_animation().get_current_texture_path()},{player.transform.pos.x:.2f},{player.transform.pos.y:.2f},"
        new_file_contents += f"{player.transform.rot:.2f},{player.transform.scale:.2f},1,1\n"

        for little_bug in Bug.all_bugs:
            new_file_contents += f"{little_bug.get_current_animation().get_current_texture_path()},{little_bug.transform.pos.x:.2f},{little_bug.transform.pos.y:.2f},"
            new_file_contents += f"{little_bug.transform.rot:.2f},{little_bug.transform.scale:.2f},{little_bug.facing_direction_x},{little_bug.facing_direction_y}\n"
        for particle in Particle.all_particles:
            new_file_contents += f"{particle.get_current_animation().get_current_texture_path()},{particle.transform.pos.x:.2f},{particle.transform.pos.y:.2f},"
            new_file_contents += f"{particle.transform.rot:.2f},{particle.transform.scale:.2f},1,1\n"
        
        file.write(new_file_contents)
#######################################################################

def main():
    set_up_data_files()
    set_up_window()
    go_to_start_menu()

    while not window_should_close():

        if game_started:
            game_loop()
        else:
            start_menu()

    quit_game()

if __name__ == "__main__":
    main()