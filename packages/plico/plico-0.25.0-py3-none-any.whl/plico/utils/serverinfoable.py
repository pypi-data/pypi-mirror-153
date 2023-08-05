import time
from plico.types.server_info import ServerInfo
from plico.utils.logger import Logger


__version__= "$Id: deformable_mirror_controller.py 26 2018-01-26 19:06:25Z lbusoni $"


class ServerInfoable(object):

    def __init__(self, name, ports, logger=None):
        self._serverName= name
        self._creationTime= time.time()
        self._ports= ports
        if logger is None:
            self._logger= Logger.of('ServerInfoable')


    def serverInfo(self):
        return ServerInfo(
            self._serverName,
            time.time() - self._creationTime,
            self._ports.SERVER_HOSTNAME,
            self._ports.SERVER_REPLY_PORT)
