import yaml


class Settings:

    def __init__(self, path_settings, path_scenario):

        with open(path_settings) as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
        self.bg_color = data['bg_color']
        self.screen_sz = data['screen_sz']
        self.car_settings = data['car']
        self.cam_settings = data['camera']

        with open(path_scenario) as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
        self.start_pos = data['path']['start']
        self.goal_pos = data['path']['goal']
