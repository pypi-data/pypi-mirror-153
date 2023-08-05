
import abc
from plico.utils.decorator import returns
from six import with_metaclass

__version__= "$Id: convergeable.py 25 2018-01-26 19:00:40Z lbusoni $"


class Convergeable(with_metaclass(abc.ABCMeta, object)):

    @abc.abstractmethod
    @returns(bool)
    def hasConverged(self):
        assert False


    @abc.abstractmethod
    def performOneConvergenceStep(self):
        assert False


    @abc.abstractmethod
    def measureConvergence(self):
        assert False
