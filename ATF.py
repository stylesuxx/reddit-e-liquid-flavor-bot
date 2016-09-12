from Source import Source
from lxml import html
import urllib
import re


class ATF(Source):
    baseUrl = 'https://alltheflavors.com'
    searchUrl = '%s/%s' % (baseUrl, 'flavors/live_search?%s')

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
                       re.search(regex, link['text'], re.IGNORECASE), links)

        # If only one is left, we are done
        if len(links) == 1:
            return links[0]

        # Filter away all hits that have more terms than the original term
        linksSameLength = filter(lambda link:
                                 len(link['text'].split(' ')) == len(terms),
                                 links)

        # If none left, be a bit more loose at the second pass
        if not linksSameLength:
            linksSameLength = filter(lambda link:
                                     len(link['text'].split(' ')) <=
                                     len(terms) + 2,
                                     links)

        if linksSameLength:
            links = linksSameLength

        if links:
            return links[0]

        return None

    def getTopHit(self, term):
        params = urllib.urlencode({
            'name_like': term
        })
        url = self.searchUrl % (params)

        f = urllib.urlopen(url)
        tree = html.fromstring(f.read())
        # text = tree.xpath('//tr[1]/td[1]/a/text()')
        # link = tree.xpath('//tr[1]/td[1]/a/@href')

        allHits = tree.xpath('//tr/td[1]/a')
        allLinks = map(lambda hit: {
            'text': hit.text,
            'link': self.baseUrl + hit.attrib['href']},
            allHits)
        link = self.filterLinks(allLinks, term)

        if link:
            return {'text': link['text'], 'link': link['link']}

        return None
