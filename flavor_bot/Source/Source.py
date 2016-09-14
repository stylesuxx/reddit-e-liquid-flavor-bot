from abc import ABCMeta, abstractmethod, abstractproperty


class Source:
    __metaclass__ = ABCMeta

    @abstractproperty
    def name(self):
        pass

    @abstractmethod
    def getTopHit(self, searchterm):
        pass
