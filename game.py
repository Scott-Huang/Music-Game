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
from model.setting import MUSIC_FOLDER

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

CAPTION = 'Music Game'
FRAME_RATE = 30

def update_time(sec, frame):
    """Increment time."""
    frame += 1
    if frame >= FRAME_RATE:
        frame = 0
        sec += 1
    return sec, frame

def get_key_imgs(key_img, light_key_img, key_num, mode):
    """Lighten keys if they are pressed."""
    key_imgs = [key_img] * key_num
    keys = key.get_pressed()
    for gamekey in mode:
        if keys[gamekey]:
            key_imgs[mode[gamekey]-1] = light_key_img
    return key_imgs

def init_screen(size):
    """Initiate the screen."""
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption(CAPTION)
    pygame.display.set_icon(load_img('icon2.png'))
    return screen

def init_components(size, track_width):
    """Initiate all image resources."""
    # background img
    background = load_img('background.jpg', size)
    # key img
    key_img = load_img('key1.png', (track_width, track_width)).convert_alpha()
    # lightened key img
    light = pygame.Surface((key_img.get_width(), key_img.get_height()), flags=pygame.SRCALPHA)
    light.fill((50, 50, 50, 0))
    light_key_img = key_img.copy()
    light_key_img.blit(light, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
    # circle img
    circle_img = load_img('circle.png', (track_width, track_width)).convert_alpha()
    return background, key_img, light_key_img, circle_img

def start_game(screen, size, mode, velocity, music, music_length):
    key_num = len(mode)

    # Game set-up
    clock = pygame.time.Clock()
    screen = init_screen(size)
    # load music
    mixer.music.load(MUSIC_FOLDER + music)

    track_width = size[0] // (key_num+1)
    track_height = size[1]-ceil(0.5*track_width)
    # get key and circle img
    background, key_img, light_key_img, circle_img = init_components(size, track_width)

    # initiate tracks into a dict
    tracks = {}
    for track_index in range(1, key_num+1):
        tracks[track_index] = Track(width=track_width, height=track_height,
                                    position=(ceil(track_width*(track_index-0.5)), -1*track_width))

    time_delay = track_height / velocity / FRAME_RATE
    circle_handler = CircleHandler(music, key_num, time_delay)

    # initiate all attributes
    in_game = True
    sec_count = 0
    frame_count = 1
    score = 0
    combo = 0

    # start the music
    mixer.music.play()
    # start game loop
    while in_game:
        # set refresh rate
        clock.tick(FRAME_RATE)

        # render background, score, and combo
        render_background(background, screen)
        display_score(score, (0, 0), screen)
        render_text_center(str(combo), screen, style='center')

        # handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                in_game = False
            if event.type == pygame.KEYDOWN:
                # update status for key being pressed
                received_score = score_press(event, tracks, mode, FRAME_RATE, velocity)
                if received_score != 0:
                    combo += 1
                    score += received_score

        # apply key pressing effects
        key_imgs = get_key_imgs(key_img, light_key_img, key_num, mode)

        # generate and update circles to tracks
        circle_handler.update_circles(velocity, tracks)
        # render all tracks
        render_all_tracks(tracks, key_imgs, circle_img, screen)
        # score miss circles
        received_score = score_miss(tracks, FRAME_RATE, velocity)
        if received_score < 0:
            combo = 0
            score += received_score

        # rerender all components
        pygame.display.update()

        # update time
        sec_count, frame_count = update_time(sec_count, frame_count)
        # stop the game if the music ends.
        if sec_count > music_length:
            in_game = False

    return score
