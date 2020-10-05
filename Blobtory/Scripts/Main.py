from panda3d.core import loadPrcFile, loadPrcFileData
from direct.showbase.ShowBase import ShowBase, PTAFloat, AmbientLight, DirectionalLight

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

        self.planetGen: PlanetGenerator = PlanetGenerator(self.winCreator, 128, 500)
        self.planetGen.cubeformer.mouseTime.setData(PTAFloat([10, 0, 0, 1]))
        self.accept("a", self.planetGen.RegenPlanet)

        alight = AmbientLight('alight')
        alight.setColor((0.1, 0.1, 0.1, 1))
        alnp = self.render.attachNewNode(alight)
        self.render.setLight(alnp)

        dlight = DirectionalLight('my dlight')
        dlnp = self.render.attachNewNode(dlight)
        self.render.setLight(dlnp)

        dlight = DirectionalLight('my dlight')
        dlight.setColor((0.05, 0.05, 0.05, 1))
        dlnp = self.render.attachNewNode(dlight)
        dlnp.setHpr(0, 180, 0)
        self.render.setLight(dlnp)


loadPrcFileData('', 'framebuffer-multisample 1')
loadPrcFileData('', 'multisamples 0')
loadPrcFileData('', 'sync-video false')
loadPrcFile("config/Config.prc")
blobtoryBase = Main()
blobtoryBase.run()
