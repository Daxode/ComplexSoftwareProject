import math

from panda3d.core import Texture, NodePath, Shader, LVecBase3i, ShaderAttrib, PTAFloat, PTAInt
from WindowCreator import WindowCreator


class CubeFormer:
    vertexBuffer: Texture = None

    def __init__(self, winCreator: WindowCreator, width: int, length: int, height: int, spacing: float):
        self.winCreator = winCreator
        self.size = LVecBase3i(width, length, height)
        self.spacing = spacing
        self.midPoint = PTAFloat([width*spacing*0.5, length*spacing*0.5, height*spacing*0.5])
        self.vertexCount = width*length*height

    def GenerateCube(self) -> Texture:
        self.vertexBuffer = Texture("vertex buffer")
        self.vertexBuffer.setup_3d_texture(self.size[0], self.size[1], self.size[2], Texture.T_float, Texture.F_rgba32)

        shader = Shader.load_compute(Shader.SL_GLSL, "assets/shaders/compute/cubebuffercreator.glsl")
        dummy = NodePath("dummy")
        dummy.set_shader(shader)
        dummy.set_shader_input("vertexBuffer", self.vertexBuffer)
        dummy.set_shader_input("spacing", self.spacing)
        dummy.set_shader_input("midPoint", self.midPoint)

        yass = LVecBase3i(math.ceil(self.size[0]/16), math.ceil(self.size[1]/8), math.ceil(self.size[2]/8))
        self.winCreator.base.graphicsEngine.dispatch_compute(yass,
            dummy.get_attrib(ShaderAttrib), self.winCreator.base.win.get_gsg())

        return self.vertexBuffer

    def GenerateNoiseSphere(self, radius: float) -> Texture:
        shader = Shader.load_compute(Shader.SL_GLSL, "assets/shaders/compute/alphaNoiseSphere.glsl")
        dummy = NodePath("dummy")
        dummy.set_shader(shader)
        dummy.set_shader_input("radius", radius)
        dummy.set_shader_input("vertexBufferWAlpha", self.vertexBuffer)

        yass = LVecBase3i(math.ceil(self.size[0]/16), math.ceil(self.size[1]/8), math.ceil(self.size[2]/8))
        self.winCreator.base.graphicsEngine.dispatch_compute(yass,
            dummy.get_attrib(ShaderAttrib), self.winCreator.base.win.get_gsg())

        return self.vertexBuffer
