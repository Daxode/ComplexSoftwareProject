from direct.filter.CommonFilters import CommonFilters
from direct.showbase.ShowBase import ShowBase, DirectionalLight, AntialiasAttrib
from panda3d.core import WindowProperties
from Blobtory.Scripts.Pipeline.BaseData import ShowBaseData
from multipledispatch import dispatch
import sys

# Description:
# This is the main window creator, made to easily switch between
# using the render pipeline and using the default one
#
# Author:  Daniel Kierkegaard Andersen (dax@daxode.dk)
# Version: 2020-09-22
#
# Copyright (c) 2020 Daniel Kierkegaard Andersen. All rights reserved.
# https://github.com/Daxode/ComplexSoftwareProject
from Blobtory.Scripts.Pipeline.PipelineSwitcher import PipelineSwitcher


class WindowCreator:
    render_pipeline = None
    cubeSpacing: float = 8

    def __init__(self, base: ShowBase, enableRP: bool = False, isFullscreen: bool = False):
        self.enableRP = enableRP
        self.isFullscreen = isFullscreen
        self.base = base
        self.baseData: ShowBaseData = ShowBaseData(self.base)
        self.pipelineSwitcher = PipelineSwitcher(self)
        self.baseData.StartDebugRunner()
        self.__UpdateWindow()
        self.__EnableDebugEventSystem()
        self.base.accept('escape', sys.exit)

    def __EnableDebugEventSystem(self):
        self.base.accept("f", self.__HandleDebugKeys, ["f"])
        self.base.accept("p", self.__HandleDebugKeys, ["p"])

    def __HandleDebugKeys(self, key: str):
        if key == "f":
            self.isFullscreen = not self.isFullscreen
        if key == "p":
            self.enableRP = not self.enableRP
        self.__UpdateWindow()

    def __InitRp(self):
        sys.path.insert(0, "../../../assets/external_libs/render_pipeline")
        from assets.external_libs.render_pipeline.rpcore import RenderPipeline
        self.render_pipeline = RenderPipeline()
        self.render_pipeline.pre_showbase_init()

    @dispatch()
    def __UpdateWindow(self):
        self.UpdateWindow(self.isFullscreen, self.enableRP)

    @dispatch(bool, bool)
    def UpdateWindow(self, isFullscreen: bool, enableRP: bool):
        self.enableRP = enableRP
        self.isFullscreen = isFullscreen

        props = WindowProperties()
        props.setTitle('Blobtory')
        props.setIconFilename("assets/pandaIcon.ico")
        if self.isFullscreen:
            props.setFullscreen(1)
            props.setSize(1920, 1080)

        self.base.win.requestProperties(props)
        # self.base.disableMouse()

        if self.enableRP:
            if self.render_pipeline is None:
                self.__InitRp()

            self.render_pipeline.settings["pipeline.display_debugger"] = True
            self.render_pipeline.create(self.base)
            self.render_pipeline.loading_screen.remove()
        else:
            filters = CommonFilters(self.base.win, self.base.cam)
            # filters.setHighDynamicRange()
            # filters.setBloom()

            dlight = DirectionalLight('my dlight')
            dlight.setColor((0.8, 0.5, 0.5, 1))
            dlnp = self.base.render.attachNewNode(dlight)
            self.base.render.setAntialias(AntialiasAttrib.MAuto)
            self.base.render.setLight(dlnp)

            #filters.setAmbientOcclusion()
            # filters.setVolumetricLighting(dlnp)
            self.base.setBackgroundColor(0, 0.01, 0.1)
            self.base.setFrameRateMeter(True)
