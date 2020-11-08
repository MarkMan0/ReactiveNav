from pygame.sprite import Sprite

import pygame
import math


class Car(Sprite):

    def __init__(self, game):

        super().__init__()
        self.screen = game.screen
        self.settings = game.settings
        self.screen_rect = game.screen.get_rect()
        self.orig_image = pygame.image.load('resources/car.png')
        self.image = self.orig_image

        self.rect = self.image.get_rect()

        self.rect.center = self.screen_rect.center

        self.orientation = 0.0

        self.turning_cw = False
        self.turning_ccw = False

        self.moving_fw = False

        self.lastX, self.lastY = self.rect.center

    def update(self, *args):

        if self.turning_cw:
            self.orientation -= self.settings.ship_ang_spd

        if self.turning_ccw:
            self.orientation += self.settings.ship_ang_spd

        self.image = pygame.transform.rotate(self.orig_image, self.orientation)

        self.rect = self.image.get_rect()

        if self.moving_fw:
            x_spd = math.cos(math.radians(self.orientation + 90)) * self.settings.ship_spd
            y_spd = -math.sin(math.radians(self.orientation + 90)) * self.settings.ship_spd

            self.lastX += x_spd
            self.lastY += y_spd

        self.rect.center = (int(self.lastX), int(self.lastY))

        if self.rect.right > self.screen_rect.right:
            self.rect.right = self.screen_rect.right

        if self.rect.bottom > self.screen_rect.bottom:
            self.rect.bottom = self.screen_rect.bottom

        if self.rect.left < 0:
            self.rect.left = 0

        if self.rect.top < 0:
            self.rect.top = 0

    def render(self):
        self.screen.blit(self.image, self.rect)
