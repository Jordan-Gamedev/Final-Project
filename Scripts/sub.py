import win32api
import win32con

from pathlib import Path
from pyray import *
from raylib import *

from bug_spawner import SpawnBugs
from cursor import *
from sprite import *

######################## set window properties ########################

# get currently used monitor
current_monitor = get_current_monitor()

# create a small resizable window
set_config_flags(FLAG_WINDOW_RESIZABLE | FLAG_WINDOW_TOPMOST)
init_window(500, 500, 'Desert Biome')
set_window_min_size(250, 250)
set_window_max_size(500, 500)
hide_cursor()

# set the maximum framerate to 60
set_target_fps(60)

# casts the raylib window into a pointer so that the Python Windows Api can access the window
hwnd = ffi.cast("uintptr_t", get_window_handle())

# retrieves the window style for configuration
style = win32api.GetWindowLong(hwnd, win32con.GWL_STYLE)

# uses the NOT and AND bitwise operators to disable maximize and minimize boxes on the window
style &= ~(win32con.WS_MAXIMIZEBOX | win32con.WS_MINIMIZEBOX)

# applies changes to the window
win32api.SetWindowLong(hwnd, win32con.GWL_STYLE, style)

# create a texture cache for easy texture lookup by path
texture_cache = { }

assets_folder = Path("Assets")
for file in assets_folder.glob("*.png"):
    texture_cache[str(file)] = load_texture(str(file))

# set up cursor
cursor_textures_paths = ["Assets\Cursor_Idle_1.png", "Assets\Cursor_Idle_2.png", "Assets\Cursor_Idle_3.png"]
cursor_textures = [texture_cache[cursor_textures_paths[0]], \
                   texture_cache[cursor_textures_paths[1]], \
                      texture_cache[cursor_textures_paths[2]]]
cursor = Cursor(cursor_textures_paths, cursor_textures, 5.0)

gnat_texture_paths = ["Assets\Gnat_1.png", "Assets\Gnat_2.png"]

# spawner spawns in bugs over time
spawner = SpawnBugs(max_capacity=4, spawn_rate=3, fly_tex_paths=gnat_texture_paths, hopper_tex_paths=gnat_texture_paths, crawler_tex_paths=gnat_texture_paths)

while not window_should_close():

    delta_time = get_frame_time()

    spawner.update(delta_time)

    for sprite in Sprite.all_sprites:
        sprite.update(delta_time)

    begin_drawing()

    for sprite in Sprite.all_sprites:
        sprite.update(delta_time)

    file = open("Data\Shared_Main_Process_Sprite_Data.txt", "r")
    contents = []
    
    while len(contents) == 0:
        contents = [line for line in file]
    
    file.close()

    clear_background(DARKGRAY)

    for line in contents:
        if ',' in line:
            texture_path, pos_x, pos_y, rot, scale = line.split(',')
            if texture_path in texture_cache:
                draw_texture_ex(texture_cache[texture_path], Vector2(float(pos_x) - get_window_position().x, float(pos_y) - get_window_position().y), float(rot), float(scale), WHITE)

    # render local sprites
    render_offset = Vector2(-get_window_position().x, -get_window_position().y)
    for sprite in Sprite.all_sprites:
        if sprite is not cursor:
            sprite.render(render_offset)

    cursor.render()

    draw_fps(0, 0)
    end_drawing()

close_window()