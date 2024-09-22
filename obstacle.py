from ursina import *

class Obstacle():
   
    def __init__(self,x,y,z,color):
        self._x, self._y, self._z = x,y,z
        self._color = color
        self._shape = Entity(
            model='cube',
            color=self._color,
            scale=(2, 1, 1),  # Slightly more than lane width to ensure coverage
            position=(self._x, self._y, self._z),  # Adjusted Y position to match player level
            collider='box'
        )
    
    def move(self,distance):
        self._z+=distance
        self._shape.z = self._z

    def get_z(self):
        return self._z

    def get_shape(self):
        return self._shape

    def get_color(self):
        return self._shape.color
      
