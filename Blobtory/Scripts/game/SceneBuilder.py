from direct.interval.LerpInterval import LerpPosInterval, Shader
from direct.interval.MetaInterval import Sequence
from panda3d.core import AmbientLight, DirectionalLight, PTAFloat

from Blobtory.Scripts.Pipeline.WindowCreator import WindowCreator
from Blobtory.Scripts.planet_former.PlanetGenerator import PlanetGenerator


class SceneBuilder:
    def __init__(self, winCreator: WindowCreator):
        self.winCreator = winCreator
        self.base = winCreator.base
        self.SetupScene()

    def SetupScene(self):
        self.SetupLighting()
        self.SetupPlanets()

        # Moving sphere for shadow testing
        sphere = self.base.loader.loadModel("assets/models/icosphere")
        sphere.reparentTo(self.base.render)
        sphere.setScale(100)

        sphere.setShader(Shader.load(Shader.SL_GLSL,
                       vertex="assets/shaders/defaults/default.vert",
                       fragment="assets/shaders/defaults/default.frag"))
        sphere.setTexture(self.base.loader.loadTexture("assets/textures/ramps/rampToonLight.png"))

        startInterval = LerpPosInterval(sphere, 1, (0, -200, 600), (0, 200, 600), blendType='easeInOut')
        endInterval = LerpPosInterval(sphere, 1, (0, 200, 600), (0, -200, 600), blendType='easeInOut')
        Sequence(startInterval, endInterval).loop()

    def SetupPlanets(self):
        planetGen: PlanetGenerator = PlanetGenerator(self.winCreator, 128, 450)
        self.base.accept("d", self.IncreaseSize, [planetGen, 1.5])
        self.base.accept("d-repeat", self.IncreaseSize, [planetGen, 1.5])
        self.base.accept("a", self.IncreaseSize, [planetGen, -1.5])
        self.base.accept("a-repeat", self.IncreaseSize, [planetGen, -1.5])

    def IncreaseSize(self, planetGen: PlanetGenerator, a):
        planetGen.cubeformer.mouseTime.setData(PTAFloat([10, 0, 0, planetGen.cubeformer.mouseTime.getElement(3)+a]))
        planetGen.cubeformerNav.mouseTime.setData(PTAFloat([10, 0, 0, planetGen.cubeformer.mouseTime.getElement(3) + a]))
        planetGen.RegenPlanet()

    def SetupLighting(self):
        # Add ambient lighting
        alight = AmbientLight('alight')
        alight.setColor((0.1, 0.1, 0.1, 1))
        alnp = self.base.render.attachNewNode(alight)
        self.base.render.setLight(alnp)

        # Make the sun and place it
        sun = DirectionalLight('TheSun')
        sunNodePath = self.base.render.attachNewNode(sun)
        sunNodePath.setPos(0, 1000, 1000)
        sunNodePath.lookAt(0, 0, 0)
        self.base.render.setLight(sunNodePath)

        # Enable shadow mapping on sun
        lens = sun.get_lens(0)
        lens.set_film_size((1024, 1024))
        lens.set_near_far(0, 10000)
        sun.setShadowCaster(True, 2048, 2048)

        # Setup back lighting - faking GI
        dlight2 = DirectionalLight('my dlight2')
        dlight2.setColor((0.05, 0.05, 0.05, 1))
        dlnp2 = self.base.render.attachNewNode(dlight2)
        dlnp2.setPos(0, -1000, -1000)
        dlnp2.lookAt(0, 0, 0)
        self.base.render.setLight(dlnp2)