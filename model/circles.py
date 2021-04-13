"""Program Description

The circle.py program will be initiated once the music is selected,
it will then create a timeline for generating circles into tracks.
"""

import numpy as np
from model.track import Track

def add_circle_per_sec(velocity, sec, frame, track_dict, possibility):
    """A hard-coded function to add circles to tracks."""
    for track in track_dict.values():
        track.update_circles(velocity)
        if frame == 0 and np.random.rand() > possibility:
            track.add_circle()