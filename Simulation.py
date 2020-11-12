import pygame
import Obstacle
from Settings import Settings
import Car
import Wall
import math


class Simulation:

    def __init__(self, scenario: str, drawing: bool = False):
        """
        Creates a Simulation object. Doesn't initialize pygame
        The creation of a window can be disabled to speed up simulation
        :param scenario: path to scenario
        :param drawing: if True a pygame window is created and the simulation is drawn on it
        """
        self._drawing = drawing
        self.running = False
        self.window = None
        self.display = None
        self.obstacles = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self._scenario = scenario
        self.settings = Settings("resources/Settings.yaml", self._scenario)
        self.window_sz = self.settings.window_sz
        self.map_sz = self.settings.map_sz
        self._start_pos = self.settings.start_pos
        self._goal_pos = self.settings.goal_pos
        self.car = None
        self.result = False     # False - collision, True - goal
        self.camera = None

    def setup(self) -> None:
        """Initializes pygame and creates a window if needed"""
        pygame.init()
        self.running = True
        if self._drawing:
            self.window = pygame.display.set_mode(size=self.window_sz)
        self.display = pygame.Surface(self.map_sz)
        self.obstacles = Obstacle.ObstacleLoader(self._scenario).create_obstacles()
        self.car = Car.Car(self)
        self._create_walls()
        self.camera = Car.Camera(self)

    def on_render(self) -> None:
        """Updates all object witihin simulation and draws them"""
        self.obstacles.update()
        self.walls.update()
        self.car.update()
        self.camera.update_pos(int(self.car.x), int(self.car.y), self.car.orientation)

        self.display.fill((0, 0, 0))
        self.obstacles.draw(self.display)
        self.walls.draw(self.display)
        self._blit_start_goal()
        self.car.render()

        if self._drawing:
            self.window.fill((0, 0, 0))
            self.camera.render(self.window)
            rect = self.display.get_rect()
            rect.topleft = (0, 0)
            self.window.blit(self.display, rect)
            pygame.display.flip()

    def on_event(self, event) -> None:
        """Dispateches events"""
        if event.type == pygame.QUIT:
            self.running = False
        elif event.type == pygame.KEYDOWN:
            self._handle_keydown_events(event)
        elif event.type == pygame.KEYUP:
            self._handle_keyup_events(event)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self._handle_mouse_down(event)

    def cleanup(self) -> None:
        """Stops pygame"""
        pygame.quit()

    def tick(self) -> None:
        """Periodic calls, to progress the simulation"""
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

    def _blit_start_goal(self) -> None:
        """Draws start and goal positions"""
        pygame.draw.circle(self.display, (0, 255, 0), self._start_pos, 20)
        pygame.draw.circle(self.display, (0, 0, 255), self._goal_pos, 20)

    def _handle_mouse_down(self, event) -> None:
        """Prints the position of a mouse click, used to help create scenarios"""
        x, y = event.pos
        print(f"[{x}, {y}]")

    def _handle_keydown_events(self, event) -> None:
        """Used to manually drive the car, along with _handle_keyup_events"""
        if event.key == pygame.K_RIGHT:
            self.car.ang_spd = -0.1
        elif event.key == pygame.K_LEFT:
            self.car.ang_spd = +0.1
        elif event.key == pygame.K_q:
            self.running = False

    def _handle_keyup_events(self, event) -> None:
        """Used to manually drive the car, along with _handle_keydown_events"""
        if event.key == pygame.K_RIGHT:
            self.car.ang_spd = 0
        elif event.key == pygame.K_LEFT:
            self.car.ang_spd = 0

    def _create_walls(self) -> None:
        """Creates the walls for the simulation. The walls are positioned, so the camera is never off-screen"""
        off = max(self.settings.cam_settings['offset_y'], self.settings.cam_settings['offset_y'])
        off = math.sqrt(2 * off**2)
        space_x = self.settings.cam_settings['view_sz']/2 + off
        space_y = self.settings.cam_settings['view_sz']/2 + off

        w, h = self.map_sz
        x_min = space_x
        y_min = space_y
        wall_w = 5

        self.walls.add(Wall.Wall((x_min, y_min), wall_w, h))            # left
        self.walls.add(Wall.Wall((x_min, y_min), w, wall_w))            # top
        self.walls.add(Wall.Wall((w-wall_w, y_min), wall_w, h))     # right
        self.walls.add(Wall.Wall((x_min, h-wall_w), w, wall_w))     # bottom

    def _check_collision(self) -> bool:
        """Checks collision between car and obstacles and walls"""
        coll_wall = pygame.sprite.spritecollideany(self.car, self.walls) is not None
        coll_obs = pygame.sprite.spritecollideany(self.car, self.obstacles) is not None
        return coll_obs or coll_wall

    def _check_goal(self) -> bool:
        """checks if goal has been reached"""
        goal_x = self._goal_pos[0]
        goal_y = self._goal_pos[1]
        car_x = self.car.x
        car_y = self.car.y

        dist_to_goal = math.sqrt(math.pow(goal_x-car_x, 2) + math.pow(goal_y-car_y, 2))

        return dist_to_goal < 20
