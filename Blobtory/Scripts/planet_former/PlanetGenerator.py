import array

from direct.task import Task
from panda3d.core import PTAFloat, LVecBase3f
import numpy as np
from typing import Dict, Set
import copy

from Blobtory.Scripts.Pipeline.WindowCreator import WindowCreator
from Blobtory.Scripts.planet_former.CubeFormer import CubeFormer
from Blobtory.Scripts.planet_former.MarchingCubes import MarchingCubes
from Blobtory.Scripts.Pipeline.PipelineInstancing import PipelineInstancing
from Blobtory.Scripts.planet_former.Nodes import NodeRef, NodeKey
from Blobtory.Scripts.planet_former.AStar import AStar


class PlanetGenerator:
    shouldUpdatePhysicsMeshes = False
    aStarHandler: AStar
    listOfItems = None
    examplePointFrom: NodeKey

    def __init__(self, winCreator: WindowCreator, gridSize: int, radius: float):
        self.radius = radius
        self.winCreator = winCreator

        # Setup Mesh
        self.cubeformer: CubeFormer = CubeFormer(self.winCreator, "Normal", gridSize, gridSize, gridSize, winCreator.cubeSpacing)
        self.cubeformer.GenerateCube()
        self.cubeformer.mouseTime.setData(PTAFloat([10, 0, 0, 60.1]))
        self.marchingCubes: MarchingCubes = MarchingCubes(self.cubeformer)

        # Setup Navigation Mesh
        self.cubeformerNav: CubeFormer = CubeFormer(self.winCreator, "Navigation", gridSize//4, gridSize//4, gridSize//4, winCreator.cubeSpacing*4)
        self.cubeformerNav.GenerateCube()
        self.cubeformerNav.mouseTime = self.cubeformer.mouseTime
        self.marchingCubesNav: MarchingCubes = MarchingCubes(self.cubeformerNav)

        # Setup Water Mesh
        self.cubeformerWater: CubeFormer = CubeFormer(self.winCreator, "Water", gridSize//4, gridSize//4, gridSize//4, winCreator.cubeSpacing*4)
        self.cubeformerWater.GenerateCube()
        self.cubeformerWater.mouseTime.setData(PTAFloat([10, 0, 0, 6.1]))
        self.cubeformerWater.GenerateNoiseSphere(self.radius * 0.98)
        self.cubeformerWater.isWater = True

        self.marchingCubesWater: MarchingCubes = MarchingCubes(self.cubeformerWater)
        self.marchingCubesWater.EdgeGenerator()
        self.marchingCubesWater.MarchCube()
        self.marchingCubesWater.GenerateMesh()

        self.sphere1 = self.winCreator.base.loader.loadModel("assets/models/icosphere")

        self.sphere2 = self.winCreator.base.loader.loadModel("assets/models/icosphere")
        self.sphere2.reparentTo(self.winCreator.base.render)
        self.sphere2.setScale(10)

        self.sphere3 = self.winCreator.base.loader.loadModel("assets/models/icosphere")
        self.sphere3.reparentTo(self.winCreator.base.render)
        self.sphere3.setScale(10)

        self.RegenPlanet()
        self.winCreator.base.taskMgr.doMethodLater(1, self.UpdatePhysicsMesh, "Planet Physics Updater")

        self.winCreator.base.accept("r", self.NextPoint)

    def NextPoint(self):
        for i in range(20): next(self.listOfItems)
        examplePointTo: NodeKey = next(self.listOfItems)

        self.sphere3.setPos(examplePointTo[0], examplePointTo[1], examplePointTo[2])
        PipelineInstancing.RenderThisModelAtVertexes(self.sphere1,
                                                     self.aStarHandler.GetPathFromTo(
                                                         self.examplePointFrom,
                                                         examplePointTo),
                                                     self.winCreator)

    def RegenPlanet(self):
        self.winCreator.baseData.debuggerPlanetFormer.Inform("Regenerating planet")
        self.cubeformerNav.GenerateNoiseSphere(self.radius)
        self.cubeformer.GenerateNoiseSphere(self.radius)
        self.UpdatePlanet()

    def UpdatePlanet(self):
        self.marchingCubes.EdgeGenerator()
        self.marchingCubes.MarchCube()
        self.marchingCubes.GenerateMesh()
        self.shouldUpdatePhysicsMeshes = True

    def UpdatePhysicsMesh(self, task):
        if self.shouldUpdatePhysicsMeshes:
            self.GenerateAStarPather()

            self.shouldUpdatePhysicsMeshes = False
        return Task.again

    def GenerateAStarPather(self):
        # Generate marching
        self.marchingCubesNav.EdgeGenerator()
        self.marchingCubesNav.MarchCube()
        # self.marchingCubesNav.GenerateMesh()

        # Extract Mesh Data (Tri Indexes and Vertexes)
        self.winCreator.base.graphicsEngine.extractTextureData(self.marchingCubesNav.edgeVertexBuffer,
                                                               self.winCreator.base.win.gsg)
        ramImageVertex = self.marchingCubesNav.edgeVertexBuffer.getRamImage()
        output = np.frombuffer(ramImageVertex, dtype=np.float32)
        output: np.ndarray = output.reshape((self.marchingCubesNav.size[2],
                                             self.marchingCubesNav.size[1],
                                             self.marchingCubesNav.size[0] * 3, 4))

        self.winCreator.base.graphicsEngine.extractTextureData(self.marchingCubesNav.triangleBuffer,
                                                               self.winCreator.base.win.gsg)
        ramImage = self.marchingCubesNav.triangleBuffer.getRamImage()
        outputTriangle = memoryview(ramImage).cast("i")

        # Restructure that data to be a node network instead using a dictionary
        outputR = output.reshape((self.marchingCubesNav.size[0] * 3 *
                                             self.marchingCubesNav.size[1] *
                                             self.marchingCubesNav.size[2], 4))
        nodeDict = dict((NodeKey(memoryview(el)), set([])) for el in outputR)
        del outputR

        buffer = np.empty(12, dtype=int)

        triagIndexCount = self.marchingCubesNav.vertexCount * 4
        for count, x in enumerate(outputTriangle):
            buffer[count % 12] = x
            if count % 12 == 11:
                v1: NodeRef = NodeRef(memoryview(output[buffer[2], buffer[1], buffer[0]]))
                v2: NodeRef = NodeRef(memoryview(output[buffer[6], buffer[5], buffer[4]]))
                v3: NodeRef = NodeRef(memoryview(output[buffer[10], buffer[9], buffer[8]]))

                nodeDict[v1].add(v2)
                nodeDict[v1].add(v3)

                nodeDict[v2].add(v1)
                nodeDict[v2].add(v3)

                nodeDict[v3].add(v2)
                nodeDict[v3].add(v1)

            if count > triagIndexCount:
                break
        self.listOfItems = (item[0] for item in nodeDict.items() if len(item[1]) > 0)

        self.examplePointFrom: NodeKey = next(self.listOfItems)
        self.sphere2.setPos(self.examplePointFrom[0], self.examplePointFrom[1], self.examplePointFrom[2])

        self.aStarHandler = AStar(nodeDict)
