"""Program Description

The model.py program is the model of the game.
It handles and updates the state of tracks
for missing circles and key pressing.
"""

from model.track import Track
from model.utils import report_error
from render import render_text

# some constants on rating accuracies in sec
MISS = -0.4
PERFECT = 0.1
GOOD = 0.25
BAD = 0.4
# duration of displaying performance in sec
PERFORM_DURATION = 0.4

def miss_check(track_dict, frame, velocity):
    """Iterate through all tracks and check any missed circles.

    Arguments:
        track_dict: A dict with values being tracks.
        frame: The frame rate.
        velocity: The velocity.
    Returns:
        A boolean whether there is a miss
    """

    # check arguments
    if frame <= 0 or velocity <= 0:
        report_error('Invalid frame rate or velocity')

    miss = False
    # loop through all tracks
    for track in track_dict.values():
        if calc_accuracy(track, frame, velocity) < MISS:
            miss = True
            track.set_miss()
            # remove missed circle
            track.remove_circle()    
    return miss

def press_check(event, track_dict, mode, frame, velocity):
    """Iterate through all tracks and check any missed circles.

    Arguments:
        event: The key_down event.
        track_dict: A dict with values being tracks.
        mode: The key set of the game.
        frame: The frame rate.
        velocity: The velocity.
    Returns:
        A boolean whether there is a valid click
    """

    # check arguments
    if frame <= 0 or velocity <= 0:
        report_error('Invalid frame rate or velocity')
    # TODO
    return False

def display_performance(track_dict, frame, screen):
    """Display performances of tracks.

    Arguments:
        track_dict: A dict with values being tracks.
        frame: The frame rate.
        screen: The game screen that the performance will be rendered on.
    """

    for track in track_dict.values():
        track.update_miss(PERFORM_DURATION * frame)
        if track.miss:
            position = track.get_key_position()
            render_text('miss', position, screen, style='perform')

def calc_accuracy(track: Track, frame, velocity):
    """Calculate the accuracy of the most front circle.

    Arguments:
        track: The track containing circles and a key.
        frame: The frame rate.
        velocity: The velocity of circles falling.
    Returns:
        The time needed for the frontest circle to flow to the key in sec.
    """

    displacement = track.height - track.get_front_circle()
    return displacement / velocity / frame