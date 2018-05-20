class VersionSpace:
    G = ['xxxxx']
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
        if len(self.G) == 1 and self.G[0] == self.S or self.numOfS() == self.numberOfAttributes:
            return self.S
        self.G = list(set(self.G))  # remove duplicates from G
        return False

    def numOfS(self):
        num = 0
        gList = list(self.S)
        for i in range(0,len(gList)):
            if gList[i] != 'x':
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
        newG = []
        invBug = self.getInvBug(bug)
        for hypothesis in self.G:
            if self.doesHypothesisMatch(hypothesis,bug):
                newG += self.specializeHypothesis(hypothesis,invBug)
            else:
                newG.append(hypothesis)
        self.G = newG

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
        newG = []
        for hypothesis in self.G:
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