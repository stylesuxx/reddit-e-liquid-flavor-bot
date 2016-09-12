from abc import ABCMeta, abstractmethod


class Source:
    __metaclass__ = ABCMeta

    @abstractmethod
    def getTopHit(self, searchterm):
        pass
