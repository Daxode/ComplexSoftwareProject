from panda3d.core import PTAFloat

from Blobtory.Scripts.Pipeline.WindowCreator import WindowCreator
from Blobtory.Scripts.planet_former.CubeFormer import CubeFormer
from Blobtory.Scripts.planet_former.MarchingCubes import MarchingCubes
from Blobtory.Scripts.Pipeline.PipelineInstancing import PipelineInstancing

class PlanetGenerator:
    def __init__(self, winCreator: WindowCreator, gridSize: int, radius: float):
        self.radius = radius
        self.winCreator = winCreator

        # Setup Mesh
        self.cubeformer: CubeFormer = CubeFormer(self.winCreator, gridSize, gridSize, gridSize, winCreator.cubeSpacing)
        self.cubeformer.GenerateCube()
        self.cubeformer.GenerateNoiseSphere(self.radius)

        self.marchingCubes: MarchingCubes = MarchingCubes(self.cubeformer)
        self.marchingCubes.EdgeGenerator()
        self.marchingCubes.MarchCube()
        self.marchingCubes.GenerateMesh()

        # Setup Navigation Mesh
        self.cubeformerNav: CubeFormer = CubeFormer(self.winCreator, gridSize//4, gridSize//4, gridSize//4, winCreator.cubeSpacing*4)
        self.cubeformerNav.GenerateCube()
        self.cubeformerNav.GenerateNoiseSphere(self.radius)

        self.marchingCubesNav: MarchingCubes = MarchingCubes(self.cubeformerNav)
        self.marchingCubesNav.EdgeGenerator()
        self.marchingCubesNav.MarchCube()

        # Setup Water Mesh
        self.cubeformerWater: CubeFormer = CubeFormer(self.winCreator, gridSize//4, gridSize//4, gridSize//4, winCreator.cubeSpacing*4)
        self.cubeformerWater.GenerateCube()
        self.cubeformerWater.mouseTime.setData(PTAFloat([10, 0, 0, 10.1]))
        self.cubeformerWater.GenerateNoiseSphere(self.radius * 0.98)
        self.cubeformerWater.isWater = True

        self.marchingCubesWater: MarchingCubes = MarchingCubes(self.cubeformerWater)
        self.marchingCubesWater.EdgeGenerator()
        self.marchingCubesWater.MarchCube()
        self.marchingCubesWater.GenerateMesh()

        # sphere = self.winCreator.base.loader.loadModel("assets/models/icosphere")
        # PipelineInstancing.RenderThisModelAtVertexesFrom3DBuffer(sphere, self.cubeformer.vertexBuffer,
        #                                                        self.cubeformer.size, self.winCreator)

        # box = self.winCreator.base.loader.loadModel("box")
        # PipelineInstancing.RenderThisModelAtVertexesFrom3DBuffer(box, self.cubeformerNav.vertexBuffer,
        #                                                          self.cubeformerNav.size, self.winCreator)

    def RegenPlanet(self):
        self.winCreator.baseData.debuggerPlanetFormer.Inform("Regenerating planet")

        self.cubeformerNav.GenerateNoiseSphere(self.radius)
        self.marchingCubesNav.EdgeGenerator()
        self.marchingCubesNav.MarchCube()
        self.marchingCubesNav.GenerateMesh()

        self.cubeformer.GenerateNoiseSphere(self.radius)
        self.marchingCubes.EdgeGenerator()
        self.marchingCubes.MarchCube()
        self.marchingCubes.GenerateMesh()
