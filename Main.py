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


class Main(ShowBase):
    def __init__(self):
        super().__init__()
        self.winCreator = WindowCreator(self, enableRP=False, isFullscreen=False)
        self.taskMgr.add(self.SpinCameraTask, "Move Cam")

        prefab = self.loader.loadModel("assets/models/icosphere")

        cubeformer: CubeFormer = CubeFormer(self.winCreator, 32, 32, 32, 4)
        cubeformer.GeneratePerlinCube()
        self.winCreator.baseData.debuggerMain.Inform(f"Loaded {cubeformer.vertexCount} instances!")
        PipelineInstancing.PipelineInstancing.RenderThisModelAtVertexesFrom3DBuffer(prefab, cubeformer.vertexBuffer,
                                                                                    cubeformer.size, self.winCreator)


    # Define a procedure to move the camera.
    def SpinCameraTask(self, task: Task.Task):
        radius: float = 300
        angle_radians: float = task.time * 0.1

        self.camera.setPos(
            radius * math.sin(angle_radians),
            radius * math.cos(angle_radians),
            (math.sin(task.time)) * 5)
        self.camera.lookAt(0, 0, 0)

        return Task.cont


loadPrcFile("config/Config.prc")
blobtoryBase = Main()
blobtoryBase.run()
