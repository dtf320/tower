import os
import re
import configparser

# chrome parse
class BookMark:
    def __init__(self):
        self.items = {}

    def add(self, category, title, url):
        if category in self.items.keys():
            self.items[category].append({title:url})
        else:
            self.items[category] = {}




class MarkHolder:
    def __init__(self):
        self.parser = configparser.ConfigParser()

    def parse_mark(self, bookmark):
        with open(bookmark,'r') as f:
            content = f.read()

        regex = "<DL><p>((?:.|\n)*)</DL><p>"
        ret = re.findall(regex, content)[0]
        ret = re.findall(regex, ret)[0]

        regex2 = '<DT><H3(?:.|\n)*?</DL><p>'
        mark_categories = re.findall(regex2, ret)

        category = lambda text:re.search('<H3.*>(.*)</H3>',text).groups()[0]
        for text in mark_categories:
            category_title = category(text)
            category_content = re.findall(' <DT><A .*</A>',text)
        pass

    def find_urls_titles(self, content):
        items = re.findall('<A .*</A>',content)
        regex = '(<A HREF=")(.+)(" ADD_DATE.+">)(.*)(</A>)'
        get_url_intro = lambda it:re.search(regex,it).groups()
        items = map(get_url_intro,items)
        urls = []
        titles = []
        for it in items:
            urls.append(it[1])
            titles.append(it[3])
        return urls, titles




if __name__ == "__main__":
    p = ''
    holder = MarkHolder()
    holder.parse_mark(p)

    # '../bookmark/marks.ini'
