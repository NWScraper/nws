# script to run webscraper.py in bulk

import time
import platform
import os
import subprocess
import scrapy.crawler
from twisted.internet import reactor
try:
    import source_v3.webscraper as nws
except ModuleNotFoundError:
    import webscraper as nws

# get input
with open('../NZR500.txt', 'r') as f:
    raw = f.readlines()

# clean input
sites = [site.strip() for site in raw]

# # serial running
# for site in sites:
#     os.system(f'scrapy runspider webscraper.py -a sitemap="praktijkinfo.json" -a site="{site}"')

# parallel running
runner = scrapy.crawler.CrawlerRunner()
print('collecting sites')
for site in sites:
    runner.crawl(nws.ScrapyScraper, sitemap="praktijkinfo.json", site=site)
d = runner.join()
d.addBoth(lambda _: reactor.stop())
print(len(runner.crawlers), 'sites')
print('crawling...')
reactor.run()

print('done running')

path = "result1.csv"
if platform.system() == "Windows":
    path = path.replace("/", "\\")
    os.startfile(path)
elif platform.system() == "Darwin":
    subprocess.Popen(["open", path])
else:
    subprocess.Popen(["xdg-open", path])
