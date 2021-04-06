import pygame
import logging

class Keyset():
    """The Keyset class have different types of key sets
    with the form of dict<key: index>
    """
    FOUR_KEYS = {pygame.K_d: 1, pygame.K_f: 2, pygame.K_j: 3, pygame.K_k: 4}
    SIX_KEYS = {pygame.K_s: 1, pygame.K_d: 2, pygame.K_f: 3, pygame.K_j: 4, pygame.K_k: 5, pygame.K_l: 6}
    EIGHT_KEYS = {pygame.K_a: 1, pygame.K_s: 2, pygame.K_d: 3, pygame.K_f: 4, 
                  pygame.K_j: 5, pygame.K_k: 6, pygame.K_l: 7, pygame.K_SEMICOLON: 8}

def report_info(msg):
    """Log info message"""
    logging.info(msg)

def report_error(msg):
    """Log error message and exit"""
    logging.error(msg)
    exit()