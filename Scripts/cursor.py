from pyray import *
from raylib import *
from sprite import *

def calc_global_mouse_properties():
    if file_exists("Data\\Mouse_Data.txt"):
        file = open("Data\\Mouse_Data.txt", "r")
        values = file.readline().split(',')
        file_data = [value for value in values]
        file.close()

        if file_data[0] == '':
            return

        Cursor.global_mouse_position = Vector2(float(file_data[0]), float(file_data[1]))
        if file_data[2] == "True":
            Cursor.is_global_mouse_right_down = True
        else:
            Cursor.is_global_mouse_right_down = False
        if file_data[3] == "True":
            Cursor.is_global_mouse_left_pressed = True
        else:
            Cursor.is_global_mouse_left_pressed = False
            
        saved_window_position = Vector2(float(file_data[4]), float(file_data[5]))
        other_window_has_mouse = vector2_distance(get_window_position(), saved_window_position) > 1
        
        if other_window_has_mouse:
            Cursor.global_mouse_position = vector2_subtract(Cursor.global_mouse_position, get_window_position())
            Cursor.global_mouse_position = vector2_add(Cursor.global_mouse_position, saved_window_position)
            #print(f"{int(Cursor.global_mouse_position.x)},{int(Cursor.global_mouse_position.y)}")
            
class Cursor(Sprite):
    
    is_global_mouse_right_down:bool = False
    is_global_mouse_left_pressed:bool = False

    global_mouse_position:Vector2 = Vector2()

    def __init__(self, transform:Transform2D, animations:list, anim_speed:float = 1.0):
        super().__init__(transform, animations, anim_speed)

    def update(self, dt):
        
        super().update(dt)

        if is_cursor_on_screen():
            file = open("Data\\Mouse_Data.txt", "w")
            file.write(f"{get_mouse_x()},{get_mouse_y()},{is_mouse_button_down(1)},{is_mouse_button_pressed(0)},{int(get_window_position().x)},{int(get_window_position().y)}")
            file.close()
        
        calc_global_mouse_properties()
        self.transform.pos = Cursor.global_mouse_position