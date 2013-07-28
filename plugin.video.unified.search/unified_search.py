import sys
import json
import urllib

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

        self.xpath = sys.argv[0]
        self.handle = int(sys.argv[1])

        self.supported_addons = self.get_supported_addons()
        self.debug = False

    def main(self):
        self.log("\nAddon: %s \nHandle: %s\nParams: %s " % (sys.argv[0], sys.argv[1], sys.argv[2]))

        params = common.getParameters(sys.argv[2])
        mode = params['mode'] if 'mode' in params else None
        keyword = params['keyword'] if 'keyword' in params else None

        url = params['url'] if 'url' in params else None
        plugin = params['plugin'] if 'plugin' in params else None

        if mode == 'search':
            self.search(keyword)
        if mode == 'reset':
            self.resetResults()
        if mode == 'play':
            self.play(plugin, url)
        elif mode is None:
            self.menu()

    def menu(self):
        self.log("Main menu")
        self.log("Supported add-ons: %s" % self.supported_addons)

        uri = self.xpath + '?mode=%s' % "search"
        item = xbmcgui.ListItem("Search for video", thumbnailImage=self.icon)
        xbmcplugin.addDirectoryItem(self.handle, uri, item, True)

        for i, item in enumerate(self.getSearchResults()):
            uri = '%s?mode=play&plugin=%s&url=%s' % (self.xpath, item['plugin'], item['url'])

            item = xbmcgui.ListItem("%s (%s)" % (item['title'], item['plugin']), thumbnailImage=item['image'])
            xbmcplugin.addDirectoryItem(self.handle, uri, item, False)

        item = xbmcgui.ListItem("Reset search results", thumbnailImage=self.icon)
        xbmcplugin.addDirectoryItem(self.handle, self.xpath + '?mode=reset', item, False)

        xbmcplugin.endOfDirectory(self.handle, True)

    def search(self, keyword):
        self.log("Call other add-ons and pass keyword: %s" % keyword)

        item = xbmcgui.ListItem("Please wait ...", thumbnailImage=self.icon)
        xbmcplugin.addDirectoryItem(self.handle, sys.argv[0], item, False)

        # Send keyword to supported add-ons
        for i, plugin in enumerate(self.supported_addons):
            script = "special://home/addons/%s/default.py" % plugin
            xbmc.executebuiltin("XBMC.RunScript(%s, %d, mode=unified_search&keyword=Drift)" % (script, self.handle))

        xbmcplugin.endOfDirectory(self.handle, True)

    def play(self, plugin, url):
        self.log("%s => %s" % (plugin, url))

        script = "special://home/addons/%s/default.py" % plugin
        xbmc.executebuiltin("XBMC.RunScript(%s, %d, mode=play&url=%s)" % (script, self.handle, urllib.quote(url)))

    def get_supported_addons(self):
        request = '{"jsonrpc": "2.0", "method": "Addons.GetAddons", "params": {"properties": ["summary"]}, "id": 1}'

        response = json.loads(xbmc.executeJSONRPC(request))["result"]["addons"]
        supported = []

        for i, addon in enumerate(response):
            try:
                if not 'pvr' in addon["addonid"] and xbmcaddon.Addon(addon["addonid"]).getSetting('unified_search') == 'true':
                    supported.append(addon["addonid"])
            except RuntimeError:
                pass

        return supported

    # RESULTS handling
    def collect(self, results):
        self.log("Save results to DB %s" % results)
        self.saveSearchResults(results)
        xbmc.executebuiltin("Container.Update(plugin://%s,replace)" % self.id)

    def getSearchResults(self):
        self.log("Get search results from storage")

        try:
            results = json.loads(self.addon.getSetting("results"))
            return results
        except ValueError:
            return []

    def saveSearchResults(self, item):
        self.log("Save search rsults in settings %s" % (item))

        try:
            results = self.getSearchResults()

            if not item in results:
                results.append(item)
                self.addon.setSetting("results", json.dumps(results))
        except Exception, e:
            self.error(e)

    def resetResults(self):
        print "Reset results"
        self.addon.setSetting("results", "")
        xbmc.executebuiltin("Container.refresh()")

    # Addon helpers
    def log(self, message):
        if self.debug:
            print "### %s: %s" % (self.id, message)

    def error(self, message):
        print "%s ERROR: %s" % (self.id, message)
