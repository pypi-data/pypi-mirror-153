import json
import copy
from datetime import datetime
from scrapy import Spider, Request
from .simpleScraper import simpleScraper

class SimpleBot(Spider):
  name = 'simpleBot'

  def __init__(self, request):
    if type(request)==str:
        self.request = json.loads(request)
    else:
        self.request = request
    self.urls = self.request['urls']

  def start_requests(self):
    for url in self.urls:
      yield Request(url=url, callback=self.parse, cb_kwargs={'request': self.request['extract_rules']})

  def parse(self, response, request, parent_data=None, paths=None, child_path=None):
    scraper = simpleScraper(response, self.parse)
    data, follow = scraper.extract(copy.deepcopy(request))
    data['date'] = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
    data['url'] = response.request.url
    if len(follow) != 0:
      for path in follow:
        nested_request = self.find_nested_request(path, data)
        yield response.follow(url=nested_request['url'], callback=self.parse, cb_kwargs={'request': nested_request['output'], 'parent_data':data, 'child_path':path, 'paths':follow}, dont_filter=True)
    elif parent_data != None:
      data = self.add_child_to_parent(parent_data, child_path, data)
      if len(paths)==1:
        yield data
      paths.pop()
    else:
      yield data

    if "next_page" in request:
      if type(request['next_page']) == str:
        request['next_page'] = {'selector': request['next_page'], 'type':'item', 'output': 'href'}
      next_page, follow = scraper.extract({'next': request['next_page']})
      if 'next' in next_page:
        if next_page['next'] is not None:
          yield response.follow(next_page['next'], self.parse, cb_kwargs={'request': request})
  
  def find_nested_request(self, element, json):
    keys = element.split('.')
    rv = json
    for key in keys:
      if key.isdigit():
        key = int(key)
      rv = rv[key]
    return rv
  
  def nested_set(self, dic, keys, value):
    d = dic
    for key in keys[:-1]:
      if key.isdigit():
        key = int(key)
      d = d[key]
    if keys[-1] in d:
        d[keys[-1]] = value
    return dic
  
  def add_child_to_parent(self, parent, child_path, value):
    keys = child_path.split('.')
    new_parent = self.nested_set(parent, keys, value)
    return new_parent
