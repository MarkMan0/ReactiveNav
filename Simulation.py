import pygame
import Obstacle
from Settings import Settings
import Car
import Wall
import math


class Simulation:

    def __init__(self, scenario, drawing=False):
        self._drawing = drawing
        self.running = False
        self.window = None
        self.display = None
        self.obstacles = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self._scenario = scenario
        self.settings = Settings("resources/Settings.yaml", self._scenario)
        self._size = self.settings.screen_sz
        self._start_pos = self.settings.start_pos
        self._goal_pos = self.settings.goal_pos
        self.car = None
        self.result = False     # False - collision, True - goal
        self.camera = None

    def setup(self):
        pygame.init()
        self.running = True
        if self._drawing:
            self.window = pygame.display.set_mode(size=self._size)
        self.display = pygame.Surface(self._size)
        self.obstacles = Obstacle.ObstacleLoader(self, self._scenario).create_obstacles()
        self.car = Car.Car(self)
        self._create_walls()
        self.camera = Car.Camera(self)

    def on_render(self):
        self.obstacles.update()
        self.walls.update()
        self.car.update()
        self.camera.update_pos(int(self.car.x), int(self.car.y), self.car.orientation)

        self.display.fill((0, 0, 0))
        self.obstacles.draw(self.display)
        self.walls.draw(self.display)
        self._blit_start_goal()
        self.car.render()
        self.camera.render()

        if self._drawing:
            rect = self.display.get_rect()
            rect.topleft = (0, 0)
            self.window.blit(self.display, rect)
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
        collision = self._check_collision()
        goal = self._check_goal()
        if collision:
            self.running = False
            self.result = False
        if goal:
            self.running = False
            self.result = True

        self.on_render()

    def _blit_start_goal(self):
        pygame.draw.circle(self.display, (0, 255, 0), self._start_pos, 20)
        pygame.draw.circle(self.display, (0, 0, 255), self._goal_pos, 20)

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

        off = max(self.settings.cam_settings['offset_y'], self.settings.cam_settings['offset_y'])
        off = math.sqrt(2 * off**2)
        space_x = self.settings.cam_settings['view_sz']/2 + off
        space_y = self.settings.cam_settings['view_sz']/2 + off

        width, height = self._size
        w = width - 2*space_x
        h = height - 2*space_y
        x_min = space_x
        y_min = space_y
        wall_w = 5

        # walls vertical
        self.walls.add(Wall.Wall(self, x_min, y_min, wall_w, h))            # left
        self.walls.add(Wall.Wall(self, x_min, y_min, w, wall_w))            # top
        self.walls.add(Wall.Wall(self, width-wall_w - space_x, y_min, wall_w, h))     # right
        self.walls.add(Wall.Wall(self, x_min, height-wall_w-space_y, w, wall_w))     # bottom

    def _check_collision(self):
        coll_wall = pygame.sprite.spritecollideany(self.car, self.walls) is not None
        coll_obs = pygame.sprite.spritecollideany(self.car, self.obstacles) is not None
        return coll_obs or coll_wall

    def _check_goal(self):
        goal_x = self._goal_pos[0]
        goal_y = self._goal_pos[1]
        car_x = self.car.x
        car_y = self.car.y

        dist_to_goal = math.sqrt(math.pow(goal_x-car_x, 2) + math.pow(goal_y-car_y, 2))

        return dist_to_goal < 20
