from requests.exceptions import RequestException
import time

from Listener import Listener
from flavor_bot.helpers import log


class Submission(Listener):
    def __init__(self, stream, action):
        super(Submission, self).__init__(stream, action)

    def run(self):
        try:
            for submission in self.stream():
                if(submission.id not in self.processed and
                   submission.author != self.author):
                    text = submission.selftext
                    self.action({'op': submission, 'text': text})
                    self.processed.append(submission.id)
                    log('Added submission to queue: %s' % submission.id)

        except RequestException as e:
            log('Request failed: %s' % (e))
            log('Sleeping for %i seconds...' % (self.timeout))
            time.sleep(self.timeout)
            self.run()
