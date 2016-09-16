from Source import Source
from lxml import html
import urllib
import re


class ATF(Source):
    name = 'ATF'
    baseUrl = 'https://alltheflavors.com'
    searchUrl = '%s/%s' % (baseUrl, 'flavors/live_search?%s')
    vendorUrl = '%s/%s' % (baseUrl, 'vendors')

    def getVendorList(self):
        vendors = {}
        url = self.vendorUrl

        try:
            f = urllib.urlopen(url)
            tree = html.fromstring(f.read())

            vendorRows = tree.xpath('//section/div[contains(@class, "row")]')
            for vendor in vendorRows:
                fullName = vendor[0].text
                shortName = vendor[1].text
                vendors[shortName] = fullName

        except IOError:
            print 'Failed getting vendor list from ATF.'

        return vendors

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
        params = urllib.urlencode({'name_like': self.aliasVendors(term)})
        url = self.searchUrl % (params)

        try:
            f = urllib.urlopen(url)
            tree = html.fromstring(f.read())

            hits = tree.xpath('//tr/td[1]/a')
            links = map(lambda hit: {
                'text': hit.text.strip(),
                'link': self.baseUrl + hit.attrib['href'],
                'machine': hit.text.strip().replace('(', '').replace(')', '')
            }, hits)

            link = self.filterLinks(links, term)
            if link:
                return {'text': link['text'], 'link': link['link']}

        except IOError:
            print 'Failed connectiong to %s' % self.name

        return None
