#!/usr/bin/python
# Writer (c) 2012, MrStealth
# Rev. 1.0.6
# -*- coding: utf-8 -*-

import sys
import xbmc
import xbmcplugin
import xbmcgui
import xbmcaddon
import XbmcHelpers
common = XbmcHelpers

class Plugin():
    def __init__(self):
        self.id = 'plugin.video.test.plugin.a'
        self.addon = xbmcaddon.Addon(self.id)
        self.icon = self.addon.getAddonInfo('icon')
        self.path = self.addon.getAddonInfo('path')
        self.profile = self.addon.getAddonInfo('profile')
        self.handle = int(sys.argv[1])

    def main(self):
        print "PluginTest: handle %s params %s " % (sys.argv[1], sys.argv[2])

        params = common.getParameters(sys.argv[2])
        mode = params['mode'] if 'mode' in params else None
        query = params['query'] if 'query' in params else None

        if mode == 'unified_search':
            self.unified_search(query)
        elif mode is None:
            self.menu()

    def menu(self):
        print "*** %s: Main menu" % self.id
        item = xbmcgui.ListItem("Main", thumbnailImage=self.icon)
        xbmcplugin.addDirectoryItem(self.handle, "", item, False)
        xbmcplugin.endOfDirectory(self.handle, True)

    def unified_search(self, query):
        print "search"
        results = 'results from - %s' % self.id
        plugin = "special://home/addons/plugin.video.unified.search/default.py"
        xbmc.executebuiltin("XBMC.RunScript(%s, %d, mode=collect&results=%s)" % (plugin, self.handle, results))

Plugin().main()
