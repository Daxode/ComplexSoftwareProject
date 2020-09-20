import math
from direct.showbase.ShowBase import ShowBase
from panda3d.core import Fog
from panda3d.core import TextNode
from direct.gui.OnscreenText import OnscreenText
from direct.showbase.DirectObject import DirectObject
from direct.interval.MetaInterval import Sequence
from direct.interval.LerpInterval import LerpFunc
from direct.interval.FunctionInterval import Func
from panda3d.core import WindowProperties
from direct.showbase.DirectObject import DirectObject
from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from panda3d.core import lookAt
from panda3d.core import GeomVertexFormat, GeomVertexData
from panda3d.core import Geom, GeomTriangles, GeomVertexWriter
from panda3d.core import Texture, GeomNode
from panda3d.core import PerspectiveLens
from panda3d.core import CardMaker
from panda3d.core import Light, Spotlight
from panda3d.core import TextNode
from panda3d.core import LPoint3, LVector3, LVecBase3f
from panda3d.core import AmbientLight, PointLight
from direct.task import Task
from direct.actor.Actor import Actor
from direct.filter.CommonFilters import CommonFilters
from panda3d.core import PerlinNoise3
from panda3d.core import NodePath
from panda3d.core import Thread
from panda3d.core import TransparencyAttrib
from panda3d.core import Shader
from panda3d.core import Vec3F, ShaderAttrib, ComputeNode, GraphicsPipe
import math
import sys
import numpy as np
import random
from panda3d.core import loadPrcFile
from BaseData import ShowBaseData

# Description:
# This is the main program, and should thus be kept clean,
# so stuff doesn't get out of control
#
# Author:  Daniel Kierkegaard Andersen (dax@daxode.dk)
# Version: 2020-09-20
#
# Copyright (c) 2020 Daniel Kierkegaard Andersen. All rights reserved.
# https://github.com/Daxode/ComplexSoftwareProject


loadPrcFile("config/Config.prc")


class FogDemo(ShowBase):
    def __init__(self):
        # Initialize the ShowBase class from which we inherit, which will
        # create a window and set up everything we need for rendering into it.
        ShowBase.__init__(self)
        self.base: ShowBase = base
        self.baseData: ShowBaseData = ShowBaseData(self.base)
        self.baseData.StartDebugRunner()

        self.SetupWindow()

        self.taskMgr.add(self.SpinCameraTask, "Move Cam")

    def SetupWindow(self):
        props = WindowProperties()
        props.setTitle('Marching Cubes')
        props.setIconFilename("pandaIcon.ico")
        # props.setFullscreen(1)
        # props.setSize(1920, 1080)
        self.base.openMainWindow()
        self.base.win.requestProperties(props)
        self.base.graphicsEngine.openWindows()
        self.base.setFrameRateMeter(True)

        self.win.setClearColor((0.2, 0.2, 0.6, 1))
        self.disableMouse()

    # Define a procedure to move the camera.
    def SpinCameraTask(self, task: Task.Task):
        radius: float = 100
        angle_radians: float = task.time * 0.1

        self.camera.setPos(
            radius * math.sin(angle_radians),
            radius * math.cos(angle_radians),
            (math.sin(task.time) + 1) * 10)
        self.camera.lookAt(0, 0, 0)

        return Task.cont


demo = FogDemo()
demo.run()
