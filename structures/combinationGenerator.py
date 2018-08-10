class SubsetGenerator:
    def __init__(self, n):
        self.n = n
        self.currentSubset = [0]*n

    def getNext(self):
        i = self.n - 1
        while(i >= 0 and self.currentSubset[i] == 1):
            self.currentSubset[i] = 0
            i -= 1
        if i == -1:
            return -1
        self.currentSubset[i] = 1
        return self.currentSubset

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

gen = RSubsetGenerator(6, 4)
nextSub = gen.getNext()
while nextSub != -1:
    print(nextSub)
    nextSub = gen.getNext()

