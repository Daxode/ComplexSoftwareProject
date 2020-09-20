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
from panda3d.core import Vec3F, ShaderAttrib, ComputeNode
import math
import sys
import numpy as np
import random
from dataclasses import dataclass
from typing import Tuple, List
from panda3d.core import ShaderBuffer, FrameBufferProperties, GraphicsPipe, GraphicsOutput
from panda3d.core import GraphicsBuffer
from panda3d.core import BamWriter

@dataclass
class Vec3FBuffer:
    output_data: List[Vec3F]

# PT(WindowFramework)                window         = framebufferTextureArguments.window;
# PT(GraphicsOutput)                 graphicsOutput = framebufferTextureArguments.graphicsOutput;
# PT(GraphicsEngine)                 graphicsEngine = framebufferTextureArguments.graphicsEngine;
# LVecBase4                          rgbaBits       = framebufferTextureArguments.rgbaBits;
# GraphicsOutput::RenderTexturePlane bitplane       = framebufferTextureArguments.bitplane;
# int                                aux_rgba       = framebufferTextureArguments.aux_rgba;
# bool                               setFloatColor  = framebufferTextureArguments.setFloatColor;
# bool                               setSrgbColor   = framebufferTextureArguments.setSrgbColor;
# bool                               setRgbColor    = framebufferTextureArguments.setRgbColor;
# bool                               useScene       = framebufferTextureArguments.useScene;
# std::string                        name           = framebufferTextureArguments.name;
# LColor                             clearColor     = framebufferTextureArguments.clearColor;
#
# NodePath   cameraNP = NodePath("");
# PT(Camera) camera   = NULL;
#
# if (useScene) {
#   cameraNP = window->make_camera();
#   camera   = DCAST(Camera, cameraNP.node());
#   camera->set_lens(window->get_camera(0)->get_lens());
# } else {
#   camera = new Camera(name + "Camera");
#   PT(OrthographicLens) lens = new OrthographicLens();
#   lens->set_film_size(2, 2);
#   lens->set_film_offset(0, 0);
#   lens->set_near_far(-1, 1);
#   camera->set_lens(lens);
#   cameraNP = NodePath(camera);
# }
#
# PT(DisplayRegion) bufferRegion =
#   buffer->make_display_region(0, 1, 0, 1);
# bufferRegion->set_camera(cameraNP);
#
# NodePath shaderNP = NodePath(name + "Shader");
#
# if (!useScene) {
#   NodePath renderNP = NodePath(name + "Render");
#   renderNP.set_depth_test( false);
#   renderNP.set_depth_write(false);
#   cameraNP.reparent_to(renderNP);
#   CardMaker card = CardMaker(name);
#   card.set_frame_fullscreen_quad();
#   card.set_has_uvs(true);
#   NodePath cardNP = NodePath(card.generate());
#   cardNP.reparent_to(renderNP);
#   cardNP.set_pos(0, 0, 0);
#   cardNP.set_hpr(0, 0, 0);
#   cameraNP.look_at(cardNP);
# }
#
# FramebufferTexture result;
# result.buffer       = buffer;
# result.bufferRegion = bufferRegion;
# result.camera       = camera;
# result.cameraNP     = cameraNP;
# result.shaderNP     = shaderNP;
# return result;
# }


class FogDemo(ShowBase):
    def generateFramebufferTexture(self):
        fbp = FrameBufferProperties()
        fbp.setBackBuffers(0)
        fbp.set_rgba_bits(32, 32, 32, 32)
        fbp.set_aux_rgba(1)
        fbp.set_float_color(True)
        fbp.set_srgb_color(False)
        fbp.set_rgb_color(True)

        name = "test"
        graphOut = self.base.win
        buffer = self.base.graphicsEngine.makeOutput(self.base.pipe, name + "Buffer", 10 - 1,
                                                     fbp, WindowProperties.size(0, 0),
                                                     GraphicsPipe.BF_refuse_window |
                                                     GraphicsPipe.BF_resizeable |
                                                     GraphicsPipe.BF_can_bind_every|
                                                     GraphicsPipe.BF_rtt_cumulative |
                                                     GraphicsPipe.BF_size_track_host,
                                                     graphOut.get_gsg(),
                                                     graphOut.get_host())
        #buffer.add_render_texture(None, GraphicsOutput.RTM_bind_or_copy, GraphicsOutput.RTP_color)
        buffer.set_clear_color(LColor(0, 0, 0, 0))
        return buffer

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
        computeNode = ComputeNode("compute")
        computeNode.addDispatch(256, 2, 1)
        self.dummy = self.render.attach_new_node(computeNode)

        # Load compute shader
        shader = Shader.load_compute(Shader.SL_GLSL, "simple.glsl")
        self.dummy.set_shader(shader)

        self.taskMgr.add(self.updateColors, "update colors")
        self.colors = [Vec3F(1, 0.8, 0), Vec3F(1, 0, 0)]
        self.dummy.set_shader_input("kage", self.colors)

        self.outputVertexes = self.generateFramebufferTexture()
        self.dummy.set_shader_input("block2", self.outputVertexes)
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
        self.colors = [Vec3F(1 - switcher, 0, 0), Vec3F(switcher, 0, 0)]
        self.dummy.set_shader_input("kage", self.colors)
        return Task.cont

demo = FogDemo()
demo.run()
