import math

from panda3d.core import Texture, Shader, NodePath, LVecBase3i, ShaderAttrib, PTAInt

from planet_former.CubeFormer import CubeFormer


class MarchingCubes:
    edgeVertexBuffer: Texture = None
    edgeBufferGeneratorNode: NodePath = None

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

        if self.edgeBufferGeneratorNode is None:
            shader = Shader.load_compute(Shader.SL_GLSL, "assets/shaders/compute/edgeBufferGenerator.glsl")
            self.edgeBufferGeneratorNode = NodePath("Edge Buffer Generator")
            self.edgeBufferGeneratorNode.set_shader(shader)
            self.edgeBufferGeneratorNode.set_shader_input("isoLevel", 0.3)
            atomicInt = PTAInt([0])
            # self.edgeBufferGeneratorNode.set_shader_input("one", atomicInt)
            self.edgeBufferGeneratorNode.set_shader_input("size", self.size)
            self.edgeBufferGeneratorNode.set_shader_input("vertexBufferWAlphaCube", self.cubeVertexBuffer)
            self.edgeBufferGeneratorNode.set_shader_input("vertexBufferEdge", self.edgeVertexBuffer)

        yass = LVecBase3i(math.ceil(self.size[0]*3 / 16), math.ceil(self.size[1] / 8), math.ceil(self.size[2] / 8))
        self.winCreator.base.graphicsEngine.dispatch_compute(yass,
                                                             self.edgeBufferGeneratorNode.get_attrib(ShaderAttrib),
                                                             self.winCreator.base.win.get_gsg())

        return self.edgeVertexBuffer
