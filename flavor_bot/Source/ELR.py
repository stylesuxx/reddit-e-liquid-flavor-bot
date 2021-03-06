from Source import Source
from lxml import html
import urllib
import re

from flavor_bot.helpers import printErr


class ELR(Source):
    name = 'ELR'
    baseUrl = 'http://e-liquid-recipes.com'
    searchUrl = '%s/%s' % (baseUrl, 'flavors/?%s')

    def filterLinks(self, links, term):
        # If only one link is available, we will use it
        if len(links) == 1:
            return links[0]

        # Only cafe for the 5 top results
        links = links[0:5]

        # Filter away all hits where the first part of the term is only part of
        # a word
        terms = term.split(' ')
        important = terms[0]
        regex = r"" + re.escape(important) + "(\s+|$)"
        links = filter(lambda link:
                       re.search(regex, link['machine'], re.IGNORECASE), links)

        # If only one is left, we are done
        if len(links) == 1:
            return links[0]

        # Filter away all hits that have more terms than the original term
        sameLength = filter(lambda link:
                            len(link['machine'].split(' ')) == len(terms),
                            links)

        # If none left, be a bit more loose at the second pass
        if not sameLength:
            limit = len(terms) + 2
            sameLength = filter(lambda link:
                                len(link['machine'].split(' ')) <= limit,
                                links)

        if sameLength:
            links = sameLength

        if links:
            return links[0]

        return None

    def getTopHit(self, term):
        params = urllib.urlencode({
            'q': self.aliasVendors(term),
            'sort': 'num_recipes',
            'direction': 'desc'
        })
        url = self.searchUrl % (params)

        try:
            f = urllib.urlopen(url)
            tree = html.fromstring(f.read())

            allHits = tree.xpath('//table[contains(@class, "flavorlist")]'
                                 '/tbody/tr/td[1]/span/a')
            allLinks = map(lambda hit: {
                'text': hit.text,
                'link': hit.attrib['href'],
                'machine': hit.text.strip().replace('(', '').replace(')', '')
            }, allHits)

            link = self.filterLinks(allLinks, term)
            if link:
                return {'text': link['text'], 'link': link['link']}

        except IOError:
            printErr(('Failed connecting to %s' % self.name))

        return None
