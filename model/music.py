"""Program Description

The music.py program analyze the music and will be responsible
for extracting the beats of the music.

Reference: https://gitlab.com/avirzayev/music-visualizer.
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
    return beats

def correlation_matrix(music, freq):
    """Calculate the identical parts among a music.

    Arguments:
        music: An array that represents a music.
        freq: The frequency of the music array.
    Returns:
        A correlation matrix between music segments.
    """

    chroma = librosa.feature.chroma_cqt(music, freq,
                                        hop_length=HOP_LENGTH)
    chroma_stack = librosa.feature.stack_memory(chroma, n_steps=10, delay=3)
    return librosa.segment.recurrence_matrix(chroma_stack,
                                             width=REPETITION_INTERVAl, sym=True)

def retrieve_repetition(music, freq):
    """Partition the music into segments with a label of their repeating
    patterns.

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
    R = correlation_matrix(music, freq)

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

    def __set_patterns(index_i, index_j, category):
        # assigned i,j to the same category
        repetition[indices+index_i] = category
        repetition[indices+j] = category
        index_i += min_repetition
        index_j += min_repetition

        # try to extend i,j for further correlation
        while R[index_i,index_j] and j < R.shape[0] - min_repetition:
            repetition[index_i] = category
            repetition[index_j] = category
            index_i += 1
            index_j += 1

    # loop through R
    i = 0
    while i < R.shape[0] - min_repetition:
        if repetition[indices+i].any():
            i += 1
            continue

        # loop through R to find segments that are related to segment i
        j = i + width
        while j < R.shape[0] - min_repetition:
            if not repetition[indices+j].any() and R[(indices+i,indices+j)].all():
                if not repetition[i]:
                    # create a new category if found new related i,j
                    category = current_category
                    current_category += 1
                else:
                    category = repetition[i]

                __set_patterns(i, j, category)
                j += min_repetition
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
    # get rhythm of the music
    beats = retrieve_beats(music, freq)
    # filter out the starting part
    beats = beats[beats>time_delay]
    # get repetition
    repetition, seg_length = retrieve_repetition(music, freq)
    # assign beats into these patterns
    patterns = repetition[(beats / seg_length).astype(int)]
    # convert into ms
    beats = beats * 1000
    # return a list so that we can pop the elements when circles are added
    return list(beats), list(patterns)

class MusicAnalyzer():
    """The MusicAnalyzer class analyzes the music features over time."""

    def __init__(self):
        """MusicAnalyzer constructor."""
        self.frequencies_index_ratio = None  # array for frequencies
        self.time_index_ratio = None  # array for time
        self.spectrogram = None  # decibels corresponding to frequency and time

    def load(self, music_file):
        """Load a music and analyze."""
        # needs thinner hop_length to achieve smoother visualization
        HOP_LENGTH = 512
        N_FFT = 2048*4

        music, sample_rate = librosa.load(MUSIC_FOLDER+music_file)
        # getting music features(amp & freq) over time
        stft = np.abs(librosa.stft(music, hop_length=HOP_LENGTH, n_fft=N_FFT))
        # converting feature to decibal
        self.spectrogram = librosa.amplitude_to_db(stft, ref=np.max)
        # converting feature to frequencies
        frequencies = librosa.core.fft_frequencies(n_fft=N_FFT)
        # getting time for features
        times = librosa.core.frames_to_time(np.arange(self.spectrogram.shape[1]),
                                            sr=sample_rate, hop_length=HOP_LENGTH, n_fft=N_FFT)

        self.time_index_ratio = len(times)/times[len(times) - 1]
        self.frequencies_index_ratio = len(frequencies)/frequencies[len(frequencies)-1]

    def get_decibel(self, target_time, freq):
        """Get amp in decibel of a music in the given time."""
        return self.spectrogram[int(freq*self.frequencies_index_ratio)][int(target_time*self.time_index_ratio)]

    def get_decibel_array(self, target_time, freq_array):
        """Get a list of amp in decibel in the given time."""
        decibel_array = []
        for freq in freq_array:
            decibel_array.append(self.get_decibel(target_time,freq))
        return decibel_array
