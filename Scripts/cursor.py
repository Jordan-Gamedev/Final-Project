from pyray import *
from raylib import *
from sprite import Sprite, Transform2D

def calc_global_mouse_properties():
    # open and retrieve the values from the shared mouse data file
    if file_exists("Data\\Mouse_Data.txt"):
        file = open("Data\\Mouse_Data.txt", "r")
        values = file.readline().split(',')
        file_data = [value for value in values]
        file.close()

        if file_data[0] == '':
            return

        # set the global mouse position to the values in the data file
        Cursor.global_mouse_position = Vector2(float(file_data[0]), float(file_data[1]))
        # set the click states of the cursor based on the data files
        if file_data[2] == "True":
            Cursor.is_global_mouse_right_down = True
        else:
            Cursor.is_global_mouse_right_down = False
        if file_data[3] == "True":
            Cursor.is_global_mouse_left_pressed = True
        else:
            Cursor.is_global_mouse_left_pressed = False
        
        # get the window position and check if the mouse is outside the window
        saved_window_position = Vector2(float(file_data[4]), float(file_data[5]))
        other_window_has_mouse = vector2_distance(get_window_position(), saved_window_position) > 1
        
        # update the mouse position based on if the other window has the mouse over it
        if other_window_has_mouse:
            Cursor.global_mouse_position = vector2_subtract(Cursor.global_mouse_position, get_window_position())
            Cursor.global_mouse_position = vector2_add(Cursor.global_mouse_position, saved_window_position)
            
class Cursor(Sprite):
    # have two boolean values that keep track of mouse button clicks
    is_global_mouse_right_down:bool = False
    is_global_mouse_left_pressed:bool = False
    # the current global mouse position
    global_mouse_position:Vector2 = Vector2()

    def __init__(self, transform:Transform2D, animations:list, anim_speed:float = 1.0):
        super().__init__(transform, animations, anim_speed)

    def update(self, dt):
        
        super().update(dt)
        # write the mouse position to the shared data file if the cursor is on screen
        if is_cursor_on_screen():
            file = open("Data\\Mouse_Data.txt", "w")
            file.write(f"{get_mouse_x()},{get_mouse_y()},{is_mouse_button_down(1)},{is_mouse_button_pressed(0)},{int(get_window_position().x)},{int(get_window_position().y)}")
            file.close()
        
        calc_global_mouse_properties()
        self.transform.pos = Cursor.global_mouse_position