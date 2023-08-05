*****************************
Mopidy-MusicBox-Darkclient
*****************************

Mopidy MusicBox Webclient (MMW) is a frontend extension and JavaScript-based web client especially
written for Mopidy

Darkclient is dark theme for MMW. Can be used as standalone Mopidy plugin without upstream MMW.

Features
========

- Responsive design that works equally well on desktop and mobile browsers.
- Browse content backend extension.
- Add one or more tracks or entire albums to the queue.
- Search for tracks, albums, or artists.
- Shows detailed track and album information in playlists and queue with album covers.
- Artwork and Like extensions
- Support for all of the Mopidy playback controls (consume mode, repeat, shuffle, etc.)
- Fullscreen mode.
- Multilanguage support

.. image:: https://github.com/stffart/mopidy-musicbox-darkclient/raw/develop/screenshots/overview.png
   :height: 425 px
   :width: 762 px
   :align: center

Dependencies
============

- MMW has been tested on the major browsers (Chrome, IE, Firefox, Safari, iOS). It *may* also work on other browsers
  that support websockets, cookies, and JavaScript.

- ``Mopidy`` >= 3.0.0. An extensible music server that plays music from local disk, Spotify, SoundCloud, Google
  Play Music, and more.

Installation
============

Install by running::

    sudo python3 -m pip install Mopidy-MusicBox-Darkclient

Or, if available, install the Debian/Ubuntu package from
`apt.mopidy.com <https://apt.mopidy.com/>`_.


Configuration
=============

MMW is shipped with default settings that should work straight out of the box for most users::

    [musicbox_darkclient]
    enabled = true
    musicbox = false
    websocket_host =
    websocket_port =
    on_track_click = PLAY_ALL
    locale = en

The following configuration values are available should you wish to customize your installation further:

- ``musicbox_darkclient/enabled``: If the MMW extension should be enabled or not. Defaults to ``true``.

- ``musicbox_darkclient/musicbox``: Set this to ``true`` if you are connecting to a Mopidy instance running on a
  Pi Musicbox. Expands the MMW user interface to include system control/configuration functionality.

- ``musicbox_darkclient/websocket_host``: Optional setting to specify the target host for Mopidy websocket connections.

- ``musicbox_darkclient/websocket_port``: Optional setting to specify the target port for Mopidy websocket connections.

- ``musicbox_darkclient/on_track_click``: The action performed when clicking on a track. Valid options are:
  ``PLAY_ALL`` (default), ``PLAY_NOW``, ``PLAY_NEXT``, ``ADD_THIS_BOTTOM``, ``ADD_ALL_BOTTOM``, and ``DYNAMIC`` (repeats last action).

- ``musicbox_darkclient/locale``: Optional setting to specify user interface language.


Usage
=====

Enter the address of the Mopidy server that you are connecting to in your browser (e.g. http://localhost:6680/musicbox_darkclient)

Credits
=======

- Original author: `Wouter van Wijk <https://github.com/woutervanwijk>`__
- `Contributors <https://github.com/pimusicbox/mopidy-musicbox-webclient/graphs/contributors>`_
