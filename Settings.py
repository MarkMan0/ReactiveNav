import yaml


class Settings:

    def __init__(self, path_scenario):
        """
        Given a path to settings.yaml and scenarion.yaml, reads the contents
        of the files and stores the internally
        :param path_settings: path to settings.yaml
        :param path_scenario: path to scenario.yaml
        """
        with open(path_scenario) as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
        self.window_sz = data['window_sz']
        self.car_settings = data['car']
        self.cam_settings = data['camera']

        self.start_pos = data['path']['start']
        self.goal_pos = data['path']['goal']
        self.map_sz = data['map_sz']

        if self.window_sz[0] < (self.map_sz[0] + 1.5*self.cam_settings['view_sz']):
            raise ValueError("width of window shouldn't be less than map_sz[1] + 1.5*camera.view_sz")
        if self.window_sz[1] < (self.map_sz[1] + 0.5*self.cam_settings['view_sz']):
            raise ValueError("height of window shouldn't be less than map_sz[1] + 0.5*camera.view_sz")