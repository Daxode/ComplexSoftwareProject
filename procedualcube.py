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
from panda3d.core import LVector3

import sys


# You can't normalize inline so this is a helper function
def normalized(*args):
    myVec = LVector3(*args)
    myVec.normalize()
    return myVec


def normals(*args):
    myVec = LVector3(*args)
    myVec = myVec * 2 - 1
    myVec.normalize()
    return myVec


# helper function to make a square given the Lower-Left-Hand and
# Upper-Right-Hand corners
def makeSquare(x1, y1, z1, x2, y2, z2):
    format = GeomVertexFormat.getV3n3cpt2()
    vdata = GeomVertexData('square', format, Geom.UHDynamic)

    vertex = GeomVertexWriter(vdata, 'vertex')
    normal = GeomVertexWriter(vdata, 'normal')
    color = GeomVertexWriter(vdata, 'color')
    texcoord = GeomVertexWriter(vdata, 'texcoord')

    # make sure we draw the sqaure in the right plane
    if x1 != x2:
        vertex.addData3(x1, y1, z1)
        vertex.addData3(x2, y1, z1)
        vertex.addData3(x2, y2, z2)
        vertex.addData3(x1, y2, z2)

        normal.addData3(normals(x1, y1, z1))
        normal.addData3(normals(x2, y1, z1))
        normal.addData3(normals(x2, y2, z2))
        normal.addData3(normals(x1, y2, z2))

    else:
        vertex.addData3(x1, y1, z1)
        vertex.addData3(x2, y2, z1)
        vertex.addData3(x2, y2, z2)
        vertex.addData3(x1, y1, z2)

        normal.addData3(normals(x1, y1, z1))
        normal.addData3(normals(x2, y2, z1))
        normal.addData3(normals(x2, y2, z2))
        normal.addData3(normals(x1, y1, z2))

    # adding different colors to the vertex for visibility
    color.addData4f(1.0, 0.0, 0.0, 1.0)
    color.addData4f(1.0, 1.0, 0.0, 1.0)
    color.addData4f(1.0, 0.0, 1.0, 1.0)
    color.addData4f(1.0, 0.0, 1.0, 1.0)

    texcoord.addData2f(0.0, 1.0)
    texcoord.addData2f(0.0, 0.0)
    texcoord.addData2f(1.0, 0.0)
    texcoord.addData2f(0.0, 1.0)

    # Quads aren't directly supported by the Geom interface
    # you might be interested in the CardMaker class if you are
    # interested in rectangle though
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
        self.disableMouse()
        self.camera.setPos(0, -10, 0)

        self.title = OnscreenText(text="Panda3D: Tutorial - Making a Cube Procedurally",
                                  style=1, fg=(1, 1, 1, 1), pos=(-0.1, 0.1), scale=.07,
                                  parent=base.a2dBottomRight, align=TextNode.ARight)
        self.escapeEvent = OnscreenText(text="1: Set a Texture onto the Cube",
                                        style=1, fg=(1, 1, 1, 1), pos=(0.06, -0.08),
                                        align=TextNode.ALeft, scale=.05,
                                        parent=base.a2dTopLeft)
        self.spaceEvent = OnscreenText(text="2: Toggle Light from the front On/Off",
                                       style=1, fg=(1, 1, 1, 1), pos=(0.06, -0.14),
                                       align=TextNode.ALeft, scale=.05,
                                       parent=base.a2dTopLeft)
        self.upDownEvent = OnscreenText(text="3: Toggle Light from on top On/Off",
                                        style=1, fg=(1, 1, 1, 1), pos=(0.06, -0.20),
                                        align=TextNode.ALeft, scale=.05,
                                        parent=base.a2dTopLeft)

        props = WindowProperties()
        props.setTitle('Den kan ændres til Dansk')
        base.win.requestProperties(props)

        # Note: it isn't particularly efficient to make every face as a separate Geom.
        # instead, it would be better to create one Geom holding all of the faces.
        square0 = makeSquare(-1, -1, -1, 1, -1, 1)
        square1 = makeSquare(-1, 1, -1, 1, 1, 1)
        square2 = makeSquare(-1, 1, 1, 1, -1, 1)
        square3 = makeSquare(-1, 1, -1, 1, -1, -1)
        square4 = makeSquare(-1, -1, -1, -1, 1, 1)
        square5 = makeSquare(1, -1, -1, 1, 1, 1)
        snode = GeomNode('square')
        snode.addGeom(square0)
        snode.addGeom(square1)
        snode.addGeom(square2)
        snode.addGeom(square3)
        snode.addGeom(square4)
        snode.addGeom(square5)

        self.cube = render.attachNewNode(snode)
        self.cube.hprInterval(10.5, (360, 360, 360)).loop()

        self.accept("space", self.toggleLightsSide)

        self.LightsOn = False
        slight = Spotlight('slight')
        slight.setColor((1, 1, 0, 1))
        lens = PerspectiveLens()
        slight.setLens(lens)
        self.slnp = render.attachNewNode(slight)

    def toggleLightsSide(self):
        self.LightsOn = not self.LightsOn

        if self.LightsOn:
            render.setLight(self.slnp)
            self.slnp.setPos(self.cube, 10, -400, 0)
            self.slnp.lookAt(10, 0, 0)
        else:
            render.setLightOff(self.slnp)


demo = FogDemo()
demo.run()
