# This is the Twisted Poetry Transform Server, version 1.0

import optparse

from twisted.internet.protocol import ServerFactory
from twisted.protocols.basic import NetstringReceiver


def parse_args():
    usage = """usage: %prog [options]

This is the Poetry Transform Server.
Run it like this:

  python transformedpoetry.py

If you are in the base directory of the twisted-intro package,
you could run it like this:

  python solutions/part-12/task_3/transformedpoetry.py --port1 11000 --port2 11001

to provide poetry transformation on port 11000.
"""

    parser = optparse.OptionParser(usage)

    help = "The port to listen on. Default to a random available port."
    parser.add_option('--port1', type='int', help=help)

    help = "The port to listen on. Default to a random available port."
    parser.add_option('--port2', type='int', help=help)

    help = "The interface to listen on. Default is localhost."
    parser.add_option('--iface', help=help, default='localhost')

    options, args = parser.parse_args()

    if len(args) != 0:
        parser.error('Bad arguments.')

    return options


class TransformService(object):

    def cummingsify(self, poem):
        return poem.lower()

    def reversify(self, poem):
        """
        return original poem written backward
        """
        return poem[::-1]


class TransformProtocol1(NetstringReceiver):

    def stringReceived(self, request):
        if '.' not in request: # bad request
            self.transport.loseConnection()
            return

        xform_name, poem = request.split('.', 1)

        self.xformRequestReceived(xform_name, poem)

    def xformRequestReceived(self, xform_name, poem):
        new_poem = self.factory.transform(xform_name, poem)

        if new_poem is not None:
            self.sendString(new_poem)

        self.transport.loseConnection()


class TransformProtocol2(NetstringReceiver):

    def stringReceived(self, request):
        if '_' not in request: # bad request
            self.transport.loseConnection()
            return

        xform_name, poem = request.split('_', 1)

        self.xformRequestReceived(xform_name, poem)

    def xformRequestReceived(self, xform_name, poem):
        new_poem = self.factory.transform(xform_name, poem)

        if new_poem is not None:
            self.sendString(new_poem)

        self.transport.loseConnection()


class TransformFactory(ServerFactory):
    def __init__(self, service, protocol):
        self.service = service
        self.protocol = protocol

    def transform(self, xform_name, poem):
        thunk = getattr(self, 'xform_%s' % (xform_name,), None)

        if thunk is None: # no such transform
            return None

        try:
            return thunk(poem)
        except:
            return None # transform failed

    def xform_cummingsify(self, poem):
        return self.service.cummingsify(poem)

    def xform_reversify(self, poem):
        return self.service.reversify(poem)


def main():
    options = parse_args()

    service = TransformService()

    factory1 = TransformFactory(service, TransformProtocol1)
    factory2 = TransformFactory(service, TransformProtocol2)

    from twisted.internet import reactor

    port1 = reactor.listenTCP(options.port1 or 0, factory1, interface=options.iface)

    port2 = reactor.listenTCP(options.port2 or 8000, factory2, interface=options.iface)

    print 'Serving transforms on \n\t%s\n\t%s.' % (port1.getHost(), port2.getHost())

    reactor.run()


if __name__ == '__main__':
    main()
