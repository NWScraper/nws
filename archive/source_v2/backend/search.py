import time
import os
import json
import re
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
from backend.scrap import Controller


class NivelSearcher(scrapy.Spider):
    result = []

    def __init__(self, skeleton: dict, origin=None):
        self.skeleton = skeleton
        self.origin = origin
        self.name = skeleton["_id"]
        self.start_urls = [skeleton["startUrl"]]
        self.questionnaire["website"] = skeleton["startUrl"]

    def parse(self, response):
        global result
        for selector in self.skeleton["selectors"]:  # go through each selector
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

        #Questionnaire.filled_in.append(self.questionnaire)

    def close(self, reason):
        if self.origin:
            self.origin(reason)






if __name__ == '__main__':
    from pprint import pprint

    c = Controller(NivelSearcher)

    with open("static/NZR500.txt") as f:
        urls = f.readlines()

    for url in urls:
        ls = NivelSearcher()

    c.start()

