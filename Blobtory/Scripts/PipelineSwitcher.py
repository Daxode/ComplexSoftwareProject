from enum import Enum
from dataclasses import dataclass
from multipledispatch import dispatch

from panda3d.core import NodePath, Shader
from direct.showbase.Loader import Loader, Filename

from typing import *
from Blobtory.Scripts import WindowCreator


class PipelineMode(Enum):
    HDRP = 1
    DEFAULTRP = 2


@dataclass
class ShadersHolder:
    fragmentShader: Filename
    vertexShader: Filename
    hdrpShaderModel: Filename
    modelToApplyOn: Union[List[Optional[NodePath]], NodePath, None, Loader._Callback]


class PipelineSwitcher:
    pipelineMode: PipelineMode = PipelineMode.HDRP
    shaderManager: List[ShadersHolder] = []

    def __init__(self, winCreator: WindowCreator):
        self.winCreator = winCreator

    @dispatch()
    def UpdateShaders(self):
        if self.winCreator.enableRP:
            for shadersHolder in self.shaderManager:
                self.winCreator.render_pipeline.set_effect(shadersHolder.modelToApplyOn, shadersHolder.hdrpShaderModel, {}, sort=250)
            # self.winCreator.render_pipeline.reload_shaders()

        else:
            for shadersHolder in self.shaderManager:
                myShader: Shader = Shader.load(Shader.SL_GLSL,
                                               vertex=shadersHolder.vertexShader,
                                               fragment=shadersHolder.fragmentShader)
                shadersHolder.modelToApplyOn.setShader(myShader, 1)

    @dispatch(ShadersHolder)
    def UpdateShaders(self, shadersHolder: ShadersHolder):
        if self.winCreator.enableRP:
            print(type(shadersHolder.hdrpShaderModel), shadersHolder.hdrpShaderModel)
            self.winCreator.render_pipeline.set_effect(shadersHolder.modelToApplyOn, shadersHolder.hdrpShaderModel, {})
        else:
            myShader: Shader = Shader.load(Shader.SL_GLSL,
                                            vertex=shadersHolder.vertexShader,
                                            fragment=shadersHolder.fragmentShader)
            shadersHolder.modelToApplyOn.setShader(myShader, 1)

    def AddModelWithShaderGeneralName(self, modelToApplyOn: Union[List[Optional[NodePath]], NodePath, None, Loader._Callback],
                           shaderName: str = "assets/shaders/default"):
        self.AddModelWithShader(modelToApplyOn, Filename(shaderName+".frag"),
                                                Filename(shaderName+".vert"),
                                                shaderName+".yaml")

    def AddModelWithShader(self, modelToApplyOn: Union[List[Optional[NodePath]], NodePath, None, Loader._Callback],
                           fragmentShader: Filename = "assets/shaders/default.frag",
                           vertexShader: Filename = "assets/shaders/default.vert",
                           hdrpShaderModel: Filename = "assets/shaders/default.yaml"):
        shadersHolder = ShadersHolder(fragmentShader, vertexShader, hdrpShaderModel, modelToApplyOn)
        self.shaderManager.append(shadersHolder)
        self.UpdateShaders(shadersHolder)

