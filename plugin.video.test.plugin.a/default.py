#!/usr/bin/python
# Writer (c) 2012, MrStealth
# Rev. 1.0.0
# -*- coding: utf-8 -*-

import os
import sys
import urllib

import xbmcplugin
import xbmcgui
import xbmcaddon
import XbmcHelpers
common = XbmcHelpers

# FIXME: Find a better way for module import
sys.path.append(os.path.join(os.path.dirname(__file__), "../plugin.video.unified.search"))
from unified_search import UnifiedSearch


class Plugin():
    def __init__(self):
        self.id = 'plugin.video.test.plugin.a'
        self.addon = xbmcaddon.Addon(self.id)
        self.icon = self.addon.getAddonInfo('icon')
        self.path = self.addon.getAddonInfo('path')
        self.profile = self.addon.getAddonInfo('profile')

        self.xpath = sys.argv[0]
        self.handle = int(sys.argv[1])

        self.debug = True

    def main(self):
        self.log("\nAddon: %s \nHandle: %s\nParams: %s " % (sys.argv[0], sys.argv[1], sys.argv[2]))

        params = common.getParameters(sys.argv[2])
        mode = params['mode'] if 'mode' in params else None
        url = urllib.unquote(params['url']) if 'url' in params else None
        keyword = params['keyword'] if 'keyword' in params else None

        if mode == 'unified_search':
            self.unified_search(keyword)
        if mode == 'play':
            self.play(url)
        elif mode is None:
            self.menu()

    def menu(self):
        self.log("*** Main menu")
        item = xbmcgui.ListItem("Main", thumbnailImage=self.icon)
        xbmcplugin.addDirectoryItem(self.handle, "", item, False)
        xbmcplugin.endOfDirectory(self.handle, True)

    def unified_search(self, keyword):
        self.log("Search for keyword and, call unified_search.collect() method")

        video = {
            "url": "http://techslides.com/demos/sample-videos/small.mp4",
            "image": "http://ftp.uni-erlangen.de/pub/rrze/tango/rrze-icon-set/tango/720x720/mime-types/audio-mp4.png",
            "title": "Sample video (%s) [MP4]" % self.addon.getAddonInfo('name'),
            "plugin": self.id
        }
        UnifiedSearch().collect(video)

    def play(self, url):
        self.log("xbmcplugin.setResolvedUrl(%d, %s)" % (self.handle, str(url)))

        item = xbmcgui.ListItem(path=url)
        xbmcplugin.setResolvedUrl(self.handle, True, item)
        xbmcplugin.endOfDirectory(self.handle, True)

    # *** Add-on helpers
    def log(self, message):
        if self.debug:
            print "*** %s: %s" % (self.id, message)

Plugin().main()
