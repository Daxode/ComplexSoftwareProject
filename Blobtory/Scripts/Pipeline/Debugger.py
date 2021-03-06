from dataclasses import dataclass
from typing import *

from direct.showbase.ShowBase import ShowBase
from multipledispatch import dispatch

# Description:
# Added a simple debugger, this might be expanded upon later
#
# Author:  Daniel Kierkegaard Andersen (dax@daxode.dk)
# Version: 2020-09-20
#
# Copyright (c) 2020 Daniel Kierkegaard Andersen. All rights reserved.
# https://github.com/Daxode/ComplexSoftwareProject
from panda3d.core import Texture


@dataclass
class DebugMsgPacket:
    msg: str
    level: int


class Debugger:
    name: str
    queue: List[DebugMsgPacket]
    debugLevel: int

    @dispatch(str, int)
    def __init__(self, name: str, debugLevel: int):
        self.name = name
        self.queue = []
        self.debugLevel = debugLevel

    @dispatch(str)
    def __init__(self, name: str):
        self.name: str = name
        self.queue: List[DebugMsgPacket] = []
        self.debugLevel: int = 0

    def SetDebugLevel(self, val: int):
        self.debugLevel = val

    @dispatch(str)
    def __AddMsgToQueue(self, msg: str):
        self.__AddMsgToQueue(msg, 4)

    @dispatch(str, int)
    def __AddMsgToQueue(self, msg: str, level: int):
        self.queue.append(DebugMsgPacket(msg,  level))

    def Message(self, msg: str):
        self.__AddMsgToQueue("M - " + msg, 3)

    def Inform(self, msg: str):
        self.__AddMsgToQueue("I - " + msg, 2)

    def Warning(self, msg: str):
        self.__AddMsgToQueue("W - " + msg, 1)

    def Error(self, msg: str):
        self.__AddMsgToQueue("E - " + msg, 0)

    def Run(self):
        if len(self.queue) > 0:
            tmp: List[DebugMsgPacket] = []
            tmpPrinter: List[str] = []

            for msgPacket in self.queue:
                if msgPacket.level < self.debugLevel:
                    tmpPrinter.append(msgPacket.msg)
                else:
                    tmp.append(msgPacket)
            self.queue = tmp

            if len(tmpPrinter):
                print(f"------ {self.name} ------")
                [print(msg) for msg in tmpPrinter]
                print(f"------ end of debug ------")

    def LogBufferVecInfo(self, base: ShowBase, buffer: Texture, castTo: chr, amount: int):
        base.graphicsEngine.extractTextureData(buffer, base.win.gsg)
        idk = buffer.getRamImage()
        idk = memoryview(idk).cast(castTo)

        i = 0
        while i < len(idk):
            # print([[[idk[i+x+y+z] for z in range(amount)] for y in range(4)] for x in range(4)])
            # i += amount*4*4
            self.Inform(str([idk[i + x] for x in range(amount)]))
            i += amount
