from pyray import *
import os

class Animation:

    def __init__(self, folder_path:str, frame_durations:tuple, is_loop = True, on_finish_event = None):
        self.texture_paths = []
        self.loaded_textures = []

        for sprite in os.listdir(folder_path):
            asset_path = folder_path + "\\" + sprite
            self.texture_paths.append(asset_path)
            self.loaded_textures.append(load_texture(asset_path))

        self.folder_path = folder_path
        self.frame_durations = frame_durations
        self.is_loop = is_loop
        self.on_finish_event = on_finish_event
        self.curr_frame = 0
        self.curr_frame_time = 0.0

    def update(self, delta):
        
        self.curr_frame_time += delta
        total_frame_duration = self.frame_durations[self.curr_frame] / 1000.0

        if self.curr_frame_time >= total_frame_duration:
            self.curr_frame_time -= total_frame_duration
            self.curr_frame += 1

            if self.curr_frame >= len(self.loaded_textures):
                self.curr_frame = 0
                
                if not self.is_loop:
                    self.curr_frame_time = 0.0
                    self.on_finish_event()
        
    def get_current_texture(self) -> Texture2D:
        return self.loaded_textures[int(self.curr_frame)]
    
    def get_current_texture_path(self):
        return self.texture_paths[int(self.curr_frame)]