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
        from assets.external_libs.render_pipeline.rpcore import RenderPipeline, PointLight
        self.render_pipeline = RenderPipeline()
        self.render_pipeline.pre_showbase_init()

        ShowBase.__init__(self)
        self.base: ShowBase = base
        self.baseData: ShowBaseData = ShowBaseData(self.base)
        self.baseData.StartDebugRunner()
        self.SetupWindow(isFullscreen=False)
        self.taskMgr.add(self.SpinCameraTask, "Move Cam")


        model = self.loader.loadModel("assets/models/icosphere")
        model.setColor(1, 0, 0)
        model.reparentTo(self.render)
        self.light: PointLight = PointLight()
        self.light.energy = 1000.0
        # set desired properties, see below
        self.render_pipeline.add_light(self.light)

    def SetupWindow(self, isFullscreen: bool):
        props = WindowProperties()
        props.setTitle('Marching Cubes')
        props.setIconFilename("pandaIcon.ico")
        if isFullscreen:
            props.setFullscreen(1)
            props.setSize(1920, 1080)

        self.base.openMainWindow()
        self.base.win.requestProperties(props)
        self.base.graphicsEngine.openWindows()
        self.disableMouse()

        self.render_pipeline.create(self.base)
        self.render_pipeline.set_effect(self.render, "assets/rp-effects/scene-effect.yaml", {}, sort=250)

    # Define a procedure to move the camera.
    def SpinCameraTask(self, task: Task.Task):
        radius: float = 5
        angle_radians: float = task.time * 0.1

        timeSine: float = (math.sin(task.time)+1)/2
        self.camera.setPos(
            radius * math.sin(angle_radians),
            radius * math.cos(angle_radians),
            (math.sin(task.time)) * 10)
        self.camera.lookAt(0, 0, 0)

        self.light.color = (timeSine, 0, 1-timeSine)
        self.light.pos = (
            radius * math.cos(angle_radians*10),
            radius * math.sin(angle_radians*10),
            (math.cos(task.time*0.5)) * -10)

        return Task.cont


loadPrcFile("config/Config.prc")
demo = FogDemo()
demo.run()
