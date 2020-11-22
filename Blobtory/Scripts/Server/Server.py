from direct.distributed.PyDatagramIterator import PyDatagramIterator
from panda3d.core import QueuedConnectionManager, QueuedConnectionListener, QueuedConnectionReader, ConnectionWriter
from panda3d.core import PointerToConnection, NetAddress, NetDatagram

from direct.task import Task

from Blobtory.Scripts.Pipeline.WindowCreator import WindowCreator


class Server:
    def __init__(self, winCreator: WindowCreator):
        self.winCreator = winCreator

        self.cManager = QueuedConnectionManager()
        self.cListener = QueuedConnectionListener(self.cManager, 0)
        self.cReader = QueuedConnectionReader(self.cManager, 0)
        self.cWriter = ConnectionWriter(self.cManager, 0)

        self.activeConnections = []  # We'll want to keep track of these later

        port_address = 25565  # No-other TCP/IP services are using this port
        backlog = 1000  # If we ignore 1,000 connection attempts, something is wrong!
        tcpSocket = self.cManager.openTCPServerRendezvous(port_address, backlog)

        self.cListener.addConnection(tcpSocket)

        self.winCreator.base.taskMgr.add(self.tskListenerPolling, "Poll the connection listener", -39)
        self.winCreator.base.taskMgr.add(self.tskReaderPolling, "Poll the connection reader", -40)

    def tskListenerPolling(self, taskdata):
        if self.cListener.newConnectionAvailable():

            rendezvous = PointerToConnection()
            netAddress = NetAddress()
            newConnection = PointerToConnection()

            if self.cListener.getNewConnection(rendezvous, netAddress, newConnection):
                newConnection = newConnection.p()
                self.activeConnections.append(newConnection)  # Remember connection
                self.cReader.addConnection(newConnection)  # Begin reading connection
        return Task.cont

    def tskReaderPolling(self, taskdata):
        if self.cReader.dataAvailable():
            datagram = NetDatagram()  # catch the incoming data in this instance
            # Check the return value; if we were threaded, someone else could have
            # snagged this data before we did
            if self.cReader.getData(datagram):
                self.myProcessDataFunction(datagram)
        return Task.cont

    def myProcessDataFunction(self, datagram):
        myIterator = PyDatagramIterator(datagram)
        msgID = myIterator.getUint8()
        if msgID == 1:
            messageToPrint = myIterator.getString()
            print(messageToPrint)
