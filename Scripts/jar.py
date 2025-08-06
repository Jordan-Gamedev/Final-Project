from pyray import *
from animation import Animation
import save_data_handler
from transform import Transform2D

class Jar:
    def __init__(self, restored_jar_texture:Texture2D, bug_anim:Animation=None, bug_scale:float=1, points=0, cycle:float=5):
        self.transform = Transform2D()
        self.restored_jar_texture = restored_jar_texture
        self.bug_anim = bug_anim
        self.bug_scale = bug_scale
        self.points = points
        self.cycle = cycle
        self.curr_time = cycle
    
    def update(self, dt):
        if not self.bug_anim:
            return
        
        # play bug animation if it is in the container
        self.bug_anim.update(dt)

        if self.curr_time > 0:
            self.curr_time -= dt
        else:
            self.curr_time = self.cycle

            file, file_data = save_data_handler.open_save_file("r+")
            
            # add points
            points = file_data[0]
            points += self.points
            file_data[0] = str(points)
            
            # finalize change
            for data in file_data:
                file.write(f"{data}\n")
            
            save_data_handler.close_save_file(file)
    
    def render(self, pos, num):
        monitor_width = get_monitor_width(get_current_monitor())
        monitor_height = get_monitor_height(get_current_monitor())

        pos = Vector2(monitor_width * 0.42 + (monitor_width * num * 0.07), monitor_height * 0.43)
        
        self.transform.pos = pos
        if self.bug_anim is not None:
            draw_texture_ex(self.bug_anim.get_current_texture(), pos, 0, self.bug_scale, WHITE)
        draw_texture_ex(self.restored_jar_texture, pos, 0, 3, WHITE)