from typing import Dict, Set, List, Tuple
from Blobtory.Scripts.planet_former.NodeRef import NodeRef, NodeKey


class AStar:
    nodeDict: Dict

    def __init__(self, nodeDict: Dict):
        self.nodeDict = nodeDict

    def GetPathFromTo(self,
                      pFrom: Tuple[float, float, float, float],
                      pTo: Tuple[float, float, float, float]
                      ) -> List[Tuple[float, float, float, float]]:
        neighboursNeighbourPoints = []

        neighbourPointsTo: Set[NodeRef] = self.nodeDict[pTo]
        neighbourPointsFrom: Set[NodeRef] = self.nodeDict[pFrom]

        for point in neighbourPointsTo:
            # keyList = list(self.nodeDict.keys())
            # print(keyList[keyList.index(point)].point)
            points = self.nodeDict[point]
            neighboursNeighbourPoints.extend([point.point for point in points])

        for point in neighbourPointsFrom:
            points = self.nodeDict[point]
            neighboursNeighbourPoints.extend([point.point for point in points])

        return neighboursNeighbourPoints
