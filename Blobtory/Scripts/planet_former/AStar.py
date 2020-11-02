from copy import deepcopy
from typing import Dict, Set, List, Tuple
from Blobtory.Scripts.planet_former.NodeRef import NodeRef, NodeKey
from queue import PriorityQueue
from multipledispatch import dispatch


def GetDist(pFrom: Tuple[float, float, float, float],
            pTo: Tuple[float, float, float, float]):
    return (abs(pFrom[0] - pTo[0]) +
            abs(pFrom[1] - pTo[1]) +
            abs(pFrom[2] - pTo[2]))


def ReconstructPath(cameFrom: Dict[NodeRef, NodeKey], current: NodeKey):
    totalPath: List[Tuple[float, float, float, float]] = [current.point]
    while current in cameFrom.keys():
        current = cameFrom[current]
        totalPath.insert(0, current.point)

    return totalPath


class AStar:
    nodeDict: Dict
    keyList: List[NodeKey]

    def __init__(self, nodeDict: Dict):
        self.nodeDict = nodeDict
        self.keyList = list(self.nodeDict.keys())

    def GetKeyNodeFromRef(self, p: NodeRef) -> NodeKey:
        return self.keyList[self.keyList.index(p.point)]

    def GetKeyNodeFromPoint(self, p: Tuple[float, float, float, float]) -> NodeKey:
        return self.keyList[self.keyList.index(p)]

    def GetH(self, p: NodeKey) -> float:
        return 1/p.weight

    def GetPathFromTo(self,
                      pFrom: Tuple[float, float, float, float],
                      pTo: Tuple[float, float, float, float]
                      ) -> List[Tuple[float, float, float, float]]:
        startNode = self.GetKeyNodeFromPoint(pFrom)
        openSet = PriorityQueue()
        openSet.put((0, startNode))
        cameFrom: Dict[NodeRef, NodeKey] = {}

        gScore = {nodeKey: float("inf") for nodeKey in self.nodeDict.keys()}
        gScore[pFrom] = 0

        fScore = deepcopy(gScore)
        fScore[pFrom] = self.GetH(startNode)

        openSetTable = {startNode}

        while not openSet.empty():
            setVal = openSet.get()
            current: NodeKey = setVal[1]
            openSetTable.remove(current)

            if current == pTo:
                return ReconstructPath(cameFrom, current)

            neighbourPoints: Set[NodeRef] = self.nodeDict[current]
            for neighbourPoint in neighbourPoints:
                tentativeGScore = gScore[current] + GetDist(current.point, neighbourPoint.point)

                if tentativeGScore < gScore[neighbourPoint]:
                    cameFrom[neighbourPoint] = current
                    gScore[neighbourPoint] = tentativeGScore
                    fScore[neighbourPoint] = gScore[neighbourPoint] + self.GetH(self.GetKeyNodeFromRef(neighbourPoint))
                    if neighbourPoint not in openSetTable:
                        openSet.put((fScore[neighbourPoint], neighbourPoint))
                        openSetTable.add(neighbourPoint)

        return []
