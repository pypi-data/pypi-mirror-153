from scrapeanything.scraper.scraper import Scraper

from requests_html import HTMLSession
import lxml.html
from lxml import etree

import logging

class RequestsHtml(Scraper):

    def on_wget(self, url):
        session = HTMLSession()
        r = session.get(url)

        logging.basicConfig() 
        logging.getLogger().setLevel(logging.CRITICAL)
        requests_log = logging.getLogger('requests.packages.urllib3')
        requests_log.setLevel(logging.CRITICAL)
        requests_log.propagate = True

        r.html.render(timeout=100)
        return r.html

    def on_xPath(self, element, path, prop=None):
        return element.xpath(path)

    def on_get_text(self, element):
        return element.text

    def on_get_html(self, element):
        return element.html

    def on_get_attribute(self, element, prop):
        return element.attrs[prop] if hasattr(element, 'attrs') else element.attrib[prop]

    def on_close(self):
        pass