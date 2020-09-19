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

class FogDemo(ShowBase):
    def __init__(self):
        # Initialize the ShowBase class from which we inherit, which will
        # create a window and set up everything we need for rendering into it.
        ShowBase.__init__(self)
        self.base = base
        base.setFrameRateMeter(True)

        #myTexture = self.loader.loadTexture("test.jpg")
        #myTexture.set_format(Texture.F_rgba32)

        # Set up a texture for procedural generation.
        tex = Texture("procedural-normal-map")
        tex.setup2dTexture(512, 512, Texture.T_unsigned_byte, Texture.F_rgba32)
        tex.set_clear_color((0.3, 0.5, 1.0, 0.0))

        tex2 = Texture("procedural-normal")
        tex2.setup2dTexture(512, 512, Texture.T_unsigned_byte, Texture.F_rgba32)
        tex2.set_clear_color((1.0, 0.5, 1.0, 0.0))

        # Create a dummy and apply compute shader to it
        computeNode = ComputeNode("compute")

        computeNode.addDispatch(512, 1, 1)
        self.dummy = self.render.attach_new_node(computeNode)

        # Load compute shader
        shader = Shader.load_compute(Shader.SL_GLSL, "simple.glsl")
        self.dummy.set_shader(shader)
        self.dummy.set_shader_input("fromTex", tex)
        self.dummy.set_shader_input("toTex", tex2)

        self.win.setClearColor((0.2, 0.2, 0.6, 1))
        self.disableMouse()

        cm = CardMaker('card')
        card = self.render.attachNewNode(cm.generate())
        card.setPos(0, 4, 0)
        card.setTexture(tex2, 1)
        #print(self.render.ls())
        #self.camera.lookAt(card.getPos())

        props = WindowProperties()
        props.setTitle('Marching Cubes')
        props.setIconFilename("pandaIcon.ico")
        base.win.requestProperties(props)


demo = FogDemo()
demo.run()
