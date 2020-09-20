from math import pi, sin, cos
from direct.showbase.ShowBase import ShowBase
from panda3d.core import Fog
from panda3d.core import TextNode
from direct.gui.OnscreenText import OnscreenText
from direct.showbase.DirectObject import DirectObject
from direct.interval.MetaInterval import Sequence
from direct.interval.LerpInterval import LerpFunc
from direct.interval.FunctionInterval import Func
from panda3d.core import WindowProperties
from direct.showbase.DirectObject import DirectObject
from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from panda3d.core import lookAt
from panda3d.core import GeomVertexFormat, GeomVertexData
from panda3d.core import Geom, GeomTriangles, GeomVertexWriter
from panda3d.core import Texture, GeomNode
from panda3d.core import PerspectiveLens
from panda3d.core import CardMaker
from panda3d.core import Light, Spotlight
from panda3d.core import TextNode
from panda3d.core import LPoint3, LVector3
from panda3d.core import AmbientLight, PointLight
from direct.task import Task
from direct.actor.Actor import Actor
from direct.filter.CommonFilters import CommonFilters


import sys

def normals(*args):
    myVec = LVector3(*args)
    myVec = myVec * 2 - 1
    myVec.normalize()
    return myVec


# helper function to make a square given the Lower-Left-Hand and
# Upper-Right-Hand corners
def makeSquare(x1, y1, z1, x2, y2, z2, x3, y3, z3):
    format = GeomVertexFormat.getV3n3cpt2()
    vdata = GeomVertexData('square', format, Geom.UHDynamic)

    vertex = GeomVertexWriter(vdata, 'vertex')
    normal = GeomVertexWriter(vdata, 'normal')
    color = GeomVertexWriter(vdata, 'color')
    texcoord = GeomVertexWriter(vdata, 'texcoord')

    vertex.addData3(x1, y1, z1)
    vertex.addData3(x2, y2, z2)
    vertex.addData3(x3, y3, z3)
    vertex.addData3(x1, y2, z3)

    normal.addData3(normals(x1, y1, z1))
    normal.addData3(normals(x2, y2, z2))
    normal.addData3(normals(x3, y3, z3))
    normal.addData3(normals(x1, y2, z3))

    # adding different colors to the vertex for visibility
    color.addData4f(1.0, 0.0, 0.0, 1.0)
    color.addData4f(1.0, 1.0, 0.0, 1.0)
    color.addData4f(1.0, 0.0, 1.0, 1.0)
    color.addData4f(1.0, 0.0, 1.0, 1.0)

    texcoord.addData2f(0.0, 1.0)
    texcoord.addData2f(0.0, 0.0)
    texcoord.addData2f(1.0, 0.0)
    texcoord.addData2f(1.0, 1.0)

    tris = GeomTriangles(Geom.UHDynamic)
    tris.addVertices(0, 1, 3)
    tris.addVertices(1, 2, 3)

    square = Geom(vdata)
    square.addPrimitive(tris)
    return square


class FogDemo(ShowBase):
    def __init__(self):
        # Initialize the ShowBase class from which we inherit, which will
        # create a window and set up everything we need for rendering into it.
        ShowBase.__init__(self)
        panda3d.core.load_prc_file_data('', 'framebuffer-srgb true')
        filters = CommonFilters(base.win, base.cam)
        self.disableMouse()
        self.camera.setPos(0, -10, 0)

        props = WindowProperties()
        props.setTitle('Den kan ændres til Dansk')
        base.win.requestProperties(props)

        # Note: it isn't particularly efficient to make every face as a separate Geom.
        # instead, it would be better to create one Geom holding all of the faces.
        square0 = makeSquare(1, 1, 1,
                             1, -1, 1,
                             -1, -1, -1)
        snode = GeomNode('square')
        snode.addGeom(square0)
        self.render.setLightOff()

        self.cube = self.render.attachNewNode(snode)
        # self.cube.setTwoSided(True)
        # self.cube.hprInterval(1.5, (360, 360, 360)).loop()

        self.env = self.render.attachNewNode("Enviroment")

        # Add a light to the scene.
        self.lightpivot = self.render.attachNewNode("lightpivot")
        self.lightpivot.setPos(0, 0, 0)
        self.lightpivot.hprInterval(2, LPoint3(360, 0, 0)).loop()
        plight = PointLight('plight')
        plight.setColor((1, 0, 0, 1))
        plight.setAttenuation(LVector3(1, 0.05, 0.001))
        plnp = self.lightpivot.attachNewNode(plight)
        plnp.setPos(5, 0, 0)
        self.env.setLight(plnp)

        # Add an ambient light
        alight = AmbientLight('alight')
        alight.setColor((0.5, 0.5, 0.5, 1))
        alnp = render.attachNewNode(alight)
        self.env.setLight(alnp)

        # Create a sphere to denote the light
        sphere = self.loader.loadModel("models/icosphere")
        sphere.reparentTo(plnp)
        sphere.setColor((0.7, 0, 0, 1))
        sphere.setScale(0.5)
        self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")

        # Tell Panda that it should generate shaders performing per-pixel
        # lighting for the room.
        self.env.setShaderAuto()
        self.shaderenable = 1
        self.cube.reparentTo(self.env)

        # cube = Actor('models/bobbing_cube.egg', {'Test': 'bobbing'})

        bob = self.loader.loadModel("models/bobbing_cube.egg")
        bob.reparentTo(self.env)
        bob.setPos(0, 0, 2)
        # cube.loop('Test')

        # filters.setVolumetricLighting(plnp, 64, 1, 0.98, 0.1)
        filters.setBloom()
        filters.setAmbientOcclusion(numsamples=128)

        print(self.env)

    # Define a procedure to move the camera.
    def spinCameraTask(self, task):
        angleDegrees = task.time * 60.0
        angleRadians = angleDegrees * (pi / 180.0)
        self.camera.setPos(20 * sin(angleRadians), -20 * cos(angleRadians), sin(task.time)*20)
        self.camera.lookAt(0, 0, 0)
        return Task.cont


demo = FogDemo()
demo.run()
