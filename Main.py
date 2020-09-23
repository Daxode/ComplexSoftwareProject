from direct.task import Task
import math
from panda3d.core import loadPrcFile
from direct.showbase.ShowBase import ShowBase

import PipelineInstancing
from WindowCreator import WindowCreator
from panda3d.core import NodePath

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
        self.taskMgr.add(self.SpinCameraTask, "Move Cam")

        prefab = self.loader.loadModel("assets/models/icosphere")

        size = 64
        spacing = 4
        midPoint = size*spacing*0.5

        # Collect all instances
        matrices = []
        for x in range(size):
            for y in range(size):
                for z in range(size):
                    placeholder: NodePath = NodePath("icosphere-placeholder")
                    placeholder.setPos(x*spacing-midPoint, y*spacing-midPoint, z*spacing-midPoint)
                    matrices.append(placeholder.get_mat(self.render))
                    placeholder.remove_node()

        self.winCreator.baseData.debuggerMain.Inform(f"Loaded {len(matrices)} instances!")
        PipelineInstancing.PipelineInstancing.RenderThisModelAtMatrices(prefab, matrices, self.winCreator)

    # Define a procedure to move the camera.
    def SpinCameraTask(self, task: Task.Task):
        radius: float = 200
        angle_radians: float = task.time * 1.1

        self.camera.setPos(
            radius * math.sin(angle_radians),
            radius * math.cos(angle_radians),
            (math.sin(task.time)) * 10)
        self.camera.lookAt(0, 0, 0)

        return Task.cont


loadPrcFile("config/Config.prc")
blobtoryBase = Main()
blobtoryBase.run()
