import math
import numpy as np
import random
import colorsys
import pygame
from model.music import MusicAnalyzer

def rotate(vector, theta):
    """Rotate a vector using a rotation matrix."""
    cos_theta, sin_theta = math.cos(theta), math.sin(theta)
    return (vector[0] * cos_theta - vector[1] * sin_theta,
            vector[0] * sin_theta + vector[1] * cos_theta)

def move_point(vector, offset):
    """Move a vector to the given point."""
    return vector[0] + offset[0], vector[1] + offset[1]

def clamp(value, min_value, max_value):
    """Clamp the value given the upper and lower threshold."""
    return min(max_value, max(min_value, value))

def generate_color():
    """Get a bright random color.
    Reference https://stackoverflow.com/questions/43437309/get-a-bright-random-colour-python.

    Returns:
        A color in an array in rgb channels.
    """

    h, s, l = random.random(), 0.5 + random.random() / 2.0, 0.4 + random.random() / 5.0
    return [int(256 * i) for i in colorsys.hls_to_rgb(h, l, s)]

class AudioBar:

    def __init__(self, x, y, freq, color, width=50,
                 min_height=10, max_height=100, min_decibel=-80, max_decibel=0):
        self.x, self.y, self.freq = x, y, freq
        self.color = color
        self.width, self.min_height, self.max_height = width, min_height, max_height
        self.height = min_height
        self.min_decibel, self.max_decibel = min_decibel, max_decibel
        self.__decibel_height_ratio = (self.max_height - self.min_height)/(self.max_decibel - self.min_decibel)

    def update(self, dt, decibel):
        desired_height = decibel * self.__decibel_height_ratio + self.max_height
        speed = (desired_height - self.height)/0.1
        self.height = clamp(speed * dt, self.min_height, self.max_height)

    def render(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y + self.max_height - self.height, self.width, self.height))


class AverageAudioBar(AudioBar):

    def __init__(self, x, y, rng, color, width=50, min_height=10, max_height=100, min_decibel=-80, max_decibel=0):
        super().__init__(x, y, 0, color, width, min_height, max_height, min_decibel, max_decibel)
        self.rng = rng
        self.avg = 0

    def update_all(self, dt, time, analyzer):
        self.avg = 0
        for channel in self.rng:
            self.avg += analyzer.get_decibel(time, channel)
        self.avg /= len(self.rng)
        self.update(dt, self.avg)


class RotatedAverageAudioBar(AverageAudioBar):

    def __init__(self, x, y, rng, color, angle=0, width=50,
                 min_height=10, max_height=100, min_decibel=-80, max_decibel=0):
        super().__init__(x, y, 0, color, width, min_height,
                         max_height, min_decibel, max_decibel)
        self.rng = rng
        self.rect = None
        self.angle = angle

    def render(self, screen):
        pygame.draw.polygon(screen, self.color, self.rect.points)

    def render_c(self, screen, color):
        pygame.draw.polygon(screen, color, self.rect.points)

    def update_rect(self):
        self.rect = Rect(self.x, self.y, self.width, self.height)
        self.rect.rotate(self.angle)


class Rect:

    def __init__(self,x ,y, w, h):
        self.x, self.y, self.w, self.h = x, y, w, h
        self.points = []
        self.origin = [self.w/2,0]
        self.offset = [self.origin[0] + x, self.origin[1] + y]
        self.rotate(0)

    def rotate(self, angle):
        template = [
            (-self.origin[0], self.origin[1]),
            (-self.origin[0] + self.w, self.origin[1]),
            (-self.origin[0] + self.w, self.origin[1] - self.h),
            (-self.origin[0], self.origin[1] - self.h)
        ]
        self.points = [move_point(rotate(xy, math.radians(angle)), self.offset) for xy in template]

    def draw(self,screen):
        pygame.draw.polygon(screen, (255,255, 0), self.points)

BASS = {"start": 50, "stop": 100, "count": 12}
HEAVY = {"start": 120, "stop": 250, "count": 40}
LOW_MIDS = {"start": 251, "stop": 2000, "count": 50}
HIGH_MIDS = {"start": 2001, "stop": 6000, "count": 20}
FREQ_GROUPS = [BASS, HEAVY, LOW_MIDS, HIGH_MIDS]
WHITE = [255,255,255]
BLACK = [0,0,0]
DEFAULT_CIRCLE_COLOR = [40,40,40]

