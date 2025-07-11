from os.path import join
from pyray import *
from raylib import *
from sprite import *

def calc_global_mouse_properties():
    if file_exists(join("Data", "Mouse_Data.txt")):
        file_data = []

        file = open(join("Data", "Mouse_Data.txt"), "r")
        for line in file:
            if ':' in line:
                value = line.split(': ', 1)[1].strip()
                file_data.append(value)
        file.close()
                
        if len(file_data) >= 2:
            Cursor.global_mouse_position = Vector2(float(file_data[0]), float(file_data[1]))
        if len(file_data) >= 3:
            if file_data[2] == "True":
                Cursor.is_global_mouse_clicking = True
            else:
                Cursor.is_global_mouse_clicking = False
        if len(file_data) >= 5:
            
            saved_window_position = Vector2(float(file_data[3]), float(file_data[4]))
            other_window_has_mouse = vector2_distance(get_window_position(), saved_window_position) > 1
            
            if other_window_has_mouse:
                Cursor.global_mouse_position = vector2_subtract(Cursor.global_mouse_position, get_window_position())
                Cursor.global_mouse_position = vector2_add(Cursor.global_mouse_position, saved_window_position)
            
class Cursor(Sprite):
    
    is_global_mouse_clicking:bool = False
    global_mouse_position:Vector2 = Vector2()

    def __init__(self, textures, anim_speed, pos = Vector2(), rot = 0.0, scale = 2.0):
        super().__init__(textures, anim_speed, pos, rot, scale)

    def update(self, dt):
        
        super().update(dt)

        if is_cursor_on_screen():
            file = open(join("Data", "Mouse_Data.txt"), "w")
            file.truncate()
            file.write(f"PosX: {get_mouse_x()}\nPosY: {get_mouse_y()}\nClicking: {is_mouse_button_down(0)}\nWinPosX: {int(get_window_position().x)}\nWinPosY: {int(get_window_position().y)}\n")
            file.close()
        
        calc_global_mouse_properties()
        self.pos = Cursor.global_mouse_position
        
    def render(self):
        super().render()