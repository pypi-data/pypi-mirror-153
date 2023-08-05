import copy

class simpleScraper():
    def __init__(self, response, parse=None):
        self.response = response
        self.parse = parse
        self.follow = []
        self.path = ""

    def extract(self, request):
        rules = self.standardizeRules(request)
        data = self.crawl(rules, self.response)
        return data

    def standardizeRules(self, rules_dict):
        for key in list(rules_dict):
            if type(rules_dict[key]) == str:
                rules_dict[key] = {
                    "selector": rules_dict[key],
                    "type": "item",
                    "output": "text" 
                }
            if ("selector" not in rules_dict[key]) or key=='next_page':
                del rules_dict[key]
                continue
            if 'type' not in rules_dict[key]:
                rules_dict[key]['type'] = "item"
            if "output" not in rules_dict[key]:
                rules_dict[key]['output'] = "text"
            if type(rules_dict[key]['output']) != str:
                if type(rules_dict[key]['output']) == dict:
                    rules_dict[key]['output'] = self.standardizeRules(
                        rules_dict[key]['output'])
                else:
                    rules_dict[key]['output'] = "text"
        return rules_dict

    def crawl(self, rules_dict, element, index=None):
        for key in rules_dict:
            isItem = (rules_dict[key]['type'] == 'item')
            isList = (rules_dict[key]['type'] == 'list')
            isPage = (rules_dict[key]['type'] == 'page')
            isText = (rules_dict[key]['output'] == 'text')
            isAttrib = (type(rules_dict[key]['output']) == str)
            isDict = (type(rules_dict[key]['output']) == dict)
            if isItem and isText:
                rules_dict[key] = element.css(
                    f"{rules_dict[key]['selector']}::text").get()
            elif isList and isText:
                rules_dict[key] = element.css(
                    f"{rules_dict[key]['selector']}::text").extract()
            elif (isItem and not isText) or (isList and not isText):
                if (isItem and isAttrib):
                    rules_dict[key] = element.css(
                        f"{rules_dict[key]['selector']}::attr({rules_dict[key]['output']})").get()
                elif (isList and isAttrib):
                    rules_dict[key] = element.css(
                        f"{rules_dict[key]['selector']}::attr({rules_dict[key]['output']})").extract()
                elif (isItem and isDict):
                    self.path += f" {key}"
                    parent = element.css(rules_dict[key]['selector'])
                    rules_dict[key] = self.crawl(
                        rules_dict.copy()[key]['output'], parent)
                elif (isList and isDict):
                    self.path += f" {key}"
                    parents = element.css(rules_dict[key]['selector'])
                    output = []
                    for index, parent in enumerate(parents):
                        output.append(self.crawl(copy.deepcopy(
                            rules_dict)[key]['output'], parent, index)[0])
                    rules_dict[key] = output
                else:
                    rules_dict[key] = self.response.css(
                        rules_dict[key]['selector']).extract()
            elif isPage:
                if 'follow' in rules_dict[key]:
                    page_selector = f"{rules_dict[key]['selector']}::attr({rules_dict[key]['follow']})"
                else:
                    page_selector = f"{rules_dict[key]['selector']}::attr(href)"
                page = element.css(page_selector).get()
                rules_dict[key] = {'url':page, 'output':rules_dict[key]['output']}
                if index == None:
                    index = ""
                follow_object = (f"{self.path} {index} {key}").strip().replace(" ", ".")
                self.follow.append(follow_object)
            else:
                rules_dict[key] = self.response.css(rules_dict[key]['selector']).extract()
        return (rules_dict, self.follow)
