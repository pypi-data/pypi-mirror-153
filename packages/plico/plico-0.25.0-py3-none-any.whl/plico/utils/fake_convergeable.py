import threading
import time
from plico.utils.decorator import override, synchronized, returns
from plico.utils.convergeable import Convergeable


class FakeConvergeable(Convergeable):

    def __init__(self):
        Convergeable.__init__(self)
        self._gain = 0.0
        self._convergenceStepInvocationCnt = 0
        self._measureConvergenceInvocationCnt = 0
        self._stepSleepDurationSec = 0
        self._mtx = threading.Lock()
        self._condition = threading.Condition()
        self._stepBlockingEnabled = False
        self._exceptionRequested = False
        self._converged = False

    @override
    def name(self):
        return "FakeConvergeable"

    def setAsConverged(self):
        self._converged = True

    def setAsUnconverged(self):
        self._converged = False

    def _panicIfRequested(self):
        if self._exceptionRequested:
            raise Exception("Exception is desired")

    @override
    def performOneConvergenceStep(self):
        self._incrementStepCount()
        self._panicIfRequested()
        time.sleep(self._stepSleepDurationSec)
        self._blockIfAny()

    @synchronized("_mtx")
    @override
    def measureConvergence(self):
        self._measureConvergenceInvocationCnt += 1
        self._panicIfRequested()

    def getMeasureConvergenceCount(self):
        return self._measureConvergenceInvocationCnt

    def requestPanic(self):
        self._exceptionRequested = True

    @synchronized("_condition")
    def unblockStep(self):
        self._condition.notifyAll()
        self._stepBlockingEnabled = False

    @synchronized("_condition")
    def blockStep(self):
        self._stepBlockingEnabled = True

    @synchronized("_condition")
    def _blockIfAny(self):
        if self._stepBlockingEnabled:
            self._condition.wait()

    def setStepSleepDurationSec(self, durationSec):
        self._stepSleepDurationSec = durationSec

    @synchronized("_mtx")
    def _incrementStepCount(self):
        self._convergenceStepInvocationCnt += 1

    @synchronized("_mtx")
    def getConvergenceStepCount(self):
        return self._convergenceStepInvocationCnt

    @returns(bool)
    def hasConverged(self):
        return self._converged
