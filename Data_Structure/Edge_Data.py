class Edge_Data:
    def __init__(self, src, dest, weight, tag) -> None:
        if weight < 0:
            raise Exception("edge weigh must be positive")
        self.src = src
        self.dest = dest
        self.tag = tag
        self.weight = weight

    def getSrc(self):
        return self.src

    def getDest(self):
        return self.dest

    def getWeight(self):
        return self.weight

    def geTag(self):
        return self.tag

    def seTag(self, t):
        self.tag = t

    def setWeight(self, w):
        self.weight = w

    def __str__(self):
        return f"src: {self.src}, dest: {self.dest}, tag: {self.tag}, weight :{self.weight}"

    def __repr__(self):
        return f"src: {self.src}, dest: {self.dest}, tag: {self.tag}, weight :{self.weight}"