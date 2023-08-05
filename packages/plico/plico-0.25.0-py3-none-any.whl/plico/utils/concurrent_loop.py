import threading
from plico.utils.logger import Logger
from plico.utils.decorator import override, synchronized, returns
from plico.utils.loop import Loop


class WorkerThread(threading.Thread):

    def __init__(self, name,
                 closedFunc,
                 convergable,
                 interStepTimeSec,
                 stepCounter,
                 logFailureFunc):
        threading.Thread.__init__(self)
        self._name = name
        self._closedFunc = closedFunc
        self._convergable = convergable
        self._stopDurationLimitSec = 5
        self._stepCounter = stepCounter
        self._logFailureFunc = logFailureFunc
        self._interStepTimeSec = interStepTimeSec

        self._runEnabled = True
        self._runEnabledCondition = threading.Condition()
        self._doneEvent = threading.Event()
        self._logger = Logger.of("ConcurrentLoop.WorkerThread")

    @override
    def run(self):
        while self._isRunEnabled():
            try:
                self._step()
            except Exception as e:
                # import traceback; traceback.print_exc()
                self._logFailureFunc(str(e))
            self._waitForNextStep()
        self._flagAsDone()

    @synchronized("_runEnabledCondition")
    def _waitForNextStep(self):
        if self._runEnabled:
            self._runEnabledCondition.wait(self._interStepTimeSec)

    def _markAsClosed(self):
        self._openEvent.clear()
        self._closeEvent.set()

    def _markAsOpen(self):
        self._openEvent.set()
        self._closeEvent.clear()

    def _step(self):
        if self._closedFunc():
            self._stepCounter.inc()
            self._convergable.performOneConvergenceStep()
        else:
            self._convergable.measureConvergence()

    def _flagAsDone(self):
        self._doneEvent.set()
        assert self._doneEvent.isSet()

    def _isDone(self):
        return self._doneEvent.isSet()

    @synchronized("_runEnabledCondition")
    def _isRunEnabled(self):
        return self._runEnabled

    @synchronized("_runEnabledCondition")
    def _disableRun(self):
        self._runEnabled = False
        self._runEnabledCondition.notifyAll()

    def setStopDurationLimitSec(self, limitSec):
        self._stopDurationLimitSec = limitSec

    def _waitForDone(self):
        self._doneEvent.wait(self._stopDurationLimitSec)
        if not self._isDone():
            raise ConcurrentLoopException(
                "Failed to stop %s within limit of %.3f s" % (
                    self._name, self._stopDurationLimitSec))
        assert self._isDone()

    def stop(self):
        self._logger.notice("Stopping ...")
        self._disableRun()
        self._waitForDone()
        self._logger.notice("Stopped.")


class ConcurrentLoopException(Exception):
    pass


class ThreadSafeStepCounter(object):

    def __init__(self):
        self._cnt = 0
        self._mtx = threading.Lock()

    @synchronized("_mtx")
    def inc(self):
        self._cnt += 1

    @synchronized("_mtx")
    def getCount(self):
        return self._cnt


class ConcurrentLoop(Loop):

    def __init__(self, name, convergable, interStepTimeSec, logFailureFunc):
        Loop.__init__(self)
        self._name = name
        self._convergable = convergable
        self._interStepTimeSec = interStepTimeSec
        self._logFailureFunc = logFailureFunc

        self._closed = False
        self._closedMtx = threading.Lock()
        self._logger = Logger.of("ConcurrentLoop")
        self._mtx = threading.Lock()
        self._stopDurationLimitSec = 5
        self._worker = None
        self._stepCounter = ThreadSafeStepCounter()
        self._initialized = False

    @synchronized("_mtx")
    def isInitialized(self):
        return self._initialized

    def initialize(self):
        if not self.isInitialized():
            self._startWorkerThread()
            with self._mtx:
                self._initialized = True

    def _startWorkerThread(self):
        assert self._worker is None
        self._worker = WorkerThread("Worker thread for %s" % self.name(),
                                    self.isClosed, self._convergable,
                                    self._interStepTimeSec,
                                    self._stepCounter,
                                    self._logFailureFunc)
        self._worker.setStopDurationLimitSec(self._stopDurationLimitSec)
        self._worker.start()
        self._logger.notice("Worker thread is started.")

    @override
    def name(self):
        return self._name

    @override
    def performOnePass(self):
        if self.isInitialized():
            if not self.isClosed():
                self._stepCounter.inc()
                self._convergable.performOneConvergenceStep()
            else:
                raise Exception("Loop is closed")
        else:
            self._logger.error("%s is not yet initialized" % self._name)
#             raise Exception("%s is not yet initialized" % self._name)

    @synchronized("_mtx")
    @override
    def close(self):
        if self._initialized:
            self._flagAsClosed()
        else:
            self._logger.error("%s is not yet initialized" % self._name)
#             raise Exception("%s is not yet initialized" % self._name)

    @synchronized("_mtx")
    def setStopDurationLimitSec(self, durationSec):
        self._stopDurationLimitSec = durationSec
        if self._worker:
            self._worker.setStopDurationLimitSec(durationSec)

    @synchronized("_mtx")
    @override
    def open(self):
        if self._initialized:
            self._flagAsOpen()
        else:
            self._logger.error("%s is not yet initialized" % self._name)

    @synchronized("_closedMtx")
    def _flagAsClosed(self):
        self._closed = True

    @synchronized("_closedMtx")
    def _flagAsOpen(self):
        self._closed = False

    @synchronized("_closedMtx")
    @override
    @returns(bool)
    def isClosed(self):
        return self._closed

    @override
    @returns(int)
    def getConvergenceStepCount(self):
        return self._stepCounter.getCount()

    @override
    def hasConverged(self):
        return self._convergable.hasConverged()

    def _stopWorkerThread(self):
        self._worker.stop()
        self._worker.join(self._stopDurationLimitSec)
        assert not self._worker.is_alive()
        self._worker = None

    def deinitialize(self):
        self._logger.debug("Deinitializing ...")
        if self._worker is not None:
            self._stopWorkerThread()
        with self._mtx:
            self._initialized = False
            self._closed = False
            self._worker = None
            self._logger.notice("Loop is deinitialized.")
