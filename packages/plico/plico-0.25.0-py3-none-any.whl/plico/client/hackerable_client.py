from plico.rpc.abstract_remote_procedure_call import \
    AbstractRemoteProcedureCall
from plico.utils.timeout import Timeout


__version__= "$Id: hackerable_client.py 28 2018-01-27 08:54:00Z lbusoni $"


class HackerableClient(object):


    def __init__(self,
                 rpcHandler,
                 requestSocket,
                 logger):
        assert isinstance(rpcHandler, AbstractRemoteProcedureCall)

        self._rpcHandler= rpcHandler
        self._requestSocket= requestSocket
        self._logger= logger



    def eval(self, expression, timeoutInSec=Timeout.MIRROR_EVAL):
        self._logger.warn("Eval is considered evil")
        return self._rpcHandler.sendRequest(
            self._requestSocket, 'eval',
            [expression], timeout=timeoutInSec)


    def execute(self,
                statement,
                timeoutInSec=Timeout.MIRROR_EXECUTE):
        self._logger.warn("Execute is for commissioning only")
        return self._rpcHandler.sendRequest(
            self._requestSocket, 'execute',
            [statement], timeout=timeoutInSec)
