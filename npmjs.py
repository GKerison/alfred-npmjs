#!/usr/bin/python
# encoding:utf-8

import sys
from workflow import Workflow3, web


class NPMJS:

    def __init__(self, wf):
        self.wf = wf

    def cache(self, keyword, url):
        libs = self.wf.cached_data(keyword, max_age=0)
        if libs is None:
            libs = web.get(url).json()
            self.wf.cache_data(keyword, libs)
        return libs

    def query(self, keyword):
        url = 'https://www.npmjs.com/-/search?text=%s&from=0&size=15' % keyword
        resp = self.cache(keyword, url)
        # print resp
        if resp is not None:
            items = resp['objects']
            if items is not None and len(items) > 0:
                for item in items:
                    self.add_item(item)
                return
        self.empty_result(keyword, u'Nothing is Here ~')

    def empty_result(self, title, message):
        return self.wf.add_item(title, subtitle=message, valid=True)

    def add_item(self, item):
        package = item['package']
        if package is not None:
            title = '%s(%s)' % (package['name'], package['version'])
            links = package['links']
            target_page_url = links['homepage'] if 'homepage' in links else links['npm']
            subtitle = target_page_url
            arg = target_page_url
            quicklookurl = target_page_url
            self.wf.add_item(title=title, subtitle=subtitle, arg=arg,
                             quicklookurl=quicklookurl, valid=True)


def main(wf):
    npmjs = NPMJS(wf)
    if(len(wf.args) > 0):
        npmjs.query(wf.args[0])
        wf.send_feedback()


if __name__ == '__main__':
    wf = Workflow3()
    sys.exit(wf.run(main))
