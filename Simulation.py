import pygame
import Obstacle
from Settings import Settings
import Car
import Wall


class Simulation:

    def __init__(self, scenario):
        self.running = False
        self._display = None
        self.obstacles = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self._scenario = scenario
        self.settings = Settings("resources/Settings.yaml", self._scenario)
        self._size = self.settings.screen_sz
        self._start_pos = self.settings.start_pos
        self._goal_pos = self.settings.goal_pos
        self.car = None

    def setup(self):
        pygame.init()
        self.running = True
        self._display = pygame.display.set_mode(size=self._size)
        self.obstacles = Obstacle.ObstacleLoader(self, self._scenario).create_obstacles()
        self.car = Car.Car(self)
        self._create_walls()

    def on_render(self):
        self.obstacles.update()
        self.walls.update()
        self.car.update()
        self._display.fill((0, 0, 0))
        self.obstacles.draw(self._display)
        self.walls.draw(self._display)
        self._blit_start_goal()
        self.car.render()
        pygame.display.flip()

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        elif event.type == pygame.KEYDOWN:
            self._handle_keydown_events(event)
        elif event.type == pygame.KEYUP:
            self._handle_keyup_events(event)
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

    def _handle_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.car.ang_spd = -0.1
        elif event.key == pygame.K_LEFT:
            self.car.ang_spd = +0.1
        elif event.key == pygame.K_q:
            self.running = False

    def _handle_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.car.ang_spd = 0
        elif event.key == pygame.K_LEFT:
            self.car.ang_spd = 0

    def _create_walls(self):
        w, h = self._size
        wall_w = 5

        # walls vertical
        self.walls.add(Wall.Wall(self, 0, 0, wall_w, h))            # left
        self.walls.add(Wall.Wall(self, 0, 0, w, wall_w))            # top
        self.walls.add(Wall.Wall(self, w-wall_w, 0, wall_w, h))     # right
        self.walls.add(Wall.Wall(self, 0, h-wall_w, w, wall_w))     # bottom
