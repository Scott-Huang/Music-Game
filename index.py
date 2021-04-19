"""Program Description

The index.py program start the menu page and load music files.
Once the start button is clicked, it will pass all parameters into
the game.py and run the main game.
"""

import os
import time
import pygame
import pygame_menu
from game import start_game
from model.setting import DefaultSetting, Keyset, MUSIC_FOLDER
from model.utils import report_error
from model.music import get_music_length
from render import render_background, render_text_center, load_img

# global constants
DEFAULT_SIZE = DefaultSetting.LARGE_SCREEN_SIZE
TEXT_DISPLAY_TIME = 2

# game initiation, reading music files
files = os.listdir(MUSIC_FOLDER)
music_files = []
for filename in files:
    if filename.endswith('.mp3'):
        music_files.append(filename)
if len(music_files) < 1:
    report_error('There is no valid music file in the music folder')

# global parameters
music = music_files[0]
size = DefaultSetting.LARGE_SCREEN_SIZE
mode = Keyset.SIX_KEYS
velocity = DefaultSetting.MEDIUM_VELOCITY
score = 0
screen = pygame.display.set_mode(DEFAULT_SIZE)

def display_text(text, screen, size):
    """Display text and rerender the screen."""
    background = load_img('background.jpg', size)
    render_background(background, screen)
    render_text_center(text, screen, 'center')
    pygame.display.update()

# functions of widget to set parameters
def set_music(_, selected_music):
    global music 
    music = selected_music

def set_size(_, selected_size):
    global size
    size = selected_size

def set_velocity(_, selected_velocity):
    global velocity
    velocity = selected_velocity

def set_mode(_, selected_mode):
    global mode
    mode = selected_mode

def init_game():
    """Initiate the game and return the length of music."""
    music_length = get_music_length(music)
    # should be longer than 30 secs at least
    # set the minimum to be 5 sec for debugging
    if music_length < 5 or music_length > 1000:
        report_error('The music is too long or too shortlkfds')

    display_text('Generating the game...', screen, DEFAULT_SIZE)
    return music_length

def close_menu():
    """Close the menu."""
    menu.disable()

# initiate the game
pygame.init()
# initiate menu
menu = pygame_menu.Menu('Game Menu', DEFAULT_SIZE[0], DEFAULT_SIZE[1],
                       theme=pygame_menu.themes.THEME_BLUE)
# menu widgets
menu.add.dropselect('Music :', list(zip(music_files, music_files)), onchange=set_music, default=0)
menu.add.dropselect('Screen Size :', DefaultSetting.SCREEN_SIZES, onchange=set_size, default=2)
menu.add.selector('Velocity: ', DefaultSetting.VELOCITIES, onchange=set_velocity, default=1)
menu.add.selector('Mode: ', DefaultSetting.MODES, onchange=set_mode, default=1)
menu.add.button('Start', close_menu)
menu.add.button('Quit', pygame_menu.events.EXIT)

# display menu
menu.mainloop(screen)
music_length = init_game()
score = start_game(screen, size, mode, velocity, music, music_length)

# display result
display_text('Result Score is: %d, see ya!' % score, screen, size)
time.sleep(TEXT_DISPLAY_TIME)
# close window
pygame.quit()