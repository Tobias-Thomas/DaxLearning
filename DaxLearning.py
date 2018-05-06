from psychopy import visual, core, event, gui, data
from psychopy.tools.filetools import fromFile, toFile
from random import randint
import numpy, random


def createBugCharacteristics(amount):
    if amount < 1 or amount > 5:
        return
    chars = ''
    positions = random.sample([0, 1, 2, 3, 4], amount)
    for i in range(0, 5):
        if i in positions:
            chars += random.choice(['0', '1'])
        else:
            chars += 'x'
    print(chars)
    return chars


def isThisADax(bugInfos):
    dax = list(bugCharacteristics)
    given = list(bugInfos)
    for i in range(0, 5):
        if dax[i] == 'x':
            continue
        elif dax[i] != given[i]:
            return False
    return True


bugCharacteristics = createBugCharacteristics(randint(1, 3))

expInfo = {'person': '', 'dateStr': data.getDateStr()}

dlg = gui.DlgFromDict(expInfo, title='Learning Experiment', fixed=['dateStr'])
if dlg.OK == False:
    core.quit()

fileName = 'data/'+expInfo['person'] + expInfo['dateStr']
dataFile = open(fileName + '.csv', 'w')
dataFile.write('corrAns,bugCharacteristics,DidVPCorr,Time\n')

win = visual.Window([800, 600], monitor='testMonitor', units='deg')
win.colorSpace = 'rgb255'
win.color = [255, 255, 255]

instr1 = visual.TextStim(win, pos=[0, +3], text='Hit any key to continue')
instr2 = visual.TextStim(win, pos=[0, -3], text='Explain Experiment here')
instr1.draw()
instr2.draw()
win.flip()
event.waitKeys()

responseTimer = core.Clock()
while True:
    event.clearEvents()
    bugName = ''
    for i in range(0, 5):
        nextElem = random.choice(['0', '1'])
        bugName += nextElem
    imagePath = 'BugImages/' + bugName + '.png'
    bug = visual.ImageStim(win, pos=[0, 0], image=imagePath, size=None, units='pix')
    bug.draw()
    win.flip()
    responseTimer.reset()
    timeForThisTrial = 0.0

    wasCorrect = None
    corrAns = isThisADax(bugName)
    while wasCorrect == None:
        allKeys = event.waitKeys()
        for thisKey in allKeys:
            if thisKey in ['q', 'escape']:
                dataFile.close()
                core.quit()
            elif thisKey in ['n', 'y']:
                timeForThisTrial = responseTimer.getTime()
                wasCorrect = (thisKey == 'y' and corrAns) or (thisKey == 'n' and (not corrAns))
        event.clearEvents()

    dataFile.write('%i,%s,%i,%.4f\n' % (corrAns, bugName, wasCorrect, timeForThisTrial))
    feedbackText = ''
    if wasCorrect:
        feedbackText = 'correct'
    else:
        feedbackText = 'wrong'
    feedback = visual.TextStim(win, pos=[0, -3], text='Your answer was ' + feedbackText)
    feedback.colorSpace = 'rgb255'
    feedback.color = [0, 0, 0]
    feedback.draw()
    win.flip()
    core.wait(1.5)