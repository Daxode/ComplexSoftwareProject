from direct.showbase.ShowBase import ShowBase
from Blobtory.Scripts.Pipeline.Debugger import Debugger
from direct.task import Task

# Description:
# stores base data about the program, like debuggers and the showbase
#
# Author:  Daniel Kierkegaard Andersen (dax@daxode.dk)
# Version: 2020-09-20
#
# Copyright (c) 2020 Daniel Kierkegaard Andersen. All rights reserved.
# https://github.com/Daxode/ComplexSoftwareProject


class ShowBaseData:
    debuggerMain: Debugger
    debuggerPlanetFormer: Debugger
    base: ShowBase

    def __init__(self, base: ShowBase):
        self.base = base
        self.debuggerMain = Debugger("Main", 4)
        self.debuggerPlanetFormer = Debugger("Planet Former", 4)

    def StartDebugRunner(self):
        self.base.taskMgr.doMethodLater(1, self.RunDebuggers, "Run debuggers")

    def RunDebuggers(self, task: Task.Task):
        self.debuggerMain.Run()
        self.debuggerPlanetFormer.Run()
        return Task.again
