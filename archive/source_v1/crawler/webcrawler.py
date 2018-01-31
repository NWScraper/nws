#!/usr/bin/env python
"""python 3.6 async web crawler.
Based on:
https://github.com/mehmetkose/python3.5-async-crawler
"""
import aiohttp
import async_timeout
import asyncio
from aiohttp import ClientSession
import time
import urllib.parse
import re
import requests
from pprint import pprint
import validators
from tqdm import tqdm
import threading
import multiprocessing


with open('log.log', 'w') as f:
    f.write('')


# def debug(*args):  # todo print function for debug
#     # writing to a file is blocking, negating the async speed advantage. Function is disabled for now.
#     # with open('log.log', encoding='utf-8', mode='a') as f:
#     #     t = ' '.join([*args, '\n'])
#     #     f.write(t)
#     return


class WebCrawler:
    """A class for retrieving information from websites"""
    def __init__(self, url, debug_out):
        self.start_time = time.time()  # time at which the class was initiated
        self.debug = debug_out
        self.root_url = self.valid_url(url)
        self.domain = self.get_domain(self.root_url)
        self.urls = set()
        self.html = list()
        self.failed = list()

        self.debug(f'url = {self.root_url}')

    def get_domain(self, url):
        domain = urllib.parse.urlparse(url).netloc
        self.debug(f'domain = {domain}')
        return domain

    def crawl(self):
        # retrieve the home page
        try:
            req = requests.request('get', self.root_url)
        except (requests.exceptions.SSLError, requests.exceptions.ConnectionError) as e:
            self.debug(f'Error: {e} for {self.root_url}')
            self.failed.append(self.root_url)
            return
        if req.status_code == 200:
            html = req.text
        else:
            self.debug(f'Error: {self.root_url} returned {req.status_code}')
            self.failed.append(self.root_url)
            return

        # add the first html text
        entry = {'html': req.text,
                 'url': self.root_url, 'domain': self.domain,
                 'root_url': self.root_url, 'path': ''}
        self.html.append(entry)

        # retrieve the URL's on the homepage within the domain
        for url in self.get_urls(html):
            vurl = self.valid_url(url)
            if vurl:
                if self.in_domain(vurl):
                    self.urls.add(vurl)

        # retrieve the HTML from those URL's
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        loop.run_until_complete(self.get_html())

        #  add th URL of the first page, for good measures
        self.urls.add(self.root_url)

    def valid_url(self, url):
        surl = url  # alternative url, without params. Not meant for returning.
        if '?' in url:
            surl = url[:url.index('?')]
        if surl[surl.rfind('.'):] in ['.png', '.css', '.json', '.csv', '.svg', '.ico']:
            #self.debug(f'URL invalid type: {url}')
            return False
        if url[0] == '/':
            url = "".join([self.root_url, url])
        if url[0] == '.':
            url = "".join([self.root_url, url[1:]])
        if '://' not in url:
            url = "".join(['http://', url])
        if validators.url(url):
            return url
        else:
            self.debug(f'URL Error: {url}')

    def in_domain(self, url):
        if self.domain not in url:
            self.debug(f'URL not in domain: {url} in {self.domain}')
            return False
        return True

    def get_urls(self, html):
        urls = set(re.findall(r'''(?i)href=["']([^\s"'<>]+)''', html))
        self.debug(f'Found {len(urls)} URL\'s')
        return urls

    async def get_html(self):
        loop = asyncio.get_event_loop()
        futures = [loop.run_in_executor(None, requests.get, link) for link in self.urls]
        for response in await asyncio.gather(*futures, return_exceptions=True):
            if type(response) == requests.models.Response:
                if response.status_code == 200:
                    entry = {'html': response.text,
                             'url': response.url, 'domain': self.domain,
                             'root_url': self.root_url, 'path': urllib.parse.urlparse(response.url).path}
                    self.html.append(entry)
                else:
                    self.failed.append(response)
            else:
                self.failed.append(response)

    def report(self):
        print("\n\n\n###>-REPORT-<###")
        print(f"{self.root_url}")
        print('-' * 30)
        n = 0
        for url in self.urls:
            n += 1
            print(f"{n}). {url}")
        print('-' * 30)
        print(f"Crawled {len(self.urls)} in {time.time()-self.start_time} seconds")
        print(f"Gathered {len(self.html)} pages")
        print(f"{len(self.failed)} failed")


class Controller:
    def __init__(self, file: str, debug_out, first_line: int=None, last_line: int=None):
        with open(file, 'r') as f:
            self.urls = [url.strip() for url in f.readlines()]
        self.start_time = time.time()
        self.first_line = first_line
        self.last_line = last_line
        self.html = list()
        self.visited = 0
        self.limit()
        self.debug = debug_out

    def limit(self):
        """Make a selection of the given URL's"""
        if self.last_line:
            self.urls = self.urls[:self.last_line]
        if self.first_line:
            self.urls = self.urls[self.first_line-1:]

    def crawl(self, url):
        """Collect the HTML from a URL"""
        c = WebCrawler(url, debug_out=self.debug)
        c.crawl()
        # c.report()
        self.html.append(c.html)
        self.visited += 1

    def run(self):
        """Sequential run"""
        for url in tqdm(self.urls, desc="Crawling"):
            self.crawl(url)

    def threaded_run(self, threads: int=None):
        """Parallel run"""
        # if max_threads isn't specified it limits it based on the the amount of CPU's the machine has
        cores = multiprocessing.cpu_count()
        print('cores:', cores)
        if not threads:
            threads = cores

        def target(self, urls):
            """Action per thread"""
            for url in urls:
                self.crawl(url)

        def distribute(total: list, chunk_size: int):
            """For separating the total list of URL's in chunks"""
            for i in range(0, len(total), chunk_size):
                yield total[i:i + chunk_size]
        per_thread = (len(self.urls) + (threads - 1)) // threads  # ceiling division
        print("per thread:", f"{per_thread} (* {threads})")

        distributed_urls = distribute(self.urls, per_thread)

        threads = []
        n = 1
        for chunk in distributed_urls:
            thread = threading.Thread(target=target, args=(self, chunk), name=f"thread {n}")
            threads.append(thread)
            n += 1

        for thread in threads:
            thread.start()

        #for i in tqdm(range(len(self.urls))):
        #    while i > self.visited:
        #        pass

        for thread in threads:
            thread.join()


if __name__ == "__main__":
    import argparse

    ARGS = argparse.ArgumentParser(description="Web crawler")
    ARGS.add_argument('url', help='Root URL')

    args = ARGS.parse_args()
    crawler = WebCrawler(args.url)
    crawler.crawl()
    crawler.report()



