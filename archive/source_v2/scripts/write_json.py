import json
import urllib.parse


class JSONwriter:
    def __init__(self, questionnaire: str, outdir: str):
        self.selectors = self.create_selectors(questionnaire)
        self.urls = None
        self.outdir = outdir

    def read_urls(self, file):
        with open(file, "r") as f:
            lines = f.readlines()
        result = []
        for line in lines:
            if "://" not in line:
                line = "".join(["http://", line])
            result.append(line.strip())
        self.urls = result
        return result

    def load_template(self, file):
        with open(file, "r") as f:
            return json.loads(f)

    def write_file(self, path: str, file: json):
        with open(''.join([self.outdir, path, ".json"]), "w+") as f:
            f.write(file)

    def bulk(self, urls: str):
        self.read_urls(file=urls)
        for url in self.urls:
            host = urllib.parse.urlparse(url).netloc
            self.write_file(path=host, file=self.create_site_map(url=url, host=host))

    def create_selectors(self, file):
        selector_template = {"parentSelectors": ["_root"],
                             "type": "SelectorText",
                             "multiple": False,
                             "id": None,
                             "selector": None,
                             "regex": None,
                             "delay": None, }
        with open(file, "r") as f:
            lines = f.readlines()

        vrs = [line.split()[0] for line in lines
               if line
               and not line.startswith('#')
               and not line.startswith(' ')
               and not line.startswith('\n')]
        result = []
        for var in vrs:
            item = selector_template.copy()
            item["id"] = var
            result.append(item)
        return result

    def create_site_map(self, url: str, host: str = None):
        if not host:
            host = urllib.parse.urlparse(url).netloc
        site_map = {"startUrl": url,
                    "selectors": self.selectors,
                    "_id": host}
        return json.dumps(site_map, indent=2, sort_keys=True)


class SiteMap:
    def __init__(self):
        self.site_map = None
        self._id = None

    def load_template(self, file):
        with open(file, "r") as f:
            self.site_map = json.loads(f.read())

    def update_id(self, _id):
        self.site_map["_id"] = _id
        self._id = _id

    def update_startUrl(self, startUrl):
        self.site_map["startUrl"] = startUrl

    def update_selector(self, id, key, value):
        for selector in self.site_map["selectors"]:
            if selector["id"] == id:
                index = self.site_map["selectors"].index(selector)
                self.site_map["selectors"][index][key] = value
                return

    def json_file(self):
        return json.dumps(self.site_map, indent=2, sort_keys=True)

    def pretty_print(self):
        print(self.json_file())

    def write_file(self):
        with open(''.join(["../sitemaps/script", self._id, ".json"]), "w+") as f:
            f.write(self.json_file())


if __name__ == '__main__':
    jw = JSONwriter("../static/questionnaire_standardised.txt", outdir='../sitemaps/Script/')
    jw.bulk("../static/NZR500.txt")
