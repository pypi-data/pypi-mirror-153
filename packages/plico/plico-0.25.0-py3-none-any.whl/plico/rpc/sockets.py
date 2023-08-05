#!/usr/bin/env/python
from plico.utils.decorator import cacheResult


__version__= "$Id: sockets.py 56 2018-09-14 16:42:15Z lbusoni $"



class Sockets():

    def __init__(self, ports, zmqRpc):
        self._zmqRpc= zmqRpc
        self._ports= ports


    @cacheResult
    def serverSubscriber(self):
        return self._zmqRpc.subscriberSocket(
            self._ports.SERVER_HOSTNAME,
            self._ports.SERVER_PUBLISHER_PORT, conflate=True)


    @cacheResult
    def serverSubscriberAddress(self):
        return self._zmqRpc.tcpAddress(
            self._ports.SERVER_HOSTNAME,
            self._ports.SERVER_PUBLISHER_PORT)


    @cacheResult
    def serverRequest(self):
        return self._zmqRpc.requestSocket(
            self._ports.SERVER_HOSTNAME, self._ports.SERVER_REPLY_PORT)


    @cacheResult
    def serverRequestAddress(self):
        return self._zmqRpc.tcpAddress(
            self._ports.SERVER_HOSTNAME,
            self._ports.SERVER_REPLY_PORT)


    @cacheResult
    def serverStatus(self):
        return self._zmqRpc.subscriberSocket(
            self._ports.SERVER_HOSTNAME,
            self._ports.SERVER_STATUS_PORT, conflate=True)


    @cacheResult
    def serverStatusAddress(self):
        return self._zmqRpc.tcpAddress(
            self._ports.SERVER_HOSTNAME,
            self._ports.SERVER_STATUS_PORT)


    @cacheResult
    def serverDisplay(self):
        return self._zmqRpc.subscriberSocket(
            self._ports.SERVER_HOSTNAME,
            self._ports.SERVER_DISPLAY_PORT, conflate=True)


    @cacheResult
    def serverDisplayAddress(self):
        return self._zmqRpc.tcpAddress(
            self._ports.SERVER_HOSTNAME,
            self._ports.SERVER_DISPLAY_PORT)
