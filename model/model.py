from model.track import Track
from render import render_text

MISS = -0.4
PERFECT = 0.1
GOOD = 0.25
BAD = 0.4
PERFORM_DURATION = 4

def miss_check(track_dict, frame, velocity, screen):
    miss = False
    for track in track_dict.values():
        if calc_accuracy(track, frame, velocity) < MISS:
            miss = True
            track.set_miss()
            track.remove_circle()
        track.update_miss(PERFORM_DURATION * frame)
        if track.miss:
            position = track.get_key_position()
            render_text('miss', position, screen, style='perform')
    return miss

def press_check(track_dict, mode, frame, velocity, screen):
    pass

def calc_accuracy(track: Track, frame, velocity):
    displacement = track.height - track.get_front_circle()
    return displacement / velocity / frame