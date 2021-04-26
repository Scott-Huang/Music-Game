"""Program Description

The game.py program run a pygame window of the main game.
It has a main game while loop that renders every component
and deals with key pressing event.
"""

import pygame
import sys
from pygame import key, mixer
from math import ceil
from render import display_score, load_img, render_background, render_all_tracks, render_text_center
from model.circles import CircleHandler
from model.track import Track
from model.score_circles import score_miss, score_press
from model.setting import MUSIC_FOLDER, CAPTION, FRAME_RATE, DefaultSetting, Keyset
from model.audio_visualizer import AudioVisualizer

"""
The code below set pygame adapt to resolutions over 2k on windows.
Reference https://stackoverflow.com/questions/62775254.
"""
if sys.platform == 'win32':
    # On Windows, the monitor scaling can be set to something besides normal 100%.
    # PyScreeze and Pillow needs to account for this to make accurate screenshots.
    import ctypes
    try:
       ctypes.windll.user32.SetProcessDPIAware()
    except AttributeError:
        pass # Windows XP doesn't support monitor scaling, so just do nothing.

class Game():
    """The Game class handles the control of the game which connects the model
    and the game interface.
    """

    class GameParameters():
        """The GameParameters class wraps all game setting attributes into
        a class instance.
        """

        def __init__(self, music, background_source,
                     size=DefaultSetting.LARGE_SCREEN_SIZE,
                     mode=Keyset.SIX_KEYS,
                     velocity=DefaultSetting.MEDIUM_VELOCITY):
            """GameParameters constructor.

            Arguments:
                music: The filename of the music file.
                background_source: The filename of the background image file.
                size: The screen size.
                mode: The game key set mode.
                velocity: The velocity of the circles.
            """

            self.music = music
            self.background_source = background_source
            self.size = size
            self.mode = mode
            self.velocity = velocity

    def __init__(self, parameters: GameParameters):
        """Game constructor.

        Arguments:
            parameters: The parameter of the game setting, wrapped as
                        a GameParameters instance.
        """

        # read parameters
        self.music = parameters.music
        self.background_source = parameters.background_source
        self.size = parameters.size
        self.mode = parameters.mode
        self.velocity = parameters.velocity

        self.score = 0
        self.key_num = len(self.mode)
        self.track_width = self.size[0] // (self.key_num+1)
        self.track_height = self.size[1]-ceil(0.5*self.track_width)

        mixer.music.load(MUSIC_FOLDER + self.music)
        self.clock = pygame.time.Clock()
        
        self.__init_screen()
        self.__init_components()
        self.__init_tracks()

        self.time_delay = self.track_height / self.velocity / FRAME_RATE
        self.circle_handler = CircleHandler(self.music, self.key_num, self.time_delay)
        self.visualizer = AudioVisualizer(self.size, self.music)


    def __init_screen(self):
        """Initiate the screen."""
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption(CAPTION)
        pygame.display.set_icon(load_img('icon2.png'))

    def __init_components(self):
        """Initiate all image resources."""
        # background img
        self.background = load_img(self.background_source, self.size)
        # key img
        self.key_img = load_img('key1.png', (self.track_width, self.track_width)).convert_alpha()
        # lightened key img
        light = pygame.Surface((self.key_img.get_width(), self.key_img.get_height()),
                                flags=pygame.SRCALPHA)
        light.fill((50, 50, 50, 0))
        self.light_key_img = self.key_img.copy()
        self.light_key_img.blit(light, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
        # circle img
        self.circle_img = load_img('circle.png', (self.track_width, self.track_width)).convert_alpha()
    
    def __init_tracks(self):
        """Initiate all tracks."""
        self.tracks = {}
        # the keys of tracks match directly the mode
        for track_index in range(1, self.key_num+1):
            self.tracks[track_index] = Track(self.track_width, self.track_height,
                                             (ceil(self.track_width*(track_index-0.5)), -self.track_width))

    def mainloop(self):
        """Run the main game loop."""
        # initiate all attributes
        in_game = True
        score = 0
        combo = 0
        # start playing the music
        mixer.music.play()

        # start game loop
        while in_game:
            # set refresh rate
            self.clock.tick(FRAME_RATE)
            # render background, score
            render_background(self.background, self.screen)
            display_score(score, (0, 0), self.screen)

            # handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    in_game = False
                if event.type == pygame.KEYDOWN:
                    # update status for key being pressed
                    received_score = score_press(event, self.tracks,
                                                 self.mode, FRAME_RATE, self.velocity)
                    if received_score != 0:
                        combo += 1
                        score += received_score

            # apply key pressing effects
            key_imgs = get_key_imgs(self.key_img, self.light_key_img,
                                    self.key_num, self.mode)

            # generate and update circles to tracks
            self.circle_handler.update_circles(self.velocity, self.tracks)
            # render audio visualizer
            self.visualizer.render(self.screen)
            # display combo
            render_text_center(str(combo), self.screen, style='center', color='white')
            # render all tracks
            render_all_tracks(self.tracks, key_imgs, self.circle_img, self.screen)
            # score miss circles
            received_score = score_miss(self.tracks, FRAME_RATE, self.velocity)
            if received_score < 0:
                combo = 0
                score += received_score

            # rerender all components
            pygame.display.update()
            # stop the game if the music ends.
            if not pygame.mixer.music.get_busy():
                in_game = False
        
        self.score = score


def get_key_imgs(key_img, light_key_img, key_num, mode):
    """Lighten keys if they are pressed."""
    key_imgs = [key_img] * key_num
    keys = key.get_pressed()
    for gamekey in mode:
        if keys[gamekey]:
            key_imgs[mode[gamekey]-1] = light_key_img
    return key_imgs
