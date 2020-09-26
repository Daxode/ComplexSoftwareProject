from Blobtory.Scripts.Pipeline.BaseData import ShowBaseData


class SphereCreator:
    def __init__(self, baseData: ShowBaseData):
        self.baseData = baseData
        self.base = baseData.base

    def ReadyUpInput(self):
        self.base.accept("d", self.ChangeGridSize, [1])
        self.base.accept("a", self.ChangeGridSize, [-1])
        self.base.accept("w", self.ChangeInnerAmount, [1])
        self.base.accept("s", self.ChangeInnerAmount, [-1])
        self.base.accept("space", self.GenerateStuff)

    def ChangeGridSize(self, amount):
        self.gridSize += amount
        print(self.gridSize)

    def ChangeInnerAmount(self, amount):
        self.innerAmount += amount
        print(self.innerAmount)

    def genCubeNode(self):
        self.cube = NodePath('cube')
        self.cube.reparentTo(self.render)
        self.cube.setTransparency(TransparencyAttrib.MAlpha)
        self.cube.setAlphaScale(0.5)

    # Spherification of a cube - based on this https://catlikecoding.com/unity/tutorials/cube-sphere/ amazing article
    def Spherize(self, x, y, z, gridSize):
        p = np.array([x, y, z]) * 2.0 / gridSize - np.array([1, 1, 1])
        p2 = p * p
        rx = p[0] * math.sqrt(1.0 - 0.5 * (p2[1] + p2[2]) + p2[1] * p2[2] / 3.0)
        ry = p[1] * math.sqrt(1.0 - 0.5 * (p2[2] + p2[0]) + p2[2] * p2[0] / 3.0)
        rz = p[2] * math.sqrt(1.0 - 0.5 * (p2[0] + p2[1]) + p2[0] * p2[1] / 3.0)
        return LVecBase3f(rx, ry, rz)

    def SetVertex(self, vertexes, i, x, y, z):
        vertexes[i] = Vec3F(x, y, z)

    def CreateSpherizedCubeWithCompute(self, gridSize, radius):
        cube = self.CreateCube(gridSize, gridSize, gridSize)

        self.dummy.set_shader_input("gridSize", self.gridSize)
        self.dummy.set_shader_input("radius", radius)
        self.dummy.set_shader_input("fromVertexes", cube.tolist())
        sphere = [Vec3F()]*cube.size
        self.dummy.set_shader_input("toVertexes", sphere)

        # Retrieve the underlying ShaderAttrib
        self.sattr = self.dummy.get_attrib(ShaderAttrib)
        # Dispatch the compute shader, right now!
        self.base.graphicsEngine.dispatch_compute((1024, 1, 1), self.sattr, self.base.win.get_gsg())

        return sphere



    def CreateSpherizedCube(self, gridSize, radius):
        cube = self.CreateCube(gridSize, gridSize, gridSize)

        for i in range(len(cube)):
            v = cube[i]
            r = (radius*((2+self.noiseGen.noise(v*0.4))/3))
            cube[i] = self.Spherize(v[0], v[1], v[2], gridSize)*r

        return cube

    def CreateCube(self, xSize, ySize, zSize):
        cornerVertices = 8
        edgeVertices = (xSize + ySize + zSize - 3) * 4
        faceVertices = (
                               (xSize - 1) * (ySize - 1) +
                               (xSize - 1) * (zSize - 1) +
                               (ySize - 1) * (zSize - 1)) * 2
        vertexes = np.ndarray([cornerVertices + edgeVertices + faceVertices], dtype=Vec3F)

        v = 0
        for y in range(ySize + 1):
            for x in range(xSize + 1):
                self.SetVertex(vertexes, v, x, y, 0)
                v += 1

            for z in range(1, zSize + 1):
                self.SetVertex(vertexes, v, xSize, y, z)
                v += 1

            for x in range(xSize - 1, -1, -1):
                self.SetVertex(vertexes, v, x, y, zSize)
                v += 1

            for z in range(zSize - 1, 0, -1):
                self.SetVertex(vertexes, v, 0, y, z)
                v += 1

        for z in range(1, zSize):
            for x in range(1, xSize):
                self.SetVertex(vertexes, v, x, ySize, z)
                v += 1

        for z in range(1, zSize):
            for x in range(1, xSize):
                self.SetVertex(vertexes, v, x, 0, z)
                v += 1

        return vertexes

    def GenerateStuff(self):
        color = (0, 0, 0)
        self.cube.removeNode()
        self.genCubeNode()
        self.noiseGen = PerlinNoise3()
        cubes = np.ndarray([self.gridSize], dtype=np.ndarray)
        for i in range(self.innerAmount):
            cubes[i] = self.CreateSpherizedCubeWithCompute(self.gridSize, 20 - i * 2)
            for v in range(len(cubes[i])):
                if v % self.gridSize == 0:
                    color = (random.random(), random.random(), random.random())

                ver = cubes[i][v]
                placeholder = self.cube.attachNewNode("Sphere-Placeholder")
                placeholder.setPos(ver[0], ver[1], ver[2])
                # b = v/len(cubes[i])
                # placeholder.setColor(b)

                placeholder.setColor(color[0], color[1], color[2])
                self.sphere.instanceTo(placeholder)