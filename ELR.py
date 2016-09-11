from Source import Source
from lxml import html
import urllib


class ELR(Source):
    baseUrl = 'http://e-liquid-recipes.com/flavors/?%s'

    def getTopHit(self, term):
        params = urllib.urlencode({
            'q': term,
            'sort': 'num_recipes',
            'direction': 'desc'
        })
        url = self.baseUrl % (params)

        f = urllib.urlopen(url)
        tree = html.fromstring(f.read())
        text = tree.xpath('//table[contains(@class, "flavorlist")]'
                          '/tbody/tr[1]/td[1]//a/text()')
        link = tree.xpath('//table[contains(@class, "flavorlist")]'
                          '/tbody/tr[1]/td[1]//a/@href')

        if text and link:
            return {'text': text[0], 'link': link[0]}

        return None
