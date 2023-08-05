
class DummySockets(object):

    def __init__(self, prefix='dummySocket'):
        self._prefix= prefix

    def serverSubscriber(self):
        return "%s-%s" % (self._prefix, 'subscriber')

    def serverSubscriberAddress(self):
        return "%s-%s" % (self._prefix, 'subscriberAddress')

    def serverRequest(self):
        return "%s-%s" % (self._prefix, 'request')

    def serverRequestAddress(self):
        return "%s-%s" % (self._prefix, 'requestAddress')

    def serverStatus(self):
        return "%s-%s" % (self._prefix, 'status')

    def serverStatusAddress(self):
        return "%s-%s" % (self._prefix, 'statusAddress')

    def serverDisplay(self):
        return "%s-%s" % (self._prefix, 'display')

    def serverDisplayAddress(self):
        return "%s-%s" % (self._prefix, 'displayAddress')

