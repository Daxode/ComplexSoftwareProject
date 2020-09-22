from direct.task import Task
import math
from panda3d.core import loadPrcFile
from direct.showbase.ShowBase import ShowBase
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


class BlobtoryBase(ShowBase):
    def __init__(self):
        super().__init__()
        self.winCreator = WindowCreator(self, enableRP=True, isFullscreen=False)
        self.taskMgr.add(self.SpinCameraTask, "Move Cam")

        model = self.loader.loadModel("assets/models/icosphere")
        model.setShaderAuto()
        model.reparentTo(self.render)
        size = 16
        spacing = 4

        midPoint = size*spacing*0.5
        for x in range(size):
            for y in range(size):
                for z in range(size):
                    placeholder: NodePath = self.render.attach_new_node("icosphere-placeholder")
                    placeholder.setPos(x*spacing-midPoint, y*spacing-midPoint, z*spacing-midPoint)
                    model.instance_to(placeholder)

    # Define a procedure to move the camera.
    def SpinCameraTask(self, task: Task.Task):
        radius: float = 200
        angle_radians: float = task.time * 0.1

        self.camera.setPos(
            radius * math.sin(angle_radians),
            radius * math.cos(angle_radians),
            (math.sin(task.time)) * 100)
        self.camera.lookAt(0, 0, 0)

        return Task.cont


loadPrcFile("config/Config.prc")
blobtoryBase = BlobtoryBase()
blobtoryBase.run()
