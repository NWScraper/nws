# script to run webscraper.py in bulk
import scrapy.crawler
from twisted.internet import reactor

try:
    import webscraper as nws
except ModuleNotFoundError:
    import lib.webscraper as nws


def run(input_data, template):
    # parallel running
    runner = scrapy.crawler.CrawlerRunner()
    print('collecting sites')

    for site in input_data:
        runner.crawl(nws.ScrapyScraper, sitemap=template, site=site)
    d = runner.join()
    d.addBoth(lambda _: reactor.stop())
    print(len(runner.crawlers), 'sites')
    print('crawling...')
    reactor.run()
    print('done!')

