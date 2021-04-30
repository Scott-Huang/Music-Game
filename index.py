"""Program Description

The index.py program start the menu page and load music files.
Once the start button is clicked, it will pass all parameters into
the game.py and run the main game.
"""

import os
import time
import pygame
import pygame_menu
from game import Game
from model.setting import DefaultSetting, MUSIC_FOLDER, IMAGE_FOLDER
from model.utils import report_error
from model.music import get_music_length
from render import render_background, render_text_center, load_img

# global constants
DEFAULT_SIZE = DefaultSetting.LARGE_SCREEN_SIZE
TEXT_DISPLAY_TIME = 2
SELECTION_SIZE = 8

# game initiation, reading music files
files = os.listdir(MUSIC_FOLDER)
music_files = []
for filename in files:
    if filename.endswith('.mp3'):
        music_files.append(filename)

# reading background img files
files = os.listdir(IMAGE_FOLDER)
background_images = []
for filename in files:
    if filename.startswith('background'):
        background_images.append(filename)

if len(music_files) < 1:
    report_error('There is no valid music file in the music folder')
if len(background_images) < 1:
    report_error('Missing background image files')

parameters = Game.GameParameters(music_files[0], background_images[0])
screen = pygame.display.set_mode(DEFAULT_SIZE)

def display_text(text, screen, size):
    """Display text and rerender the screen."""
    background = load_img('index.jpg', size)
    render_background(background, screen)
    render_text_center(text, screen, 'center')
    pygame.display.update()

# functions of widget to set parameters
def set_music(_, selected_music):
    parameters.music = selected_music

def set_background(_, selected_background):
    parameters.background_source = selected_background

def set_size(_, selected_size):
    parameters.size = selected_size

def set_velocity(_, selected_velocity):
    parameters.velocity = selected_velocity

def set_mode(_, selected_mode):
    parameters.mode = selected_mode

def prepare_game():
    """Initiate the game and return the length of music."""
    music_length = get_music_length(parameters.music)
    # music should be longer than 30 secs at least
    if music_length < 30 or music_length > 1000:
        report_error('The music is too long or too short')
    display_text('Generating the game...', screen, DEFAULT_SIZE)

def close_menu():
    """Close the menu."""
    menu.disable()

# initiate the game
pygame.init()
# initiate menu
menu = pygame_menu.Menu('Game Menu', DEFAULT_SIZE[0], DEFAULT_SIZE[1],
                       theme=pygame_menu.themes.THEME_BLUE)
# menu widgets
menu.add.dropselect('Music :', list(zip(music_files, music_files)), onchange=set_music,
                    default=0, selection_box_height=SELECTION_SIZE)
menu.add.dropselect('Background :', list(zip(background_images, background_images)),
                    onchange=set_background, default=0, selection_box_height=SELECTION_SIZE)
menu.add.dropselect('Screen Size :', DefaultSetting.SCREEN_SIZES, onchange=set_size, default=2)
menu.add.selector('Velocity: ', DefaultSetting.VELOCITIES, onchange=set_velocity, default=1)
menu.add.selector('Mode: ', DefaultSetting.MODES, onchange=set_mode, default=1)
menu.add.button('Start', close_menu)
menu.add.button('Quit', pygame_menu.events.EXIT)

# display menu
menu.mainloop(screen)
# loading screen
prepare_game()
# start game
game = Game(parameters)
game.mainloop()

# display result
display_text('Result Score is: %d, see ya!' % game.score, screen, game.size)
time.sleep(TEXT_DISPLAY_TIME)
# close window
pygame.quit()
