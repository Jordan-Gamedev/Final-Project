import win32api
import win32con

from pathlib import Path
from pyray import *
from raylib import *

from animation import *
from bug_spawner import SpawnBugs
from cursor import *
from sprite import *

######################## set window properties ########################

# get currently used monitor
current_monitor = get_current_monitor()

# create a small resizable window
set_config_flags(FLAG_WINDOW_RESIZABLE | FLAG_WINDOW_TOPMOST)
init_window(500, 500, 'Mountain Biome')
set_window_min_size(250, 250)
set_window_max_size(500, 500)
hide_cursor()

# make it so that the only way to close the biome is with the window exit button
set_exit_key(KEY_NULL)

# set the maximum framerate to 60
set_target_fps(60)

# casts the raylib window into a pointer so that the Python Windows Api can access the window
hwnd = ffi.cast("uintptr_t", get_window_handle())

# retrieves the window style for configuration
style = win32api.GetWindowLong(hwnd, win32con.GWL_STYLE)

# uses bitwise operators to disable maximize and minimize boxes on the window
style &= ~(win32con.WS_MAXIMIZEBOX | win32con.WS_MINIMIZEBOX)

# applies changes to the window
win32api.SetWindowLong(hwnd, win32con.GWL_STYLE, style)

# create a texture cache for easy texture lookup by path
texture_cache = { }

assets_folder = Path("Assets")
for file in assets_folder.rglob("**\\*.png"):
    texture_cache[str(file)] = load_texture(str(file))

# set up custom cursor
cursor_idle_anim = Animation("Assets\\Sprites\\Cursor", (50.0, 50.0, 50.0))
cursor = Cursor(Transform2D(get_mouse_position(), rot=0, scale=2), [cursor_idle_anim])

# set up spawner which spawns bugs over time
gnat_idle_anim = Animation("Assets\\Sprites\\Gnat", (300.0, 300.0))
hoverer_idle_anim = Animation("Assets\\Sprites\\Hoverer", (50, 50))
hopper_idle_anim = Animation("Assets\\Sprites\\Hopper\\Idle", (50, 50, 50, 50, 50, 50))
hopper_jump_anim = Animation("Assets\\Sprites\\Hopper\\Jump", (50, 50, 50, 50, 50, 50), is_loop=False)
crawler_idle_anim = Animation("Assets\\Sprites\\Crawler\\Idle", (50, 50, 50, 50, 50, 50, 50, 50))
crawler_walk_anim = Animation("Assets\\Sprites\\Crawler\\Walk", (50, 50, 50, 50, 50, 50))
crawler_fall_anim = Animation("Assets\\Sprites\\Crawler\\Fall", (25, 25, 25, 25, 25, 25))
spawner = SpawnBugs(max_capacity=12, spawn_rate=1, fly_anims=[gnat_idle_anim], hover_anims=[hoverer_idle_anim], \
                hopper_anims=[hopper_idle_anim, hopper_jump_anim], crawler_anims=[crawler_idle_anim, crawler_walk_anim, crawler_fall_anim])

background_art = load_texture("Assets\\Sprites\\Background\\Mountain_Background.jpg")

while not window_should_close():

    delta_time = get_frame_time()

    spawner.update(delta_time)

    # update local sprites
    for sprite in Sprite.all_sprites:
        sprite.update(delta_time)

    begin_drawing()

    file = open("Data\\Shared_Main_Process_Sprite_Data.txt", "r")
    contents = []
    
    while len(contents) == 0:
        contents = [line for line in file]
    
    file.close()

    clear_background(WHITE)

    source_rect = Rectangle(0, 0, background_art.width, background_art.height)
    dest_rect = Rectangle(0, 0, GetMonitorWidth(get_current_monitor()), GetMonitorHeight(get_current_monitor()))
    
    draw_texture_pro(background_art, source_rect, dest_rect, Vector2(get_window_position().x, get_window_position().y), 0, WHITE)
    
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