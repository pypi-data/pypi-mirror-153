from abc import ABC, abstractmethod, abstractproperty, abstractclassmethod


class LocDataBase(ABC):

    @abstractproperty
    def data(self):
        return self.dataframe

class _LocData(LocDataBase):

    def __init__(self):
        pass

    def