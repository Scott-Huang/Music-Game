"""Program Description

The music.py program analyze the music and will be responsible
for extracting the beats of the music.
"""

import librosa
import numpy as np
from model.setting import MUSIC_FOLDER

# num of frames being analyzed together
HOP_LENGTH = 4096
# the minimum interval that each repetion can occur
REPETITION_INTERVAl = 10
# the minimum duration of a repetitive part
REPETITION_MIN_DURATION = 3

def get_music_length(filename):
    """Get the length of the music.
    
    Arguments:
        filename: The file name of the music file.
    Returns:
        The length of the music in sec.
    """

    return librosa.get_duration(filename=MUSIC_FOLDER+filename)

def retrieve_beats(music, freq):
    """Retrieve the beats of a music.

    Arguments:
        music: An array that represents a music.
        freq: The frequency of the music array.
    Returns:
        An array that contains the time in second that all beats occur.
    """
    beats = librosa.onset.onset_detect(music, freq, units='time')
    #_, beats = librosa.beat.beat_track(music, freq)
    #beats = librosa.frames_to_time(beats, sr=freq)
    return beats

def retrieve_repetition(music, freq):
    """

    Arguments:
        music: An array that represents a music.
        freq: The frequency of the music array.
    Returns:
        repetition: An array that partitions segments of the music
                    into categories, where category 0 means the default
                    category.
        seg_length: The length in second that one segment lasts.
    """

    # calculate correlation among features of segments
    chroma = librosa.feature.chroma_cqt(music, freq,
                                        hop_length=HOP_LENGTH)
    chroma_stack = librosa.feature.stack_memory(chroma, n_steps=10, delay=3)
    R = librosa.segment.recurrence_matrix(chroma_stack,
                                          width=REPETITION_INTERVAl, sym=True)

    # the duration of one segment in sec
    seg_length = music.shape[0] / freq / R.shape[0]
    # the minimum num of continuous segments need to be correlated
    min_repetition = int(REPETITION_MIN_DURATION // seg_length)
    # a helper indices from 0 to min_repetition
    indices = np.arange(min_repetition, dtype=int)
    # the width between two possible related segments
    width = min_repetition + REPETITION_INTERVAl
    
    # a repetition array that partitions segments into categories
    repetition = np.zeros(R.shape[0], dtype=int)
    current_category = 1
    # loop through R
    i = 0
    while i < R.shape[0] - min_repetition:
        if repetition[indices+i].any():
            i += 1
            continue

        # loop through R to find segments that are related to i
        j = i + width
        temp_i = i
        while j < R.shape[0] - min_repetition:
            if not repetition[indices+j].any() and R[(indices+i,indices+j)].all():
                if not repetition[i]:
                    # create a new category if found new related i,j
                    category = current_category
                    current_category += 1
                else:
                    category = repetition[i]

                # assigned i,j to the same category
                repetition[indices+i] = category
                repetition[indices+j] = category
                temp_i += min_repetition
                j += min_repetition

                # try to extend i,j for further correlation
                while R[temp_i,j] and j < R.shape[0] - min_repetition:
                    repetition[temp_i] = category
                    repetition[j] = category
                    temp_i += 1
                    j += 1

            j += 1
        i += 1
    
    return repetition, seg_length

def get_patterned_beats(filename, time_delay=0):
    """Retrieve the beats of a music file and analyze its
    repeting patterns.

    Arguments:
        filename: The file name of the music file.
    Returns:
        beats: A list of time in ms that beats occur.
        patterns: A list of patterns corresponding to beats
                  where pattern 0 means the default pattern
                  (no pattern).
    """

    music, freq = librosa.load(MUSIC_FOLDER+filename)
    beats = retrieve_beats(music, freq)
    beats = beats[beats>time_delay]
    repetition, seg_length = retrieve_repetition(music, freq)
    patterns = repetition[(beats / seg_length).astype(int)]
    beats = beats * 1000
    return list(beats), list(patterns)
