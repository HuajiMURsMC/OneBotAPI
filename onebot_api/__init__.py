from mcdreforged.api.types import PluginServerInterface, CommandSource
from mcdreforged.api.decorator.new_thread import new_thread
from mcdreforged.api.command import *

from onebot_api.constants import PREFIX, HELP_MESSAGE, ID, CONFIG, CONFIG_FILE
from onebot_api.ws import OneBotAPI

api: OneBotAPI


def on_load(server: PluginServerInterface, old):
    global api
    register_command(server)
    config = server.load_config_simple(
        CONFIG_FILE, in_data_folder=False, target_class=CONFIG
    )
    api = OneBotAPI(server.as_basic_server_interface(), config.url, config.access_token)
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
    server.register_command(Literal(PREFIX).then(Literal("reload").runs(reload)))
