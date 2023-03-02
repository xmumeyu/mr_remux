from typing import Dict, Any
from mbot.core.plugins import plugin, PluginMeta, PluginContext
from mbot.openapi import mbot_api
from plugins.remux.logger import Logger
import json
from plugins.remux.main import Remux


class event_var:

    def __init__(self):
        self.outpath = None
        self.simple_mode = True
        self.dv_enable = True


event_var = event_var()

@plugin.after_setup
def after_setup(plugin_meta: PluginMeta, config: Dict[str, Any]):
    mbot_api.auth.add_permission([1, 2], '/api/plugins/remux')
    mbot_api.auth.add_permission([1, 2], '/api/plugins/remux/tmp')
    event_var.outpath = config.get('outpath')
    event_var.simple_mode = config.get('simple_mode')
    event_var.dv_enable = config.get('dv_enable')
    Logger.info(config)


@plugin.config_changed
def config_changed(config: Dict[str, Any]):
    event_var.outpath = config.get('outpath')
    event_var.simple_mode = config.get('simple_mode')
    event_var.dv_enable = config.get('dv_enable')
    Logger.info(config)


@plugin.on_event(bind_event=['DownloadCompleted'], order=1)
def on_bluraydown_complete(ctx: PluginContext, event_type: str, data: Dict):
    Logger.info(json.dumps(data))
    if data['media_type'] == 'Movie' and data['media_stream']['media_source'] == 'Blu-ray':
        myremux = Remux(event_var)
        myremux.makeremux(data['source_path'])

