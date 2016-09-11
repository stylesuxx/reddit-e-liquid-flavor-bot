from Formatter import Markdown
from ELR import ELR


class Processor:
    def __init__(self, pattern):
        self.pattern = pattern
        self.elr = ELR()
        self.formatter = Markdown()

    def submission(self, submission):
        matches = self.pattern.findall(submission.selftext)
        if matches:
            terms = self.buildSearchTerms(matches)
            linksELR = map(lambda term: self.elr.getTopHit(term), terms)
            linksELR = map(lambda link: self.formatter.link(link), linksELR)
            links = {
                'ELR': linksELR,
                'ATF': linksELR
            }

            if len(terms) > 0:
                reply = self.formatter.reply(terms, links)
                # submission.add_comment(reply)
                print reply
                print 'Processed submission: %s' % submission.id

    def comment(self, comment):
        skip

    def buildSearchTerm(self, match):
        term = match.split('by')
        if len(term) > 1:
            term = '%s (%s)' % (term[0].strip(), term[1].strip())
            return term

        return term[0]

    def buildSearchTerms(self, matches):
        matches = map(lambda match: match.strip(), matches)
        terms = map(lambda match: self.buildSearchTerm(match), matches)
        terms = set(terms)
        terms = sorted(terms)

        return terms
