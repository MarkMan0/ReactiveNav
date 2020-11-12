import yaml


class Settings:

    def __init__(self, path_settings, path_scenario):
        """
        Given a path to settings.yaml and scenarion.yaml, reads the contents
        of the files and stores the internally
        :param path_settings: path to settings.yaml
        :param path_scenario: path to scenario.yaml
        """
        with open(path_settings) as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
        self.bg_color = data['bg_color']
        self.window_sz = data['window_sz']
        self.map_sz = data['map_sz']
        self.car_settings = data['car']
        self.cam_settings = data['camera']

        with open(path_scenario) as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
        self.start_pos = data['path']['start']
        self.goal_pos = data['path']['goal']
