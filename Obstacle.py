from cgi import parse

from pygame.sprite import Sprite
import pygame
import random
import yaml


class Obstacle(Sprite):

    def __init__(self, game, x=-1, y=-1, sz=100):
        super().__init__()
        self.image = pygame.Surface((sz, sz), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 255, 255), (int(sz/2), int(sz/2)), int(sz/2))
        self.rect = self.image.get_rect()

        if x != -1 and y != -1:
            self.x = x
            self.y = y
        else:
            self._get_initial_pos()

    def _get_initial_pos(self):
        """ Initial position is random on the screen """
        self.x = random.uniform(0, self.rect.size[0])
        self.y = random.uniform(0, self.rect.size[1])

    def update(self, *args):
        self.rect.center = (int(self.x), int(self.y))
        return super().update(*args)


class ObstacleLoader:
    """Loads obstacles from yaml file"""

    def __init__(self, game, path):
        self._game = game
        self._conf_path = path
        with open(self._conf_path) as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
        self.positions = data['obstacles']

    def create_obstacles(self):
        """Creates static obstacle objects"""
        obstacles = pygame.sprite.Group()
        for pos in self.positions:
            obstacles.add(Obstacle(self._game, pos[0], pos[1], pos[2]))

        return obstacles
