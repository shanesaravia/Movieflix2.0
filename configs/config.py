import yaml

class Config(object):

    @staticmethod
    def load(config_file='config.yml'):
        with open('configs/{}'.format(config_file), 'r') as config:
            return yaml.load(config)
