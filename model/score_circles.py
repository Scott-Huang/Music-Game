"""Program Description

The model.py program is the model of the game.
It handles and updates the state of tracks
for missing circles and key pressing.
"""

from model.track import Track
from model.utils import report_error

# some constants on rating accuracies in sec
MISS = -0.25
PERFECT = 0.08
GOOD = 0.15
BAD = 0.25
MISS_SCORE = -20
PERFECT_SCORE = 8
GOOD_SCORE = 3
BAD_SCORE = -5
# duration of displaying performance in sec
PERFORM_DURATION = 0.3

def score_miss(track_dict, frame, velocity):
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

    score = 0
    # loop through all tracks
    for track in track_dict.values():
        # update perform flag of the track
        track.update_perform(PERFORM_DURATION * frame)

        # find any missed circle
        if calculate_accuracy(track, frame, velocity) < MISS:
            score += MISS_SCORE
            track.set_miss()
            # remove missed circle
            track.remove_circle()
    return score

def score_press(event, track_dict, mode, frame, velocity):
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

    # get the pressed key
    index = mode.get(event.key, 0)
    # return 0 for invalid key pressing
    if index == 0:
        return 0
    # get corresponding track
    track = track_dict[index]
    # calculate accuracy
    accuracy = abs(calculate_accuracy(track, frame, velocity))
    # set score and perform
    score = 0
    if accuracy < PERFECT:
        track.set_perfect()
        score = PERFECT_SCORE
    elif accuracy < GOOD:
        track.set_good()
        score = GOOD_SCORE
    elif accuracy < BAD:
        track.set_bad()
        score = BAD_SCORE
    # remove circle if valid
    if score != 0:
        track.remove_circle()
    return score

def calculate_accuracy(track: Track, frame, velocity):
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