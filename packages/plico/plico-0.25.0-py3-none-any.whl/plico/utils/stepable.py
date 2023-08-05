import abc
from plico.utils.decorator import returns
from six import with_metaclass


__version__= "$Id: stepable.py 25 2018-01-26 19:00:40Z lbusoni $"


class Stepable(with_metaclass(abc.ABCMeta, object)):


    @abc.abstractmethod
    def step(self):
        assert False


    @abc.abstractmethod
    @returns(bool)
    def isTerminated(self):
        assert False
