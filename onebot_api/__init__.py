from mcdreforged.plugin.server_interface import PluginServerInterface
from mcdreforged.command.command_source import CommandSource
from mcdreforged.command.builder.nodes.basic import Literal
from mcdreforged.api.decorator.new_thread import new_thread
from mcdreforged.command.builder.nodes.arguments import *
from mcdreforged.utils.serializer import Serializable

from onebot_api.constants import DEFAULT_CONFIG, PREFIX, HELP_MESSAGE, ID
from onebot_api.ws import OneBotAPI

api: OneBotAPI


class Config(Serializable):
    url: str


def on_load(server: PluginServerInterface, old):
    global api
    register_command(server)
    config = server.load_config_simple("onebot_api.json", DEFAULT_CONFIG, in_data_folder=False, target_class=Config)
    api = OneBotAPI(server.as_basic_server_interface(), config.url)
    api.start()


@new_thread
def on_unload(server: PluginServerInterface):
    api.stop()


def reload(src: CommandSource):
    server = src.get_server()
    server.logger.info("Reloading OneBot API...")
    src.reply("Reloading...")
    api.stop()
    server.reload_plugin(ID)


def register_command(server: PluginServerInterface):
    server.register_help_message("{} reload".format(PREFIX), HELP_MESSAGE.RELOAD)
    server.register_command(
        Literal(PREFIX)
        .then(
            Literal("reload")
            .runs(reload)
        )
    )
