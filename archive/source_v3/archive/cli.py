import argparse
import os
import scrapy.crawler

try:
    import source_v3.scrapers as scraper
except ModuleNotFoundError:
    import scrapers as scraper


parser = argparse.ArgumentParser(description='Nivel Webscraper')
source = parser.add_mutually_exclusive_group(required=True)
source.add_argument('--url', default=None, help='URL(\'s) om te scrapen')
source.add_argument('--urlfile', default=None, help='Tekstbestand met URL\'s')
source.add_argument('--sitemap', default=None, help='JSON sitemap om te gebruiken')
source.add_argument('--sitemapfolder', default=None, help='Folder met JSON sitemaps')

parser.add_argument('--find', default=None, help='Vind een specifiek onderdeel')
parser.add_argument('--csv', default=None, help='Output naar een CSV bestand')

args = parser.parse_args()

# Een URL is meegegeven
if args.url:
    scraper.FromURL(url=args.url, find=args.find, csv=args.csv).start()

# # Een tekstbestand met URL's is meegegeven
# elif args.urlfile:
#     with open(args.urlfile, 'r') as f:
#         urls = f.readline()
#     for url in urls:
#         scraper.FromURL(url=url, find=args.find, csv=args.csv).start()

# Een sitemap is meegegevn
elif args.sitemap:
    process = scrapy.crawler.CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })

    process.crawl(scraper.FromSitemap, sitemap=args.sitemap, find=args.find, csv=args.csv)
    process.start()


# # Een folder met sitemaps is meegegeven
# elif args.sitemapfolder:
#     runner = scrapy.crawler.CrawlerRunner()
#     for dirName, subdirList, fileList in os.walk(args.sitemapfolder):
#         for fname in fileList:
#             if fname.lower().endswith('.json'):
#                 runner.crawl(scraper.FromSitemap, sitemap=args.sitemap, find=args.find, csv=args.csv)






