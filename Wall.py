from pygame.sprite import Sprite
import pygame


class Wall(Sprite):

    def __init__(self, top_left: tuple, w: int, h: int):
        """
        Creates a wall as rectangle
        :param top_left: tuple of ints
        :param w: width of wall
        :param h: height of wall
        """
        super().__init__()
        self.image = pygame.Surface((w, h), pygame.SRCALPHA)
        pygame.draw.rect(self.image, (255, 255, 255), pygame.Rect(0, 0, w, h), )
        self.rect = self.image.get_rect()
        self.rect.topleft = top_left
