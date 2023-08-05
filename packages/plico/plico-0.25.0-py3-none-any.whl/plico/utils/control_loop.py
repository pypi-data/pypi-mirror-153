
import abc
import time
import traceback
from six import with_metaclass

__version__= "$Id: control_loop.py 25 2018-01-26 19:00:40Z lbusoni $"


class ControlLoop(with_metaclass(abc.ABCMeta, object)):
    @abc.abstractmethod
    def start(self):
        assert False, "Abstract method"


class FaultTolerantControlLoop(ControlLoop):

    def __init__(self,
                 steppable,
                 logger,
                 timeModule=time,
                 loopPeriodInSecond=1):
        self._steppable= steppable
        self._logger= logger
        self._timeModule= timeModule
        self._loopPeriodSec= loopPeriodInSecond


    def start(self):
        while self._isAlive():
            try:
                self._steppable.step()
            except Exception as e:
                traceback.print_exc()
                self._logger.error(str(e))
            self._timeModule.sleep(self._loopPeriodSec)


    def _isAlive(self):
        return not self._steppable.isTerminated()


class IntolerantControlLoop(ControlLoop):

    def __init__(self,
                 steppable,
                 logger,
                 timeModule=time,
                 loopPeriodInSecond=1):
        self._steppable= steppable
        self._logger= logger
        self._timeModule= timeModule
        self._loopPeriodSec= loopPeriodInSecond

    def start(self):
        while self._isAlive():
            self._steppable.step()
            self._timeModule.sleep(self._loopPeriodSec)

    def _isAlive(self):
        return not self._steppable.isTerminated()
