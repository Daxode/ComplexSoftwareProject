from direct.task import Task
import math
from panda3d.core import loadPrcFile
from direct.showbase.ShowBase import ShowBase
from WindowCreator import WindowCreator

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
        self.winCreator = WindowCreator(self, enableRP=True)
        self.accept("space", self.winCreator.UpdateWindow, [False])
        self.taskMgr.add(self.SpinCameraTask, "Move Cam")

        model = self.loader.loadModel("assets/models/icosphere")
        model.reparentTo(self.render)

    # Define a procedure to move the camera.
    def SpinCameraTask(self, task: Task.Task):
        radius: float = 20
        angle_radians: float = task.time * 0.1

        self.camera.setPos(
            radius * math.sin(angle_radians),
            radius * math.cos(angle_radians),
            (math.sin(task.time)) * 10)
        self.camera.lookAt(0, 0, 0)

        return Task.cont


loadPrcFile("config/Config.prc")
blobtoryBase = BlobtoryBase()
blobtoryBase.run()
