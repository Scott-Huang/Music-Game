import unittest
import os, sys
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if path not in sys.path:
    sys.path.append(path)
from model.track import Track
from utils import add_update_circle

class TrackTest(unittest.TestCase):
    def test_track_circles(self):
        # test track handles correct amount of circles
        track = Track(0,1000,(0,0))
        add_update_circle(track, 20)
        add_update_circle(track, 50)
        self.assertEqual(len(track.get_circles()), 2)
    
    def test_track_circles_position(self):
        # test track has circles at correct position
        track = Track(0,1000,(0,0))
        add_update_circle(track, 20)
        add_update_circle(track, 50)
        self.assertTrue((0,20+50) in track.get_circles())
        self.assertTrue((0,50) in track.get_circles())

    def test_track_remove_circle(self):
        # test track remove circles correctly
        track = Track(0,1000,(0,0))
        add_update_circle(track, 50)
        add_update_circle(track, 30)
        track.remove_circle()
        self.assertEqual(len(track.get_circles()), 1)
        self.assertTrue((0,30) in track.get_circles())
    
    def test_update_miss_simple(self):
        # test track can set and update miss state
        track = Track(0,1000,(0,0))
        track.set_miss()
        track.update_miss(1)
        self.assertTrue(track.miss)
        track.update_miss(1)
        self.assertFalse(track.miss)
    
    def test_update_miss_hard(self):
        # test track can handle complex set/update miss command
        track = Track(0,1000,(0,0))
        track.set_miss()
        track.update_miss(1)
        self.assertTrue(track.miss)
        track.set_miss()
        track.update_miss(1)
        self.assertTrue(track.miss)
        track.update_miss(1)
        self.assertFalse(track.miss)

if __name__ == '__main__':
    unittest.main()