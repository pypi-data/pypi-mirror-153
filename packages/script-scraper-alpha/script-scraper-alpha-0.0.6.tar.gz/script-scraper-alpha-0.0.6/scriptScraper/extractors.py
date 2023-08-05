import scrapydo
import logging
from .simpleSpider import SimpleBot

main_settings = {
    'USER_AGENT':'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
    'ROBOTSTXT_OBEY': False,
    'COOKIES_ENABLED': False,
    'DEFAULT_REQUEST_HEADERS': {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en'
        }
}
def special_feeds(filename):
    return {
        filename: {
        'format': 'json',
        'encoding': 'utf8',
        'store_empty': False,
        'fields': None,
        'indent': 2,
        'item_export_kwargs': {
            'export_empty_fields': True
            }
        }
    }

class ScriptRunner():
    def __init__(self, delay=1, log=False, output='data.json', custom_settings={}):
        self.delay = delay
        self.log = log
        self.output = output
        self.custom_settings = custom_settings

    def scrape(self, request):
        scrapydo.setup()
        other_settings = {'DOWNLOAD_DELAY':self.delay, 'FEEDS':special_feeds(self.output)}
        scrapydo.default_settings.update(main_settings)
        self.custom_settings.update(other_settings)
        scrapydo.default_settings.update(self.custom_settings)
        if self.log:
            logging.getLogger('scrapy').propagate = True
            logging.basicConfig(level=logging.DEBUG)
        else:
            logging.getLogger('scrapy').propagate = False
            logging.basicConfig(level=logging.WARNING)
        results = scrapydo.run_spider(SimpleBot, request=request)
        print('Massage:', 'Scraping complete.')
        return results
