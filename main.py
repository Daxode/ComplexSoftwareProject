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
from panda3d.core import TransparencyAttrib
from panda3d.core import Shader
from panda3d.core import Vec3F, ShaderAttrib, ComputeNode
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

        # Load compute shader
        shader = Shader.load_compute(Shader.SL_GLSL, "ComputeSpherizeCube.glsl")

        # Create a dummy and apply compute shader to it
        computeNode = ComputeNode("compute")
        computeNode.add_dispatch(512, 1, 1)
        self.dummy = self.render.attach_new_node(computeNode)
        self.dummy.set_shader(shader)

        panda3d.core.load_prc_file_data('', 'framebuffer-srgb true')
        filters = CommonFilters(base.win, base.cam)
        self.win.setClearColor((0.2, 0.2, 0.6, 1))
        self.disableMouse()

        props = WindowProperties()
        props.setTitle('Marching Cubes')
        props.setIconFilename("pandaIcon.ico")
        base.win.requestProperties(props)

        self.sphere = self.loader.loadModel("models/icosphere")
        self.noiseGen = PerlinNoise3()
        self.noiseScale: float = 1.5

        self.sphereVectors = []

        placeholder = self.render.attachNewNode("Square-Placeholder")
        self.sphere.instanceTo(placeholder)

        self.gridSize = 10
        self.innerAmount = 1
        self.cube = NodePath('cube')
        self.generateStuff()

        self.accept("d", self.changeGridSize, [1])
        self.accept("a", self.changeGridSize, [-1])
        self.accept("space", self.generateStuff)
        self.accept("w", self.changeInnerAmount, [1])
        self.accept("s", self.changeInnerAmount, [-1])

        taskMgr.setupTaskChain('cubegen', numThreads=2)
        taskMgr.add(self.spinCameraTask, "Move Cam")
        # taskMgr.add(self.noisify, "Create noise on cube spheres", taskChain='cubegen')

    def genCubeNode(self):
        self.cube = NodePath('cube')
        self.cube.reparentTo(self.render)
        self.cube.setTransparency(TransparencyAttrib.MAlpha)
        self.cube.setAlphaScale(0.5)

    def changeGridSize(self, amount):
        self.gridSize += amount
        print(self.gridSize)
        self.generateStuff()

    def changeInnerAmount(self, amount):
        self.innerAmount += amount
        print(self.innerAmount)
        self.generateStuff()

    def generateStuff(self):
        color = (0, 0, 0)
        self.cube.removeNode()
        self.genCubeNode()
        self.noiseGen = PerlinNoise3()
        cubes = np.ndarray([self.gridSize], dtype=np.ndarray)
        for i in range(self.innerAmount):
            cubes[i] = self.CreateSpherizedCubeWithCompute(self.gridSize, 20 - i * 2)
            for v in range(len(cubes[i])):
                if v % self.gridSize == 0:
                    color = (random.random(), random.random(), random.random())

                ver = cubes[i][v]
                placeholder = self.cube.attachNewNode("Sphere-Placeholder")
                placeholder.setPos(ver[0], ver[1], ver[2])
                # b = v/len(cubes[i])
                # placeholder.setColor(b)

                placeholder.setColor(color[0], color[1], color[2])
                self.sphere.instanceTo(placeholder)

    # Spherification of a cube - thanks to this https://catlikecoding.com/unity/tutorials/cube-sphere/ amazing article
    def Spherize(self, x, y, z, gridSize):
        p = np.array([x, y, z]) * 2.0 / gridSize - np.array([1, 1, 1])
        p2 = p * p
        rx = p[0] * math.sqrt(1.0 - 0.5 * (p2[1] + p2[2]) + p2[1] * p2[2] / 3.0)
        ry = p[1] * math.sqrt(1.0 - 0.5 * (p2[2] + p2[0]) + p2[2] * p2[0] / 3.0)
        rz = p[2] * math.sqrt(1.0 - 0.5 * (p2[0] + p2[1]) + p2[0] * p2[1] / 3.0)
        return LVecBase3f(rx, ry, rz)

    def SetVertex(self, vertexes, i, x, y, z):
        vertexes[i] = Vec3F(x, y, z)

    def CreateSpherizedCubeWithCompute(self, gridSize, radius):
        cube = self.CreateCube(gridSize, gridSize, gridSize)

        self.dummy.set_shader_input("gridSize", self.gridSize)
        self.dummy.set_shader_input("radius", radius)
        self.dummy.set_shader_input("fromVertexes", cube.tolist())
        sphere = [Vec3F()]*cube.size
        self.dummy.set_shader_input("toVertexes", sphere)

        # Retrieve the underlying ShaderAttrib
        self.sattr = self.dummy.get_attrib(ShaderAttrib)
        # Dispatch the compute shader, right now!
        self.base.graphicsEngine.dispatch_compute((1024, 1, 1), self.sattr, self.base.win.get_gsg())

        return sphere



    def CreateSpherizedCube(self, gridSize, radius):
        cube = self.CreateCube(gridSize, gridSize, gridSize)

        for i in range(len(cube)):
            v = cube[i]
            r = (radius*((2+self.noiseGen.noise(v*0.4))/3))
            cube[i] = self.Spherize(v[0], v[1], v[2], gridSize)*r

        return cube

    def CreateCube(self, xSize, ySize, zSize):
        cornerVertices = 8
        edgeVertices = (xSize + ySize + zSize - 3) * 4
        faceVertices = (
                               (xSize - 1) * (ySize - 1) +
                               (xSize - 1) * (zSize - 1) +
                               (ySize - 1) * (zSize - 1)) * 2
        vertexes = np.ndarray([cornerVertices + edgeVertices + faceVertices], dtype=Vec3F)

        v = 0
        for y in range(ySize + 1):
            for x in range(xSize + 1):
                self.SetVertex(vertexes, v, x, y, 0)
                v += 1

            for z in range(1, zSize + 1):
                self.SetVertex(vertexes, v, xSize, y, z)
                v += 1

            for x in range(xSize - 1, -1, -1):
                self.SetVertex(vertexes, v, x, y, zSize)
                v += 1

            for z in range(zSize - 1, 0, -1):
                self.SetVertex(vertexes, v, 0, y, z)
                v += 1

        for z in range(1, zSize):
            for x in range(1, xSize):
                self.SetVertex(vertexes, v, x, ySize, z)
                v += 1

        for z in range(1, zSize):
            for x in range(1, xSize):
                self.SetVertex(vertexes, v, x, 0, z)
                v += 1

        return vertexes

    def noisify(self, task):
        mover = [self.base.mouseWatcherNode.getMouseX(),
                 self.base.mouseWatcherNode.getMouseY()] if self.base.mouseWatcherNode.hasMouse() else [0, 0]

        for sphereHolder in self.cube.findAllMatches("**/Sphere-Placeholder"):
            sphere = sphereHolder.children[0]
            spherePos = sphere.getNetTransform().getPos()
            brightness = (1 + self.noiseGen.noise(
                ((spherePos[0] / self.gridSize) + mover[0]) * self.noiseScale,
                ((spherePos[1] / self.gridSize) + mover[1]) * self.noiseScale,
                ((spherePos[2] / self.gridSize)) * self.noiseScale)) / 2
            sphereHolder.setColor(brightness, 0, 1 - brightness, 1)

        return Task.cont

    # Define a procedure to move the camera.
    def spinCameraTask(self, task):
        radius = 100
        angle_radians = task.time * 0.1

        self.camera.setPos(radius * sin(angle_radians), radius * cos(angle_radians), (sin(task.time) + 1) * 10)
        self.camera.lookAt(0, 0, 0)

        cube = self.CreateCube(2, 2, 2)
        print(self.sphereVectors)

        texIn = Texture("procedural-normal-map")
        texIn.setup_1d_texture(cube.size, Texture.T_float, Texture.F_rgba32)
        texIn.setClearColor((1,0,1,1))

        texOut = Texture("procedural-normal-map")
        texOut.setup_1d_texture(cube.size, Texture.T_float, Texture.F_rgba32)
        texIn.setClearColor((0, 0, 0.823, 1))

        self.dummy.set_shader_input("gridSize", self.gridSize)
        self.dummy.set_shader_input("radius", radius)
        self.dummy.set_shader_input("fromVertexes", texIn)
        self.sphereVectors = [Vec3F()] * cube.size
        self.dummy.set_shader_input("toVertexes", texOut)
        print(texOut)

        # Retrieve the underlying ShaderAttrib
        #self.sattr = self.dummy.get_attrib(ShaderAttrib)
        # Dispatch the compute shader, right now!
        #self.base.graphicsEngine.dispatch_compute((1024, 1, 1), self.sattr, self.base.win.get_gsg())


        return Task.cont


demo = FogDemo()
demo.run()
