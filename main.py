from direct.showbase.ShowBase import ShowBase
from panda3d.core import WindowProperties
from direct.task import Task
import math
from panda3d.core import loadPrcFile
from BaseData import ShowBaseData
import sys

# Description:
# This is the main program, and should thus be kept clean,
# so stuff doesn't get out of control
#
# Author:  Daniel Kierkegaard Andersen (dax@daxode.dk)
# Version: 2020-09-20
#
# Copyright (c) 2020 Daniel Kierkegaard Andersen. All rights reserved.
# https://github.com/Daxode/ComplexSoftwareProject


class FogDemo(ShowBase):
    def __init__(self):
        # Setup render pipeline
        sys.path.insert(0, "assets/external_libs/render_pipeline")
        from rpcore import RenderPipeline, PointLight
        self.render_pipeline = RenderPipeline()
        self.render_pipeline.create(self)

        # Main setup
        self.base: ShowBase = base
        self.baseData: ShowBaseData = ShowBaseData(self.base)
        self.baseData.StartDebugRunner()
        self.SetupWindow(isFullscreen=False)
        self.taskMgr.add(self.SpinCameraTask, "Move Cam")

        # Test code
        self.render_pipeline.daytime_mgr.time = "19:17"
        model = self.loader.loadModel("assets/models/icosphere")
        self.render_pipeline.set_effect(render, "assets/external_libs/render_pipeline/samples/02-Roaming-Ralph/scene-effect.yaml", {}, sort=250)
        model.setColor(1, 0, 0)
        model.reparentTo(self.render)

        my_light = PointLight()
        my_light.setPos(1, 1, 0)
        my_light.color = (0.9, 0.6, 0.0)
        my_light.energy = 100000.0

        self.render_pipeline.add_light(my_light)

    # Setup basic props on window
    def SetupWindow(self, isFullscreen: bool):
        props = WindowProperties()
        props.setTitle('Marching Cubes')
        props.setIconFilename("assets/pandaIcon.ico")
        if isFullscreen:
            props.setFullscreen(1)
            props.setSize(1920, 1080)

        #self.base.openMainWindow()
        #self.base.win.requestProperties(props)
        #self.base.graphicsEngine.openWindows()
        #self.base.setFrameRateMeter(True)

        #self.win.setClearColor((0.2, 0.2, 0.6, 1))
        self.disableMouse()

    # Define a procedure to move the camera.
    def SpinCameraTask(self, task: Task.Task):
        radius: float = 100
        angle_radians: float = task.time * 5

        self.camera.setPos(
            radius * math.sin(angle_radians),
            radius * math.cos(angle_radians),
            (math.sin(task.time) + 1) * 10)
        self.camera.lookAt(0, 0, 0)

        return Task.cont


loadPrcFile("config/Config.prc")
demo = FogDemo()
demo.run()
