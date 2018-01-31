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


class NivelScraper(scrapy.Spider):
    """A scraper which acts like webscraper.io
    Takes one skeleton and one url
    Creates a filled in Questionnaire
    """
    result = []

    def __init__(self, skeleton: dict, origin=None):
        self.skeleton = skeleton
        self.origin = origin
        self.name = skeleton["_id"]
        self.start_urls = skeleton["startUrl"]
        self.questionnaire = Questionnaire()
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
        Questionnaire.filled_in.append(self.questionnaire)

    def close(self, reason):
        if self.origin:
            self.origin(reason)


class LearningScraper(scrapy.Spider):
    """A scraper for creating site maps
    Takes one skeleton and one url
    Creates a skeleton
    """
    result_skeleton = []

    def __init__(self, skeleton_to_match: dict, url=None, origin=None):
        self.skeleton = skeleton_to_match
        self.origin = origin
        self.name = skeleton_to_match["_id"]
        self.start_urls = [url]

    def parse(self, response):
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

                        self.result_skeleton.append({selector["id"]: text})

    def close(self, reason):
        if self.origin:
            self.origin(reason)


class Questionnaire(dict):
    """A representation of the questionnaire to store the results"""
    filled_in = []

    def __init__(self, **kwargs):
        # pagina 1
        self.praktijknaam = None
        self.plaatsnaam = None
        self.adres = None
        self.postcode = None
        self.telefoon = None
        self.email = None
        self.website = None

        # pagina 2
        self.huisarts = list()  # list(dict) {voorletters, achternaam, geslacht, functie, dienstverband, FTE}

        # pagina 3
        self.ondersteunend_personeel = list()

        # pagina 4
        self.zorgaanbod = list()
        self.bereikbaarheid = list()
        self.categoraal_spreekuur = list()
        self.informatie_voorziening = list()
        self.opleiders_in_de_praktijk = list()

        # pagina 5
        self.voorziening = list()

        # pagina 6
        self.zorggroep = dict()

        # pagina 7
        self.huisartseninformatiesysteem = None
        self.keteninformatiesysteem = None

        # for key, value in kwargs.items():
        #     self.__dict__[key] = value


class Controller:
    result = []

    def __init__(self, scraper, origin=None, url=None):
        scrapy.utils.log.configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
        self.runner = scrapy.crawler.CrawlerRunner()
        self.scraper = scraper
        self.origin = origin



    def get_skeleton(self, path: str):
        """Read a JSON site map"""

        with open(path, "r") as f:
            return json.load(f)


    def add_file(self, path: str):
        """Add a JSON site map to the crawler"""
        if path.lower().endswith('.json'):
            site_map = self.get_skeleton(path)
            self.runner.crawl(self.scraper, skeleton=site_map, origin=self.origin)

    def add_dir(self, folder: str):
        """Add a directory of JSON site maps to the crawler"""
        for dirName, subdirList, fileList in os.walk(folder):
            for fname in fileList:
                skeleton_path = os.path.join(dirName, fname)
                self.add_file(skeleton_path,)

    def start(self):
        """Start the crawler"""
        d = self.runner.join()
        d.addBoth(lambda _: reactor.stop())
        reactor.run()




if __name__ == '__main__':
    from pprint import pprint

    c = Controller(NivelScraper)
    c.add_dir("sitemaps/Test")
    c.start()
    print(Questionnaire.filled_in)

    # print(LearningScraper.result_skeleton)

    # with open("static/NZR500.txt") as f:
    #     urls = f.readlines()
    #
    # for url in urls:
    #     ls = LearningScraper("berkelmans.praktijkinfo.nl", Controller.get_skeleton(url),)


    # doesn't work yet
