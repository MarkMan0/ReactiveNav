import pygame
import Obstacle
from Settings import Settings


class Simulation:

    def __init__(self, scenario):
        self.running = False
        self._display = None
        self.obstacles = pygame.sprite.Group()
        self._scenario = scenario
        self.settings = Settings("resources/Settings.yaml", self._scenario)
        self._size = self.settings.screen_sz
        self._start_pos = self.settings.start_pos
        self._goal_pos = self.settings.goal_pos

    def setup(self):
        pygame.init()
        self.running = True
        self._display = pygame.display.set_mode(size=self._size)
        self.obstacles = Obstacle.ObstacleLoader(self, self._scenario).create_obstacles()

    def on_render(self):
        self.obstacles.update()
        self._display.fill((0, 0, 0))
        self.obstacles.draw(self._display)
        self._blit_start_goal()
        pygame.display.flip()

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self._handle_mouse_down(event)

    def cleanup(self):
        pygame.quit()


    def tick(self):
        for event in pygame.event.get():
            self.on_event(event)
        self.on_render()

    def _blit_start_goal(self):
        pygame.draw.circle(self._display, (0, 255, 0), self._start_pos, 20)
        pygame.draw.circle(self._display, (0, 0, 255), self._goal_pos, 20)

    def _handle_mouse_down(self, event):
        x, y = event.pos
        print(f"[{x}, {y}]")
