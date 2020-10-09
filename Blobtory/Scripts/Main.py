from panda3d.core import loadPrcFile, loadPrcFileData
from direct.showbase.ShowBase import ShowBase

from Blobtory.Scripts.Pipeline.WindowCreator import WindowCreator
from Blobtory.Scripts.game.SceneBuilder import SceneBuilder

# Description:
# This is the main program, and should thus be kept clean,
# so stuff doesn't get out of control
#
# Author:  Daniel Kierkegaard Andersen (dax@daxode.dk)
# Version: 2020-09-22
#
# Copyright (c) 2020 Daniel Kierkegaard Andersen. All rights reserved.
# https://github.com/Daxode/ComplexSoftwareProject


class Main(ShowBase):
    def __init__(self):
        super().__init__()
        self.winCreator = WindowCreator(self, enableRP=False, isFullscreen=False)
        self.scene: SceneBuilder = SceneBuilder(self.winCreator)


loadPrcFileData('', 'framebuffer-multisample 0')
loadPrcFileData('', 'multisamples 1')
loadPrcFileData('', 'sync-video false')
loadPrcFile("config/Config.prc")
blobtoryBase = Main()
blobtoryBase.run()
