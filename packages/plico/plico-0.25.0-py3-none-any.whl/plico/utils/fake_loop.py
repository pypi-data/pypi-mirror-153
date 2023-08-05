from plico.utils.loop import Loop
from plico.utils.decorator import override, returns

__version__= "$Id: fake_loop.py 25 2018-01-26 19:00:40Z lbusoni $"


class FakeLoop(Loop):

    def __init__(self):
        Loop.__init__(self)
        self._closed= False
        self._gain= -1.0
        self._convergenceStepCount= 0
        self._converged= False
        self._initialized= False


    @override
    def name(self):
        return "FakeLoop"


    def initialize(self):
        self._initialized= True


    def deinitialize(self):
        self._initialized= False
        self._closed= False
        self._converged= False


    @override
    def performOnePass(self):
        self._convergenceStepCount+= 1


    @override
    def close(self):
        self._convergenceStepCount+= 1
        self._closed= True


    @override
    def open(self):
        self._closed= False


    @override
    @returns(bool)
    def isClosed(self):
        return self._closed


    @returns(bool)
    def isInitialized(self):
        return self._initialized


    @override
    @returns(int)
    def getConvergenceStepCount(self):
        return self._convergenceStepCount


    def setConvergenceFlagTo(self, converged):
        self._converged= converged


    @override
    @returns(bool)
    def hasConverged(self):
        return self._converged
