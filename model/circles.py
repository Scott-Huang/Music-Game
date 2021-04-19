"""Program Description

The circle.py program will be initiated once the music is selected,
it will then create a timeline for generating circles into tracks.
"""

from pygame import mixer

def update_circles(velocity, track_dict, beats, patterns, pattern_library, time_delay=0):
    generate_circles(track_dict, beats, patterns, pattern_library, time_delay)
    for track in track_dict.values():
        increment_circles(velocity, track)

def increment_circles(velocity, track):
    track.update_circles(velocity)

def generate_circles(track_dict, beats, patterns, pattern_library, time_delay):
    if beats and mixer.music.get_pos() + time_delay * 1000 > beats[0]:
        beats.pop(0)
        pattern = patterns.pop(0)
        for track_index in pattern_library.get_tracks(pattern):
            track_dict[track_index].add_circle()
