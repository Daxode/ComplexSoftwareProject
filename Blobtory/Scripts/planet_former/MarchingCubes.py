import math

from panda3d.core import Texture, Shader, NodePath, LVecBase3i, ShaderAttrib, GeomEnums, GeomNode, \
    GeomVertexFormat, GeomVertexData, GeomTriangles, Geom, OmniBoundingVolume, Material, LColor, SamplerState, \
    TextureStage

from assets.shaders.compute.includes import MarchTable
from Blobtory.Scripts.planet_former.CubeFormer import CubeFormer


class MarchingCubes:
    atomic: Texture = None
    edgeVertexBuffer: Texture = None
    triangleBuffer: Texture = None
    triangulationBuffer: Texture = None
    normalBuffer: Texture = None
    edgeBufferGeneratorNode: NodePath = None
    cubeMarchBufferGeneratorNode: NodePath = None
    geom: Geom = None
    geomPath: NodePath = None
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
            self.edgeBufferGeneratorNode.set_shader_input("isoLevel", 0.5)
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
            self.normalBuffer = Texture("Cube march normal Buffer")
            self.normalBuffer.setupBufferTexture((self.size[0] - 1) * (self.size[1] - 1) * (self.size[2] - 1) * 4,
                                                   Texture.T_float, Texture.F_rgba32, GeomEnums.UH_dynamic)
        else:
            self.triangleBuffer.setClearColor(-1)

        if self.triangulationBuffer is None:
            self.triangulationBuffer = Texture("Triangulation buffer")
            self.triangulationBuffer.setup_2d_texture(16, 256, Texture.T_int, Texture.F_r32i)
            self.triangulationBuffer.set_ram_image(MarchTable.TRIANGULATION.tobytes())
        else:
            self.triangleBuffer.setClearColor(0)

        if self.cubeMarchBufferGeneratorNode is None:
            shader = Shader.load_compute(Shader.SL_GLSL, "assets/shaders/compute/cubemarcher.glsl")
            self.cubeMarchBufferGeneratorNode = NodePath("Cube march triangle Generator")
            self.cubeMarchBufferGeneratorNode.set_shader(shader)
            self.cubeMarchBufferGeneratorNode.set_shader_input("isoLevel", 0.5)
            self.cubeMarchBufferGeneratorNode.set_shader_input("size", self.size)
            self.cubeMarchBufferGeneratorNode.set_shader_input("triagIndexBuffer", self.atomic)

            self.cubeMarchBufferGeneratorNode.set_shader_input("vertexBufferWAlphaCube", self.cubeVertexBuffer)
            self.cubeMarchBufferGeneratorNode.set_shader_input("vertexBufferEdge", self.edgeVertexBuffer)
            self.cubeMarchBufferGeneratorNode.set_shader_input("triangleBuffer", self.triangleBuffer)
            self.cubeMarchBufferGeneratorNode.set_shader_input("triangulationBuffer", self.triangulationBuffer)
            self.cubeMarchBufferGeneratorNode.set_shader_input("normalBuffer", self.normalBuffer)

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
        # We need to set a bounding volume so that Panda doesn't try to cull it.
        # You could be smarter about this by assigning a bounding volume that encloses
        # the vertices.
        self.geom = Geom(vdata)

        # This represents a draw call, indicating how many vertices we want to draw.
        tris = GeomTriangles(GeomEnums.UH_dynamic)
        tris.add_next_vertices(self.vertexCount)
        self.geom.add_primitive(tris)

        self.geom.set_bounds(OmniBoundingVolume())
        node = GeomNode("node")
        node.add_geom(self.geom)
        if self.geomPath is not None: # Since it creates a new now, it should remove the last one
            self.winCreator.base.render.find("**/node").removeNode()

        self.geomPath = self.winCreator.base.render.attach_new_node(node)
        self.geomPath.setPos(
            -self.size.getX()*0.5*self.cubeformer.spacing,
            -self.size.getY()*0.5*self.cubeformer.spacing,
            -self.size.getZ()*0.5*self.cubeformer.spacing)

        self.winCreator.pipelineSwitcher.AddModelWithShaderGeneralName(self.geomPath, "assets/shaders/planets/planet")
        self.geomPath.set_shader_input('vertexBufferEdge', self.edgeVertexBuffer)
        self.geomPath.set_shader_input('triangleBuffer', self.triangleBuffer)
        self.geomPath.set_shader_input('normalBuffer', self.normalBuffer)

        myMaterial = Material()
        myMaterial.setShininess(0.8)  # Make this material shiny
        myMaterial.setDiffuse(LColor(0.99, 0.16, 0.06, 1)*0.1)
        myMaterial.setSpecular((1.1, 1.1, 1.1, 1))
        self.geomPath.setMaterial(myMaterial)

        myDiffTex = self.winCreator.base.loader.loadTexture(
            "assets/textures/ramps/rampTerrainDiffuse.png",
            "assets/textures/ramps/rampTerrainSpecular.png")
        #myDiffTex.setMagfilter(SamplerState.FT_linear)
        #myDiffTex.setMinfilter(SamplerState.FT_linear)

        stageDiff = TextureStage("Diffuse")
        stageDiff.setSort(1)
        self.geomPath.setTexture(stageDiff, myDiffTex)