class AudioVisualizer():
    def __init__(self, size, music_file, bass_trigger=-30, min_decibel=-80, max_decibel=80,
                 min_radius=100, max_radius=150, polygon_default_color=WHITE):
        self.analyzer = MusicAnalyzer()
        self.analyzer.load(music_file)
        self.screen_width = size[0]
        self.screen_height = size[1]

        self.last_frame = pygame.time.get_ticks()
        self.timeCount = 0
        self.avg_bass = 0
        self.bass_trigger = bass_trigger
        self.bass_trigger_started = 0
        self.min_decibel = min_decibel
        self.max_decibel = max_decibel

        self.circle_color = DEFAULT_CIRCLE_COLOR
        self.polygon_default_color = polygon_default_color
        self.polygon_bass_color = polygon_default_color.copy()
        self.polygon_color_vel = BLACK

        self.poly = []
        self.poly_color = polygon_default_color.copy()

        self.circleX = int(self.screen_width/2)
        self.circleY = int(self.screen_height/2)

        self.min_radius = min_radius
        self.max_radius = max_radius
        self.radius = min_radius
        self.radius_vel = 0

        self.bars = []
        self.__init_bars()
    
    def __init_bars(self):
        tmp_bars = []
        length = 0

        for frequencies in FREQ_GROUPS:
            categories = []
            s = frequencies["stop"] - frequencies["start"]
            count = frequencies["count"]
            reminder = s%count
            step = int(s/count)
            rng = frequencies["start"]

            for _ in range(count):
                arr = None
                if reminder > 0:
                    reminder -= 1
                    arr = np.arange(start=rng, stop=rng + step + 2)
                    rng += step + 3
                else:
                    arr = np.arange(start=rng, stop=rng + step + 1)
                    rng += step + 2
                categories.append(arr)
                length += 1

            tmp_bars.append(categories)

        angle_dt = 360 / length
        ang = 0

        for group in tmp_bars:
            all_freq = []
            for category in group:
                all_freq.append(
                    RotatedAverageAudioBar(self.circleX+self.radius*math.cos(math.radians(ang - 90)),
                                           self.circleY+self.radius*math.sin(math.radians(ang - 90)),
                                           category, (255, 0, 255), angle=ang, width=10,
                                           max_height=self.screen_height))
                ang += angle_dt
            self.bars.append(all_freq)
        
    def render(self, screen):
        avg_bass = 0
        poly = []

        t = pygame.time.get_ticks()
        deltaTime = (t - self.last_frame) / 1000
        self.last_frame = t
        self.timeCount += deltaTime

        for b1 in self.bars:
            for b in b1:
                b.update_all(deltaTime, pygame.mixer.music.get_pos() / 1000, self.analyzer)

        for b in self.bars[0]:
            avg_bass += b.avg

        avg_bass /= len(self.bars[0])

        if avg_bass > self.bass_trigger:
            if self.bass_trigger_started == 0:
                bass_trigger_started = pygame.time.get_ticks()
            if (pygame.time.get_ticks() - bass_trigger_started)/1000.0 > 2:
                self.polygon_bass_color = generate_color()
                bass_trigger_started = 0
            if self.polygon_bass_color is None:
                self.polygon_bass_color = generate_color()
            newr = (self.min_radius +
                    int(avg_bass * ((self.max_radius - self.min_radius) / 
                                    (self.max_decibel - self.min_decibel)) + (self.max_radius - self.min_radius)))
            self.radius_vel = (newr - self.radius) / 0.15

            polygon_color_vel = [(self.polygon_bass_color[x] - self.poly_color[x])/0.15
                                 for x in range(len(self.poly_color))]

        elif self.radius > self.min_radius:
            self.bass_trigger_started = 0
            self.polygon_bass_color = None
            self.radius_vel = (self.min_radius - self.radius) / 0.15
            polygon_color_vel = [(self.polygon_default_color[x] - self.poly_color[x])/0.15 for x in range(len(self.poly_color))]

        else:
            self.bass_trigger_started = 0
            self.poly_color = self.polygon_default_color.copy()
            self.polygon_bass_color = None
            polygon_color_vel = [0, 0, 0]

            self.radius_vel = 0
            self.radius = self.min_radius

        self.radius += self.radius_vel * deltaTime

        for x in range(len(polygon_color_vel)):
            value = polygon_color_vel[x]*deltaTime + self.poly_color[x]
            self.poly_color[x] = value

        for b1 in self.bars:
            for b in b1:
                b.x, b.y = (self.circleX+self.radius*math.cos(math.radians(b.angle - 90)),
                            self.circleY+self.radius*math.sin(math.radians(b.angle - 90)))
                b.update_rect()

                poly.append(b.rect.points[3])
                poly.append(b.rect.points[2])

        pygame.draw.polygon(screen, self.poly_color, poly)
        pygame.draw.circle(screen, self.circle_color, (self.circleX, self.circleY), int(self.radius))
