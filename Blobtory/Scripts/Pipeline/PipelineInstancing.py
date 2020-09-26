import struct
from typing import *

from panda3d.core import Texture, GeomEnums, LMatrix4f, NodePath, OmniBoundingVolume, LVector3f
from Blobtory.Scripts.Pipeline import WindowCreator
from direct.showbase.Loader import Loader, PTAInt


class PipelineInstancing:
    @staticmethod
    def RenderThisModelAtMatrices(modelToApplyOn: Union[List[Optional[NodePath]], NodePath, None, Loader._Callback],
                                  matrices: List[LMatrix4f], winCreator: WindowCreator.WindowCreator) -> Texture:
        buffer = PipelineInstancing.__LoadBufferWithMatrices(matrices)
        PipelineInstancing.__AddMatrixBasedInstanceShader(modelToApplyOn, buffer, len(matrices), winCreator)
        PipelineInstancing.__DefineBoundingBox(modelToApplyOn)
        modelToApplyOn.reparentTo(winCreator.base.render)

        return buffer

    @staticmethod
    def RenderThisModelAtVertexes(modelToApplyOn: Union[List[Optional[NodePath]], NodePath, None, Loader._Callback],
                                  vertexes: List[LVector3f], winCreator: WindowCreator.WindowCreator) -> Texture:
        buffer = PipelineInstancing.__LoadBufferWithVertexes(vertexes)
        return PipelineInstancing.RenderThisModelAtVertexesFromBuffer(modelToApplyOn, buffer, len(vertexes), winCreator)

    @staticmethod
    def RenderThisModelAtVertexesFromBuffer(modelToApplyOn: Union[List[Optional[NodePath]], NodePath, None, Loader._Callback],
                                            buffer: Texture, vertexCount: int, winCreator: WindowCreator.WindowCreator) -> Texture:
        PipelineInstancing.__AddVertexBasedInstanceShader(modelToApplyOn, buffer, vertexCount, winCreator)
        PipelineInstancing.__DefineBoundingBox(modelToApplyOn)
        modelToApplyOn.reparentTo(winCreator.base.render)

        return buffer

    @staticmethod
    def RenderThisModelAtVertexesFrom3DBuffer(
            modelToApplyOn: Union[List[Optional[NodePath]], NodePath, None, Loader._Callback],
            buffer: Texture, vertexCount: PTAInt, winCreator: WindowCreator.WindowCreator) -> Texture:
        PipelineInstancing.__AddVertexBasedInstance3DBufferShader(modelToApplyOn, buffer, vertexCount, winCreator)
        PipelineInstancing.__DefineBoundingBox(modelToApplyOn)
        modelToApplyOn.reparentTo(winCreator.base.render)

        return buffer

    @staticmethod
    def __LoadBufferWithMatrices(matrices: List[LMatrix4f]) -> Texture:
        # Allocate storage for the matrices, each matrix has 16 elements,
        # but because one pixel has four components, we need amount * 4 pixels.
        buffer_texture = Texture()
        buffer_texture.setup_buffer_texture(len(matrices) * 4, Texture.T_float, Texture.F_rgba32, GeomEnums.UH_static)

        floats = []

        # Serialize matrices to floats
        ram_image = buffer_texture.modify_ram_image()

        for idx, mat in enumerate(matrices):
            for i in range(4):
                for j in range(4):
                    floats.append(mat.get_cell(i, j))

        # Write the floats to the texture
        data = struct.pack("f" * len(floats), *floats)
        ram_image.set_subdata(0, len(data), data)

        return buffer_texture

    @staticmethod
    def __LoadBufferWithVertexes(vertexes: List[LVector3f]) -> Texture:
        # Allocate storage for the matrices, each matrix has 16 elements,
        # but because one pixel has four components, we need amount * 4 pixels.
        buffer_texture = Texture()
        buffer_texture.setup_buffer_texture(len(vertexes), Texture.T_float, Texture.F_rgba32, GeomEnums.UH_static)

        floats = []

        # Serialize matrices to floats
        ram_image = buffer_texture.modify_ram_image()

        for vertex in vertexes:
            for j in range(3):
                floats.append(vertex[j])
            floats.append(0)

        # Write the floats to the texture
        data = struct.pack("f" * len(floats), *floats)
        ram_image.set_subdata(0, len(data), data)

        return buffer_texture

    @staticmethod
    def __AddMatrixBasedInstanceShader(modelToApplyOn: Union[List[Optional[NodePath]], NodePath, None, Loader._Callback],
                                       buffer_texture: Texture, instanceCount: int, winCreator: WindowCreator.WindowCreator):
        winCreator.pipelineSwitcher.AddModelWithShaderGeneralName(modelToApplyOn, "assets/shaders/instancing/instancing_basic_matrixbased")
        modelToApplyOn.set_shader_input("InstancingData", buffer_texture)
        modelToApplyOn.set_instance_count(instanceCount)

    @staticmethod
    def __AddVertexBasedInstanceShader(modelToApplyOn: Union[List[Optional[NodePath]], NodePath, None, Loader._Callback],
                                       buffer_texture: Texture, instanceCount: int, winCreator: WindowCreator.WindowCreator):
        winCreator.pipelineSwitcher.AddModelWithShaderGeneralName(modelToApplyOn, "assets/shaders/instancing/instancing_basic_vertexbased")
        modelToApplyOn.set_shader_input("InstancingData", buffer_texture)
        modelToApplyOn.set_instance_count(instanceCount)

    @staticmethod
    def __AddVertexBasedInstance3DBufferShader(modelToApplyOn: Union[List[Optional[NodePath]], NodePath, None, Loader._Callback],
                                               buffer_texture: Texture, instanceCount: PTAInt,
                                               winCreator: WindowCreator.WindowCreator):
        winCreator.pipelineSwitcher.AddModelWithShaderGeneralName(modelToApplyOn, "assets/shaders/instancing/instancing_3dbuffer_vertexbased")
        modelToApplyOn.set_shader_input("InstancingData", buffer_texture)
        modelToApplyOn.set_shader_input("size", instanceCount)
        modelToApplyOn.set_instance_count(instanceCount[0]*instanceCount[1]*instanceCount[2])


    @staticmethod
    def __DefineBoundingBox(modelToApplyOn: Union[List[Optional[NodePath]], NodePath, None, Loader._Callback]):
        # We have do disable culling, so that all instances stay visible
        modelToApplyOn.node().set_bounds(OmniBoundingVolume())
        modelToApplyOn.node().set_final(True)
