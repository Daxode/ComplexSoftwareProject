from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator
from direct.task import Task
from panda3d.core import QueuedConnectionManager, QueuedConnectionListener, QueuedConnectionReader, ConnectionWriter
from panda3d.core import PointerToConnection, NetAddress, NetDatagram

from Blobtory.Scripts.Pipeline.WindowCreator import WindowCreator
from Blobtory.Scripts.game.SceneBuilder import SceneBuilder


class Client:
    def __init__(self, winCreator: WindowCreator, scene: SceneBuilder):
        self.winCreator = winCreator
        self.scene = scene
        self.cManager = QueuedConnectionManager()
        self.cReader = QueuedConnectionReader(self.cManager, 0)
        self.cWriter = ConnectionWriter(self.cManager, 0)

        port_address = 25565
        ip_address = "localhost"
        timeout = 3000  # 3 seconds

        self.winCreator.base.taskMgr.add(self.tskReaderPolling, "Poll the connection reader", -41)

        self.myConnection = self.cManager.openTCPClientConnection(ip_address, port_address, timeout)
        if self.myConnection:
            self.cReader.addConnection(self.myConnection)  # receive messages from server

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
            if "Go" in messageToPrint:
                if "Next" in messageToPrint:
                    print("yay it worked")
                    self.scene.planetGen.NextPoint()

            print(messageToPrint)

    def GoNextMsg(self):
        myPyDatagram = PyDatagram()
        myPyDatagram.addUint8(1)
        myPyDatagram.addString("Go Next")
        self.cWriter.send(myPyDatagram, self.myConnection)
