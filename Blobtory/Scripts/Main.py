from direct.task import Task
from panda3d.core import loadPrcFile, loadPrcFileData
from direct.showbase.ShowBase import ShowBase, PTAFloat, \
    DirectionalLight, AntialiasAttrib, AmbientLight

from Blobtory.Scripts.Pipeline.WindowCreator import WindowCreator

# Description:
# This is the main program, and should thus be kept clean,
# so stuff doesn't get out of control
#
# Author:  Daniel Kierkegaard Andersen (dax@daxode.dk)
# Version: 2020-09-22
#
# Copyright (c) 2020 Daniel Kierkegaard Andersen. All rights reserved.
# https://github.com/Daxode/ComplexSoftwareProject
from Blobtory.Scripts.planet_former.PlanetGenerator import PlanetGenerator


class Main(ShowBase):
    def __init__(self):
        super().__init__()
        self.winCreator = WindowCreator(self, enableRP=False, isFullscreen=False)

        self.planetGen: PlanetGenerator = PlanetGenerator(self.winCreator, 128, 150)
        self.planetGen.cubeformer.mouseTime.setData(PTAFloat([10, 0, 0, 1]))
        self.accept("a", self.planetGen.RegenPlanet)

        alight = AmbientLight('alight')
        alight.setColor((0.6, 0.6, 0.6, 1))
        alnp = self.render.attachNewNode(alight)
        self.render.setLight(alnp)


loadPrcFileData('', 'framebuffer-multisample 1')
loadPrcFileData('', 'multisamples 1')
loadPrcFile("config/Config.prc")
blobtoryBase = Main()
blobtoryBase.run()
