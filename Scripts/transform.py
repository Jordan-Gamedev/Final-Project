from pyray import Vector2

class Transform2D:
    def __init__(self, pos:Vector2 = Vector2(), rot:float = 0.0, scale:float = 1.0):
        self.pos = pos
        self.rot = rot
        self.scale = scale