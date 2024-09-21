from ursina import *

class Billboard():

    def __init__(self,lane_width,color):
        self._color = color
        self._shape = Entity(
            model='quad',
            color=self._color,
            scale=(4, 4, .5),
            position=(lane_width + 5.5, 1, 2)  # Positioned to the right of the screen
        ) 
    
    def change_color(self,color):
        self._color = color
        self._shape.color = self._color
