from Formatter import Markdown
from ELR import ELR
from ATF import ATF


class Processor:
    def __init__(self, pattern, username):
        self.pattern = pattern
        self.username = username
        self.formatter = Markdown()

        self.elr = ELR()
        self.atf = ATF()

    def submission(self, submission):
        matches = self.pattern.findall(submission.selftext)
        if matches:
            terms = self.buildSearchTerms(matches)
            linksELR = map(lambda term: self.elr.getTopHit(term), terms)
            linksATF = map(lambda term: self.atf.getTopHit(term), terms)

            links = {
                'ELR': map(lambda link: self.formatter.link(link), linksELR),
                'ATF': map(lambda link: self.formatter.link(link), linksATF)
            }

            if len(terms) > 0:
                reply = self.formatter.reply(terms, links)
                # submission.add_comment(reply)
                print reply
                print 'Processed submission: %s' % submission.id

    def comment(self, comment):
        if comment.author.name != self.username:
            matches = self.pattern.findall(comment.body)
            if matches:
                terms = self.buildSearchTerms(matches)
                linksELR = map(lambda term: self.elr.getTopHit(term), terms)
                linksATF = map(lambda term: self.atf.getTopHit(term), terms)

                links = {
                    'ELR': map(lambda link:
                               self.formatter.link(link), linksELR),
                    'ATF': map(lambda link:
                               self.formatter.link(link), linksATF)
                }

                if len(terms) > 0:
                    reply = self.formatter.reply(terms, links)
                    # comment.reply(reply)
                    print reply
                    print 'Processed comment: %s' % comment.id

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
