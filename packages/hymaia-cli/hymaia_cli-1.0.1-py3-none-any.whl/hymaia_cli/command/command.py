import os
import configparser


class Command:

    def __init__(self, name: str, url_parameter: str):
        self.name: str = name
        self.url_parameter: str = url_parameter
        self.url: str = Command.get_base_url() + self.url_parameter

    def get_url_with_parameter(self):
        return self.get_base_url(), self.url_parameter

    @staticmethod
    def get_base_url(config_path: str = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'resources/config.ini')) -> str:
        config = configparser.ConfigParser()
        config.read(config_path)
        base_url = config['aws.api-gateway']['url']
        return base_url


class ParametrizedCommand(Command):
    def __init__(self, commands, url_parameter, name):
        super().__init__(name, url_parameter)
        self.commands: list[Command] = commands

    def get_commands(self):
        return self.commands
