import time
import re
import json
from twisted.internet import reactor
import scrapy
import scrapy.crawler
import scrapy.utils.log
import scrapy.spiderloader
import scrapy.statscollectors
import scrapy.logformatter
import scrapy.extensions
import scrapy.extensions.corestats
import scrapy.extensions.telnet
import scrapy.extensions.memusage
import scrapy.extensions.memdebug
import scrapy.extensions.logstats
import scrapy.extensions.closespider
import scrapy.extensions.feedexport
import scrapy.extensions.spiderstate
import scrapy.extensions.throttle

class FromSitemap(scrapy.Spider):
    """A scraper which acts like webscraper.io
    Takes one sitemap and one url
    Creates a filled in Questionnaire
    """
    result = []
    def __init__(self, sitemap: str or dict, origin=None, find=None, csv=None):
        if type(sitemap) == str:
            with open(sitemap) as json_data:
                sitemap = json.load(json_data)
        self.sitemap = sitemap
        self.origin = origin
        self.name = sitemap["_id"]
        self.start_urls = [sitemap["startUrl"]]
        self.questionnaire = {}
        self.questionnaire["website"] = sitemap["startUrl"]

    def parse(self, response):
        global result
        for selector in self.sitemap["selectors"]:  # go through each selector
            if selector.get("selector"):
                for item in response.css(selector["selector"]):

                    delay = selector.get("delay")  # if delay specified
                    if delay:
                        time.sleep(delay)

                    if selector.get("type") == "SelectorText":  # if the selection should be text
                        text = ', '.join([sent.strip() for sent in item.css('::text').extract() if not sent.isspace()])

                        # Text results can be parsed further with regex
                        regex = selector.get("regex")
                        if regex:
                            #pattern = re.compile(sel_regex)
                            try:
                                text = re.findall(regex, text)[0]
                            except IndexError:
                                pass

                        self.questionnaire[selector["id"]] = text

    def close(self, reason):
        if self.origin:
            self.origin(reason)


class FromURL(scrapy.Spider):
    """A scraper for creating site maps
    Takes one sitemap and one url
    Creates a sitemap
    """
    result_sitemap = []

    def __init__(self, sitemap_to_match: dict=None, url=None, origin=None, find=None, csv=None):
        self.sitemap = sitemap_to_match
        self.origin = origin
        self.name = sitemap_to_match["_id"]
        self.start_urls = [url]

    def parse(self, response):
        for selector in self.sitemap["selectors"]:  # go through each selector
            if selector.get("selector"):
                for item in response.css(selector["selector"]):

                    delay = selector.get("delay")  # if delay specified
                    if delay:
                        time.sleep(delay)

                    if selector.get("type") == "SelectorText":  # if the selection should be text
                        text = ', '.join([sent.strip() for sent in item.css('::text').extract() if not sent.isspace()])

                        # Text results can be parsed further with regex
                        regex = selector.get("regex")
                        if regex:
                            #pattern = re.compile(sel_regex)
                            try:
                                text = re.findall(regex, text)[0]
                            except IndexError:
                                pass

                        self.result_sitemap.append({selector["id"]: text})

    def close(self, reason):
        if self.origin:
            self.origin(reason)