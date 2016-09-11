from Source import Source
from lxml import html
import urllib


class ATF(Source):
    baseUrl = 'https://alltheflavors.com'
    searchUrl = '%s/%s' % (baseUrl, 'flavors/live_search?%s')

    def getTopHit(self, term):
        params = urllib.urlencode({
            'name_like': term
        })
        url = self.searchUrl % (params)

        f = urllib.urlopen(url)
        tree = html.fromstring(f.read())
        text = tree.xpath('//tr[1]/td[1]/a/text()')
        link = tree.xpath('//tr[1]/td[1]/a/@href')

        if text and link:
            return {'text': text[0], 'link': '%s/%s' % (self.baseUrl, link[0])}

        return None
