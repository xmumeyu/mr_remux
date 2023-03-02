from mbot.core.params import ArgSchema, ArgType
from mbot.core.plugins import plugin, PluginCommandContext, PluginCommandResponse
from plugins.remux.main import Remux

from .event import event_var

@plugin.command(name='remux', title='手动制作remux', desc='', icon='', run_in_background=True)
def remux(
        ctx: PluginCommandContext,
        path: ArgSchema(ArgType.String, 'Bluray盘路径', '')):
    myremux = Remux(event_var)
    myremux.makeremux(path)
    return PluginCommandResponse(True, '')
