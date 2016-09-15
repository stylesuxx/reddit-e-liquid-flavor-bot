from abc import ABCMeta, abstractmethod, abstractproperty


class Source:
    __metaclass__ = ABCMeta

    @abstractproperty
    def name(self):
        raise NotImplementedError

    @abstractmethod
    def getTopHit(self, searchterm):
        raise NotImplementedError
