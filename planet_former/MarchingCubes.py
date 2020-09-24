import math

from panda3d.core import Texture, Shader, NodePath, LVecBase3i, ShaderAttrib, PTAInt, GeomEnums, GeomNode, \
    GeomVertexFormat, GeomVertexData, GeomTriangles, Geom, OmniBoundingVolume

from planet_former.CubeFormer import CubeFormer


class MarchingCubes:
    atomic: Texture = None
    edgeVertexBuffer: Texture = None
    triangleBuffer: Texture = None
    edgeBufferGeneratorNode: NodePath = None
    geom: GeomNode = None
    vertexCount: int = 0

    def __init__(self, cubeformer: CubeFormer):
        self.cubeformer = cubeformer
        self.winCreator = cubeformer.winCreator
        self.size = cubeformer.size
        self.cubeVertexBuffer = cubeformer.vertexBuffer
        self.edgeVertexCount = self.cubeformer.vertexCount*3

    def EdgeGenerator(self) -> Texture:
        if self.edgeVertexBuffer is None:
            self.edgeVertexBuffer = Texture("edge vertex buffer")
            self.edgeVertexBuffer.setup_3d_texture(self.size[0]*3, self.size[1], self.size[2],
                                                   Texture.T_float, Texture.F_rgba32)
        if self.atomic is None:
            self.atomic = Texture("atomic int")
            self.atomic.setupBufferTexture(1, Texture.T_int, Texture.F_r32i, GeomEnums.UH_dynamic)

        if self.edgeBufferGeneratorNode is None:
            shader = Shader.load_compute(Shader.SL_GLSL, "assets/shaders/compute/edgeBufferGenerator.glsl")
            self.edgeBufferGeneratorNode = NodePath("Edge Buffer Generator")
            self.edgeBufferGeneratorNode.set_shader(shader)
            self.edgeBufferGeneratorNode.set_shader_input("isoLevel", 0.3)

            self.edgeBufferGeneratorNode.set_shader_input("one", self.atomic)
            self.edgeBufferGeneratorNode.set_shader_input("size", self.size)
            self.edgeBufferGeneratorNode.set_shader_input("vertexBufferWAlphaCube", self.cubeVertexBuffer)
            self.edgeBufferGeneratorNode.set_shader_input("vertexBufferEdge", self.edgeVertexBuffer)

        self.atomic.setClearColor(0)
        yass = LVecBase3i(math.ceil(self.size[0]*3 / 16), math.ceil(self.size[1] / 8), math.ceil(self.size[2] / 8))
        self.winCreator.base.graphicsEngine.dispatch_compute(yass,
                                                             self.edgeBufferGeneratorNode.get_attrib(ShaderAttrib),
                                                             self.winCreator.base.win.get_gsg())

        self.winCreator.base.graphicsEngine.extractTextureData(self.atomic, self.winCreator.base.win.gsg)
        ramImage = self.atomic.getRamImage()
        self.vertexCount = memoryview(ramImage).cast('i')[0]
        print(self.vertexCount)

        return self.edgeVertexBuffer

    def MarchCube(self):
        self.winCreator.base.graphicsEngine.extractTextureData(self.atomic, self.winCreator.base.win.gsg)
        ramImage = self.atomic.getRamImage()
        self.vertexCount = memoryview(ramImage).cast('i')

        if self.triangleBuffer is None:
            shader = Shader.load_compute(Shader.SL_GLSL, "assets/shaders/compute/edgeBufferGenerator.glsl")
            self.triangleBuffer = NodePath("Edge Buffer Generator")
            self.triangleBuffer.set_shader(shader)
            self.triangleBuffer.set_shader_input("isoLevel", 0.3)

            self.triangleBuffer.set_shader_input("one", self.atomic)
            self.triangleBuffer.set_shader_input("size", self.size)
            self.triangleBuffer.set_shader_input("vertexBufferWAlphaCube", self.cubeVertexBuffer)
            self.triangleBuffer.set_shader_input("vertexBufferEdge", self.edgeVertexBuffer)

    def GenerateMesh(self):
        # Create a dummy vertex data object.
        format = GeomVertexFormat.get_empty()
        vdata = GeomVertexData('abc', format, GeomEnums.UH_static)

        # This represents a draw call, indicating how many vertices we want to draw.
        tris = GeomTriangles(GeomEnums.UH_static)
        tris.add_next_vertices(self.vertexCount)

        # We need to set a bounding volume so that Panda doesn't try to cull it.
        # You could be smarter about this by assigning a bounding volume that encloses
        # the vertices.
        geom = Geom(vdata)
        geom.add_primitive(tris)
        geom.set_bounds(OmniBoundingVolume())

        node = GeomNode("node")
        node.add_geom(geom)

        path = self.winCreator.base.render.attach_new_node(node)
        path.set_shader(self.winCreator.pipelineSwitcher.AddModelWithShaderGeneralName())
        path.set_shader_input('vdata', self.edgeVertexBuffer)
        path.set_shader_input('triagdata', self.triangleBuffer)