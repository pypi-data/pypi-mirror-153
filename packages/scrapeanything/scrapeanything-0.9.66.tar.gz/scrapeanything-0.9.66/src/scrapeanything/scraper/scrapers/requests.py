from scrapeanything.scraper.scraper import Scraper

import requests
import lxml.html
from lxml import etree

class Requests(Scraper):

    def on_wget(self, url):
        headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36' }
        page = requests.get(url, headers=headers, verify=True, proxies=None)
        if page.content == b'':
            raise Exception()

        return lxml.html.fromstring(page.content)

    def on_xPath(self, element, path, prop=None):
        return element.xpath(path)

    def on_get_text(self, element):
        return element.text_content()

    def on_get_html(self, element):
        return etree.tostring(element, pretty_print=True)

    def on_get_attribute(self, element, prop):
        return element.get(prop)

    def on_get_css(self, element, prop):
        pass

    def on_close(self):
        pass