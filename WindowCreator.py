from direct.showbase.ShowBase import ShowBase
from panda3d.core import WindowProperties
from BaseData import ShowBaseData
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


class WindowCreator:
    render_pipeline = None

    def __init__(self, base: ShowBase, enableRP: bool = False, isFullscreen: bool = False):
        self.enableRP = enableRP
        self.isFullscreen = isFullscreen
        self.base = base
        self.baseData: ShowBaseData = ShowBaseData(self.base)
        self.baseData.StartDebugRunner()
        self.UpdateWindow()
        self.EnableDebugEventSystem()

    def EnableDebugEventSystem(self):
        self.base.accept("f", self.HandleKey, ["f"])
        self.base.accept("p", self.HandleKey, ["p"])

    def HandleKey(self, key: str):
        if key == "f":
            self.isFullscreen = not self.isFullscreen
        if key == "p":
            self.enableRP = not self.enableRP
        self.UpdateWindow()

    def InitRp(self):
        sys.path.insert(0, "assets/external_libs/render_pipeline")
        from assets.external_libs.render_pipeline.rpcore import RenderPipeline
        self.render_pipeline = RenderPipeline()
        self.render_pipeline.pre_showbase_init()

    @dispatch()
    def UpdateWindow(self):
        self.UpdateWindow(self.isFullscreen, self.enableRP)

    @dispatch(bool, bool)
    def UpdateWindow(self, isFullscreen: bool, enableRP: bool):
        self.enableRP = enableRP
        self.isFullscreen = isFullscreen

        props = WindowProperties()
        props.setTitle('Marching Cubes')
        props.setIconFilename("assets/pandaIcon.ico")
        if self.isFullscreen:
            props.setFullscreen(1)
            props.setSize(1920, 1080)

        self.base.openMainWindow()
        self.base.win.requestProperties(props)
        self.base.graphicsEngine.openWindows()
        self.base.disableMouse()

        if self.enableRP:
            if self.render_pipeline is None:
                self.InitRp()

            self.render_pipeline.settings["pipeline.display_debugger"] = False
            self.render_pipeline.create(self.base)
            self.render_pipeline.set_effect(self.base.render, "assets/rp-effects/scene-effect.yaml", {}, sort=250)
            self.render_pipeline.loading_screen.remove()
        else:
            self.base.setBackgroundColor(0, 0.2, 0.4)
            self.base.render.setShaderAuto(True)
            self.base.setFrameRateMeter(True)
