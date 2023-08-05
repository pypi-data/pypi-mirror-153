from plico.utils.constants import Constants

__version__= "$Id: zmq_ports.py 56 2018-09-14 16:42:15Z lbusoni $"



class ZmqPorts(object):

    def __init__(self, hostname, basePort):
        self._hostname= hostname
        self._basePort= basePort


    @staticmethod
    def fromConfiguration(configuration, configSection):
        hostname= configuration.networkHostName(configSection)
        basePort= configuration.basePort(configSection)
        return ZmqPorts(hostname, basePort)


    @property
    def SERVER_REPLY_PORT(self):
        return self._basePort + Constants.PORT_REPLY_OFFSET


    @property
    def SERVER_STATUS_PORT(self):
        return self._basePort + Constants.PORT_STATUS_OFFSET


    @property
    def SERVER_PUBLISHER_PORT(self):
        return self._basePort + Constants.PORT_PUBLISHER_OFFSET


    @property
    def SERVER_DISPLAY_PORT(self):
        return self._basePort + Constants.PORT_DISPLAY_OFFSET


    @property
    def SERVER_HOSTNAME(self):
        return self._hostname
