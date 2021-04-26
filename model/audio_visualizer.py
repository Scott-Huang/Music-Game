"""Program Description

The audio_visualizer.py program is responsible for displaying
the music visualization part in the background.

Reference: https://gitlab.com/avirzayev/music-visualizer.
"""

import math
import numpy as np
import random
import colorsys
import pygame
from model.music import MusicAnalyzer

# various modes of music freq
BASS = {"start": 50, "end": 100, "count": 12}
HEAVY = {"start": 120, "end": 250, "count": 40}
LOW_MIDS = {"start": 251, "end": 2000, "count": 50}
HIGH_MIDS = {"start": 2001, "end": 6000, "count": 20}
FREQ_GROUPS = [BASS, HEAVY, LOW_MIDS, HIGH_MIDS]

WHITE = [255,255,255]
BLACK = [0,0,0]
YELLOW = [255,255, 0]
DEFAULT_CIRCLE_COLOR = [40,40,40]

# updating speed constant parameter
UPDATE_SPEED = 0.1
UPDATE_RADIUS_SPEED = 0.15

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
    """The AudioBar class represent a bar as a component in visualization.
    It can update its length and color according to the music features.
    """

    def __init__(self, x, y, freq, color, width=50,
                 min_height=10, max_height=100, min_decibel=-80, max_decibel=0):
        """AudioBar constructor."""
        self.x, self.y, self.freq = x, y, freq
        self.color = color
        self.width, self.min_height, self.max_height = width, min_height, max_height
        self.height = min_height
        self.min_decibel, self.max_decibel = min_decibel, max_decibel
        # the ratio between the height space and the db space
        self.__decibel_height_ratio = ((self.max_height - self.min_height)
                                        / (self.max_decibel - self.min_decibel))

    def update(self, time_interval, decibel):
        """Update the bar height."""
        desired_height = decibel * self.__decibel_height_ratio + self.max_height
        speed = (desired_height - self.height) / UPDATE_SPEED
        self.height = clamp(speed * time_interval, self.min_height, self.max_height)

    def render(self, screen):
        pygame.draw.rect(screen, self.color,
                         (self.x, self.y + self.max_height - self.height, self.width, self.height))


class AudioBarGroup(AudioBar):
    """The AudioBarGroup class contains a groups of audio bars."""

    def __init__(self, x, y, rng, color, width=50,
                 min_height=10, max_height=100, min_decibel=-80, max_decibel=0):
        """AudioBarGroup constructor."""
        super().__init__(x, y, 0, color, width, min_height, max_height, min_decibel, max_decibel)
        self.rng = rng
        self.avg = 0

    def update_all(self, time_interval, time, analyzer):
        """Update heights of all bars."""
        self.avg = 0
        for channel in self.rng:
            self.avg += analyzer.get_decibel(time, channel)
        self.avg /= len(self.rng)
        self.update(time_interval, self.avg)


class RotatedAudioBarGroup(AudioBarGroup):
    """The RotatedAudioBarGroup is a groups of audio bars after rotated position index."""

    def __init__(self, x, y, rng, color, angle=0, width=50,
                 min_height=10, max_height=100, min_decibel=-80, max_decibel=0):
        """RotatedAudioBarGroup constructor."""
        super().__init__(x, y, 0, color, width, min_height,
                         max_height, min_decibel, max_decibel)
        self.rng = rng
        self.rect = None
        self.angle = angle

    def render(self, screen):
        """Render all rectangular bars."""
        pygame.draw.polygon(screen, self.color, self.rect.points)

    def update_rect(self):
        """Update all rectangular bars."""
        self.rect = Rect(self.x, self.y, self.width, self.height)
        self.rect.place(self.angle)


class Rect():
    """A rectangular bar that represent the visualized audio bar."""

    def __init__(self,x ,y, w, h):
        """Rect constructor."""
        self.x, self.y, self.w, self.h = x, y, w, h
        self.points = []
        self.origin = [self.w/2,0]
        self.offset = [self.origin[0] + x, self.origin[1] + y]
        self.place(0)

    def place(self, angle):
        """Place the points to the positions in screen."""
        rect_corners = [
            (-self.origin[0], self.origin[1]),
            (-self.origin[0] + self.w, self.origin[1]),
            (-self.origin[0] + self.w, self.origin[1] - self.h),
            (-self.origin[0], self.origin[1] - self.h)
        ]
        self.points = [move_point(rotate(corners, math.radians(angle)), self.offset)
                       for corners in rect_corners]

    def draw(self,screen):
        """Display the rect in screen."""
        pygame.draw.polygon(screen, YELLOW, self.points)

