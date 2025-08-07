from pathlib import Path
from pyray import *
from raylib import *
import sys
import win32api
import win32con

from animation import *
from bug_spawner import SpawnBugs
from cursor import *
import save_data_handler
from sprite import *

set_trace_log_level(LOG_ERROR | LOG_FATAL)

# get the biome stats
BIOME_NAME = sys.argv[1]
BIOME_START_SIZE = int(sys.argv[2])
BIOME_SIZE_INCREMENT = int(sys.argv[3])
BIOME_MAX_SIZE = int(sys.argv[4])

# get the current max window size
file_data = save_data_handler.get_save_contents()
times_purchased = int(file_data[2]) if BIOME_NAME == "Cave" else int(file_data[3])
curr_max_window_size = min(BIOME_START_SIZE + (BIOME_SIZE_INCREMENT * (times_purchased - 1)), BIOME_MAX_SIZE)

# create a small resizable window
set_config_flags(FLAG_WINDOW_RESIZABLE | FLAG_WINDOW_TOPMOST)
init_window(max(BIOME_START_SIZE, curr_max_window_size // 2), max(BIOME_START_SIZE, curr_max_window_size // 2), BIOME_NAME)
set_window_min_size(BIOME_START_SIZE, BIOME_START_SIZE)
set_window_max_size(curr_max_window_size, curr_max_window_size)
hide_cursor()

MONITOR_WIDTH = get_monitor_width(get_current_monitor())
MONITOR_HEIGHT = get_monitor_height(get_current_monitor())

init_audio_device()

# set the starting biome position based on biome type
if BIOME_NAME == "Cave":
    set_window_position(int(MONITOR_WIDTH * 0.25), int(MONITOR_HEIGHT) // 2)
else:
    set_window_position(int(MONITOR_WIDTH * 0.75), int(MONITOR_HEIGHT) // 2)

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
cursor_idle_anim = Animation("Assets\\Sprites\\Cursor", 50)
cursor = Cursor(Transform2D(get_mouse_position(), rot=0, scale=2), [cursor_idle_anim])

# set up spawner which spawns bugs over time
fly_anims = []
hover_anims = []
hopper_anims = []
crawler_anims = []

if BIOME_NAME == "Cave":

    hover_anims.append(Animation("Assets\\Sprites\\Cave_Hover_Bug", 50))
    hopper_anims.append(Animation("Assets\\Sprites\\Cave_Hopper\\Idle", 50))
    hopper_anims.append(Animation("Assets\\Sprites\\Cave_Hopper\\Jump", 50, is_loop=False))
    crawler_anims.append(Animation("Assets\\Sprites\\Cave_Crawler\\Idle", 50))
    crawler_anims.append(Animation("Assets\\Sprites\\Cave_Crawler\\Walk", 50))
    crawler_anims.append(Animation("Assets\\Sprites\\Cave_Crawler\\Fall", 25))

    fly_pnts = 0
    hover_pnts = 25
    hopper_pnts = 35
    crawler_pnts = 5
    blood_color = RED

else:
    
    fly_anims.append(Animation("Assets\\Sprites\\Mountain_Flyer_Bug", 300))
    hover_anims.append(Animation("Assets\\Sprites\\Mountain_Hover_Bug", 50))

    fly_pnts = 40
    hover_pnts = 30
    hopper_pnts = 0
    crawler_pnts = 0
    blood_color = BLUE

spawner = SpawnBugs(max_capacity=10, spawn_rate=2, fly_anims=fly_anims, hover_anims=hover_anims, hopper_anims=hopper_anims, \
        crawler_anims=crawler_anims, fly_pnts=fly_pnts, hover_pnts=hover_pnts, hop_pnts=hopper_pnts, crawl_pnts=crawler_pnts, blood_color=blood_color)

# get the correct background for the biome
if BIOME_NAME == "Cave":
    background_art = load_texture("Assets\\Sprites\\Background\\Cave_Background.jpg")
else:
    background_art = load_texture("Assets\\Sprites\\Background\\Mountain_Background.jpg")

while not window_should_close():

    delta_time = get_frame_time()

    # update spawner
    spawner.update(delta_time)

    # update local sprites
    for sprite in Sprite.all_sprites:
        sprite.update(delta_time)

    # updates the min and max of the window
    file_data = save_data_handler.get_save_contents()
    times_purchased = int(file_data[2]) if BIOME_NAME == "Cave" else int(file_data[3])
    window_size = min(BIOME_START_SIZE + (BIOME_SIZE_INCREMENT * (times_purchased - 1)), BIOME_MAX_SIZE)
    set_window_min_size(BIOME_START_SIZE, BIOME_START_SIZE)
    set_window_max_size(window_size, window_size)
    
    # wait for the main process to send its sprite data
    contents = []
    with open("Data\\Shared_Main_Process_Sprite_Data.txt") as file:
        while len(contents) == 0:
            contents = [line for line in file]

    begin_drawing()

    # draw the background
    clear_background(WHITE)
    source_rect = Rectangle(0, 0, background_art.width, background_art.height)
    dest_rect = Rectangle(0, 0, MONITOR_WIDTH, MONITOR_HEIGHT)
    draw_texture_pro(background_art, source_rect, dest_rect, Vector2(get_window_position().x, get_window_position().y), 0, WHITE)
    
    # draw main process's sprites if they are in this window's area
    try:
        for line in contents:
            if ',' in line:
                texture_path, pos_x, pos_y, rot, scale, dir_x, dir_y = line.split(',')
                if texture_path in texture_cache:

                    dir_x = int(dir_x)
                    dir_y = int(dir_y)
                    if dir_x == -1 or dir_y == -1:

                        image = load_image(texture_path)
                        if dir_x == -1:
                            image_flip_horizontal(image)
                        if dir_y == -1:
                            image_flip_vertical(image)
                        
                        tex = load_texture_from_image(image)
                        draw_texture_ex(tex, Vector2(float(pos_x) - get_window_position().x, float(pos_y) - get_window_position().y), float(rot), float(scale), WHITE)
                        unload_image(image)
                    else:
                        draw_texture_ex(texture_cache[texture_path], Vector2(float(pos_x) - get_window_position().x, float(pos_y) - get_window_position().y), float(rot), float(scale), WHITE)
    except:
        pass
    
    # render local sprites
    render_offset = Vector2(-get_window_position().x, -get_window_position().y)
    for sprite in Sprite.all_sprites:
        if sprite is not cursor:
            sprite.render(render_offset)

    # render cursor
    cursor.render()

    end_drawing()

close_window()
close_audio_device()