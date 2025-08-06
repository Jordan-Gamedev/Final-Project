from pyray import *
import os

class Animation:

    def __init__(self, folder_path:str, frame_duration:int, is_loop = True, on_finish_event = None):
        self.texture_paths = []
        self.loaded_textures = []

        if ".png" in folder_path or ".jpg" in folder_path:
            self.texture_paths.append(folder_path)
            self.loaded_textures.append(load_texture(folder_path))
        else:
            for sprite in os.listdir(folder_path):
                asset_path = folder_path + "\\" + sprite

                if ".png" in asset_path or ".jpg" in asset_path:
                    self.texture_paths.append(asset_path)
                    self.loaded_textures.append(load_texture(asset_path))

        self.folder_path = folder_path
        self.frame_duration = frame_duration
        self.is_loop = is_loop
        self.on_finish_event = on_finish_event
        self.curr_frame = 0
        self.curr_frame_time = 0.0
        self.is_anim_finished = False

    def update(self, delta):
        
        if self.curr_frame < len(self.loaded_textures):

            self.curr_frame_time += delta
            total_frame_duration = self.frame_duration / 1000.0

            if self.curr_frame_time >= total_frame_duration:
                self.curr_frame_time -= total_frame_duration
                self.curr_frame += 1

            if self.curr_frame >= len(self.loaded_textures):
                
                self.curr_frame_time = 0.0

                # if it is looping then this animation can continue to play
                if self.is_loop:
                    self.curr_frame = 0                  
                else:
                    self.curr_frame = len(self.loaded_textures) - 1
                    
                # animation has finished a round, so play finish event
                if self.on_finish_event != None:
                    self.on_finish_event()
        
    def get_current_texture(self) -> Texture2D:
        return self.loaded_textures[int(self.curr_frame)]
    
    def get_current_texture_path(self):
        return self.texture_paths[int(self.curr_frame)]
    
    def center_position_at_other(self, pos, scale):
        texture = self.get_current_texture()
        return Vector2(pos.x - texture.width * 0.5 * scale, pos.y - texture.height * 0.5 * scale)