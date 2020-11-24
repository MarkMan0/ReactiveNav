from pygame.sprite import Sprite
import pygame
import random
import yaml


class Obstacle(Sprite):

    def __init__(self, x: int = -1, y: int = -1, sz: tuple = (100, 100)):
        """
        Obstacle is a white rectangle, with position and size
        :param x: if -1, x position is random
        :param y: if -1, y position is random
        :param sz: size of obstacle
        """
        super().__init__()
        self.image = pygame.Surface(sz, pygame.SRCALPHA)
        pygame.draw.rect(self.image, (255, 255, 255), pygame.Rect(0, 0, sz[0], sz[1]))
        self.rect = self.image.get_rect()

        if x != -1 and y != -1:
            self.x = x
            self.y = y
        else:
            self.x = random.uniform(0, self.rect.size[0])
            self.y = random.uniform(0, self.rect.size[1])

    def update(self, *args):
        self.rect.center = (int(self.x), int(self.y))
        return super().update(*args)


class ObstacleLoader:
    """Loads obstacles from yaml file"""

    def __init__(self, path: str):
        self._conf_path = path
        with open(self._conf_path) as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
        self.positions = data['obstacles']

    def create_obstacles(self) -> pygame.sprite.Group:
        """Creates obstacle objects"""
        obstacles = pygame.sprite.Group()
        for pos in self.positions:
            obstacles.add(Obstacle(pos[0], pos[1], (pos[2], pos[3])))

        return obstacles
