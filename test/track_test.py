import unittest
import os, sys
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if path not in sys.path:
    sys.path.append(path)
from model.track import Track, MISS, BAD, GOOD, PERFECT
from utils import add_update_circle

def create_track():
    HEIGHT = 1000
    return Track(0,HEIGHT,(0,0))

class TrackTest(unittest.TestCase):
    def test_track_circles(self):
        # test track handles correct amount of circles
        FIRST_UPDATE = 20
        SECOND_UPDATE = 50
        track = create_track()
        add_update_circle(track, FIRST_UPDATE)
        add_update_circle(track, SECOND_UPDATE)
        self.assertEqual(len(track.get_circles()), 2)
    
    def test_track_circles_position(self):
        # test track has circles at correct position
        FIRST_UPDATE = 20
        SECOND_UPDATE = 50
        track = create_track()
        add_update_circle(track, FIRST_UPDATE)
        add_update_circle(track, SECOND_UPDATE)
        self.assertEqual([(0,FIRST_UPDATE+SECOND_UPDATE), (0,SECOND_UPDATE)],
                          track.get_circles())

    def test_track_remove_circle(self):
        # test track remove circles correctly
        FIRST_UPDATE = 20
        SECOND_UPDATE = 50
        track = create_track()
        add_update_circle(track, FIRST_UPDATE)
        add_update_circle(track, SECOND_UPDATE)
        track.remove_circle()
        self.assertEqual(track.get_circles(), [(0,SECOND_UPDATE)])
    
    def test_update_miss_simple(self):
        # test track can set and update miss state
        track = create_track()
        track.set_miss()
        track.update_perform(1)
        self.assertEqual(track.perform, MISS)
        track.update_perform(1)
        self.assertNotEqual(track.perform, MISS)
    
    def test_update_miss_hard(self):
        # test track can handle complex set/update miss command
        track = create_track()
        track.set_miss()
        track.update_perform(1)
        self.assertEqual(track.perform, MISS)
        track.set_miss()
        track.update_perform(1)
        self.assertEqual(track.perform, MISS)
        track.update_perform(1)
        self.assertNotEqual(track.perform, MISS)
    
    def test_update_bad(self):
        # test track can set and update bad state
        track = create_track()
        track.set_bad()
        track.update_perform(1)
        self.assertEqual(track.perform, BAD)
        track.update_perform(1)
        self.assertNotEqual(track.perform, BAD)
    
    def test_update_good(self):
        # test track can set and update good state
        track = create_track()
        track.set_good()
        track.update_perform(1)
        self.assertEqual(track.perform, GOOD)
        track.update_perform(1)
        self.assertNotEqual(track.perform, GOOD)
    
    def test_update_perfect(self):
        # test track can set and update perfect state
        track = create_track()
        track.set_perfect()
        track.update_perform(1)
        self.assertEqual(track.perform, PERFECT)
        track.update_perform(1)
        self.assertNotEqual(track.perform, PERFECT)
    
    def test_update_mixture(self):
        # test track can handle mixed perform flags
        track = create_track()
        track.set_perfect()
        track.update_perform(1)
        self.assertEqual(track.perform, PERFECT)
        track.set_good()
        track.update_perform(1)
        self.assertEqual(track.perform, GOOD)
        track.update_perform(1)
        self.assertNotEqual(track.perform, GOOD)
        track.set_bad()
        track.update_perform(1)
        self.assertEqual(track.perform, BAD)

if __name__ == '__main__':
    unittest.main()