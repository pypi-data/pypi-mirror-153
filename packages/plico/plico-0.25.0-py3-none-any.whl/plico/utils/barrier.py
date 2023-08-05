import abc
import time
from plico.utils.decorator import override
from six import with_metaclass


__version__= "$Id: barrier.py 25 2018-01-26 19:00:40Z lbusoni $"


class Predicate(with_metaclass(abc.ABCMeta, object)):

    @abc.abstractmethod
    def isFullfilled(self):
        assert False


    @abc.abstractmethod
    def errorMessage(self):
        assert False


class FunctionPredicate(Predicate):

    def __init__(self, nulladicFunction, functionName=""):
        self._nulladicFunction= nulladicFunction
        self._functionName= functionName


    @staticmethod
    def create(func, *args, **kwds):
        return FunctionPredicate(lambda: func(*args, **kwds),
                                 functionName=func.__name__)


    @override
    def isFullfilled(self):
        return self._nulladicFunction()


    @override
    def errorMessage(self):
        return "Predicate '%s' has failed." % self._functionName


class BarrierTimeout(Exception):

    def __init__(self, message):
        Exception.__init__(self, message)


class Barrier:

    @classmethod
    def waitUntil(cls, predicate, timeoutSec, period=0.5, timeModule=time):
        mustEnd = timeModule.time() + timeoutSec

        done= False
        while not done:
            ok= predicate()
            if ok:
                done= True
            elif timeModule.time() >= mustEnd:
                raise BarrierTimeout("Timeout occurred after %.1f s" %
                                     timeoutSec)
            else:
                timeModule.sleep(period)


    def __init__(self, timeoutSec, pollingPeriodSec=0.1, timeModule=time):
        self._timeoutSec= timeoutSec
        self._pollingPeriodSec= pollingPeriodSec
        self._timeModule= timeModule


    def waitFor(self, predicate):
        try:
            Barrier.waitUntil(
                predicate.isFullfilled, self._timeoutSec,
                self._pollingPeriodSec, self._timeModule)
        except BarrierTimeout:
            raise BarrierTimeout("Timeout occurred after %.1f s: %s" % (
                                 self._timeoutSec, predicate.errorMessage()))
