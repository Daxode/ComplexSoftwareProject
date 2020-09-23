from direct.task import Task
import math
from panda3d.core import loadPrcFile
from direct.showbase.ShowBase import ShowBase, Texture, GeomEnums, Shader, ShaderAttrib, LVecBase3i, PTAFloat

import PipelineInstancing
from WindowCreator import WindowCreator
from panda3d.core import NodePath, LVector3f

# Description:
# This is the main program, and should thus be kept clean,
# so stuff doesn't get out of control
#
# Author:  Daniel Kierkegaard Andersen (dax@daxode.dk)
# Version: 2020-09-22
#
# Copyright (c) 2020 Daniel Kierkegaard Andersen. All rights reserved.
# https://github.com/Daxode/ComplexSoftwareProject


class Main(ShowBase):
    def __init__(self):
        super().__init__()
        self.winCreator = WindowCreator(self, enableRP=False, isFullscreen=False)
        self.taskMgr.add(self.SpinCameraTask, "Move Cam")

        prefab = self.loader.loadModel("assets/models/icosphere")

        size = 64
        spacing = 2
        midPoint = size*spacing*0.5
        self.mouseTime = PTAFloat([0, 0, 0])

        # Different ways of instancing.. The first being recommended by Panda3D, the rest done by me, based on
        # an example found inside the render pipeline.. Which i also repurposed to a glsl shader
        if True:
            if False:
                if False:
                    # Collect all instances
                    prefab.reparentTo(self.render)
                    for x in range(size):
                        for y in range(size):
                            for z in range(size):
                                placeholder: NodePath = self.render.attachNewNode("icosphere-placeholder")
                                placeholder.setPos(x * spacing - midPoint, y * spacing - midPoint,
                                                   z * spacing - midPoint)
                                prefab.instanceTo(placeholder)
                else:
                    # Collect all instances
                    matrices = []
                    for x in range(size):
                        for y in range(size):
                            for z in range(size):
                                placeholder: NodePath = NodePath("icosphere-placeholder")
                                placeholder.setPos(x * spacing - midPoint, y * spacing - midPoint,
                                                   z * spacing - midPoint)
                                matrices.append(placeholder.get_mat(self.render))
                                placeholder.remove_node()

                    self.winCreator.baseData.debuggerMain.Inform(f"Loaded {len(matrices)} instances!")
                    PipelineInstancing.PipelineInstancing.RenderThisModelAtMatrices(prefab, matrices, self.winCreator)
            else:
                vertexCount = pow(size, 3)
                vertexBuffer = Texture("vertex buffer")
                vertexBuffer.setup_3d_texture(size, size, size, Texture.T_float, Texture.F_rgba32)

                shader = Shader.load_compute(Shader.SL_GLSL, "assets/shaders/compute/cubebuffercreator.glsl")
                dummy = NodePath("dummy")
                dummy.set_shader(shader)
                dummy.set_shader_input("vertexBuffer", vertexBuffer)
                dummy.set_shader_input("spacing", spacing)
                dummy.set_shader_input("midPoint", midPoint)

                batchSize = int(size/8)
                self.graphicsEngine.dispatch_compute(LVecBase3i(batchSize*2, batchSize, batchSize),
                                                     dummy.get_attrib(ShaderAttrib), self.win.get_gsg())

                self.winCreator.baseData.debuggerMain.Inform(f"Loaded {vertexCount} instances!")
                PipelineInstancing.PipelineInstancing.RenderThisModelAtVertexesFrom3DBuffer(prefab, vertexBuffer, vertexCount, self.winCreator)
                prefab.set_shader_input("mouseTime", self.mouseTime)
        else:
            # Collect all instances
            vertexes = []
            for x in range(size):
                for y in range(size):
                    for z in range(size):
                        vertexes.append(
                            LVector3f(x * spacing - midPoint, y * spacing - midPoint, z * spacing - midPoint))

            self.winCreator.baseData.debuggerMain.Inform(f"Loaded {len(vertexes)} instances!")
            PipelineInstancing.PipelineInstancing.RenderThisModelAtVertexes(prefab, vertexes, self.winCreator)

        self.x, self.y = 0, 0


    # Define a procedure to move the camera.
    def SpinCameraTask(self, task: Task.Task):
        radius: float = 1000
        angle_radians: float = task.time * 0.1

        self.camera.setPos(
            radius * math.sin(angle_radians),
            radius * math.cos(angle_radians),
            (math.sin(task.time)) * 5)
        self.camera.lookAt(0, 0, 0)

        if self.mouseWatcherNode.hasMouse():
            self.x = self.mouseWatcherNode.getMouseX()
            self.y = self.mouseWatcherNode.getMouseY()

        self.mouseTime.setData(PTAFloat([self.x, self.y, task.time]))

        return Task.cont


loadPrcFile("config/Config.prc")
blobtoryBase = Main()
blobtoryBase.run()