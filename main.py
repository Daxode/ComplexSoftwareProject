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
from panda3d.core import LPoint3, LVector3, LVecBase3f
from panda3d.core import AmbientLight, PointLight
from direct.task import Task
from direct.actor.Actor import Actor
from direct.filter.CommonFilters import CommonFilters
from panda3d.core import PerlinNoise3
from panda3d.core import NodePath
from panda3d.core import Thread
import math
import sys
import numpy as np
import random

import marchingcubes


class FogDemo(ShowBase):
    def __init__(self):
        # Initialize the ShowBase class from which we inherit, which will
        # create a window and set up everything we need for rendering into it.
        ShowBase.__init__(self)
        self.base = base
        base.setFrameRateMeter(True)

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
        self.noiseGen = PerlinNoise3()
        self.noiseScale: float = 1.5
        self.cube = NodePath('cube')

        placeholder = self.cube.attachNewNode("Square-Placeholder")
        self.sphere.instanceTo(placeholder)

        r = 5
        kage = 0
        color = (0, 0, 0)
        self.vertexes = self.CreateVertecies(4, 4, 4)
        print(len(self.vertexes))
        for v in self.vertexes:
            if kage%(len(self.vertexes) / 6) == 0:
                color = (random.random(), random.random(), random.random())

            kage += 1
            placeholder = self.cube.attachNewNode("Sphere-Placeholder")
            print(v)
            placeholder.setPos(v[0]*r, v[1]*r, v[2]*r)
            b = kage/len(self.vertexes)

            placeholder.setColor(color[0], color[1], color[2])
            self.sphere.copyTo(placeholder)


        self.cube.reparentTo(self.render)

        taskMgr.setupTaskChain('cubegen', numThreads=2)
        taskMgr.add(self.spinCameraTask, "Move Cam")
        # taskMgr.add(self.noisify, "Create noise on cube spheres", taskChain='cubegen')

    def SetVertex(self, vertexes, i, x, y, z):
        # p = origin + 2.0 * (right * i + up * j) / div_count
        p = np.array([x, y, z]) * 2.0 / self.gridSize - np.array([1, 1, 1])
        # p = origin + step3 * (right * i + up * j)

        p2 = p * p
        rx = p[0] * math.sqrt(1.0 - 0.5 * (p2[1] + p2[2]) + p2[1] * p2[2] / 3.0)
        ry = p[1] * math.sqrt(1.0 - 0.5 * (p2[2] + p2[0]) + p2[2] * p2[0] / 3.0)
        rz = p[2] * math.sqrt(1.0 - 0.5 * (p2[0] + p2[1]) + p2[0] * p2[1] / 3.0)
        v = LVecBase3f(x, y, z)
        # v = LVecBase3f(rx, ry, rz)
        print(i, v)
        vertexes[i] = v

    def CreateVertecies(self, xSize, ySize, zSize):
        self.gridSize = xSize
        cornerVertices = 8
        edgeVertices = (xSize + ySize + zSize - 6) * 4
        faceVertices = (
                               (xSize - 2) * (ySize - 2) +
                               (xSize - 2) * (zSize - 2) +
                               (ySize - 2) * (zSize - 2)) * 2
        verticesCount = cornerVertices + edgeVertices + faceVertices
        print(cornerVertices, edgeVertices,  faceVertices, verticesCount)
        vertexes = np.ndarray([verticesCount], dtype=LVecBase3f)

        v = 0
        for y in range(ySize):
            print(y)
            for x in range(xSize):
                self.SetVertex(vertexes, v, x, y, 0)
                v += 1

            for z in range(1, zSize):
                self.SetVertex(vertexes, v, xSize, y, z)
                v += 1

            for x in range(xSize-1, 0, -1):
                self.SetVertex(vertexes, v, x, y, zSize)
                v += 1

            for z in range(zSize-1, 1, -1):
                self.SetVertex(vertexes, v, 0, y, z)
                v += 1

        for z in range(1, zSize-1):
            for x in range(1, xSize-1):
                self.SetVertex(vertexes, v, x, ySize, z)
                v += 1

        for z in range(1, zSize - 1):
            for x in range(1, xSize - 1):
                self.SetVertex(vertexes, v, x, 0, z)
                v += 1

        print(vertexes)
        return vertexes

    def noisify(self, task):
        size = self.cubeSize * self.splitBetween
        mover = [self.base.mouseWatcherNode.getMouseX(),
                 self.base.mouseWatcherNode.getMouseY()] if self.base.mouseWatcherNode.hasMouse() else [0, 0]

        for sphereHolder in self.cube.findAllMatches("**/Sphere-Placeholder"):
            sphere = sphereHolder.children[0]
            spherePos = sphere.getNetTransform().getPos()
            brightness = (1 + self.noiseGen.noise(
                ((spherePos[0] / self.midPoint) + mover[0]) * self.noiseScale,
                ((spherePos[1] / self.midPoint) + mover[1]) * self.noiseScale,
                ((spherePos[2] / self.midPoint)) * self.noiseScale)) / 2
            sphereHolder.setColor(brightness, 0, 1 - brightness, 1)

        return Task.cont

    # Define a procedure to move the camera.
    def spinCameraTask(self, task):
        radius = 100
        angle_radians = task.time * 0.1

        self.camera.setPos(radius * sin(angle_radians), radius * cos(angle_radians), (sin(task.time) + 1) * 10)
        self.camera.lookAt(0, 0, 0)
        return Task.cont


demo = FogDemo()
demo.run()
