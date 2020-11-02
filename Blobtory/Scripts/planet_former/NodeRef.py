class NodeRef:
    point: (float, float, float, float)
    relativeDist: float = None

    def __init__(self, point: (float, float, float, float)):
        self.point = point

    def __hash__(self):
        return hash(self.point)

    def __getitem__(self, key):
        return self.point[key]

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __str__(self):
        return str(self.point)

    def __repr__(self):
        return str(self.point)


class NodeKey:
    point: (float, float, float, float)
    weight: float = 1

    def __init__(self, point: (float, float, float, float)):
        self.point = point

    def __hash__(self):
        return hash(self.point)

    def __getitem__(self, key):
        return self.point[key]

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __str__(self):
        return str(self.point)

    def __repr__(self):
        return str(self.point)