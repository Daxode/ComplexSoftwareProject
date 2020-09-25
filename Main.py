from direct.task import Task
import math
from panda3d.core import loadPrcFile
from direct.showbase.ShowBase import ShowBase, Texture, GeomEnums, Shader, ShaderAttrib, LVecBase3i, PTAFloat

import PipelineInstancing
from WindowCreator import WindowCreator
from panda3d.core import NodePath, LVector3f

# Description:
# This is the main program, and should thus be kept clean,
# so stuff doesn't get out of control
#
# Author:  Daniel Kierkegaard Andersen (dax@daxode.dk)
# Version: 2020-09-22
#
# Copyright (c) 2020 Daniel Kierkegaard Andersen. All rights reserved.
# https://github.com/Daxode/ComplexSoftwareProject
from planet_former.CubeFormer import CubeFormer
from planet_former.MarchingCubes import MarchingCubes


class Main(ShowBase):
    def __init__(self):
        super().__init__()
        self.winCreator = WindowCreator(self, enableRP=False, isFullscreen=False)
        self.taskMgr.add(self.SpinCameraTask, "Move Cam")

        size = 128
        spacing = 4
        mid = size * spacing / 2
        prefab = self.loader.loadModel("assets/models/icosphere")
        prefab.setPos(-mid, -mid, -mid)
        prefab2 = self.loader.loadModel("assets/models/icosphere")
        prefab2.setPos(-mid, -mid, -mid)

        self.cubeformer: CubeFormer = CubeFormer(self.winCreator, size, size, size, spacing)
        self.cubeformer.GenerateCube()
        self.cubeformer.GenerateNoiseSphere(5)
        self.winCreator.baseData.debuggerMain.Inform(f"Loaded {self.cubeformer.vertexCount} instances!")
        #PipelineInstancing.PipelineInstancing.RenderThisModelAtVertexesFrom3DBuffer(prefab, self.cubeformer.vertexBuffer,
        #                                                                          self.cubeformer.size, self.winCreator)
        self.marchingCubes: MarchingCubes = MarchingCubes(self.cubeformer)
        self.marchingCubes.EdgeGenerator()
        self.winCreator.baseData.debuggerMain.Inform(
            f"Loaded {self.marchingCubes.edgeVertexCount} instances! With size of {self.marchingCubes.size}")

        self.marchingCubes.MarchCube()
        self.marchingCubes.GenerateMesh()
        # PipelineInstancing.PipelineInstancing.RenderThisModelAtVertexesFrom3DBuffer(prefab2,
        #                                                                            self.marchingCubes.edgeVertexBuffer,
        #                                                                            self.marchingCubes.size*3, self.winCreator)
        self.accept("space", self.Update, extraArgs=[1])
        self.accept("space-repeat", self.Update, extraArgs=[1])

        self.accept("e", self.Update, extraArgs=[-1])
        self.accept("e-repeat", self.Update, extraArgs=[-1])
        #self.winCreator.baseData.debuggerMain.LogBufferVecInfo(self, self.marchingCubes.triangleBuffer, "i", 4)
        #self.winCreator.baseData.debuggerMain.Inform(f"inform {self.marchingCubes.vertexCount}")
        #self.winCreator.baseData.debuggerMain.LogBufferVecInfo(self, self.cubeformer.vertexBuffer, "f", 4)
        self.winCreator.baseData.debuggerMain.Inform("inform")
        #self.render.ls()
        self.i = 0

    def Update(self, adjust):
        self.i += adjust
        self.cubeformer.GenerateNoiseSphere(5+self.i*5)
        #self.cubeformer.offset.setData(PTAFloat([self.i]))
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

        self.camera.setPos(
            radius * math.sin(angle_radians),
            radius * math.cos(angle_radians),
            (math.sin(task.time)) * 20)
        self.camera.lookAt(0, 0, 0)

        return Task.cont


loadPrcFile("config/Config.prc")
blobtoryBase = Main()
blobtoryBase.run()
