import yaml

class Config(object):

    @staticmethod
    def load():
        with open('configs/config.yml', 'r') as config:
            return yaml.load(config)
