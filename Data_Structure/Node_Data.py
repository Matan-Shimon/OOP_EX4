class Node_Data:
    def __init__(self, point, weight, node_id, tag) -> None:
        self.weight = weight
        self.node_id = node_id
        self.point = point
        self.tag = tag
        self.out_edges = 0
        self.in_edges = 0

    def getKey(self):
        return self.node_id

    def getPoint2D(self):
        return self.point

    def setPoint2D(self, otherPoint):
        self.point.setPoint(otherPoint)

    def getWeight(self):
        return self.weight

    def geTag(self):
        return self.tag

    def setWeight(self, w):
        self.weight = w

    def seTag(self, t):
        self.tag = t

    def __lt__(self, other):
        return self.weight < other.weight

    def __str__(self):
        return f"weight: {self.weight}, id: {self.node_id}, point: {self.point}, tag: {self.tag}"

    def __repr__(self):
        return f"{self.node_id}: |edges_out| {self.out_edges} |edges in| {self.in_edges}"