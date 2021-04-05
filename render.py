import pygame
from model.track import Track

BLACK = (0,0,0)

pygame.font.init() # you have to call this at the start, 
                   # if you want to use this module.
font = pygame.font.SysFont('Comic Sans MS', 32)

def load_img(filename, size=None):
    img = pygame.image.load('res/image/'+filename)
    if size:
        img = scale_img(img, size)
    return img

def scale_img(img, size):
    if img.get_size() == size:
        return img
    return pygame.transform.scale(img, size)

def render_background(background, screen):
    screen.blit(background, (0,0))

def render_key(key_img, position, screen):
    screen.blit(key_img, position)

def render_track(track: Track, key_img, circle_img, screen):
    screen.blit(key_img, track.get_key_position())
    for circle_position in track.get_circles():
        screen.blit(circle_img, circle_position)

def render_all_tracks(track_dict, key_imgs, circle_img, screen):
    for track, key_img in zip(track_dict.values(), key_imgs):
        render_track(track, key_img, circle_img, screen)

def display_score(score, position, screen):
    textsurface = font.render('Score:%d' % score, False, BLACK)
    screen.blit(textsurface, position)
