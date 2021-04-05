import pygame
import sys
from pygame import key
from math import ceil
from render import display_score, load_img, render_background, render_all_tracks
from model.circles import add_circle_per_sec
from model.utils import KeySet
from model.track import Track
from model.model import miss_check, press_check

'''
The code below set pygame adapt to resolution above 2k on windows.
Reference https://stackoverflow.com/questions/62775254.
'''
if sys.platform == 'win32':
    # On Windows, the monitor scaling can be set to something besides normal 100%.
    # PyScreeze and Pillow needs to account for this to make accurate screenshots.
    # TODO - How does macOS and Linux handle monitor scaling?
    import ctypes
    try:
       ctypes.windll.user32.SetProcessDPIAware()
    except AttributeError:
        pass # Windows XP doesn't support monitor scaling, so just do nothing.

CAPTION = 'Music Game'
FRAME_RATE = 60
#SIZE = (1920, 1080)
SIZE = (2560, 1440)
MODE = KeySet.SIX_KEYS
KEY_NUM = len(MODE)
VELOCITY = 10

# Game set-up
pygame.init()
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption(CAPTION)
pygame.display.set_icon(load_img('icon2.png'))
background = load_img('background.jpg', SIZE)
clock = pygame.time.Clock()

track_width = SIZE[0]//(KEY_NUM+1)
key_img = load_img('key1.png', (track_width, track_width)).convert_alpha()
dark = pygame.Surface((key_img.get_width(), key_img.get_height()), flags=pygame.SRCALPHA)
dark.fill((50, 50, 50, 0))
light_key_img = key_img.copy()
light_key_img.blit(dark, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
circle_img = load_img('circle.png', (track_width, track_width)).convert_alpha()

tracks = {}
for track_index in range(1, KEY_NUM+1):
    tracks[track_index] = Track(width=track_width, height=SIZE[1]-ceil(0.5*track_width), 
                                position=(ceil(track_width*(track_index-0.5)), -1*track_width))

gameloop = True
sec_count = 0
frame_count = 0
score = 0
while gameloop:
    clock.tick(60)
    render_background(background, screen)
    display_score(score, (0, 0), screen)

    key_imgs = [key_img] * KEY_NUM
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameloop = False
        if event.type == pygame.KEYDOWN:
            # TODO
            press_check(tracks, MODE)

    keys = key.get_pressed() 
    for gamekey in MODE:
        if keys[gamekey]:
            key_imgs[MODE[gamekey]-1] = light_key_img

    add_circle_per_sec(VELOCITY, sec_count, frame_count, tracks, 0.6)
    render_all_tracks(tracks, key_imgs, circle_img, screen)
    miss_check(tracks)
    pygame.display.update()

    frame_count += 1
    if frame_count >= 60:
        frame_count = 0
        sec_count += 1

pygame.quit()
