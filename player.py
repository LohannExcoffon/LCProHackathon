from ursina import *

class Player:

    def __init__(self,x,y,z,size):
        self._x, self._y, self._z = x,y,z
        self._scale = size
        self._shape = Entity(
            model='cube',
            color=color.azure,
            scale=self._scale,
            position=(self._x, self._y, self._z), # 0 0.5 -5
            collider='box'
        )
    
    def get_x(self):
        return self._x

    def get_z(self):
        return self._z

    def move(self,distance,lane_width):
        self._x+=distance
        self._x = max(-lane_width, min(lane_width, self._x))
        self._shape.x = self._x
    
    def get_shape(self):
        return self._shape
