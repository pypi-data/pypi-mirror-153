from twisted.internet.protocol import Protocol, ClientFactory
from twisted.internet import reactor
import sys
from datetime import datetime


class Echo(Protocol):
    def __init__(self, factory):
        self.factory = factory

    def connectionMade(self):
        self.factory.num
        print("Connected to the server!")

    def dataReceived(self, data):
        print("got messages: ", data.decode())
        reactor.callLater(5, self.say_hello)

    def connectionLost(self, reason=connectionDone):
        print("Disconnected from the server!")

    def say_hello(self):
        if self.transport.connected:
            self.transport.write(u"hello, I'm {} {}".format(sys.argv[1], datetime.now()))
