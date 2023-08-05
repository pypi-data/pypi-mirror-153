import pathlib

import pkg_resources

from mopidy import config, ext
from tornado import locale

__version__ = pkg_resources.get_distribution(
    "Mopidy-MusicBox-Darkclient"
).version


class Extension(ext.Extension):

    dist_name = "Mopidy-MusicBox-Darkclient"
    ext_name = "musicbox_darkclient"
    version = __version__

    def get_default_config(self):
        return config.read(pathlib.Path(__file__).parent / "ext.conf")

    def get_config_schema(self):
        schema = super().get_config_schema()
        schema["musicbox"] = config.Boolean(optional=True)
        schema["locale"] = config.String(optional=True, choices=["en","ru"])
        schema["websocket_host"] = config.Hostname(optional=True)
        schema["websocket_port"] = config.Port(optional=True)
        schema["on_track_click"] = config.String(
            optional=True,
            choices=[
                "PLAY_NOW",
                "PLAY_NEXT",
                "ADD_THIS_BOTTOM",
                "ADD_ALL_BOTTOM",
                "PLAY_ALL",
                "DYNAMIC",
            ],
        )
        return schema

    def setup(self, registry):
        locale.load_gettext_translations(pathlib.Path(__file__).parent / 'locale', 'messages')
        registry.add(
            "http:app", {"name": self.ext_name, "factory": self.factory}
        )

    def factory(self, config, core):
        from tornado.web import RedirectHandler
        from .web import IndexHandler, StaticHandler, LikeHandler

        path = pathlib.Path(__file__).parent / "static"
        return [
            (r"/", RedirectHandler, {"url": "index.html"}),
            (r"/(index.html)", IndexHandler, {"config": config, "path": path}),
            (r"/(liked:.*)", LikeHandler, {"core": core}),
            (r"/(.*)", StaticHandler, {"path": path}),
        ]
