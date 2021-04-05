import numpy as np

DEFAULT_CIRCLE = -1
MAX_CIRCLE_NUM = 10

class Track:
    def __init__(self, width, height, position):
        self.width = width
        self.height = height
        self.position = position
        self.circles = np.full((MAX_CIRCLE_NUM,), DEFAULT_CIRCLE)
        self.miss = False
        self.miss_count = 0

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
    
    def get_front_circle(self):
        '''
        Get the circle that is the closest to the key.

        Returns:
            The value of the circle has been traveled.
        '''
        # return -1 when there is no circle rather than 0, but it does not matter.
        return np.max(self.circles)

    def set_miss(self):
        '''
        Helper function to set miss and reset miss_count.
        '''
        self.miss = True
        self.miss_count = 0
    
    # need to be refactored since I also need to update other perform
    def update_miss(self, duration_count):
        '''
        '''
        if self.miss:
            self.miss_count += 1
            if self.miss_count > duration_count:
                self.miss = False
                self.miss_count = 0
