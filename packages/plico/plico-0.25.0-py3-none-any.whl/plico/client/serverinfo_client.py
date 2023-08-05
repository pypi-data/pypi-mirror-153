from plico.rpc.abstract_remote_procedure_call import \
    AbstractRemoteProcedureCall
from plico.utils.timeout import Timeout


__version__= "$Id: serverinfo_client.py 35 2018-01-28 13:33:16Z lbusoni $"


class ServerInfoClient(object):


    def __init__(self,
                 rpcHandler,
                 requestSocket,
                 logger):
        assert isinstance(rpcHandler, AbstractRemoteProcedureCall)

        self._rpcHandler= rpcHandler
        self._requestSocket= requestSocket
        self._logger= logger



    def serverInfo(self, timeoutInSec=Timeout.SERVER_INFO):
        return self._rpcHandler.sendRequest(
            self._requestSocket, 'serverInfo',
            [], timeout=timeoutInSec)
