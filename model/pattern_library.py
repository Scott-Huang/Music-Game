"""Program Description

The pattern_library.py program handles the generated patterns and
return the corresponding track index for adding circles.
"""

import random
from random import randint, sample
from model.setting import Keyset
from model.patterns import PATTERNS
from model.utils import report_error

class PatternLibrary():
    DEFAULT_SEQ_NUM = 3

    def __init__(self, pattern_num, mode):
        """Class constructor of PatternLibrary.

        Arguments:
            pattern_num: The number of total patterns (not counting the default).
            key_num: The number of keys in the keyset.
        """

        # get patterns
        patterns = get_pattern(pattern_num, mode)

        # get default pattern
        default_seq = [circles for sublist in patterns[pattern_num:] for circles in sublist]
        default_seq = [PatternLibrary.Sequence(default_seq, shuffle=True)]
        self.sequences = default_seq + [PatternLibrary.Sequence(sequence)
                                        for sequence in patterns[:pattern_num]]
        self.current_pattern = 0

    def get_track_index(self, pattern):
        """Get the track index of circles being added to given the pattern categories."""
        if pattern != self.current_pattern:
            self.sequences[self.current_pattern].reset_index()
            self.current_pattern = pattern
        return self.sequences[self.current_pattern].get_element()
    
    class Sequence():
        """The class Sequence is a subclass of PatternLibrary.
        It handles the sequence of a single pattern categories.
        It is responsible for tracking and updating the position inside the sequence
        and output the element which is the track index.
        """

        def __init__(self, sequence, shuffle=False):
            """Class constructor of Sequence.

            Arguments:
                sequence: The sequence of track indexes in a pattern.
                shuffle: A bool whether to shuffle the sequence.
            """

            self.sequence = sequence
            self.length = len(sequence)
            if self.length <= 0:
                report_error('Empty pattern sequence')
            self.initial = randint(0,self.length-1)
            if shuffle:
                random.shuffle(self.sequence)
            self.reset_index()
        
        def get_element(self):
            """Get the track index and increment the position."""
            element = self.sequence[self.index % self.length]
            self.index += 1
            return element
        
        def reset_index(self):
            """Reset the position."""
            self.index = self.initial

def transfer_filter(circle, accepted_keys: set):
    """A filter that map a sequence of circles into circles in the accepted keyset."""
    return tuple(accepted_keys.intersection(circle))

def transfer_seq_into_keys(sequence, key_set):
    """Filter sequences into keyset format."""
    accepted_keys = set(key_set.values())
    return [transfer_filter(circle, accepted_keys) for circle in sequence]

def get_pattern(pattern_num, mode):
    """Get some patterns of circles generation."""
    # get patterns
    patterns = sample(PATTERNS, pattern_num + PatternLibrary.DEFAULT_SEQ_NUM)
    # adapt patterns to the keyset
    patterns = [transfer_seq_into_keys(pattern, mode) for pattern in patterns]
    return patterns