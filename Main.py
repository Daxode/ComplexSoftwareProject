import struct

from direct.task import Task
import math
from panda3d.core import loadPrcFile, OmniBoundingVolume, Texture, GeomEnums, Shader, PTAFloat
from direct.showbase.ShowBase import ShowBase
from WindowCreator import WindowCreator
from panda3d.core import NodePath

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
        prefab.reparentTo(self.render)
        size = 48
        spacing = 4

        midPoint = size*spacing*0.5

        # Collect all instances
        matrices = []
        for x in range(size):
            for y in range(size):
                for z in range(size):
                    placeholder: NodePath = NodePath("icosphere-placeholder")
                    placeholder.setPos(x*spacing-midPoint, y*spacing-midPoint, z*spacing-midPoint)
                    matrices.append(placeholder.get_mat(self.render))
                    placeholder.remove_node()

        print("Loaded", len(matrices), "instances!")

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

        # Load the effect
        # self.winCreator.render_pipeline.set_effect(prefab, "effects/basic_instancing.yaml", {})
        # myShader: Shader = Shader.load(Shader.SL_GLSL, vertex="assets/shaders/instancingShader.vert", fragment="assets/shaders/instancingShader.frag")
        # prefab.setShader(myShader, 1)

        prefab.set_shader_input("InstancingData", buffer_texture)
        prefab.set_instance_count(len(matrices))

        self.mouseTime = PTAFloat([0, 0, 0])
        prefab.set_shader_input("mouseTime", self.mouseTime)

        # We have do disable culling, so that all instances stay visible
        prefab.node().set_bounds(OmniBoundingVolume())
        prefab.node().set_final(True)
        self.x, self.y = 0, 0

    # Define a procedure to move the camera.
    def SpinCameraTask(self, task: Task.Task):
        radius: float = 200
        angle_radians: float = task.time * 0.1

        self.camera.setPos(
            radius * math.sin(angle_radians),
            radius * math.cos(angle_radians),
            (math.sin(task.time)) * 1)
        self.camera.lookAt(0, 0, 0)

        if self.mouseWatcherNode.hasMouse():
            self.x = self.mouseWatcherNode.getMouseX()
            self.y = self.mouseWatcherNode.getMouseY()

        self.mouseTime.setData(PTAFloat([self.x, self.y, task.time]))

        return Task.cont


loadPrcFile("config/Config.prc")
blobtoryBase = Main()
blobtoryBase.run()
