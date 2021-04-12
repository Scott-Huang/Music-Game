import librosa
from model.setting import MUSIC_FOLDER

def get_music_length(filename):
    return librosa.get_duration(filename=MUSIC_FOLDER+filename)