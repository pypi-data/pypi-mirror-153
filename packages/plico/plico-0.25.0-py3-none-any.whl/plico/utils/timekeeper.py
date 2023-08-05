import time


__version__= "$Id: timekeeper.py 25 2018-01-26 19:00:40Z lbusoni $"


class TimeKeeper(object):

    def __init__(self, interval=1.0, timeMod=time):
        self.interval = interval
        self.t0= timeMod.time()
        self.cnt = 0

    def inc(self):
        self.cnt +=1
        t1 = time.time()
        if (t1 - self.t0)>=self.interval:
            tdiff = t1 - self.t0
            self.rate = self.cnt / tdiff
            self.count = self.cnt
            self.ms = 1.0 / self.rate * 1e3
            self.cnt=0
            self.t0=t1
            return True
        return False
