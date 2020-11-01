import math
from copy import copy, deepcopy

from panda3d.core import Texture, NodePath, Shader, LVecBase3i, ShaderAttrib, PTAFloat, LVecBase3f
from Blobtory.Scripts.Pipeline.WindowCreator import WindowCreator


class CubeFormer:
    vertexBuffer: Texture = None
    __alphaNoiseSphereComputeNode: NodePath = None
    __cubeBufferCreatorComputeNode: NodePath = None
    offset = PTAFloat([0])
    radius = PTAFloat([0])
    isWater = False

    def __init__(self, winCreator: WindowCreator, name: str, width: int, length: int, height: int, spacing: float):
        self.name = name
        self.winCreator = winCreator
        self.size = LVecBase3i(width, length, height)
        self.spacing = spacing
        self.vertexCount = width*length*height
        self.mouseTime: PTAFloat = PTAFloat([0, 0, 0, 0])
        self.planetCenters: PTAFloat = PTAFloat([0, 0, 0, 0])

    def GenerateCube(self) -> Texture:
        if self.vertexBuffer is None:
            self.vertexBuffer = deepcopy(Texture("vertex buffer"+self.name))
            self.vertexBuffer.setup_3d_texture(self.size[0], self.size[1], self.size[2], Texture.T_float, Texture.F_rgba32)

        if self.__cubeBufferCreatorComputeNode is None:
            shader = Shader.load_compute(Shader.SL_GLSL, "assets/shaders/compute/cubebuffercreator.glsl")
            self.__cubeBufferCreatorComputeNode = NodePath("Cube Buffer Creator Compute Node")
            self.__cubeBufferCreatorComputeNode.set_shader(shader)
            self.__cubeBufferCreatorComputeNode.set_shader_input("vertexBuffer", self.vertexBuffer)
            self.__cubeBufferCreatorComputeNode.set_shader_input("spacing", self.spacing)

        yass = LVecBase3i(math.ceil(self.size[0]/16), math.ceil(self.size[1]/8), math.ceil(self.size[2]/8))
        self.winCreator.base.graphicsEngine.dispatch_compute(yass,
            self.__cubeBufferCreatorComputeNode.get_attrib(ShaderAttrib), self.winCreator.base.win.get_gsg())

        return self.vertexBuffer

    def GenerateNoiseSphere(self, radius: float) -> Texture:
        self.radius.setData(PTAFloat([radius]))
        if self.__alphaNoiseSphereComputeNode is None:
            shader = Shader.load_compute(Shader.SL_GLSL, "assets/shaders/compute/alphaNoiseSphere.glsl")
            self.__alphaNoiseSphereComputeNode = NodePath("alphaNoiseSphere Compute Node")
            self.__alphaNoiseSphereComputeNode.set_shader(shader)
            self.__alphaNoiseSphereComputeNode.set_shader_input("center", LVecBase3f(
                self.size.getX()*self.spacing,
                self.size.getY()*self.spacing,
                self.size.getZ()*self.spacing)*0.5)
            self.__alphaNoiseSphereComputeNode.set_shader_input("radius", self.radius)
            self.__alphaNoiseSphereComputeNode.set_shader_input("vertexBufferWAlpha", self.vertexBuffer)
            self.__alphaNoiseSphereComputeNode.set_shader_input("offset", self.offset)
            self.__alphaNoiseSphereComputeNode.set_shader_input("mouseTime", self.mouseTime)

        yass = LVecBase3i(math.ceil(self.size[0]/16), math.ceil(self.size[1]/8), math.ceil(self.size[2]/8))
        self.winCreator.base.graphicsEngine.dispatch_compute(yass,
            self.__alphaNoiseSphereComputeNode.get_attrib(ShaderAttrib), self.winCreator.base.win.get_gsg())

        return self.vertexBuffer
