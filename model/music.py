"""Program Description

The music.py program analyze the music and will be responsible
for extracting the beats of the music.
"""

import librosa
from model.setting import MUSIC_FOLDER

def get_music_length(filename):
    """Get the length of the music.
    
    Arguments:
        filename: the file name of the music file.
    Returns:
        The length of the music in sec.
    """

    return librosa.get_duration(filename=MUSIC_FOLDER+filename)