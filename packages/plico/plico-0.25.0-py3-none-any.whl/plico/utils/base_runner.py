from __future__ import print_function

import logging.handlers
import os
import sys
import signal
from plico.utils.configuration import Configuration
from plico.rpc.zmq_remote_procedure_call import ZmqRemoteProcedureCall
from plico.rpc.sockets import Sockets
from plico.rpc.zmq_ports import ZmqPorts


class BaseRunner(object):

    def __init__(self):
        INITIALIZED_LATER = None
        self._configFilePath = INITIALIZED_LATER
        self._rpc = INITIALIZED_LATER
        self._configuration = INITIALIZED_LATER
        self._sockets = INITIALIZED_LATER
        self._argv = INITIALIZED_LATER

    def _logRunning(self):
        self._logger.notice(self.RUNNING_MESSAGE)
        sys.stdout.flush()

    def _createFoldersIfMissing(self, filename):
        if not os.path.isdir(os.path.dirname(filename)):
            os.makedirs(os.path.dirname(filename))

    def _determineLoggingLevel(self):
        try:
            levelAsStr = self._configuration.logLevel(
                self._configurationSection)
        except KeyError:
            levelAsStr = 'debug'
        if levelAsStr == 'fatal':
            loggingLevel = logging.CRITICAL
        elif levelAsStr == 'error':
            loggingLevel = logging.ERROR
        elif levelAsStr == 'warning':
            loggingLevel = logging.WARNING
        elif levelAsStr == 'info':
            loggingLevel = logging.INFO
        elif levelAsStr == 'debug':
            loggingLevel = logging.DEBUG
        else:
            loggingLevel = logging.WARNING
        return loggingLevel

    def _setUpLogging(self, logFilePath):
        loggingLevel = self._determineLoggingLevel()
        print(('Setting up logging in file %s level %s' % (
            logFilePath, loggingLevel)))
        self._createFoldersIfMissing(logFilePath)
        FORMAT = '%(asctime)s %(levelname)s %(message)s'
        f = logging.Formatter(fmt=FORMAT)
        rotHandler = logging.handlers.RotatingFileHandler(
            logFilePath, encoding='utf8',
            maxBytes=10000000, backupCount=10)
        handlers = [rotHandler]
        root_logger = logging.getLogger()
        root_logger.setLevel(loggingLevel)
        for h in handlers:
            h.setFormatter(f)
            h.setLevel(loggingLevel)
            root_logger.addHandler(h)
        rotHandler.doRollover()

    def _createConfiguration(self):
        self._configuration = Configuration()
        self._configuration.load(self._configFilePath)

    def _createZmqBasedRPC(self):
        zmqPorts = ZmqPorts.fromConfiguration(self._configuration,
                                              self._configurationSection)
        self._rpc = ZmqRemoteProcedureCall()
        self._sockets = Sockets(zmqPorts, self._rpc)

    def _checkCommandLine(self, argv):
        if 3 > len(argv):
            programName = argv[0]
            print("Usage:", file=sys.stderr)
            print("\t%s <configuration_file> <configuration_section>" %
                  programName, file=sys.stderr)
            print("Example:", file=sys.stderr)
            print(("\t%s /home/plico/.plico/plico.conf") %
                  programName, file=sys.stderr)
            print("\nargv was: %s" % str(argv))
            sys.exit(os.EX_USAGE)
        print('argv: %s' % str(argv))

    def _parseCommandLine(self, argv):
        self._checkCommandLine(argv)
        self._configFilePath = argv[1]
        self._configurationSection = argv[2]

    def _logFilePath(self):
        return os.path.join(self._configuration.loggingDir(),
                            '%s.log' % self._configurationSection)

    def start(self, argv):
        self._argv = argv
        self._parseCommandLine(argv)
        self._createConfiguration()
        self._setUpLogging(self._logFilePath())
        self._createZmqBasedRPC()
        self._registerHandlers()
        return self.run()

    def run(self):
        pass

    def getConfigFilePath(self):
        return self._configFilePath

    @property
    def name(self):
        return self._configuration.getValue(
            self._configurationSection,
            'name')

    @property
    def configuration(self):
        return self._configuration

    def getConfigurationSection(self):
        return self._configurationSection

    def rpc(self):
        return self._rpc

    def sockets(self):
        return self._sockets

    def argv(self):
        return self._argv

    def terminate(self, signal, frame):
        pass

    def _registerHandlerForSigInt(self):
        signal.signal(signal.SIGINT, self.terminate)

    def _registerHandlerForSigTerm(self):
        signal.signal(signal.SIGTERM, self.terminate)

    def _registerHandlerForSigKill(self):
        try:
            signal.signal(signal.SIGKILL, self.terminate)
        except Exception:
            pass

    def _registerHandlers(self):
        self._registerHandlerForSigInt()
        self._registerHandlerForSigTerm()
        self._registerHandlerForSigKill()
