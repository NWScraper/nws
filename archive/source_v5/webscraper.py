import time
import re
import json
import csv
import sys
import time
from pprint import pprint
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
import platform
import subprocess
import os

try:
    import source_v3.filters as filters
except ModuleNotFoundError:
    import filters


class ScrapyScraper(scrapy.Spider):
    """A scraper which acts like webscraper.io
    Takes one sitemap and one url
    Creates a filled in result
    """
    name = 'scrapyscraper'
    custom_settings = {
        'DNS_TIMEOUT': 5,
        'TELNETCONSOLE_ENABLED': False
    }
    completed = 0
    stamp = int(time.time())

    def __init__(self, sitemap: str or dict, origin=None, site=None):
        if type(sitemap) == str:
            # create JSON from path
            with open(sitemap) as json_data:
                sitemap = json.load(json_data)
        self.sitemap = sitemap  # JSON/dict
        self.origin = origin  # output
        if not site:
            self.name = sitemap["_id"]  # name
            self.start_urls = sitemap["startUrl"]  # url list
        else:
            self.name, self.start_urls = site, [site]
        self.result = {}
        self.result["website"] = self.start_urls[0]
        self.start_urls = [f"http://{site}" for site in self.start_urls if "://" not in site] + [site for site in self.start_urls if "://" in site]
        self.start_urls += [f"{self.start_urls[0]}/modules/medewerkers.php"]

    def parse(self, response):
        for selector in self.sitemap["selectors"]:  # go through each selector
            if selector.get("selector"):
                for item in response.css(selector["selector"]):
                    text = ""

                    # if delay specified (probably not)
                    delay = selector.get("delay")
                    if delay:
                        time.sleep(delay)

                    # if the selection should be text
                    if selector.get("type") == "SelectorText":
                        text = ', '.join([sent.strip() for sent in item.css('::text').extract() if not sent.isspace()])

                        # Text results can be parsed further with regex
                        regex = selector.get("regex")
                        if regex:
                            #pattern = re.compile(sel_regex)
                            try:
                                text = re.findall(regex, text)[0]
                                #print(text)

                            except IndexError:
                                continue

                    # additional filter
                    try:
                        text = eval(f"filters.{selector['id']}('{text}')")
                    except AttributeError:
                        continue

                    self.result[selector["id"]] = text


    def close(self, reason):
        if self.origin:
            self.origin(reason)
        path = f"result.csv"
        if len(self.result.items()) > 1 or True:
            with open(path, "a") as f:
                w = csv.DictWriter(f, self.result.keys(), delimiter=';')
                #w.writeheader()
                w.writerow(self.result)
        ScrapyScraper.completed += 1
        sys.stdout.write("-")
        sys.stdout.flush()
        if ScrapyScraper.completed % 100 == 0:
            print(ScrapyScraper.completed)


