import os
from pprint import pprint
import bs4


class SiteWriter:
    def __init__(self, entrylist: list):
        self.entrylist = entrylist

    def save(self):
        sites_path = "websites/"
        if not os.path.isdir(sites_path):
            print("Couldn't find the folder 'websites/'. Make sure you are running from the right directory")
            return

        for entry in self.entrylist:
            self._write_site(entry)

    @staticmethod
    def clean_path(path: str) -> str:
        result = path.replace('/', '_')
        try:
            result = result.strip('_')
            assert result is not None
        except AssertionError:
            pass
        return result

    @staticmethod
    def get_text(html) -> str:
        soup = bs4.BeautifulSoup(html, "html.parser")
        text = soup.text
        txt = []
        for line in text.splitlines():
            if line:
                txt.append(line)
        return '\n'.join(txt)


    @staticmethod
    def _write_in_folder(path, **kwargs):
        if not os.path.isdir(path):
            print('Creating new folder', path)
            os.mkdir(path)

        if kwargs:
            for key, value in kwargs.items():
                kwarg_path = os.path.join(path, f'page.{key}')
                with open(kwarg_path, 'wb+') as f:
                    f.write(value.encode('utf-8'))

    def _write_site(self, entry: list):
        """Write the data to files in the correct structure"""
        if not entry:
            return

        # Folder websites/
        sites_path = "websites/"
        self._write_in_folder(sites_path)

        # Entry[0] - Home Page
        # Folder websites/www.huisarts.nl/
        #assert entry[0]['path'] == ''  # First item of entry should be the home page (no sitepath)
        for key, value in entry[0].items():
            print(key)
            if key != 'html':
                print(value)

        assert entry[0]['url'] == entry[0]['root_url']
        assert entry[0]['path'] == ''


        homepage_path = os.path.join(sites_path, entry[0]['domain'])
        homepage_html = entry[0]['html']
        homepage_txt = self.get_text(homepage_html)
        self._write_in_folder(homepage_path, html=homepage_html, txt=homepage_txt)

        if len(entry) > 1:
            for page in entry[1:]:
                # Folder websites/www.huisarts.nl/info
                link_path = os.path.join(homepage_path, self.clean_path(page['path']))
                html = page['html']
                txt = self.get_text(html)
                self._write_in_folder(link_path, html=html, txt=txt)
