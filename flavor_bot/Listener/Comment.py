from requests.exceptions import RequestException
from Listener import Listener
import time

from flavor_bot.helpers import log


class Comment(Listener):
    def __init__(self, stream, action):
        super(Comment, self).__init__(stream, action)

    def run(self):
        while True:
            try:
                for comment in self.stream():
                    if(comment.id not in self.processed and
                       comment.author != self.author):
                        self.action({
                            'op': comment,
                            'text': comment.body})
                        self.processed.append(comment.id)
                        log('Added comment to queue: %s' % comment.id)

            except RequestException as e:
                log('Request failed: %s' % (e))
                log('Sleeping for %i seconds...' % (self.timeout))
                time.sleep(self.timeout)
