from panda3d.core import loadPrcFile, loadPrcFileData
from panda3d.core import PointerToConnection, NetAddress, NetDatagram

from direct.showbase.ShowBase import ShowBase

from Blobtory.Scripts.Pipeline.WindowCreator import WindowCreator
from Blobtory.Scripts.game.SceneBuilder import SceneBuilder
from Blobtory.Scripts.Server import Server, Client
# Description:
# This is the main program, and should thus be kept clean,
# so stuff doesn't get out of control
#
# Author:  Daniel Kierkegaard Andersen (dax@daxode.dk)
# Version: 2020-10-24
#
# Copyright (c) 2020 Daniel Kierkegaard Andersen. All rights reserved.
# https://github.com/Daxode/ComplexSoftwareProject


class Main(ShowBase):
    server: Server.Server
    client: Client.Client

    def __init__(self):
        super().__init__()
        self.winCreator = WindowCreator(self, enableRP=False, isFullscreen=False)
        self.scene: SceneBuilder = SceneBuilder(self.winCreator)
        self.accept("c", self.ConnectClient)
        self.accept("v", self.StartServer)

    def StartServer(self):
        self.server: Server = Server.Server(self.winCreator)

    def ConnectClient(self):
        self.client = Client.Client(self.winCreator)


loadPrcFileData('', 'framebuffer-srgb #t')
loadPrcFileData('', 'framebuffer-multisample 0')
loadPrcFileData('', 'multisamples 1')
loadPrcFileData('', 'sync-video false')
loadPrcFile("config/Config.prc")
blobtoryBase = Main()
blobtoryBase.run()
