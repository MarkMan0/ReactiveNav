from pygame.sprite import Sprite
import pygame
import math
import numpy


class Car(Sprite):

    def __init__(self, simulation):
        """
        Creates a car object, which is a circle
        The car has a constant speed, it's direction can be altered using the ang_spd member variable
        :param simulation: the Simulation object
        """
        super().__init__()
        self.screen = simulation.display
        self.settings = simulation.settings
        sz = self.settings.car_settings['size']
        self.orig_img = pygame.Surface((sz, sz), pygame.SRCALPHA)
        pygame.draw.circle(self.orig_img, (255, 0, 0), (int(sz/2), int(sz/2)), int(sz/2))
        pygame.draw.circle(self.orig_img, (0, 0, 255), (int(sz/2), int(sz*1/3)), (int(sz/3)))

        self.image = self.orig_img.copy()
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

    def render(self) -> None:
        self.image = pygame.transform.rotate(self.orig_img, self.orientation)
        self.rect = self.image.get_rect()
        self.rect.center = (int(self.x), int(self.y))
        self.screen.blit(self.image, self.rect)


class Camera(Sprite):

    def __init__(self, game):
        """
        Camera used to watch a rectangle around a given point
        The camera's size and offset from the pivot is defined in the .yaml file
        :param game: Simulation object
        """
        super().__init__()
        self.screen = game.display
        self.settings = game.settings
        self.view_sz = self.settings.cam_settings['view_sz']
        self.line_w = 3
        sz = self.view_sz + 2*self.line_w
        self.orig_img = pygame.Surface((sz, sz), pygame.SRCALPHA)
        pygame.draw.rect(self.orig_img, (255, 255, 255), pygame.Rect(0, 0, sz, sz), self.line_w)

        self.image = self.orig_img.copy()
        self.rect = self.image.get_rect()
        self.rect.center = self.settings.start_pos
        self.rotation = 0
        self.cam_view = None

    def update_pos(self, x: float, y: float, rot: float) -> None:
        """
        Updates the position of the camera
        :param x: x position of pivot(car)
        :param y: y position of pivot(car)
        :param rot: orientation of pivot(car)
        :return:
        """
        self.rotation = rot
        self.rect = self.image.get_rect()
        x_off = self.settings.cam_settings['offset_x']
        y_off = self.settings.cam_settings['offset_y']

        r = math.sqrt(x_off**2 + y_off**2)

        dx = r*math.cos(math.radians(-self.rotation-90))
        dy = r*math.sin(math.radians(self.rotation-90))
        x += dx
        y += dy
        self.rect.center = (int(x), int(y))

        self._update_cam()

    def _update_cam(self):
        """Updates the camera's view"""
        x, y = self.rect.center
        cam_sz = self.view_sz / 2
        x_min = int(x - cam_sz)
        y_min = int(y - cam_sz)
        x_max = int(x + cam_sz)
        y_max = int(y + cam_sz)

        # get pixels of camera view
        arr = pygame.PixelArray(self.screen)
        arr2 = arr[x_min:x_max, y_min:y_max]
        arr.close()
        # convert to surface
        surf = arr2.make_surface()
        arr2.close()
        # rotate surface so car is always pointing in upward direction
        surf.set_colorkey(pygame.Color(0))
        surf = pygame.transform.rotate(surf, -self.rotation)
        x, y = surf.get_rect().center
        x_min = int(x - cam_sz)
        y_min = int(y - cam_sz)
        w = self.view_sz
        h = self.view_sz
        self.cam_view = pygame.Surface((self.view_sz, self.view_sz))
        self.cam_view.blit(surf, (0, 0), (x_min, y_min, w, h))

    def render(self, window) -> None:
        rect = self.cam_view.get_rect()
        rect.topright = (self.settings.window_sz[0], 0)
        self.screen.blit(self.image, self.rect)
        window.blit(self.cam_view, rect)

    def get_cam_arr(self) -> numpy.array:
        """
        Returns a numpy array of the camera's view
        :return: numpy.array
        """
        np_arr = pygame.surfarray.array2d(self.cam_view)
        threshold = 16777210  # white
        np_arr[np_arr < threshold] = 0  # ignore non-white pixels
        return np_arr
