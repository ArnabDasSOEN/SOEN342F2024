from abc import ABC, abstractmethod


class PackageSpecificationInterface(ABC):
    @abstractmethod
    def get_weight(self):
        pass

    @abstractmethod
    def get_dimensions(self):
        pass
