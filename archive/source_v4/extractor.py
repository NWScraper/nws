try:
    import source_v4.base as base
except ModuleNotFoundError:
    import base

class Praktijkinfo(base.Scraper):
    name = 'praktijkinfoscraper'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = self.start_urls + [f"{self.start_urls[0]}/modules/medewerkers.php"]

