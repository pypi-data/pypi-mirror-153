import abc
from plico.utils.decorator import returnsNone
from six import with_metaclass

__version__= "$Id: abstract_remote_procedure_call.py 25 2018-01-26 19:00:40Z lbusoni $"


class AbstractRemoteProcedureCall(with_metaclass(abc.ABCMeta, object)):
    @abc.abstractmethod
    @returnsNone
    def sendRequest(self):
        assert False


    @abc.abstractmethod
    def handleRequest(self):
        assert False


    @abc.abstractmethod
    def recvCameraFrame(self):
        assert False


    @abc.abstractmethod
    @returnsNone
    def sendCameraFrame(self):
        assert False


    @abc.abstractmethod
    @returnsNone
    def publishPickable(self, socket, pickableObject):
        assert False


    @abc.abstractmethod
    def receivePickable(self, socket, timeoutInSec=10):
        assert False
