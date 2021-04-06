import unittest
import os, sys
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if path not in sys.path:
    sys.path.append(path)
from model.track import Track
from model.model import calc_accuracy, miss_check
from utils import add_update_circle, get_track_dict

class AccuracyTest(unittest.TestCase):
    def test_accuracy(self):
        # test calc_accuracy return correct accuracy
        track = Track(0,1000,(0,0))
        add_update_circle(track, 800)
        accuracy = calc_accuracy(track, 1, 1)
        self.assertEqual(accuracy, 1000-800)

    def test_accuracy_pass_over(self):
        # test calc_accuracy return correct accuracy
        # when the circle passes over the key
        track = Track(0,1000,(0,0))
        add_update_circle(track, 1200)
        accuracy = calc_accuracy(track, 1, 1)
        self.assertEqual(accuracy, 1000-1200)

class MissTest(unittest.TestCase):
    def test_miss(self):
        # test miss is detected
        tracks = get_track_dict(6)
        add_update_circle(tracks[2], 1200)
        miss = miss_check(tracks, 1, 1)
        self.assertTrue(miss)

    def test_remove_miss_circle(self):
        # test miss circle is removed
        tracks = get_track_dict(6)
        add_update_circle(tracks[2], 1200)
        miss_check(tracks, 1, 1)
        circles = tracks[2].get_circles()
        self.assertEqual(len(circles), 0)

    def test_no_miss(self):
        # test detection on no miss
        tracks = get_track_dict(6)
        add_update_circle(tracks[2], 800)
        miss = miss_check(tracks, 1, 1)
        self.assertFalse(miss)
    
    