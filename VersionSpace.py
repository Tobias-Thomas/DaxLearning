class VersionSpace:
    G = [[] for _ in range(0,6)]
    G[0].append('xxxxx')
    S = ''
    numberOfAttributes = -1

    def __init__(self,numberOfAttributes):
        self.numberOfAttributes = numberOfAttributes

    def showNewBug(self,bug,isDax):
        if isDax:
            self.generalizeSpecial(bug)
        else:
            self.spezializeGeneral(bug)
        if self.S != '':
            self.correctMissmatches(self.S)
        self.removeDoublesFromG()
        if self.numOfHypo(self.S) == self.numberOfAttributes:
            return self.S
        if len(self.G[self.numberOfAttributes]) == 1:
            return self.G[self.numberOfAttributes][0]
        return False

    def removeDoublesFromG(self):
        i = 0
        for hList in self.G:
            if not hList:
                self.G[i] = []
            else:
                self.G[i] = self.removeDuplicates(hList)
            i += 1

    def removeDuplicates(self,list):
        seen = set()
        seenAdd = seen.add
        return[x for x in list if not (x in seen or seenAdd(x))]

    def numOfHypo(self,hypo):
        num = 0
        hypoList = list(hypo)
        for i in range(0,len(hypoList)):
            if hypoList[i] != 'x':
                num += 1
        return num

    def generalizeSpecial(self, bug):
        if self.S == '':
            self.S = bug
        else:
            newS = ''
            SList = list(self.S)
            bugList = list(bug)
            for i in range(0,len(bugList)):
                if SList[i] == bugList[i]:
                    newS += SList[i]
                else:
                    newS += 'x'
            self.S = newS

    def spezializeGeneral(self, bug):
        newG = [[] for _ in range(0,6)]
        invBug = self.getInvBug(bug)
        for i in range(0,len(self.G)):
            for hypothesis in self.G[i]:
                if self.doesHypothesisMatch(hypothesis,bug):
                    newHypoList = self.specializeHypothesis(hypothesis,invBug)
                    for h in newHypoList:
                        self.addToG(newG,h)
                else:
                    self.addToG(newG,hypothesis)
        self.G = newG

    def addToG(self,currG,newHypo):
        numOfAttributes = self.numOfHypo(newHypo)
        currG[numOfAttributes].append(newHypo)

    def specializeHypothesis(self,hypothesis,bug):
        specHypo = []
        hypoList = list(hypothesis)
        bugList = list(bug)
        for i in range(0,len(hypoList)):
            if hypoList[i] == 'x':
                newEntry = hypoList.copy()
                newEntry[i] = bugList[i]
                specHypo.append(self.convert(newEntry))
        return specHypo

    def convert(self,listChars):
        str = ''
        return(str.join(listChars))

    def getInvBug(self,bug):
        invBug = ''
        bugList = list(bug)
        for i in range(0,len(bugList)):
            if bugList[i] == '0':
                invBug += '1'
            elif bugList[i] == '1':
                invBug += '0'
            else:
                print('something got wrong')
        return invBug

    def correctMissmatches(self, reference):
        newG = [[] for i in range(0,6)]
        for i in range(0,len(self.G)):
            for hypothesis in self.G[i]:
                if self.doesHypothesisMatch(hypothesis,reference):
                    newG.append(hypothesis)
        self.G = newG

    def doesHypothesisMatch(self,hypothesis,reference):
        doesMatch = True
        hypoList = list(hypothesis)
        refList = list(reference)
        for i in range(0,len(hypoList)):
            if refList[i] != hypoList[i]:
                if hypoList[i] == 'x':
                    continue
                else:
                    doesMatch = False
        return doesMatch