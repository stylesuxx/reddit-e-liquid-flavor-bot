class Processor:
    def __init__(self, pattern, formatter, sources):
        self.pattern = pattern
        self.formatter = formatter
        self.sources = sources

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
            term = '%s %s' % (term[0].strip(), term[1].strip())
            return term

        return term[0]

    def buildSearchTerms(self, matches):
        matches = map(lambda match: match.strip(), matches)
        terms = map(lambda match: self.buildSearchTerm(match), matches)
        terms = set(terms)
        terms = sorted(terms)

        return terms
