from math import pi, sin, cos
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
from panda3d.core import LPoint3, LVector3
from panda3d.core import AmbientLight, PointLight
from direct.task import Task
from direct.actor.Actor import Actor
from direct.filter.CommonFilters import CommonFilters
from panda3d.core import PerlinNoise3
from panda3d.core import NodePath

import sys

import marchingcubes


class FogDemo(ShowBase):
    def __init__(self):
        # Initialize the ShowBase class from which we inherit, which will
        # create a window and set up everything we need for rendering into it.
        ShowBase.__init__(self)
        panda3d.core.load_prc_file_data('', 'framebuffer-srgb true')
        filters = CommonFilters(base.win, base.cam)
        self.win.setClearColor((0.2, 0.2, 0.6, 1))
        self.disableMouse()
        self.camera.setPos(0, -10, 0)

        props = WindowProperties()
        props.setTitle('Marching Cubes')
        props.setIconFilename("pandaIcon.ico")
        base.win.requestProperties(props)

        self.sphere = self.loader.loadModel("models/icosphere")
        self.sphere.setPos(0, 0, 0)
        self.cubeSize: int = 10
        self.splitBetween: float = 5
        self.midPoint = (self.cubeSize * self.splitBetween) / 2

        self.noiseGen = PerlinNoise3()
        self.noiseScale: float = 5000

        row = NodePath('row')
        for x in range(self.cubeSize):
            placeholder = row.attachNewNode("Sphere-Placeholder")
            placeholder.setPos(x * self.splitBetween - self.midPoint, 0, 0)
            self.sphere.instanceTo(placeholder)

        square = NodePath('square')
        for y in range(self.cubeSize):
            placeholder = square.attachNewNode("Row-Placeholder")
            placeholder.setPos(0, y * self.splitBetween - self.midPoint, 0)
            row.instanceTo(placeholder)

        self.cube = NodePath('cube')
        for z in range(self.cubeSize):
            placeholder = self.cube.attachNewNode("Square-Placeholder")
            placeholder.setPos(0, 0, z * self.splitBetween - self.midPoint)
            square.instanceTo(placeholder)

        self.cube.reparentTo(self.render)

        taskMgr.add(self.spinCameraTask, "Move Cam")
        taskMgr.add(self.noisify, "Create noise on cube spheres")

    def noisify(self, task):
        squaresHolders = self.cube.children
        size = self.cubeSize*self.splitBetween

        for squareHolder in squaresHolders:
            square = squareHolder.children[0]
            for rowHolder in square.children:
                row = rowHolder.children[0]
                for sphereHolder in row.children:
                    sphere = sphereHolder.children[0]
                    spherePos = sphere.getNetTransform().getPos()
                    mover = task.time/200
                    brightness = (1+self.noiseGen.noise(
                        (spherePos[0]+mover / self.midPoint) * self.noiseScale,
                        (spherePos[1]+mover / self.midPoint) * self.noiseScale,
                        (spherePos[2]+mover / self.midPoint) * self.noiseScale))/2
                    print(brightness)
                    sphereHolder.setColor(brightness, brightness, brightness, 1)
        return Task.cont

    # Define a procedure to move the camera.
    def spinCameraTask(self, task):
        radius = 150
        angle_radians = task.time * 0.5

        self.camera.setPos(radius * sin(angle_radians), radius * cos(angle_radians), 50)
        self.camera.lookAt(0, 0, 0)
        return Task.cont


demo = FogDemo()
demo.run()