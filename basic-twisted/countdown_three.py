global_counter = 3

class Countdown(object):
    def count(self, counter=5, name='anonymous', time_delay=1):
        if counter == 0:
            global global_counter
            global_counter -= 1
            if global_counter == 0:
                reactor.stop()
        else:
            print counter, '... counted by', name
            counter -= 1
            reactor.callLater(time_delay, self.count, counter=counter, name=name, time_delay=time_delay)


from twisted.internet import reactor

reactor.callWhenRunning(Countdown().count, name='counter_1', time_delay=0.5)
reactor.callWhenRunning(Countdown().count, name='counter_2', time_delay=1)
reactor.callWhenRunning(Countdown().count, name='counter_2', time_delay=1.5)


print 'Start!'
reactor.run()
print 'Stop!'
