import prawcore
import time

from Listener import Listener
from flavor_bot.helpers import logNote, logWarn


class Comment(Listener):
    def __init__(self, stream, action):
        super(Comment, self).__init__(stream, action)

    def run(self):
        try:
            for comment in self.stream():
                if(comment.id not in self.processed and
                   comment.author != self.author):
                    text = comment.body
                    self.action({'op': comment, 'text': text})
                    self.processed.append(comment.id)
                    logNote('New comment: %s' % (comment.id))

        except prawcore.exceptions.RequestException as e:
            logWarn('Comment stream failed. Sleeping for %i seconds...' %
                    (self.timeout))
            time.sleep(self.timeout)
            self.run()
