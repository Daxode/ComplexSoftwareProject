from panda3d.core import PTAFloat

from Blobtory.Scripts.Pipeline.WindowCreator import WindowCreator
from Blobtory.Scripts.planet_former.CubeFormer import CubeFormer
from Blobtory.Scripts.planet_former.MarchingCubes import MarchingCubes


class PlanetGenerator:
    def __init__(self, winCreator: WindowCreator, gridSize: int, radius: float):
        self.radius = radius
        self.winCreator = winCreator
        self.cubeformer: CubeFormer = CubeFormer(self.winCreator, gridSize, gridSize, gridSize, winCreator.cubeSpacing)
        self.cubeformer.GenerateCube()
        self.cubeformer.GenerateNoiseSphere(self.radius)
        self.marchingCubes: MarchingCubes = MarchingCubes(self.cubeformer)
        self.marchingCubes.EdgeGenerator()
        self.marchingCubes.MarchCube()
        self.marchingCubes.GenerateMesh()

    def RegenPlanet(self):
        self.winCreator.baseData.debuggerPlanetFormer.Inform("Regenerating planet")
        self.cubeformer.GenerateNoiseSphere(self.radius)
        self.marchingCubes.EdgeGenerator()
        self.marchingCubes.MarchCube()
        self.marchingCubes.GenerateMesh()