# script-scraper: Intuitive queries for nested scraping tasks
## What is it?
**script-scraper** is a Python package that provides a simple and intuitive
interface, designed to make the web scraping procedure fast and modifiable.
It aims to help developers in writing simple and interpretable bots.
**script-scraper** is built on top of the **Scrapy** framework, providing 
the user with a familiar interface.
## Where to get it
The source code is currently hosted on GitHub at:
https://github.com/vlad-yeghiazaryan/script-scraper

You can also install it with pip, by running:
```sh
pip install script-scraper
```
## Working example
```python
from scriptScraper.extractors import ScriptRunner
request = {
  "urls": ["https://quotes.toscrape.com"],
  "extract_rules": {
    "quotes": {
      "selector": ".quote",
      "type": "list",
      "output": {
        "text": ".text",
        "author": ".author",
        "tags": {
          "selector": ".tag",
          "type": "list"
        },
        "about": {
          "selector": "span a",
          "type": "page",
          "follow": "href",
          "output": {
            "author_name": ".author-title",
            "author_birth_date": ".author-born-date",
            "author_birth_location": ".author-born-location",
            "author_description": ".author-description"
          }
        }
      }
    }
  }
}
crawler = ScriptRunner(delay=1, log=False, output='data.json')
scraped_data = crawler.scrape(request)
```