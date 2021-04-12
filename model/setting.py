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
    SCREEN_SIZES = [('Small', (1200, 1200)), ('Medium', (1500, 1500)), ('Large', (2000, 2000))]
    VELOCITIES = [('Slow', 16), ('Medium', 20), ('Fast', 25)]
    MODES = [('Four keys', Keyset.FOUR_KEYS), ('Six keys', Keyset.SIX_KEYS), ('Eight keys', Keyset.EIGHT_KEYS)]