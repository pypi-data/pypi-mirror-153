import argparse

from hymaia_cli.command.hymaia_cli_commands import HymaiaCliCommands


class VerboseStore(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if not values:
            for command in getattr(HymaiaCliCommands(), self.dest).get_commands():
                print(command.name, sep="\n")
        else:
            setattr(namespace, self.dest, values)
