from twisted.internet.task import LoopingCall

class Countdown(object):
    counter = 5

    def count(self):
        if self.counter == 0:
            reactor.stop()
        else:
            print self.counter, '...'
            self.counter -= 1
            # reactor.callLater(1, self.count)

from twisted.internet import reactor

print 'Start!'

lc = LoopingCall(Countdown().count)
lc.start(1)

reactor.run()
lc.stop()

print 'Stop!'
