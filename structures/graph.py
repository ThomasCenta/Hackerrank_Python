class RSubsetGenerator:
    def __init__(self, n, r):
        self.n = n
        self.r = r
        self.currentSubset = [0]*r
        for i in range(r):
            self.currentSubset[i] = i
        self.currentSubset[r-1] -= 1

    def getNext(self):
        if self.currentSubset[self.r-1] < self.n-1:
            self.currentSubset[self.r-1] += 1
            return self.currentSubset
        i = self.r-2
        while i >= 0 and self.currentSubset[i] == self.currentSubset[i+1]-1:
            i -= 1
        if i == -1:
            return -1
        self.currentSubset[i] += 1
        base = self.currentSubset[i]
        for j in range(i+1,  self.r):
            self.currentSubset[j] = base + j-i
        return self.currentSubset

class Graph:

    #all nodes have indexing starting at 0
    def __init__(self, numNodes):
        self.numNodes = numNodes
        self.edgeMatrix = []
        self.allEdges = []
        for i in range(numNodes):
            self.edgeMatrix.append(['n']*numNodes)

    # value must be an int
    def addEdge(self, startNode, endNode, value):
        self.edgeMatrix[startNode][endNode] = value
        self.allEdges.append([startNode, endNode, value])

    # no negative weights allowed!
    # This is kind of a brute implementation. Doesnt use a growing frontier or anything
    def getShortestPathDijkstras(self, start, end):
        values = ['n']*self.numNodes
        setNodes = [False]*self.numNodes
        setNodes[start] = True
        values[start] = 0
        while not setNodes[end]:
            # update values
            minValue = 'n'
            minNode = 0
            for edge in self.allEdges:
                if values[edge[0]] != 'n' and not setNodes[edge[1]]:
                    newValue = values[edge[0]]+edge[2]
                    if values[edge[1]] == 'n' or newValue < values[edge[1]]:
                        values[edge[1]] = newValue
                    if minValue == 'n' or newValue < minValue:
                        minValue = newValue
                        minNode = edge[1]
            if minValue == 'n':
                return -1
            setNodes[minNode] = True
        return values[end]

    def _buildTSPPath(self, edgeIndices, start):
        path = [start]
        for i in range(self.numNodes-1):
            for edgeIndex in edgeIndices:
                if self.allEdges[edgeIndex][0] == path[len(path)-1]:
                    path.append(self.allEdges[edgeIndex][1])
        return path

    # returns all paths starting from start that touch every node
    def bruteTravellingSalesmen(self, start):
        gen = RSubsetGenerator(len(self.allEdges), self.numNodes-1)
        allPaths = []
        nextPath = gen.getNext()
        while nextPath != -1:
            foundValues = [False]*self.numNodes
            for index in nextPath:
                foundValues[self.allEdges[index][0]] = True
                foundValues[self.allEdges[index][1]] = True
            if not False in foundValues:
                allPaths.append(self._buildTSPPath(nextPath, start))
            nextPath = gen.getNext()
        return allPaths