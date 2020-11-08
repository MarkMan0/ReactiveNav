from pygame.sprite import Sprite
import pygame
import random
import yaml


class Wall(Sprite):

    def __init__(self, game, x: int, y: int, w: int, h: int):
        super().__init__()
        self.image = pygame.Surface((w, h), pygame.SRCALPHA)
        pygame.draw.rect(self.image, (255, 255, 255), pygame.Rect(0, 0, w, h), )
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
