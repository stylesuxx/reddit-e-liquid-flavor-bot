from abc import ABCMeta, abstractmethod, abstractproperty
import threading
import prawcore
import time

from flavor_bot.helpers import logNote, logWarn


class Listener(threading.Thread):
    __metaclass__ = ABCMeta

    @abstractproperty
    def name(self):
        raise NotImplementedError

    def __init__(self, stream, action):
        self.stream = stream
        self.action = action
        self.processed = []

        self.timeout = 0
        self.author = ''

        super(Listener, self).__init__()

    def setProcessed(self, processed):
        self.processed = processed

    def setTimeout(self, timeout):
        self.timeout = timeout

    def setAuthor(self, author):
        self.author = author

    @abstractmethod
    def getItem(self, item):
        raise NotImplementedError

    def run(self):
        try:
            for message in self.stream():
                if(message.id not in self.processed and
                   message.author != self.author):
                    item = self.getItem(message)
                    self.action(item)
                    self.processed.append(message.id)
                    logNote('%s: %s' % (self.name, message.id))

        except prawcore.exceptions.RequestException as e:
            logWarn('%s stream failed. Sleeping for %i seconds...' %
                    (self.name, self.timeout))
            time.sleep(self.timeout)
            self.run()
