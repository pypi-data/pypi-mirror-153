from plico.utils.logger import Logger


__version__= "$Id: hackerable.py 25 2018-01-26 19:00:40Z lbusoni $"


class Hackerable(object):

    def __init__(self, logger=None):
        self._hackerableExecuteCnt= 0
        self._hackerableEvalCnt= 0
        if logger is None:
            self._logger= Logger.of('Hackerable')


    def eval(self, expression):
        self._logger.warn("Evaluating '%s' (counter: %d)" % (
            expression, self._hackerableEvalCnt))
        self._hackerableEvalCnt+= 1
        return repr(eval(expression))


    def execute(self, statement):
        self._logger.warn("Executing '%s' (counter: %d)" % (
            statement, self._hackerableExecuteCnt))
        self._hackerableExecuteCnt+= 1
        exec(statement)
