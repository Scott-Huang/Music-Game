import os, sys
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if path not in sys.path:
    sys.path.append(path)
from model.track import Track

def add_update_circle(track: Track, velocity):
    track.add_circle()
    track.update_circles(velocity)

def get_track_dict(num, height=1000):
    tracks = {}
    for track_index in range(1, num+1):
        tracks[track_index] = Track(width=0, height=height,
                                    position=(5*(track_index-1), 0))
    return tracks