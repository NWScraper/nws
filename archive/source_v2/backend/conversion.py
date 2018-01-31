import json


class SiteMap(dict):
    selector_template = {"parentSelectors": ["_root"],
                         "type": "SelectorText",
                         "multiple": False,
                         "id": None,
                         "selector": None,
                         "regex": None,
                         "delay": None, }

    def __init__(self, **kwargs):
        super().__init__()
        self.__dict__.update(kwargs)


class Selector(dict):
    

from pprint import pprint

s = SiteMap(hee="hee", waar="daar")
pprint(s.hee)
for x in s:
    print(x)
