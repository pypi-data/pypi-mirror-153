from plico.rpc.abstract_remote_procedure_call import AbstractRemoteProcedureCall
from plico.utils.decorator import override


class DummyRpcHandler(AbstractRemoteProcedureCall):

    def __init__(self):
        pass


    @override
    def sendRequest(self):
        pass


    @override
    def handleRequest(self):
        pass


    @override
    def recvCameraFrame(self):
        pass


    @override
    def sendCameraFrame(self):
        pass


    @override
    def publishPickable(self):
        pass


    @override
    def receivePickable(self):
        pass
