import numpy as np
import model.patterns
from model.track import Track

def add_circle_per_sec(velocity, sec, frame, track_dict, possibility):
    """A hard-coded function to add circles to tracks.
    """
    for track in track_dict.values():
        track.update_circles(velocity)
        if frame == 0 and np.random.rand() > possibility:
            track.add_circle()