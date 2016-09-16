from abc import ABCMeta, abstractmethod, abstractproperty


class Source:
    __metaclass__ = ABCMeta
    alias = {}

    @abstractproperty
    def name(self):
        raise NotImplementedError

    @abstractmethod
    def getTopHit(self, searchterm):
        raise NotImplementedError

    def setVendorAlias(self, alias):
        self.alias = alias

    def aliasVendors(self, searchTerm):
        for vendor in self.alias:
            searchTerm = searchTerm.replace(vendor, self.alias[vendor])

        return searchTerm
