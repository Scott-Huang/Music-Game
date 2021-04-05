import pygame
from math import ceil
from render import load_img, render_background, render_all_tracks
from model.circles import add_circle_per_sec
from model.utils import KeySet
from model.track import Track

CAPTION = 'Music Game'
FRAME_RATE = 60
SIZE = (1920,1080)
MODE = KeySet.FOUR_KEYS
KEY_NUM = len(MODE)
VELOCITY = 10

# Game set-up
pygame.init()
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption(CAPTION)
pygame.display.set_icon(load_img('icon2.png'))
background = load_img('background.jpg', SIZE)
clock = pygame.time.Clock()

track_width = SIZE[0]//(KEY_NUM*2+1)
key_img = load_img('key1.png', (track_width, track_width)).convert_alpha()
circle_img = load_img('circle.png', (track_width, track_width)).convert_alpha()

tracks = {}
for track_index in range(1, KEY_NUM+1):
    tracks[track_index] = Track(width=track_width, height=SIZE[1]-ceil(0.5*track_width), 
                                position=(track_width*(track_index*2-1), -1*track_width))

gameloop = True
sec_count = 0
frame_count = 0
while gameloop:
    clock.tick(60)
    render_background(background, screen)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameloop = False

    add_circle_per_sec(VELOCITY, sec_count, frame_count, tracks, 0.6)
    render_all_tracks(tracks, key_img, circle_img, screen)
    pygame.display.update()

    frame_count += 1
    if frame_count >= 60:
        frame_count = 0
        sec_count += 1

pygame.quit()
