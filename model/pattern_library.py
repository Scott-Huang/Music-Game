import random
from random import randint, sample
from model.setting import Keyset
from model.patterns import PATTERNS
from model.utils import report_error

class PatternLibrary():
    DEFAULT_SEQ_NUM = 3

    def __init__(self, pattern_num, key_num):
        patterns = sample(PATTERNS, pattern_num + PatternLibrary.DEFAULT_SEQ_NUM)
        if key_num == 8:
            patterns = [transfer_seq_into_eight_key(pattern) for pattern in patterns]
        elif key_num == 6:
            patterns = [transfer_seq_into_six_key(pattern) for pattern in patterns]
        elif key_num == 4:
            patterns = [transfer_seq_into_four_key(pattern) for pattern in patterns]
        else:
            report_error('Unknown key_num')

        default_seq = [circles for sublist in patterns[pattern_num:] for circles in sublist]
        default_seq = [PatternLibrary.Sequence(default_seq, shuffle=True)]
        self.sequences = default_seq + [PatternLibrary.Sequence(sequence)
                                        for sequence in patterns[:pattern_num]]
        self.current_pattern = 0

    def get_tracks(self, pattern):
        if pattern != self.current_pattern:
            self.sequences[self.current_pattern].reset_index()
            self.current_pattern = pattern
        return self.sequences[self.current_pattern].get_element()
    
    class Sequence():
        def __init__(self, sequence, shuffle=False):
            self.sequence = sequence
            self.length = len(sequence)
            if self.length <= 0:
                report_error('Empty pattern sequence')
            self.initial = randint(0,self.length-1)
            if shuffle:
                random.shuffle(self.sequence)
            self.reset_index()
        
        def get_element(self):
            element = self.sequence[self.index % self.length]
            self.index += 1
            return element
        
        def reset_index(self):
            self.index = self.initial

def transfer_filter(circle, accepted_keys: set):
    return tuple(accepted_keys.intersection(circle))

def transfer_seq_into_eight_key(sequence):
    accepted_keys = set(Keyset.EIGHT_KEYS.values())
    return [transfer_filter(circle, accepted_keys) for circle in sequence]

def transfer_seq_into_six_key(sequence):
    accepted_keys = set(Keyset.SIX_KEYS.values())
    return [transfer_filter(circle, accepted_keys) for circle in sequence]

def transfer_seq_into_four_key(sequence):
    accepted_keys = set(Keyset.FOUR_KEYS.values())
    return [transfer_filter(circle, accepted_keys) for circle in sequence]
