"""Program Description

The track.py program holds a Track class that represent
a track in the game where circles will flow in the track to
the key.
"""

import numpy as np

# default value to represent a null circle
DEFAULT_CIRCLE = -1
# max num of circles that a track can have
MAX_CIRCLE_NUM = 10

class Track:
    """The Track class represent a track in the game.
    It keeps and updates positions of all circles in the track
    and the perform status of on this track.
    """

    def __init__(self, width, height, position):
        """Track constructor.

        Arguments:
            width: The width of the track.
            height: The height of the track.
            position: A tuple which is the position of the track.
        """

        self.width = width
        self.height = height
        self.position = position
        # initiate an array of circles
        self.circles = np.full((MAX_CIRCLE_NUM,), DEFAULT_CIRCLE)
        # miss flag
        self.miss = False
        self.miss_count = 0
        # more flag to be added...

    def update(self, velocity):
        """Update all existing circles
        
        Arguments:
            velocity: The amount to be added to circles.
        """

        self.circles[self.circles != DEFAULT_CIRCLE] += velocity
    
    def remove_circle(self):
        """Remove the circle at the most front."""
        self.circles[np.argmax(self.circles)] = DEFAULT_CIRCLE

    def add_circle(self):
        """Add one circle to the track."""
        self.circles[np.argmin(self.circles)] = 0

    def get_circles(self):
        """Get all exsiting circles in the track.

        Returns:
            An array of the tuples that are positions of the circles.
        """

        return [(self.position[0], self.position[1]+height) 
                    for height in self.circles[self.circles != DEFAULT_CIRCLE]]

    def get_key_position(self):
        """
        Get the position of the key in the track.

        Returns:
            A tuple representing the position of the key.
        """

        return (self.position[0], self.position[1] + self.height)
    
    def get_front_circle(self):
        """
        Get the circle that is the closest to the key.

        Returns:
            The value of the circle has been traveled.
        """

        # will return -1 when there is no circle rather than 0,
        # but it does not matter anyway.
        return np.max(self.circles)

    def set_miss(self):
        """Set miss and reset miss_count."""
        self.miss = True
        self.miss_count = 0
    
    # need to be refactored since I also need to update other perform
    def update_miss(self, duration_count):
        """
        Update miss config. Reset miss if miss_count is over threshhold.

        Arguments:
            duration_count: The threshold to reset.
        """

        if self.miss:
            self.miss_count += 1
            if self.miss_count > duration_count:
                self.miss = False
                self.miss_count = 0
