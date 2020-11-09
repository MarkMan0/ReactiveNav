from pygame.sprite import Sprite

import pygame
import math


class Car(Sprite):

    def __init__(self, game):

        super().__init__()
        self.screen = game._display
        self.settings = game.settings
        sz = self.settings.car_settings['size']
        self.image = pygame.Surface((sz, sz), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 0, 0), (int(sz/2), int(sz/2)), int(sz/2))
        self.rect = self.image.get_rect()

        self.rect.center = self.settings.start_pos

        self.orientation = 0.0
        self.speed = self.settings.car_settings['speed']

        self.ang_spd = 0.0

        self.x, self.y = self.rect.center

    def update(self, *args):

        self.orientation += self.ang_spd

        self.rect = self.image.get_rect()

        x_spd = math.cos(math.radians(self.orientation + 90)) * 0.1
        y_spd = -math.sin(math.radians(self.orientation + 90)) * 0.1

        self.x += x_spd
        self.y += y_spd

        self.rect.center = (int(self.x), int(self.y))

    def render(self):
        self.screen.blit(self.image, self.rect)
