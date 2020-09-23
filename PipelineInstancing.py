import struct
from typing import *

from panda3d.core import Texture, GeomEnums, LMatrix4f, NodePath, OmniBoundingVolume
import WindowCreator
from direct.showbase.Loader import Loader


class PipelineInstancing:
    @staticmethod
    def RenderThisModelAtMatrices(modelToApplyOn: Union[List[Optional[NodePath]], NodePath, None, Loader.Callback],
                                  matrices: List[LMatrix4f], winCreator: WindowCreator.WindowCreator) -> Texture:
        buffer = PipelineInstancing.__LoadBufferWithMatrices(matrices)
        PipelineInstancing.__AddShader(modelToApplyOn, buffer, len(matrices), winCreator)
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
    def __AddShader(modelToApplyOn: Union[List[Optional[NodePath]], NodePath, None, Loader.Callback],
                    buffer_texture: Texture, instanceCount: int, winCreator: WindowCreator.WindowCreator):
        winCreator.pipelineSwitcher.AddModelWithShaderGeneralName(modelToApplyOn, "assets/shaders/instancing/instancing_basic")
        modelToApplyOn.set_shader_input("InstancingData", buffer_texture)
        modelToApplyOn.set_instance_count(instanceCount)


    @staticmethod
    def __DefineBoundingBox(modelToApplyOn: Union[List[Optional[NodePath]], NodePath, None, Loader.Callback]):
        # We have do disable culling, so that all instances stay visible
        modelToApplyOn.node().set_bounds(OmniBoundingVolume())
        modelToApplyOn.node().set_final(True)
