class Markdown:
    def link(self, link):
        if link:
            return '[%s](%s)' % (link['text'], link['link'])

        return 'Not found'

    def reply(self, terms, links):
        reply = '| Searchterm |'
        for key in links:
            reply += ' %s Top Hit |' % (key)

        reply += '  \n'
        reply += '| ---------- |'
        for key in links:
            reply += ' ----------- |'

        reply += '  \n'
        for i in range(0, len(terms)):
            reply += '| %s |' % (terms[i])
            for key in links:
                reply += ' %s |' % (links[key][i])

            reply += '  \n'

        reply += '  \n'
        reply += '  \n'
        reply += ('To use, post a flavor name like so: [[ Flavor Name by '
                  'Vendor Short Name ]], [[ Flavor Name ]] or '
                  '[[ Vendor Short Name Flavor Name ]].  \n')
        reply += ('My source may be found on [github]'
                  '(https://github.com/stylesuxx/reddit-e-liquid-flavor-bot). '
                  'Feel free to submit bug reports or feature requests.')

        return reply
