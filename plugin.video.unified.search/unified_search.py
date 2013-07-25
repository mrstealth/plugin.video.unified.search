import os, sys, json
import xbmc
import xbmcplugin
import xbmcgui
import xbmcaddon

import XbmcHelpers
common = XbmcHelpers

import Translit as translit
translit = translit.Translit(encoding='cp1251')


class UnifiedSearch():
    def __init__(self):
        self.id = 'plugin.video.unified.search'
        self.addon = xbmcaddon.Addon(self.id)
        self.icon = self.addon.getAddonInfo('icon')
        self.path = self.addon.getAddonInfo('path')
        self.profile = self.addon.getAddonInfo('profile')
        self.handle = int(sys.argv[1])

        self.supported_addons = self.get_supported_addons()
        self.count = 0

    def main(self):
        params = common.getParameters(sys.argv[2])
        mode = params['mode'] if 'mode' in params else None
        query = params['query'] if 'query' in params else None
        results = params['results'] if 'results' in params else None

        if mode == 'search':
            self.search(query)
        if mode == 'collect':
            self.collect(results)
        elif mode is None:
            self.menu()

    def menu(self):
        print "*** UnifiedSearch: Main menu"
        
        uri = sys.argv[0] + '?mode=%s' % "search"
        item = xbmcgui.ListItem("Search for video", thumbnailImage=self.icon)
        xbmcplugin.addDirectoryItem(self.handle, uri, item, True)

        print self.supported_addons

        results =  self.getSearchResults()

        for i, item in enumerate(results):
            item = xbmcgui.ListItem("%s" % item, thumbnailImage=self.icon)
            xbmcplugin.addDirectoryItem(self.handle, "", item, False)

        xbmcplugin.endOfDirectory(self.handle, True)

    def search(self, query):
        print "*** UnifiedSearch: search: %s" % query

        item = xbmcgui.ListItem("Please wait ...", thumbnailImage=self.icon)
        xbmcplugin.addDirectoryItem(self.handle, sys.argv[0], item, False)

        # Send keyword to supported add-ons
        for i, addon in enumerate(self.supported_addons):
            script = "special://home/addons/%s/default.py" % addon
            xbmc.executebuiltin("XBMC.RunScript(%s, %d, mode=unified_search&query=Drift)" % (script, self.handle))
        
        xbmcplugin.endOfDirectory(self.handle, True)

    def collect(self, results):
        print "*** UnifiedSearch: save results to DB %s" % results

        self.saveSearchResults(results)
        xbmc.executebuiltin("Container.Update(plugin://%s,replace)" % self.id)            

    def getSearchResults(self):
        # self.resetResults()
        print "*** UnifiedSearch:  Get search results from storage"

        try: 
            results = json.loads(self.addon.getSetting("results"))
            return results
        except ValueError:
            return []

    def  saveSearchResults(self, item):
        print "*** UnifiedSearch: Save search rsults in settings %s" % (item)

        results = self.getSearchResults()
        
        if not item in results:
            results.append(item)
            self.addon.setSetting("results", json.dumps(results))

    def resetResults(self):
        print "Reset results"
        self.addon.setSetting("results", "")

    def get_supported_addons(self):
         request = '{"jsonrpc": "2.0", "method": "Addons.GetAddons", "params": {"properties": ["summary"]}, "id": 1}'
         response = json.loads(xbmc.executeJSONRPC(request))["result"]["addons"]
         supported = []

         for i, addon in enumerate(response):
            try:
                if not 'pvr' in  addon["addonid"] and xbmcaddon.Addon(addon["addonid"]).getSetting('unified_search') == 'true':
                    supported.append(addon["addonid"])
            except RuntimeError:
                pass

         return supported
