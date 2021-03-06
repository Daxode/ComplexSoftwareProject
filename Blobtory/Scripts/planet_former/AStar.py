from copy import deepcopy, copy
from typing import Dict, Set, List, Tuple
from Blobtory.Scripts.planet_former.Nodes import NodeRef, NodeKey, Node
from queue import PriorityQueue
from multipledispatch import dispatch
import numpy as np


def GetDist(pFrom: Node,
            pTo: Node):
    return (abs(pFrom[0] - pTo[0]) +
            abs(pFrom[1] - pTo[1]) +
            abs(pFrom[2] - pTo[2]))


def ReconstructPath(cameFrom: Dict[NodeRef, NodeKey], current: NodeKey):
    totalPath: List[Node] = [current]
    while current in cameFrom.keys():
        current = cameFrom[current]
        totalPath.insert(0, current)

    return totalPath


class AStar:
    nodeDict: Dict
    keyList: List[NodeKey]

    def __init__(self, nodeDict: Dict):
        self.nodeDict = nodeDict
        self.keyList = list(self.nodeDict.keys())

    def GetKeyNodeFromRef(self, p: NodeRef) -> NodeKey:
        return self.keyList[self.keyList.index(p)]

    def GetKeyNodeFromPoint(self, p: Node) -> NodeKey:
        return self.keyList[self.keyList.index(p)]

    def GetH(self, p: NodeKey) -> float:
        return 1/p.weight

    def GetPathFromTo(self,
                      pFrom: Node,
                      pTo: Node
                      ) -> List[Node]:
        startNode = self.GetKeyNodeFromPoint(pFrom)
        openSet = PriorityQueue()
        openSet.put((0, startNode))
        cameFrom: Dict[NodeRef, NodeKey] = {}

        gScore = {nodeKey: float("inf") for nodeKey in self.nodeDict.keys()}
        gScore[pFrom] = 0

        fScore = copy(gScore)
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
                tentativeGScore = gScore[current] + GetDist(current, neighbourPoint)

                if tentativeGScore < gScore[neighbourPoint]:
                    cameFrom[neighbourPoint] = current
                    gScore[neighbourPoint] = tentativeGScore
                    fScore[neighbourPoint] = gScore[neighbourPoint] + self.GetH(self.GetKeyNodeFromRef(neighbourPoint))
                    if neighbourPoint not in openSetTable:
                        openSet.put((fScore[neighbourPoint], neighbourPoint))
                        openSetTable.add(neighbourPoint)

        return []
