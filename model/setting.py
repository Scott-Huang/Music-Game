"""Program Description

The setting.py program holds sone constants for the game settings.
"""

import pygame

MUSIC_FOLDER = './res/music/'
IMAGE_FOLDER = './res/image/'

class Keyset():
    """The Keyset class have different types of key sets
    with the form of dict<key: index>
    """
    FOUR_KEYS = {pygame.K_d: 1, pygame.K_f: 2, pygame.K_j: 3, pygame.K_k: 4}
    SIX_KEYS = {pygame.K_s: 1, pygame.K_d: 2, pygame.K_f: 3, pygame.K_j: 4, pygame.K_k: 5, pygame.K_l: 6}
    EIGHT_KEYS = {pygame.K_a: 1, pygame.K_s: 2, pygame.K_d: 3, pygame.K_f: 4, 
                  pygame.K_j: 5, pygame.K_k: 6, pygame.K_l: 7, pygame.K_SEMICOLON: 8}

class DefaultSetting():
    """The DefaultSetting class have all setting attributes of
    the game setting.
    """
    SMALL_SCREEN_SIZE = (1250, 1050)
    MEDIUM_SCREEN_SIZE = (1800, 1400)
    LARGE_SCREEN_SIZE = (2500, 2000)
    SLOW_VELOCITY = 16
    MEDIUM_VELOCITY = 20
    FAST_VELOCITY = 25

    SCREEN_SIZES = [('Small', SMALL_SCREEN_SIZE), ('Medium', MEDIUM_SCREEN_SIZE),
                    ('Large', LARGE_SCREEN_SIZE)]
    VELOCITIES = [('Slow', SLOW_VELOCITY), ('Medium', MEDIUM_VELOCITY), ('Fast', FAST_VELOCITY)]
    MODES = [('Four keys', Keyset.FOUR_KEYS), ('Six keys', Keyset.SIX_KEYS), ('Eight keys', Keyset.EIGHT_KEYS)]
