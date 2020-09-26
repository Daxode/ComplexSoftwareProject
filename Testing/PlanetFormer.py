from direct.task import Task
from Blobtory.Scripts.BaseData import ShowBaseData


class PlanetFormer:
    def __init__(self, baseData: ShowBaseData):
        self.base = baseData.base
        self.gridSize = 5
        self.noiseScale = 5

    def noisify(self, task):
        mover = [self.base.mouseWatcherNode.getMouseX(),
                 self.base.mouseWatcherNode.getMouseY()] if self.base.mouseWatcherNode.hasMouse() else [0, 0]

        for sphereHolder in self.cube.findAllMatches("**/Sphere-Placeholder"):
            sphere = sphereHolder.children[0]
            spherePos = sphere.getNetTransform().getPos()
            brightness = (1 + self.noiseGen.noise(
                ((spherePos[0] / self.gridSize) + mover[0]) * self.noiseScale,
                ((spherePos[1] / self.gridSize) + mover[1]) * self.noiseScale,
                ((spherePos[2] / self.gridSize)) * self.noiseScale)) / 2
            sphereHolder.setColor(brightness, 0, 1 - brightness, 1)

        return Task.cont
