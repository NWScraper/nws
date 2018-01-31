#!/usr/bin/env python
"""python 3.6 Huisartsenpraktijk-website information parser
"""
from pprint import pprint
import bs4
import os
import re


class Reader:
    def __init__(self, url):
        self.url = url
        self.soups = []
        self.texts = []
        self.template = None
        self.result: Vragenlijst = None

    def get_files_dir(self, dir_path):
        html_path = os.path.join(dir_path, 'page.html')
        html = open(html_path, 'r', encoding='utf-8')
        soup = bs4.BeautifulSoup(html, "html.parser")
        self.soups.append(soup)

        txt_path = os.path.join(dir_path, 'page.txt')
        txt = open(txt_path, 'r', encoding='utf-8').read()
        self.texts.append(txt)

    def read(self):
        path = os.path.join('websites_back/', self.url)

        # Get homepage
        self.get_files_dir(path)

        # Get other pages
        for dir in os.listdir(path):
            sub_path = os.path.join(path, dir)
            if os.path.isdir(sub_path):
                self.get_files_dir(sub_path)

    def set_template(self, template: str=None):
        if not template:
            self.template = "BaseTemplate"
        else:
            self.template = template

    def parse(self):
        template = BaseTemplate(soups=self.soups, texts=self.texts, url=self.url)  # todo pick template
        vragenlijst = template.fill_in()
        self.result = vragenlijst

    def show(self):
        if not self.result:
            print("No result")
        else:
            self.result.pretty_print()


class Vragenlijst(object):
    def __init__(self, *args, **kwargs):
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


        for key, value in kwargs.items():
            setattr(self, key, value)

    def pretty_print(self):
        print('-'*80)
        for key, value in self.__dict__.items():
            if value:
                print(f"{key}:", value)

    def export(self, type):
        if type == 'CSV':
            pass


class BaseTemplate(object):
    def __init__(self, soups: list, texts: list, url: str):
        self.soups = soups
        self.texts = texts
        self.full_text = '\n'.join([text for text in texts])
        self.root_url = url

    def fill_in(self) -> Vragenlijst:
        self._test()
        # values = {key: value(self) for (key, value) in BaseTemplate.__dict__.items()
        #           if not key.startswith('_')
        #           and key is not 'fill_in'}
        # vragenlijst = Vragenlijst(**values)
        # return vragenlijst

    @staticmethod
    def _get_index(sentence: str, keywords: list) -> int:
        for word in sentence.lower().split():
            if word in keywords:
                index = sentence.lower().index(word)
                return index

    def _test(self):
        for soup in self.soups:
            # x = soup.find_all(text=re.compile('^contact$'))
            x =re.findall('(contact)', soup.text)

            print(x)





    # pagina 1
    def praktijknaam(self) -> str or None:
        soup = self.soups[0]
        tag = soup.find_all(attrs={"name": "apple-mobile-web-app-title"})  # Try to find name by mobile title
        try:
            praktijknaam = tag[0]["content"].strip()

            if praktijknaam in ["PeriScaldes"]:  # Incorrect result
                tag = soup.find_all(attrs={"name": "keywords"})  # Try to find name by keyword
                try:
                    praktijknaam = tag[0]["content"].strip().split(',')[0]
                    return " ".join(praktijknaam.split())
                except IndexError:
                    return

            else:
                return " ".join(praktijknaam.split())
        except IndexError:
            return


    def plaatsnaam(self) -> str or None:
        pass

    def adres(self) -> str or None:
        pass

    def postcode(self) -> str or None:
        pass

    def telefoon(self) -> str or None:
        pass

    def email(self) -> str or None:
        pass

    def website(self) -> str or None:
        return self.root_url

    # pagina 2
    def huisarts(self) -> list or None:
        pass

    # pagina 3
    def ondersteunend_personeel(self) -> list:
        pass

    # pagina 4
    def zorgaanbod(self) -> list:
        pass

    def bereikbaarheid(self) -> list:
        pass

    def categoraal_spreekuur(self) -> list:
        pass

    def informatie_voorziening(self) -> list:
        pass

    def opleiders_in_de_praktijk(self) -> list:
        pass

    # pagina 5
    def voorziening(self) -> list:
        pass

    # pagina 6
    def zorggroep(self) -> list:
        pass

    # pagina 7
    def huisartseninformatiesysteem(self) -> str or None:
        pass

    def keteninformatiesysteem(self) -> str or None:
        pass


if __name__ == '__main__':
    os.chdir('../../')

    def main():
        with open("NZR500.txt", 'r') as f:
            urls = f.readlines()

        x = 0
        for url in urls[:101]:
            try:
                reader = Reader(url.strip().replace('/', '_'))
                reader.read()
                # reader.set_template()
                #print('Go parse')
                reader.parse()
                reader.show()
                # if reader.result.praktijknaam:  # change for count
                #     x += 1
            except (FileNotFoundError) as e:
                #print(e, url)
                pass

        print(f'\n\n\nSuccess: {x}%')

    main()
