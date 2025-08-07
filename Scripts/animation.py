from pyray import *
import os

class Animation:

    def __init__(self, folder_path:str, frame_duration:int, is_loop = True, on_finish_event = None):
        self.texture_paths = []
        self.loaded_textures = []

        # if a png or jpg is passed in, the animation is just that one texture
        if ".png" in folder_path or ".jpg" in folder_path:
            self.texture_paths.append(folder_path)
            self.loaded_textures.append(load_texture(folder_path))
        # a directory was passed, so add each texture in that directory
        else:
            for sprite in os.listdir(folder_path):
                asset_path = folder_path + "\\" + sprite
                
                # the path is an image, so add the texture to the animation
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

    # updates the animation every frame
    def update(self, delta):
        
        # go through the animation frames
        if self.curr_frame < len(self.loaded_textures):

            # update the frame time
            self.curr_frame_time += delta
            total_frame_duration = self.frame_duration / 1000.0

            # go to the next animation frame once the frame has finished playing
            if self.curr_frame_time >= total_frame_duration:
                self.curr_frame_time -= total_frame_duration
                self.curr_frame += 1

            # reached the end of the animation
            if self.curr_frame >= len(self.loaded_textures):
                
                self.curr_frame_time = 0.0

                # if it is looping then this animation can continue to play
                if self.is_loop:
                    self.curr_frame = 0
                # stop the animation at the last frame
                else:
                    self.curr_frame = len(self.loaded_textures) - 1
                    
                # animation has finished a round, so play finish event
                if self.on_finish_event != None:
                    self.on_finish_event()
    
    # get the texture from the current animation frame
    def get_current_texture(self) -> Texture2D:
        return self.loaded_textures[int(self.curr_frame)]
    
    # get the texture path from the current animation frame
    def get_current_texture_path(self):
        return self.texture_paths[int(self.curr_frame)]
    
    # find the position needed to center this texture at the specified position
    def center_position_at_other(self, pos_to_center_at, scale):
        texture = self.get_current_texture()
        return Vector2(pos_to_center_at.x - texture.width * 0.5 * scale, pos_to_center_at.y - texture.height * 0.5 * scale)