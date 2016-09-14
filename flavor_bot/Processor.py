class Processor:
    def __init__(self, pattern, formatter, sources, settings={}):
        self.pattern = pattern
        self.formatter = formatter
        self.sources = sources
        self.settings = settings

    def process(self, text):
        matches = self.pattern.findall(text)
        if matches:
            links = {}
            terms = self.buildSearchTerms(matches)

            for source in self.sources:
                results = map(lambda term: source.getTopHit(term), terms)
                links[source.name] = map(
                    lambda link: self.formatter.link(link), results)

            if len(terms) > 0:
                reply = self.formatter.reply(terms, links)
                return reply

            return None

    def buildSearchTerm(self, match):
        term = match.split('by')
        if len(term) > 1:
            potentialFlavor = term[0].strip()
            potentialVendor = term[1].strip()
            if self.settings['vendors']:
                vendors = self.settings['vendors']
                for short in vendors:
                    full = vendors[short]
                    if(short.lower() == potentialVendor.lower() or
                       full.lower() == potentialVendor.lower()):
                        potentialVendor = short
                        break

                print 'Checking for vendor'
                # Check if the vendor is in short names - use the short name
                # - else check if vendor matches long name

            term = '%s %s' % (potentialVendor, potentialFlavor)
            return term

        return term[0]

    def buildSearchTerms(self, matches):
        matches = map(lambda match: match.strip(), matches)
        terms = map(lambda match: self.buildSearchTerm(match), matches)
        terms = set(terms)
        terms = sorted(terms)

        return terms
