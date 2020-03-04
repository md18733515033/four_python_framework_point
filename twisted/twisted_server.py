from twisted.internet import reactor
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet.protocol import Protocol, Factory

# 保存客户端的连接,(即Protocol子类Spreader的实例)
clients = []


class Spreader(Protocol):

    def __init__(self, factory):
        self.factory = factory
        self.connect_id = None

    def connectionMade(self):
        """对连接的client进行计数,并且将self保存到clients中"""
        self.factory.numProtocols = self.factory.numProtocols + 1
        self.connect_id = self.factory.numProtocols
        self.transport.write((u"欢迎来到spread site,您是第%d个客户端用户!\n" % self.factory.numProtocols).encode('utf-8'))
        print("new connect: %d" % self.factory.numProtocols)
        clients.append(self)

    def connectionLost(self, reason):
        """断开时执行的操作"""
        clients.remove(self)
        print("lose connect: %d" % self.connect_id)

    def dataReceived(self, data):
        print("dataReceived() entered!")
        if data == "close":
            # 如果data = close,主动关闭与客户端的连接
            self.transport.loseConnection()
            print("%s closed" % self.connect_id)
        else:
            print("spreading message from %s : %s" % (self.connect_id, data))
            # 轮询所有的客户端,将收到的数据通过Protocol.transport.write()函数发送给除了自己的客户端
            for client in clients:
                if client != self:
                    client.transport.write(data)


class SpreadFactory(Factory):
    def __init__(self):
        self.numProtocols = 0

    def buildProtocol(self, addr):
        return Spreader(self)


endpoint = TCP4ServerEndpoint(reactor, 8007)
endpoint.listen(SpreadFactory())
reactor.run()
