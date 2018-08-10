import copy
def getRightmostCharacterSmallerThanNext(str):
    for i in reversed(range(len(str)-1)):
        if str[i] < str[i+1]:
            return i
    return -1

# insertion sort in range [l, r)
def sort(arr, l, r):
    i = l
    while i < r:
        j = i
        while j > l and arr[j-1] > arr[j]:
            arr[j-1], arr[j] = arr[j], arr[j-1]
            j = j-1
        i += 1

# Find the ceil of 'first char' in right of first character.
# Ceil of a character is the smallest character greater than it
def findCeil(str, c, startIndex):
    ceilIndex = startIndex
    for i in range(startIndex, len(str)):
        if str[i] > c and str[i] < str[ceilIndex]:
            ceilIndex = i
    return ceilIndex

# generates all distinct strings of str in alphabetical order
class DistinctPermutationGenerator:
    def __init__(self, str):
        self.current = sorted(str)
        self.n = len(str)
        self.isFinished = False

    def getCurrent(self):
        if self.isFinished:
            return ''
        return self.current

    def getNext(self):
        if self.isFinished:
            return ''
        rmsn = getRightmostCharacterSmallerThanNext(self.current)
        if rmsn == -1:
            self.isFinished = True
            return ''
        ceilIndex = findCeil(self.current, self.current[rmsn], rmsn + 1)
        self.current[rmsn], self.current[ceilIndex] = self.current[ceilIndex], self.current[rmsn]
        sort(self.current, rmsn + 1, len(self.current))
        return self.current

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
        used = [False]*len(edgeIndices)
        for i in range(self.numNodes-1):
            for j in range(len(edgeIndices)):
                if not used[j] and self.allEdges[edgeIndices[j]][0] == path[len(path)-1]:
                    path.append(self.allEdges[edgeIndices[j]][1])
                    used[j] = True
                if not used[j] and self.allEdges[edgeIndices[j]][1] == path[len(path)-1]:
                    path.append(self.allEdges[edgeIndices[j]][0])
                    used[j] = True
        return path

    # returns all paths starting from start that touch every node
    def bruteTravellingSalesmen(self, start):
        gen = RSubsetGenerator(len(self.allEdges), self.numNodes-1)
        allPaths = []
        nextPath = gen.getNext()
        count = 0
        while nextPath != -1:
            count += 1
            if count % 1000 == 0:
                print(count)
            #print(nextPath)
            foundValues = [0]*self.numNodes
            for index in nextPath:
                foundValues[self.allEdges[index][0]] += 1
                foundValues[self.allEdges[index][1]] += 1
            if foundValues[start] == 1 and foundValues.count(2) == self.numNodes-2:
                tpsPath = self._buildTSPPath(nextPath, start)
                if len(tpsPath) == self.numNodes and tpsPath not in allPaths:
                    allPaths.append(tpsPath)
            nextPath = gen.getNext()
        return allPaths



def getAllSwapNeighbors(str):
    toReturn = []
    for i in range(len(str)-1):
        newStr = list(str)
        newStr[i], newStr[i+1] = newStr[i+1], newStr[i]
        toReturn.append(''.join(newStr))
    return toReturn

def _swap(str, i, j):
    newStr = list(str)
    newStr[i], newStr[j] = newStr[j], newStr[i]
    return ''.join(newStr)

def getSwapIndex(str1, str2):
    for i in range(len(str1)-1):
        for j in range(i+1, len(str1)):
            if _swap(str1, i, j) == str2:
                return (i, j)
    return -1

def printIfSingleSwap(swapIndices):
    toPrint = []
    for swap in swapIndices:
        if abs(swap[0]-swap[1]) != 1:
            return
        toPrint.append(min(swap[0], swap[1]))
    print(toPrint)


startingSequence = '1234'
genPerms = DistinctPermutationGenerator(startingSequence)
allSequences = [''.join(genPerms.getCurrent())]
nextPerm = genPerms.getNext()
while(nextPerm != ''):
    allSequences.append(''.join(nextPerm))
    nextPerm = genPerms.getNext()


graph = Graph(len(allSequences))
for i in range(len(allSequences)):
    neighbors = getAllSwapNeighbors(allSequences[i])
    for neighbor in neighbors:
        graph.addEdge(i, allSequences.index(neighbor), 1)
allTSP = graph.bruteTravellingSalesmen(0)
for tsp in allTSP:
    swapIndices = []
    for i in range(len(tsp)-1):
        swapIndices.append(getSwapIndex(allSequences[tsp[i]], allSequences[tsp[i+1]]))
    printIfSingleSwap(swapIndices)









