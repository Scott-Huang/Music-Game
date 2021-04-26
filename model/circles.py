"""Program Description

The circle.py program will be initiated once the music is selected,
it will then create a timeline for generating circles into tracks.
"""

from pygame import mixer
from model.pattern_library import PatternLibrary
from model.music import get_patterned_beats

class CircleHandler():
    """The CircleHandler class is responsible for generating circles."""

    def __init__(self, filename, mode, time_delay=0):
        """Class constructor of CircleHandler.

        Arguments:
            filename: The name of music file.
            mode: The keyset mode.
        """

        self.beats, self.patterns = get_patterned_beats(filename)
        self.pattern_library = PatternLibrary(max(self.patterns), mode)
        self.time_delay = time_delay

    def update_circles(self, velocity, track_dict):
        """Update circles in tracks.

        Arguments:
            velocity: The velocity of circles will be incremented.
            track_dict: A dict with values being tracks.
        """

        self.generate_circles(track_dict)
        for track in track_dict.values():
            CircleHandler.increment_circles(velocity, track)

    @staticmethod
    def increment_circles(velocity, track):
        """Increment circle positions in each track."""
        track.update_circles(velocity)

    def generate_circles(self, track_dict):
        """Generate circles to tracks if beats occur."""
        if self.beats and mixer.music.get_pos() + self.time_delay * 1000 > self.beats[0]:
            self.beats.pop(0)
            self.pattern = self.patterns.pop(0)
            for track_index in self.pattern_library.get_track_index(self.pattern):
                track_dict[track_index].add_circle()
