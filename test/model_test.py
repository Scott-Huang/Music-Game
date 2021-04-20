import unittest
import os, sys
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if path not in sys.path:
    sys.path.append(path)
from model.track import Track
from model.score_circles import (calculate_accuracy, score_miss,
    MISS, MISS_SCORE)
from utils import add_update_circle, get_track_dict

FRAME_RATE = 10
VELOCITY = 1
TRACK_NUM = 6

def create_and_update_tracks(update_velocity):
    tracks = get_track_dict(TRACK_NUM)
    update = tracks[1].height + int(update_velocity * FRAME_RATE)
    add_update_circle(tracks[1], update)
    return tracks

class AccuracyTest(unittest.TestCase):
    def test_accuracy(self):
        # test calc_accuracy return correct accuracy
        HEIGHT = 1000
        UPDATE = 800
        track = Track(0,HEIGHT,(0,0))
        add_update_circle(track, UPDATE)
        accuracy = calculate_accuracy(track, FRAME_RATE, VELOCITY)
        self.assertEqual(accuracy, (HEIGHT-UPDATE) / FRAME_RATE / VELOCITY)

    def test_accuracy_pass_over(self):
        # test calc_accuracy return correct accuracy
        # when the circle passes over the key
        HEIGHT = 1000
        UPDATE = 1200
        track = Track(0,HEIGHT,(0,0))
        add_update_circle(track, UPDATE)
        accuracy = calculate_accuracy(track, FRAME_RATE, VELOCITY)
        self.assertEqual(accuracy, (HEIGHT-UPDATE) / FRAME_RATE / VELOCITY)

class PerformanceMissTest(unittest.TestCase):
    def test_miss(self):
        # test miss is detected
        tracks = create_and_update_tracks(1 - MISS)
        score = score_miss(tracks, FRAME_RATE, VELOCITY)
        self.assertEqual(score, MISS_SCORE)

    def test_remove_miss_circle(self):
        # test miss circle is removed
        tracks = create_and_update_tracks(1 - MISS)
        score_miss(tracks, FRAME_RATE, VELOCITY)
        circles = tracks[1].get_circles()
        self.assertEqual(len(circles), 0)

    def test_no_miss(self):
        # test detection on no miss
        tracks = create_and_update_tracks(0)
        score = score_miss(tracks, FRAME_RATE, VELOCITY)
        self.assertEqual(score, 0)    

if __name__ == '__main__':
    unittest.main()
