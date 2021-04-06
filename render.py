"""Program Description

The render.py program renders all components to the game screen.
"""

import pygame
from model.track import Track
from model.utils import report_error

# some fonts
pygame.font.init()
SCORE_FONT = pygame.font.SysFont('Comic Sans MS', 32)
COMBO_FONT = pygame.font.SysFont('Comic Sans MS', 60)
PERFORM_FONT = pygame.font.SysFont('Comic Sans MS', 28)
styles = {'score': SCORE_FONT, 'combo': COMBO_FONT, 'perform': PERFORM_FONT}

def load_img(filename, size=None):
    """Load an image from res/image folder.

    Arguments:
        filename: The name of the file.
        size: The size of the output image, none for original size.
    Returns:
        The loaded image.
    """

    img = pygame.image.load('res/image/'+filename)
    if size:
        img = scale_img(img, size)
    return img

def scale_img(img, size):
    """Rescale an image.

    Arguments:
        img: The image to be rescaled.
        size: The size of the image to scale.
    Returns:
        The rescaled image.
    """

    if img.get_size() == size:
        return img
    return pygame.transform.scale(img, size)

def render_background(background, screen):
    """Render the background."""
    screen.blit(background, (0,0))

def render_track(track: Track, key_img, circle_img, screen):
    """Render the tracks. A track has its key and circles.

    Arguments:
        track: The track that has key and circles.
        key_img: The image of the key.
        circle_img: The image of the circles.
        screen: The game screen that the track will be rendered on.
    """

    screen.blit(key_img, track.get_key_position())
    for circle_position in track.get_circles():
        screen.blit(circle_img, circle_position)

def render_all_tracks(track_dict, key_imgs, circle_img, screen):
    """Render all tracks. Each track has its key and circles.

    Arguments:
        track_dict: A dict with keys being index and values being tracks.
        key_imgs: The list of images of the key. The order should match track_dict.
        circle_img: The image of the circles.
        screen: The game screen that the track will be rendered on.
    """

    # validate arguments
    if len(track_dict) != len(key_imgs):
        report_error('Keys and key_imgs do not match')

    for track, key_img in zip(track_dict.values(), key_imgs):
        render_track(track, key_img, circle_img, screen)

def render_text(text, position, screen, style, color='black'):
    """Render text to the screen.

    Arguments:
        text: The message to be rendered.
        position: The position of the text, can be a tuple or 'center'.
        screen: The game screen that the track will be rendered on.
        style: The style of the text, 'score', 'combo', or 'perform'.
        color: The color of the text.
    """

    # validate arguments
    if style not in styles:
        report_error('No such text style')

    textsurface = styles[style].render(text, False, pygame.Color(color))
    if position == 'center':
        position = textsurface.get_rect(center=(screen.get_width()/2, screen.get_height()/2))

    screen.blit(textsurface, position)

def display_score(score, position, screen):
    """Render the score."""
    render_text('Score:%d' % score, position, screen, 'score')

