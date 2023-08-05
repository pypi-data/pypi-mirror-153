'''
Created on Nov 5, 2019

@author: lbusoni
'''

import logging


def setUpLogger(filePath, loggingLevel):
    import logging.handlers
    FORMAT = '%(asctime)s %(levelname)s %(name)s %(message)s'
    f = logging.Formatter(fmt=FORMAT)
    handler = logging.handlers.RotatingFileHandler(
        filePath, encoding='utf8', maxBytes=1000, backupCount=3)
    root_logger = logging.getLogger()
    root_logger.setLevel(loggingLevel)
    handler.setFormatter(f)
    handler.setLevel(loggingLevel)
    root_logger.addHandler(handler)
    handler.doRollover()


def pippo(a):
    logger = logging.getLogger('IlLoggerDiPippo')
    logger.debug('debug mi hai passato %d' % a)
    if a < 0:
        logger.error('error a<0 (a=%g)' % a)


class Pluto():

    def __init__(self):
        self._logger = logging.getLogger('PLUTO')

    def funz1(self, a):
        self._logger.debug('debug mi hai passato %d' % a)
        if a < 0:
            self._logger.error('error a<0 (a=%g)' % a)
