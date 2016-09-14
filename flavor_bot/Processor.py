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

    def buildSearchTerms(self, matches):
        matches = map(lambda match: match.strip(), matches)
        terms = map(lambda match: self.buildSearchTerm(match), matches)
        terms = set(terms)
        terms = sorted(terms)

        return terms

    def buildSearchTerm(self, match):
        term = match.split('by')

        # Sanitize vendor if available
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

            term = '%s %s' % (potentialFlavor, potentialVendor)
            return term

        # Vendor might be provided, but not properly delimited
        else:
            searchTerm = term[0]
            if self.settings['vendors']:
                vendors = self.settings['vendors']
                for short in vendors:
                    if searchTerm.startswith(short.lower()):
                        flavor = searchTerm[len(short):].strip()
                        term = '%s %s' % (flavor, short)
                        return term

        # Search term could not be optimized, no vendor provided
        return term[0]
