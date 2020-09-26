from direct.task import Task
from panda3d.core import loadPrcFile
from direct.showbase.ShowBase import ShowBase, PTAFloat, \
    DirectionalLight, AntialiasAttrib

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
from Blobtory.Scripts.planet_former.CubeFormer import CubeFormer
from Blobtory.Scripts.planet_former.MarchingCubes import MarchingCubes


class Main(ShowBase):
    def __init__(self):
        super().__init__()
        self.winCreator = WindowCreator(self, enableRP=False, isFullscreen=False)
        self.taskMgr.add(self.SpinCameraTask, "Move Cam")

        size = 64
        spacing = 4
        dlight = DirectionalLight('my dlight')
        dlight.setColor((0.8, 0.8, 0.5, 1))
        self.dlnp = self.render.attachNewNode(dlight)
        self.render.setAntialias(AntialiasAttrib.MAuto)
        self.render.setLight(self.dlnp)

        self.cubeformer: CubeFormer = CubeFormer(self.winCreator, size, size, size, spacing)
        self.cubeformer.GenerateCube()
        self.cubeformer.GenerateNoiseSphere(50)
        self.marchingCubes: MarchingCubes = MarchingCubes(self.cubeformer)
        self.marchingCubes.EdgeGenerator()
        self.marchingCubes.MarchCube()
        self.marchingCubes.GenerateMesh()


        self.accept("space", self.Update, extraArgs=[1])
        self.accept("space-repeat", self.Update, extraArgs=[1])
        self.accept("e", self.Update, extraArgs=[-1])
        self.accept("e-repeat", self.Update, extraArgs=[-1])
        self.i = 0
        self.camera.setPos(0, -500, 0)
        self.camera.lookAt(0, 0, 0)

        prefab = self.loader.loadModel("assets/models/icosphere")
        # prefab.setPos(-128, -128, -128)
        # PipelineInstancing.PipelineInstancing.RenderThisModelAtVertexesFrom3DBuffer(prefab, self.cubeformer.vertexBuffer,
        #                                                                           self.cubeformer.size, self.winCreator)
        self.taskMgr.doMethodLater(1, self.TimedUpdate, "Update planet")
        self.mouseX, self.mouseY = 0, 0
        self.keyMap = {
            "mouse": False,
            "down": False,
            "left": False,
            "right": False,
            "shoot": False
        }

        self.accept("mouse1", self.updateKeyMap, ["mouse", True])
        self.accept("mouse1-up", self.updateKeyMap, ["mouse", False])

    def updateKeyMap(self, controlName, controlState):
        self.keyMap[controlName] = controlState
        print(controlName, "set to", controlState)

    def TimedUpdate(self, task: Task.Task):
        if self.mouseWatcherNode.hasMouse():
            self.mouseX = self.mouseWatcherNode.getMouseX()
            self.mouseY = self.mouseWatcherNode.getMouseY()

        self.cubeformer.mouseTime.setData(PTAFloat([self.mouseX, self.mouseY, task.time, float(self.keyMap["mouse"])]))
        self.cubeformer.GenerateNoiseSphere(50+self.i*5)
        self.marchingCubes.EdgeGenerator()
        self.marchingCubes.MarchCube()
        self.marchingCubes.GenerateMesh()
        return Task.again

    def Update(self, adjust):
        self.i += adjust
        self.cubeformer.GenerateNoiseSphere(50+self.i*5)
        self.cubeformer.offset.setData(PTAFloat([self.i*20]))
        self.marchingCubes.EdgeGenerator()
        self.marchingCubes.MarchCube()
        self.marchingCubes.GenerateMesh()
        # self.winCreator.baseData.debuggerMain.LogBufferVecInfo(self, self.cubeformer.vertexBuffer, "f", 4)
        # self.winCreator.baseData.debuggerMain.Inform(f"inform {self.marchingCubes.vertexCount}")
        # self.winCreator.baseData.debuggerMain.LogBufferVecInfo(self, self.marchingCubes.triangleBuffer, "i", 4)

    # Define a procedure to move the camera.
    def SpinCameraTask(self, task: Task.Task):
        radius: float = 500
        angle_radians: float = task.time * 0.6

        # self.camera.setPos(
        #     radius * math.sin(angle_radians),
        #     radius * math.cos(angle_radians),
        #     (math.sin(task.time)) * 100)
        # self.camera.lookAt(0, 0, 0)

        self.dlnp.setHpr(0, task.time*3, 0)



        return Task.cont


loadPrcFile("config/Config.prc")
blobtoryBase = Main()
blobtoryBase.run()
