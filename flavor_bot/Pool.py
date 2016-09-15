from Queue import Queue
import threading

from flavor_bot.helpers import log


class Pool():
    def __init__(self, handler):
        self.queue = Queue()
        self.handler = handler

    def addWork(self, item):
        self.queue.put(item)

    def worker(self):
        while True:
            item = self.queue.get()
            self.handler(item)
            self.queue.task_done()

    def spawn(self, amount):
        for i in range(amount):
            worker = threading.Thread(target=self.worker)
            worker.daemon = True
            worker.start()
            log('Worker #%i started...' % (i))
