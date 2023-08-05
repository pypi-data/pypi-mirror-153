import json
import logging
import socket
import string
import urllib.parse

import tornado.web
import tornado.locale

import mopidy_musicbox_darkclient.webclient as mmw

logger = logging.getLogger(__name__)
import json
import urllib.parse



class StaticHandler(tornado.web.StaticFileHandler):
    def get(self, path, *args, **kwargs):
        version = self.get_argument("v", None)
        if version:
            logger.debug("Get static resource for %s?v=%s", path, version)
        else:
            logger.debug("Get static resource for %s", path)
        return super().get(path, *args, **kwargs)

    @classmethod
    def get_version(cls, settings, path):
        return mmw.Extension.version


class IndexHandler(tornado.web.RequestHandler):
    def initialize(self, config, path):

        webclient = mmw.DarkWebclient(config)

        self.locale_name = webclient.locale()

        if webclient.is_music_box():
            program_name = "MusicBox"
        else:
            program_name = "Mopidy"

        url = urllib.parse.urlparse(
            f"{self.request.protocol}://{self.request.host}"
        )
        port = url.port or 80
        try:
            ip = socket.getaddrinfo(url.hostname, port)[0][4][0]
        except Exception:
            ip = url.hostname

        self.__dict = {
            "isMusicBox": json.dumps(webclient.is_music_box()),
            "locale": self.locale_name,
            "websocketUrl": webclient.get_websocket_url(self.request),
            "hasAlarmClock": json.dumps(webclient.has_alarm_clock()),
            "hasMarket": json.dumps(webclient.has_market()),
            "onTrackClick": webclient.get_default_click_action(),
            "programName": program_name,
            "hostname": url.hostname,
            "serverIP": ip,
            "serverPort": port,
        }
        self.__path = path
        self.__title = string.Template(f"{program_name} on $hostname")

    def get_user_locale(self):
        return tornado.locale.get(self.locale_name)

    def get(self, path):
        return self.render(path, title=self.get_title(), **self.__dict)

    def get_title(self):
        url = urllib.parse.urlparse(
            f"{self.request.protocol}://{self.request.host}"
        )
        return self.__title.safe_substitute(hostname=url.hostname)

    def get_template_path(self):
        return self.__path

class LikeHandler(tornado.web.RequestHandler):

    def initialize(self, core):
        self._core = core

    def get(self, path):
      logger.error(path)
      if 'liked:' in path:
        params = path.split(':')
        liked = params[1]
        uri_scheme = params[2]
        track_id = params[4]
        uri = f"{uri_scheme}:track:{track_id}"
        logger.error(uri)
        tl_tracks = self._core.tracklist.filter({"uri": [uri]}).get()
        if len(tl_tracks) == 0:
            tl_track = self._core.playback.get_current_tl_track().get()
            if uri in tl_track.track.uri:
                tl_tracks = [tl_track]
        position = self._core.tracklist.index(tl_tracks[0]).get()
        #replacing track in current playback with liked one
        #mopidy has not method for this, so we need to delete old one, create new on the same position
        if hasattr(tl_tracks[0].track,'switchLike'):
          switched = tl_tracks[0].track.switchLike()
          self._core.tracklist.remove({"tlid": [tl_tracks[0].tlid] })
          self._core.tracklist.add(tracks=[switched],at_position=position)
          tl_tracks = self._core.tracklist.filter({"uri": [uri]}).get()
          #We need to call private method to set current track to replaced one
          self._core._actor.playback._set_current_tl_track(tl_tracks[0])
          self._core.playlists.create(path, uri_scheme).get()
          self.write(json.dumps({'result':True,'message':'ok'}))
        else:
          self.write(json.dumps({'result':False,'message':'Not likable'}))
      else:
        self.write(json.dumps({'result':False,'message':'Not found'}))
