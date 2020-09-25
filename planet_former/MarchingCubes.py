import math

from panda3d.core import Texture, Shader, NodePath, LVecBase3i, ShaderAttrib, PTAInt, GeomEnums, GeomNode, \
    GeomVertexFormat, GeomVertexData, GeomTriangles, Geom, OmniBoundingVolume, PTA_uchar

from assets.shaders.compute.includes import MarchTable
from planet_former.CubeFormer import CubeFormer


class MarchingCubes:
    atomic: Texture = None
    edgeVertexBuffer: Texture = None
    triangleBuffer: Texture = None
    triangulationBuffer: Texture = None
    edgeBufferGeneratorNode: NodePath = None
    cubeMarchBufferGeneratorNode: NodePath = None
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
        else:
            self.edgeVertexBuffer.setClearColor(0)

        if self.edgeBufferGeneratorNode is None:
            shader = Shader.load_compute(Shader.SL_GLSL, "assets/shaders/compute/edgeBufferGenerator.glsl")
            self.edgeBufferGeneratorNode = NodePath("Edge Buffer Generator")
            self.edgeBufferGeneratorNode.set_shader(shader)
            self.edgeBufferGeneratorNode.set_shader_input("isoLevel", 0.3)
            self.edgeBufferGeneratorNode.set_shader_input("size", self.size)
            self.edgeBufferGeneratorNode.set_shader_input("vertexBufferWAlphaCube", self.cubeVertexBuffer)
            self.edgeBufferGeneratorNode.set_shader_input("vertexBufferEdge", self.edgeVertexBuffer)

        yass = LVecBase3i(math.ceil(self.size[0]*3 / 16), math.ceil(self.size[1] / 8), math.ceil(self.size[2] / 8))
        self.winCreator.base.graphicsEngine.dispatch_compute(yass,
                                                             self.edgeBufferGeneratorNode.get_attrib(ShaderAttrib),
                                                             self.winCreator.base.win.get_gsg())

        return self.edgeVertexBuffer

    def MarchCube(self):
        if self.atomic is None:
            self.atomic = Texture("atomic int")
            self.atomic.setupBufferTexture(1, Texture.T_int, Texture.F_r32i, GeomEnums.UH_dynamic)

        if self.triangleBuffer is None:
            self.triangleBuffer = Texture("Cube march triangle Buffer")
            self.triangleBuffer.setupBufferTexture((self.size[0]-1)*(self.size[1]-1)*(self.size[2]-1)*4*3,
                                                   Texture.T_int, Texture.F_rgba32, GeomEnums.UH_dynamic)
        else:
            self.triangleBuffer.setClearColor(-1)

        if self.triangulationBuffer is None:
            self.triangulationBuffer = Texture("Triangulation buffer")
            self.triangulationBuffer.setup_2d_texture(16, 256, Texture.T_int, Texture.F_r32i)
            # triangulationBufferRam: PTA_uchar = self.triangulationBuffer.modifyRamImage()
            # concatenatedTRIANGULATION = []
            # for x in range(len(MarchTable.TRIANGULATION)):
            #     for y in range(len(MarchTable.TRIANGULATION[0])):
            #         concatenatedTRIANGULATION.append(MarchTable.TRIANGULATION[x][y].())
            # triangulationBufferRam.setData(PTA_uchar(concatenatedTRIANGULATION))
            self.triangulationBuffer.set_ram_image(MarchTable.TRIANGULATION.tobytes())
        else:
            self.triangleBuffer.setClearColor(0)

        if self.cubeMarchBufferGeneratorNode is None:
            shader = Shader.load_compute(Shader.SL_GLSL, "assets/shaders/compute/cubemarcher.glsl")
            self.cubeMarchBufferGeneratorNode = NodePath("Cube march triangle Generator")
            self.cubeMarchBufferGeneratorNode.set_shader(shader)
            self.cubeMarchBufferGeneratorNode.set_shader_input("isoLevel", 0.6)
            self.cubeMarchBufferGeneratorNode.set_shader_input("size", self.size)
            self.cubeMarchBufferGeneratorNode.set_shader_input("triagIndexBuffer", self.atomic)

            self.cubeMarchBufferGeneratorNode.set_shader_input("vertexBufferWAlphaCube", self.cubeVertexBuffer)
            self.cubeMarchBufferGeneratorNode.set_shader_input("vertexBufferEdge", self.edgeVertexBuffer)
            self.cubeMarchBufferGeneratorNode.set_shader_input("triangleBuffer", self.triangleBuffer)
            self.cubeMarchBufferGeneratorNode.set_shader_input("triangulationBuffer", self.triangulationBuffer)

        self.atomic.setRamImage((0).to_bytes(4, 'big'))
        yass = LVecBase3i(math.ceil(self.size[0] / 16), math.ceil(self.size[1] / 8), math.ceil(self.size[2] / 8))
        self.winCreator.base.graphicsEngine.dispatch_compute(yass,
                                                             self.cubeMarchBufferGeneratorNode.get_attrib(ShaderAttrib),
                                                             self.winCreator.base.win.get_gsg())

        self.winCreator.base.graphicsEngine.extractTextureData(self.atomic, self.winCreator.base.win.gsg)
        ramImage = self.atomic.getRamImage()
        self.vertexCount = memoryview(ramImage).cast('i')[0]

        return self.triangleBuffer

    def GenerateMesh(self):
        # Create a dummy vertex data object.
        format = GeomVertexFormat.get_empty()
        vdata = GeomVertexData('March VData', format, GeomEnums.UH_dynamic)

        # This represents a draw call, indicating how many vertices we want to draw.
        tris = GeomTriangles(GeomEnums.UH_dynamic)
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
        self.winCreator.pipelineSwitcher.AddModelWithShaderGeneralName(path, "assets/shaders/planets/planet")
        path.set_shader_input('vertexBufferEdge', self.edgeVertexBuffer)
        path.set_shader_input('triangleBuffer', self.triangleBuffer)
        path.setTwoSided(True)
