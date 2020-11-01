import array

from direct.task import Task
from panda3d.core import PTAFloat, LVecBase3f
import numpy as np
from typing import Dict
import cv2
import copy

from Blobtory.Scripts.Pipeline.WindowCreator import WindowCreator
from Blobtory.Scripts.planet_former.CubeFormer import CubeFormer
from Blobtory.Scripts.planet_former.MarchingCubes import MarchingCubes
from Blobtory.Scripts.Pipeline.PipelineInstancing import PipelineInstancing


class PlanetGenerator:
    shouldUpdatePhysicsMeshes = False
    nodeDict: Dict = {}
    listOfItems = None

    def __init__(self, winCreator: WindowCreator, gridSize: int, radius: float):
        self.radius = radius
        self.winCreator = winCreator

        # Setup Mesh
        self.cubeformer: CubeFormer = CubeFormer(self.winCreator, "Normal", gridSize, gridSize, gridSize, winCreator.cubeSpacing)
        self.cubeformer.GenerateCube()
        self.marchingCubes: MarchingCubes = MarchingCubes(self.cubeformer)

        # Setup Navigation Mesh
        self.cubeformerNav: CubeFormer = CubeFormer(self.winCreator, "Navigation", gridSize//8, gridSize//8, gridSize//8, winCreator.cubeSpacing*8)
        self.cubeformerNav.GenerateCube()
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

        self.sphere = self.winCreator.base.loader.loadModel("assets/models/icosphere")
        self.sphere2 = self.winCreator.base.loader.loadModel("assets/models/icosphere")

        # sphere = self.winCreator.base.loader.loadModel("assets/models/icosphere")
        # PipelineInstancing.RenderThisModelAtVertexesFrom3DBuffer(sphere, self.cubeformer.vertexBuffer,
        #                                                        self.cubeformer.size, self.winCreator)

        # box = self.winCreator.base.loader.loadModel("box")
        # PipelineInstancing.RenderThisModelAtVertexesFrom3DBuffer(box, self.cubeformerNav.vertexBuffer,
        #                                                          self.cubeformerNav.size, self.winCreator)

        self.RegenPlanet()
        # self.winCreator.base.taskMgr.setupTaskChain('physics', numThreads=1)
        self.winCreator.base.taskMgr.doMethodLater(1, self.UpdatePhysicsMesh, "Planet Physics Updater"''', taskChain="physics"''')
        self.winCreator.base.accept("r", self.TryNavmesh)
        self.winCreator.base.accept("r-repeat", self.TryNavmesh)

    def TryNavmesh(self):
        examplePoint = next(self.listOfItems)
        neighbourPoints = self.nodeDict[examplePoint]

        self.sphere2.reparentTo(self.winCreator.base.render)
        self.sphere2.setScale(10)
        self.sphere2.setPos(examplePoint[0], examplePoint[1], examplePoint[2])
        print(examplePoint, neighbourPoints)

        # PipelineInstancing.RenderThisModelAtVertexesFrom3DBuffer(sphere, self.marchingCubesNav.edgeVertexBuffer, self.marchingCubesNav.size, self.winCreator)
        PipelineInstancing.RenderThisModelAtVertexes(self.sphere, list(neighbourPoints), self.winCreator)

    def RegenPlanet(self):
        self.winCreator.baseData.debuggerPlanetFormer.Inform("Regenerating planet")
        self.cubeformerNav.GenerateNoiseSphere(self.radius)
        self.cubeformer.GenerateNoiseSphere(self.radius)
        self.UpdatePlanet()

    def UpdatePlanet(self):
        self.marchingCubes.EdgeGenerator()
        self.marchingCubes.MarchCube()
        #self.marchingCubes.GenerateMesh()
        self.shouldUpdatePhysicsMeshes = True

    def UpdatePhysicsMesh(self, task):
        if self.shouldUpdatePhysicsMeshes:
            # Generate marching
            self.marchingCubesNav.EdgeGenerator()
            self.marchingCubesNav.MarchCube()
            self.marchingCubesNav.GenerateMesh()

            # Extract Mesh Data (Tri Indexes and Vertexes)
            self.winCreator.base.graphicsEngine.extractTextureData(self.marchingCubesNav.edgeVertexBuffer,
                                                                   self.winCreator.base.win.gsg)
            ramImageVertex = self.marchingCubesNav.edgeVertexBuffer.getRamImage()
            output = np.frombuffer(ramImageVertex, dtype=np.float32)
            output: np.ndarray = output.reshape((self.marchingCubesNav.size[2],
                                     self.marchingCubesNav.size[1],
                                     self.marchingCubesNav.size[0]*3, 4))

            self.winCreator.base.graphicsEngine.extractTextureData(self.marchingCubesNav.triangleBuffer,
                                                                   self.winCreator.base.win.gsg)
            ramImage = self.marchingCubesNav.triangleBuffer.getRamImage()
            outputTriangle = memoryview(ramImage).cast("i")

            # Restructure that data to be a node network instead using a dictionary
            outputR = map(tuple, output.reshape((self.marchingCubesNav.size[0]*3 *
                                     self.marchingCubesNav.size[1] *
                                     self.marchingCubesNav.size[2], 4)))
            self.nodeDict = dict((el, set([])) for el in outputR)
            del outputR

            buffer = np.empty(12, dtype=int)

            triagIndexCount = self.marchingCubesNav.vertexCount * 4
            for count, x in enumerate(outputTriangle):
                buffer[count % 12] = x
                if count % 12 == 11:
                    print(output.shape, buffer)
                    v1 = tuple(output[buffer[2], buffer[1], buffer[0]])
                    v2 = tuple(output[buffer[6], buffer[5], buffer[4]])
                    v3 = tuple(output[buffer[10], buffer[9], buffer[8]])

                    self.nodeDict[v1].add(v2)
                    self.nodeDict[v1].add(v3)

                    self.nodeDict[v2].add(v1)
                    self.nodeDict[v2].add(v3)

                    self.nodeDict[v3].add(v2)
                    self.nodeDict[v3].add(v1)

                if count > triagIndexCount:
                    break
            self.listOfItems = (item[0] for item in self.nodeDict.items() if len(item[1]) > 0)

            self.shouldUpdatePhysicsMeshes = False
        return Task.again
