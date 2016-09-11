from Source import Source
from lxml import html
import urllib
import re


class ELR(Source):
    baseUrl = 'http://e-liquid-recipes.com'
    searchUrl = '%s/%s' % (baseUrl, 'flavors/?%s')

    def filterLinks(self, links, term):
        # Filter away all hits where the first part of the term is only part of
        # a word
        terms = term.split(' ')
        important = terms[0]
        regex = r"" + re.escape(important) + "[ \n]"
        links = filter(lambda link:
                       re.search(regex, link['text'], re.IGNORECASE), links)

        # If only one is left, we are done
        if len(links) == 1:
            return links[0]

        # Filter away all hits that have more terms than the original term
        linksSameLength = filter(lambda link:
                                 len(link['text'].split(' ')) == len(terms),
                                 links)

        # Only apply the same length filter if somthing is left in the list
        if linksSameLength:
            links = linksSameLength

        if links:
            return links[0]

        return None

    def getTopHit(self, term):
        params = urllib.urlencode({
            'q': term,
            'sort': 'num_recipes',
            'direction': 'desc'
        })
        url = self.searchUrl % (params)

        f = urllib.urlopen(url)
        tree = html.fromstring(f.read())

        allHits = tree.xpath('//table[contains(@class, "flavorlist")]'
                             '/tbody/tr/td[1]/span/a')
        allLinks = map(lambda hit: {
            'text': hit.text,
            'link': hit.attrib['href']},
            allHits)
        link = self.filterLinks(allLinks, term)

        if link:
            return {'text': link['text'], 'link': link['link']}

        return None
