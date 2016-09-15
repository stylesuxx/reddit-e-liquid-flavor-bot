from abc import ABCMeta, abstractmethod, abstractproperty
import threading


class Listener(threading.Thread):
    __metaclass__ = ABCMeta

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
    def run(self):
        raise NotImplementedError