class AudioVisualizer():
    """The AudioVisualizer class is responsible for
    setting the attributes of the bars and the circle to
    match the music features over time.
    """

    def __init__(self, size, music_file, bass_trigger=-30, min_decibel=-80, max_decibel=80,
                 min_radius=100, max_radius=150, polygon_default_color=WHITE):
        """AudioVisualizer constructor
        
        Arguments:
            size: The size of the screen.
            music_file: The filename of the music file.
            bass_trigger: The trigger threshold of bass freq.
            min_decibel: The min decibel of the music.
            max_decibel: The max decibel of the music.
            min_radius: The min radius of music freq change
                        (The music is visualized as circles).
            max_radius: The max radius of music freq change.
            polygon_default_color: The default color of polygon bars.
        """

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
            freq_channels = []
            s = frequencies["end"] - frequencies["start"]
            count = frequencies["count"]
            reminder = s%count
            step = int(s/count)
            rng = frequencies["start"]

            for _ in range(count):
                channel = None
                if reminder > 0:
                    reminder -= 1
                    channel = np.arange(rng, rng+step+2)
                    rng += step + 3
                else:
                    channel = np.arange(rng, rng+step+1)
                    rng += step + 2
                freq_channels.append(channel)
                length += 1

            tmp_bars.append(freq_channels)

        angle_dt = 360 / length
        ang = 0

        for group in tmp_bars:
            all_freq = []
            for category in group:
                all_freq.append(
                    RotatedAudioBarGroup(self.circleX+self.radius*math.cos(math.radians(ang - 90)),
                                         self.circleY+self.radius*math.sin(math.radians(ang - 90)),
                                         category, (255, 0, 255), angle=ang, width=10,
                                         max_height=self.screen_height))
                ang += angle_dt
            self.bars.append(all_freq)
        
    def render(self, screen):
        avg_bass = 0
        poly = []

        t = pygame.time.get_ticks()
        time_interval = (t - self.last_frame) / 1000
        self.last_frame = t
        self.timeCount += time_interval

        for bar in self.bars:
            for bar_channel in bar:
                bar_channel.update_all(time_interval, pygame.mixer.music.get_pos() / 1000, self.analyzer)

        for bar_channel in self.bars[0]:
            avg_bass += bar_channel.avg

        avg_bass /= len(self.bars[0])
        polygon_color_vel = self.update_radius(avg_bass, time_interval)

        for x in range(len(polygon_color_vel)):
            value = polygon_color_vel[x]*time_interval + self.poly_color[x]
            self.poly_color[x] = value

        for bar in self.bars:
            for bar_channel in bar:
                bar_channel.x, bar_channel.y = (self.circleX+self.radius*math.cos(math.radians(bar_channel.angle - 90)),
                            self.circleY+self.radius*math.sin(math.radians(bar_channel.angle - 90)))
                bar_channel.update_rect()

                poly.append(bar_channel.rect.points[3])
                poly.append(bar_channel.rect.points[2])

        pygame.draw.polygon(screen, self.poly_color, poly)
        pygame.draw.circle(screen, self.circle_color, (self.circleX, self.circleY), int(self.radius))
    
    def update_radius(self, avg_bass, time_interval):
        if avg_bass > self.bass_trigger:
            if self.bass_trigger_started == 0:
                bass_trigger_started = pygame.time.get_ticks()
            if (pygame.time.get_ticks() - bass_trigger_started)/1000.0 > 2:
                self.polygon_bass_color = generate_color()
                bass_trigger_started = 0
            if self.polygon_bass_color is None:
                self.polygon_bass_color = generate_color()
            
            new_radius = int(avg_bass * ((self.max_radius - self.min_radius) / 
                                         (self.max_decibel - self.min_decibel))
                                         + (self.max_radius - self.min_radius))
            new_radius += self.min_radius
            self.radius_vel = (new_radius - self.radius) / UPDATE_RADIUS_SPEED

            polygon_color_vel = [(self.polygon_bass_color[x] - self.poly_color[x])/UPDATE_RADIUS_SPEED
                                 for x in range(len(self.poly_color))]

        elif self.radius > self.min_radius:
            self.bass_trigger_started = 0
            self.polygon_bass_color = None
            self.radius_vel = (self.min_radius - self.radius) / UPDATE_RADIUS_SPEED
            polygon_color_vel = [(self.polygon_default_color[x] - self.poly_color[x])/UPDATE_RADIUS_SPEED 
                                 for x in range(len(self.poly_color))]

        else:
            self.bass_trigger_started = 0
            self.poly_color = self.polygon_default_color.copy()
            self.polygon_bass_color = None
            polygon_color_vel = [0, 0, 0]

            self.radius_vel = 0
            self.radius = self.min_radius

        self.radius += self.radius_vel * time_interval
        return polygon_color_vel
