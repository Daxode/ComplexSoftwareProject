from direct.showbase.ShowBase import ShowBase
from panda3d.core import WindowProperties
from BaseData import ShowBaseData
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
    test: bool = False

    def __init__(self, base: ShowBase, enableRP: bool = False):
        self.enableRP = enableRP

        # Setup render pipeline
        if enableRP:
            sys.path.insert(0, "assets/external_libs/render_pipeline")
            from assets.external_libs.render_pipeline.rpcore import RenderPipeline
            self.render_pipeline = RenderPipeline()
            self.render_pipeline.pre_showbase_init()

        self.base = base
        self.baseData: ShowBaseData = ShowBaseData(self.base)
        self.baseData.StartDebugRunner()
        self.UpdateWindow(isFullscreen=True)

    def UpdateWindow(self, isFullscreen: bool):
        props = WindowProperties()
        props.setTitle('Marching Cubes')
        props.setIconFilename("assets/pandaIcon.ico")
        if isFullscreen:
            props.setFullscreen(1)
            props.setSize(1920, 1080)

        self.base.openMainWindow()
        self.base.win.requestProperties(props)
        self.base.graphicsEngine.openWindows()
        self.base.disableMouse()

        if self.enableRP:
            self.render_pipeline.settings["pipeline.display_debugger"] = False
            self.render_pipeline.create(self.base)
            self.render_pipeline.set_effect(self.base.render, "assets/rp-effects/scene-effect.yaml", {}, sort=250)
            self.render_pipeline.loading_screen.remove()
        else:
            self.base.setBackgroundColor(0, 0.2, 0.4)
            self.base.render.setShaderAuto(True)
            self.base.setFrameRateMeter(True)
