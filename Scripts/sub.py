from os.path import join
from pyray import *
from raylib import *

from cursor import *

######################## set window properties ########################

# get currently used monitor
current_monitor = get_current_monitor()

# create maximized window
set_config_flags(FLAG_WINDOW_ALWAYS_RUN | FLAG_WINDOW_RESIZABLE | FLAG_WINDOW_TOPMOST)
init_window(500, 500, 'Desert Biome')
set_window_min_size(250, 250)
set_window_max_size(500, 500)
hide_cursor()

cursor_texture = [load_texture(join("Assets", "Cursor_Idle_1.png"))]
cursor = Cursor(cursor_texture, 0.0)

# set the maximum frame rate to the maximum refresh rate of the monitor 
set_target_fps(get_monitor_refresh_rate(current_monitor))

while not window_should_close():

    delta_time = get_frame_time()

    cursor.update(delta_time)

    begin_drawing()

    clear_background(DARKGRAY)
    cursor.render()    
    
    end_drawing()

close_window()