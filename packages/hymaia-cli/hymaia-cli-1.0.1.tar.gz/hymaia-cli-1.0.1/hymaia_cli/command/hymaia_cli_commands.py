from hymaia_cli.command.command import Command
from hymaia_cli.command.command import ParametrizedCommand


class HymaiaCliCommands:
    why: Command = Command(name="why", url_parameter="why")
    manifest: Command = Command(name="manifest", url_parameter="manifest")
    contact: Command = Command(name="contact", url_parameter="contact")

    data_engineer: Command = Command(name="data_engineer", url_parameter="join/data-engineer")
    data_scientist: Command = Command(name="data_scientist", url_parameter="join/data-scientist")
    data_product_manager: Command = Command(name="data_product_manager", url_parameter="join/data-product-manager")
    data_strategist: Command = Command(name="data_strategist", url_parameter="join/data-strategist")
    join: ParametrizedCommand = ParametrizedCommand(name="join",
                                                    commands=[data_engineer, data_scientist, data_product_manager,
                                                              data_strategist], url_parameter="join")

    pragmatisme: Command = Command(name="pragmatisme", url_parameter="values/pragmatisme")
    integrite: Command = Command(name="integrite", url_parameter="values/integrite")
    passion: Command = Command(name="passion", url_parameter="values/passion")
    values: ParametrizedCommand = ParametrizedCommand(name="values", commands=[pragmatisme, integrite, passion],
                                                      url_parameter="values")
