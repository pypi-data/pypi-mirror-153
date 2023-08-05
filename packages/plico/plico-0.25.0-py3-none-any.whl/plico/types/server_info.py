

__version__= "$Id:$"



class ServerInfo(object):

    def __init__(self,
                 name,
                 uptimeInSec,
                 hostname,
                 replyPort):
        self.name= name
        self.uptimeInSec= uptimeInSec
        self.hostname= hostname
        self.replyPort= replyPort


    def __repr__(self):
        return "Name: %s, Uptime: %g, Hostname: %s:%s" % (
            self.name,
            self.uptimeInSec,
            self.hostname,
            self.replyPort)
