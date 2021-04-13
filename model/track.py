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
# perform flags
MISS = 'MISS'
BAD = 'BAD'
GOOD = 'GOOD'
PERFECT = 'PERFECT'

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
        self.key_position = (self.position[0], self.position[1] + self.height)
        # initiate an array of circles
        self.circles = np.full((MAX_CIRCLE_NUM,), DEFAULT_CIRCLE)
        # perform flags
        self.perform = None
        self.count = 0

    def update_circles(self, velocity):
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
        """Set miss and reset count."""
        self.perform = MISS
        self.count = 0
    
    def set_bad(self):
        """Set bad and reset count."""
        self.perform = BAD
        self.count = 0
    
    def set_good(self):
        """Set good and reset count."""
        self.perform = GOOD
        self.count = 0
    
    def set_perfect(self):
        """Set perfect and reset count."""
        self.perform = PERFECT
        self.count = 0
    
    def update_perform(self, duration_count):
        """
        Update perform config. Reset perform if count is over threshhold.

        Arguments:
            duration_count: The threshold to reset.
        """
        if self.perform:
            self.count += 1
            if self.count > duration_count:
                self.perform = None
                self.count = 0
