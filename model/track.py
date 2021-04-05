import numpy as np

DEFAULT_CIRCLE = -1
MAX_CIRCLE_NUM = 10

class Track:
    def __init__(self, width, height, position):
        self.width = width
        self.height = height
        self.position = position
        self.circles = np.full((MAX_CIRCLE_NUM,), DEFAULT_CIRCLE)

    def update(self, velocity):
        self.circles[self.circles != DEFAULT_CIRCLE] += velocity
    
    def remove_circle(self):
        self.circles[np.argmax(self.circles)] = DEFAULT_CIRCLE

    def add_circle(self):
        self.circles[np.argmin(self.circles)] = 0

    def get_circles(self):
        return [(self.position[0], self.position[1]+height) 
                    for height in self.circles[self.circles != DEFAULT_CIRCLE]]

    def get_key_position(self):
        return (self.position[0], self.position[1] + self.height)