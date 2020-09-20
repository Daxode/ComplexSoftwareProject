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
from panda3d.core import LPoint3, LVector3, LVecBase3f, LColor
from panda3d.core import AmbientLight, PointLight
from direct.task import Task
from direct.actor.Actor import Actor
from direct.filter.CommonFilters import CommonFilters
from panda3d.core import PerlinNoise3
from panda3d.core import NodePath
from panda3d.core import Thread
from panda3d.core import TransparencyAttrib
from panda3d.core import Shader
from panda3d.core import Vec3F, PTAVecBase3f
from panda3d.core import ShaderAttrib, ComputeNode
from panda3d.core import GeomEnums
from panda3d.core import CullBinManager
import math
import sys
import numpy as np
import random
from dataclasses import dataclass
from typing import Tuple, List
from panda3d.core import ShaderBuffer, FrameBufferProperties, GraphicsPipe, GraphicsOutput
from panda3d.core import GraphicsBuffer
from panda3d.core import BamWriter

class FogDemo(ShowBase):

    def __init__(self):
        # Initialize the ShowBase class from which we inherit, which will
        # create a window and set up everything we need for rendering into it.
        ShowBase.__init__(self)
        self.base = base
        self.base.setFrameRateMeter(True)

        # myTexture = self.loader.loadTexture("test.jpg")
        # myTexture.set_format(Texture.F_rgba32)

        # Set up a texture for procedural generation.
        tex = Texture("procedural-normal-map")
        tex.setup2dTexture(512, 512, Texture.T_unsigned_byte, Texture.F_rgba32)
        tex.set_clear_color((0.3, 0.5, 1.0, 0.0))

        tex2 = Texture("procedural-normal")
        tex2.setup2dTexture(512, 512, Texture.T_unsigned_byte, Texture.F_rgba32)

        # Create a dummy and apply compute shader to it
        # computeNode = ComputeNode("compute")
        # computeNode.addDispatch(1024, 1, 1)
        self.dummy = NodePath("computeNode")

        # Load compute shader
        shader = Shader.load_compute(Shader.SL_GLSL, "simple.glsl")
        self.dummy.set_shader(shader)

        self.taskMgr.add(self.updateColors, "update colors")
        self.colors = PTAVecBase3f([Vec3F(1, 0.8, 0), Vec3F(1, 0, 0)])
        self.dummy.set_shader_input("kage", self.colors)

        self.outputVertexes = Texture("buffer")
        self.outputVertexes.setupBufferTexture(512, Texture.T_float, Texture.F_rgba32, GeomEnums.UH_static)

        self.dummy.set_shader_input("someimg", self.outputVertexes)
        self.dummy.set_shader_input("fromTex", tex)
        self.dummy.set_shader_input("toTex", tex2)

        self.win.setClearColor((0.2, 0.2, 0.6, 1))
        self.disableMouse()

        cm = CardMaker('card')
        card = self.render.attachNewNode(cm.generate())
        card.setPos(0, 4, 0)
        card.setTexture(tex2, 1)
        # print(self.render.ls())
        # self.camera.lookAt(card.getPos())

        props = WindowProperties()
        props.setTitle('Marching Cubes')
        props.setIconFilename("pandaIcon.ico")
        self.base.win.requestProperties(props)

    def updateColors(self, task):
        switcher = task.time / 10
        self.colors.setData(PTAVecBase3f([Vec3F(1 - switcher, 0, 0), Vec3F(switcher, 0, 0)]))

        # Retrieve the underlying ShaderAttrib
        self.sattr = self.dummy.get_attrib(ShaderAttrib)
        # Dispatch the compute shader, right now!
        self.base.graphicsEngine.dispatch_compute((1024, 1, 1), self.sattr, self.base.win.get_gsg())

        self.base.graphicsEngine.extractTextureData(self.outputVertexes, base.win.gsg)
        idk = self.outputVertexes.getRamImage()
        idk = memoryview(idk).cast('f')

        i = 0
        amount = 4
        print("start")
        while i < len(idk):
            print([idk[i+x] for x in range(amount)])
            i += 4
        return Task.cont

demo = FogDemo()
demo.run()
