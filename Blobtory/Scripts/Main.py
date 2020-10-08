from direct.interval.LerpInterval import LerpPosInterval
from panda3d.core import loadPrcFile, loadPrcFileData, LPoint3f
from direct.showbase.ShowBase import ShowBase, PTAFloat, AmbientLight, DirectionalLight, Shader, Texture, TextureStage, \
    SamplerState, FrameBufferProperties, WindowProperties, GraphicsPipe, GraphicsOutput, NodePath

from Blobtory.Scripts.Pipeline.WindowCreator import WindowCreator

# Description:
# This is the main program, and should thus be kept clean,
# so stuff doesn't get out of control
#
# Author:  Daniel Kierkegaard Andersen (dax@daxode.dk)
# Version: 2020-09-22
#
# Copyright (c) 2020 Daniel Kierkegaard Andersen. All rights reserved.
# https://github.com/Daxode/ComplexSoftwareProject
from Blobtory.Scripts.planet_former.PlanetGenerator import PlanetGenerator


class Main(ShowBase):
    def __init__(self):
        super().__init__()
        self.winCreator = WindowCreator(self, enableRP=False, isFullscreen=False)

        self.planetGen: PlanetGenerator = PlanetGenerator(self.winCreator, 128, 500)
        self.planetGen.cubeformer.mouseTime.setData(PTAFloat([10, 0, 0, 1]))
        self.accept("a", self.planetGen.RegenPlanet)

        sphere = self.loader.loadModel("assets/models/icosphere")
        sphere.reparentTo(self.render)
        myShader: Shader = Shader.load(Shader.SL_GLSL,
                                       vertex="assets/shaders/defaults/default.vert",
                                       fragment="assets/shaders/defaults/default.frag")
        sphere.setShader(myShader, 1)
        sphere.setScale(100)
        sphere.setPos((0,50,600))

        myToonLightTex = self.winCreator.base.loader.loadTexture(
            "assets/textures/ramps/rampToonLight.png")
        myToonLightTex.setWrapU(Texture.WM_clamp)
        myToonLightTex.setWrapV(Texture.WM_clamp)
        myToonLightTex.setMagfilter(SamplerState.FT_nearest)
        myToonLightTex.setMinfilter(SamplerState.FT_nearest)

        stageToonLight = TextureStage("ToonLight")
        stageToonLight.setSort(1)
        sphere.setTexture(stageToonLight, myToonLightTex)

        winprops = WindowProperties(size=(512, 512))
        props = FrameBufferProperties()
        props.setRgbColor(1)
        props.setAlphaBits(1)
        props.setDepthBits(1)
        LBuffer = self.graphicsEngine.makeOutput(
            self.pipe, "offscreen buffer", -2,
            props, winprops,
            GraphicsPipe.BFRefuseWindow,
            self.win.getGsg(), self.win)

        Ldepthmap = Texture()
        LBuffer.addRenderTexture(Ldepthmap, GraphicsOutput.RTMBindOrCopy,
                                 GraphicsOutput.RTPDepthStencil)

        self.accept("v", self.bufferViewer.toggleEnable)

        alight = AmbientLight('alight')
        alight.setColor((0.1, 0.1, 0.1, 1))
        alnp = self.render.attachNewNode(alight)
        self.render.setLight(alnp)

        dlight1 = DirectionalLight('my dlight1')
        dlight1.setShadowCaster(True, 512, 512)
        #dlight1.show_frustum()
        dlnp1 = self.render.attachNewNode(dlight1)
        dlnp1.setPos(0,0,512)
        dlnp1.setHpr(0, 270, 0)
        self.render.setLight(dlnp1)

        bmin, bmax = self.render.get_tight_bounds(dlnp1)
        size=128
        bmin, bmax = LPoint3f(-size,0, -size), LPoint3f(size, size,size)
        print(bmin,bmax)
        lens = dlight1.get_lens(0)
        lens.set_film_offset((bmin.xz + bmax.xz) * 0.5)
        lens.set_film_size(bmax.xz - bmin.xz)
        lens.set_near_far(bmin.y, bmax.y)

        i = LerpPosInterval(sphere,
                            2,
                            (0,-100,600),(0,100,600))
        i.loop()

        dlight2 = DirectionalLight('my dlight2')
        dlight2.setColor((0.05, 0.05, 0.05, 1))
        dlight2.setShadowCaster(True, 512, 512)
        dlnp2 = self.render.attachNewNode(dlight2)
        dlnp2.setHpr(0, 180, 0)
        self.render.setLight(dlnp2)


loadPrcFileData('', 'framebuffer-multisample 1')
loadPrcFileData('', 'multisamples 0')
loadPrcFileData('', 'sync-video false')
loadPrcFile("config/Config.prc")
blobtoryBase = Main()
blobtoryBase.run()
