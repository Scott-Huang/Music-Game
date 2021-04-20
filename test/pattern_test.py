import unittest
import os, sys
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if path not in sys.path:
    sys.path.append(path)
from model.patterns import generate_patterns, combine_sequence
from model.pattern_library import PatternLibrary

PATTERN_LENGTH = 50
PATTERN_NUM = 5
KEY_NUM = 8

class PatternGenerationTest(unittest.TestCase):
    def test_combine_sequence_simple(self):
        # test whether combine sequence combines successfully on one normal element
        left = [(1,2)]
        right = [(3,)]
        self.assertEqual(combine_sequence(left, right), [(1,2,3)])
    
    def test_combine_sequence_complex(self):
        # test whether combine sequence combines successfully on various elements
        left = [(1,2), (), ()]
        right = [(3,), (1,4), ()]
        self.assertEqual(combine_sequence(left, right), [(1,2,3), (1,4), ()])

    def test_generation(self):
        # test whether pattern can be generated without errors
        TEST_TIME = 100
        for _ in range(TEST_TIME):
            pattern = generate_patterns(PATTERN_LENGTH)
            self.assertEqual(len(pattern), PATTERN_LENGTH)
    
class PatternLibraryTest(unittest.TestCase):
    def setUp(self):
        # set up pattern_library before every 
        self.pattern_library = PatternLibrary(PATTERN_NUM, KEY_NUM)
        self.wanted_sequence = self.pattern_library.sequences[1]

    def test_single_output_pattern(self):
        # test pattern_library to output single pattern
        wanted_index = self.wanted_sequence.sequence[self.wanted_sequence.initial]
        track_index = self.pattern_library.get_track_index(1)
        self.assertEqual(wanted_index,track_index)
    
    def test_multiple_output_pattern(self):
        # test pattern_library to output multiple patterns
        wanted_initial = self.wanted_sequence.initial
        OUTPUT_NUM = min(5, len(self.wanted_sequence.sequence) - wanted_initial)
        wanted_indexes = self.wanted_sequence.sequence[wanted_initial:wanted_initial+OUTPUT_NUM]
        track_indexes = [self.pattern_library.get_track_index(1) for _ in range(OUTPUT_NUM)]
        self.assertEqual(wanted_indexes,track_indexes)
    
    def test_switch_output_pattern(self):
        # test pattern_library to switch among patterns
        self.wanted_sequence = self.pattern_library.sequences[1]
        wanted_index = self.wanted_sequence.sequence[self.wanted_sequence.initial]
        self.pattern_library.get_track_index(1)
        self.pattern_library.get_track_index(2)
        track_index = self.pattern_library.get_track_index(1)
        self.assertEqual(wanted_index,track_index)

if __name__ == '__main__':
    unittest.main()
