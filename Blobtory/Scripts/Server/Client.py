from direct.distributed.PyDatagram import PyDatagram
from panda3d.core import QueuedConnectionManager, QueuedConnectionListener, QueuedConnectionReader, ConnectionWriter
from panda3d.core import PointerToConnection, NetAddress, NetDatagram

from Blobtory.Scripts.Pipeline.WindowCreator import WindowCreator

class Client:
    def __init__(self, winCreator: WindowCreator):
        self.cManager = QueuedConnectionManager()
        self.cReader = QueuedConnectionReader(self.cManager, 0)
        self.cWriter = ConnectionWriter(self.cManager, 0)

        port_address = 25565
        ip_address = "localhost"
        timeout = 3000  # 3 seconds

        myConnection = self.cManager.openTCPClientConnection(ip_address, port_address, timeout)
        if myConnection:
            self.cReader.addConnection(myConnection)  # receive messages from server

            myPyDatagram = PyDatagram()
            myPyDatagram.addUint8(1)
            myPyDatagram.addString("Hello, world!")

            self.cWriter.send(myPyDatagram, myConnection)
