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

        x_spd = math.cos(math.radians(self.orientation + 90)) * self.speed
        y_spd = -math.sin(math.radians(self.orientation + 90)) * self.speed

        self.x += x_spd
        self.y += y_spd

        self.rect.center = (int(self.x), int(self.y))

    def render(self):
        self.screen.blit(self.image, self.rect)


class Camera(Sprite):

    def __init__(self, game):

        super().__init__()
        self.screen = game._display
        self.settings = game.settings
        self.view_sz = self.settings.cam_view_sz
        self.line_w = 3
        sz = self.view_sz + 2*self.line_w
        self.orig_img = pygame.Surface((sz, sz), pygame.SRCALPHA)
        pygame.draw.rect(self.orig_img, (255, 255, 255), pygame.Rect(0, 0, sz, sz), self.line_w)

        self.image = self.orig_img.copy()
        self.rect = self.image.get_rect()
        self.rect.center = self.settings.start_pos
        self.rotation = 0

    def update_pos(self, x, y, rot):
        self.rotation = rot
        self.image = pygame.transform.rotate(self.orig_img, rot)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def render(self):
        self.screen.blit(self.image, self.rect)

    def get_cam_view(self):

        arr = pygame.PixelArray(self.screen)
        x = self.rect.center[0]
        y = self.rect.center[1]
        x_max, y_max = self.screen.get_size()
        x = int(x + self.view_sz/2 * math.cos(math.radians(-self.rotation)))
        y = int(y + self.view_sz/2 * math.sin(math.radians(-self.rotation)))

        x = max(x, 0)
        y = max(y, 0)
        x = min(x, x_max)
        y = min(y, y_max)

        print(arr[x, y])
        arr.close()
