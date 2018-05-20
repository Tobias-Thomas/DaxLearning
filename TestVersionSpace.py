from random import shuffle,randint,sample,choice
from VersionSpace import VersionSpace

def checkIfDax(bug,daxInfos):
    dax = list(daxInfos)
    given = list(bug)
    for j in range(0, 5):
        if dax[j] == 'x':
            continue
        elif dax[j] != given[j]:
            return False
    return True

def createListOfBugs():
    allBugs = []
    for i in range(0,32):
        binI = createUniformBinary(i)
        allBugs.append(str(binI))
    return allBugs

def createUniformBinary(i):
    binI = bin(i)
    binI = binI[2:]
    while len(binI) < 5:
        binI = '0'+binI
    return binI

def createBugCharacteristics(amount):
    if amount < 1 or amount > 5:
        return
    chars = ''
    positions = sample([0, 1, 2, 3, 4], amount)
    for i in range(0, 5):
        if i in positions:
            chars += choice(['0', '1'])
        else:
            chars += 'x'
    return chars

allBugs = createListOfBugs()

for _ in range(0,10000):
    attributeNumber = randint(1, 3)
    daxCharacteristics = createBugCharacteristics(attributeNumber)
    vs = VersionSpace(attributeNumber)
    shuffle(allBugs)


    finished = False
    for i in range(0,32):
        thisBug = allBugs[i]
        isDax = checkIfDax(thisBug,daxCharacteristics)
        finished = vs.showNewBug(thisBug,isDax)
        if type(finished) is str:
            break

    if finished != daxCharacteristics:
        print(finished)
        print(daxCharacteristics)
        print(attributeNumber)
        break

print('All Tests done')