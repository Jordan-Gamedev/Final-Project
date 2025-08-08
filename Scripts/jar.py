from pyray import *
import save_data_handler
from transform import Transform2D

class Jar:
    def __init__(self, restored_jar_texture:Texture2D, cycle:float=5):
        self.transform = Transform2D()
        self.restored_jar_texture = restored_jar_texture
        self.cycle = cycle
        self.curr_time = cycle
        self.bug_anim = None
        self.points = 0
        self.bug_scale = 1
    
    def update(self, dt):
        # check if the jar is empty
        if not self.bug_anim:
            return
        
        # play bug animation if it is in the container
        self.bug_anim.update(dt)

        # update the cyclical timer
        if self.curr_time > 0:
            self.curr_time -= dt
        else:
            self.curr_time = self.cycle

            file, file_data = save_data_handler.open_save_file("r+")
            
            # add points
            points = int(file_data[0])
            points += self.points
            file_data[0] = str(points)
            
            # finalize change
            for data in file_data:
                file.write(f"{data}\n")
            
            save_data_handler.close_save_file(file)
    
    def render(self, pos, num):
        # get the height and width of the current screen
        screen_width = get_screen_width()
        screen_height = get_screen_height()
       
        # set the positions of the jars based on the which jar number is being rendered
        pos = Vector2(screen_width * 0.42 + (screen_width * num * 0.07), pos.y)
        self.transform.pos = pos
        # check to see if the jar is filled
        if self.bug_anim is not None:
            # set the bug position based on the jar's position
            bug_pos = Vector2(pos.x + self.restored_jar_texture.width * 1.5, pos.y + self.restored_jar_texture.height * 1.5)
            bug_pos = self.bug_anim.center_position_at_other(bug_pos, self.bug_scale)
            draw_texture_ex(self.bug_anim.get_current_texture(), bug_pos, 0, self.bug_scale, WHITE)
        # draw the jar over the bug
        draw_texture_ex(self.restored_jar_texture, pos, 0, 3, WHITE)