from VersionSpace import VersionSpace
from random import randint, shuffle, sample, choice
from psychopy import visual, core, event, gui, data, prefs
prefs.general['audioLib']=['pygame']
from psychopy import sound

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


def isThisADax(bugInfos):
    dax = list(bugCharacteristics)
    given = list(bugInfos)
    for i in range(0, 5):
        if dax[i] == 'x':
            continue
        elif dax[i] != given[i]:
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

def intermediateQuestion():
    questions = {'wings': ['Does Not Matter', 'Yes', 'No'],
                 'legs': ['Does Not Matter', 'Four', 'Six'],
                 'antenna': ['Does Not Matter', 'Straight', 'Curly'],
                 'dots': ['Does Not Matter', 'Small', 'Big'],
                 'eyes': ['Does Not Matter', 'White', 'Black']}
    guess = gui.DlgFromDict(questions, title='Guess what a Dax is', sort_keys=False)
    if guess.OK:
        for key in questions:
            dataFile.write(key + ': ' + questions[key]+', ')
        dataFile.write('\n')
        return checkIfCorrect(questions)
    return False

def checkIfCorrect(dict):
    answer = ''
    for key in dict:
        answer += translateWordsToChars(dict[key])
    if answer == bugCharacteristics:
        return True
    return False

def translateWordsToChars(word):
    zeroWords = ['No','Four','Straight','Small','White']
    oneWords = ['Yes','Six','Curly','Big','Black']
    if word in zeroWords:
        return '0'
    elif word in oneWords:
        return '1'
    elif word == 'Does Not Matter':
        return 'x'
    else:
        print('illegal word')

amountOfAttributes = randint(1, 5)
bugCharacteristics = createBugCharacteristics(amountOfAttributes)

expInfo = {'person': '', 'dateStr': data.getDateStr()}

dlg = gui.DlgFromDict(expInfo, title='Learning Experiment', fixed=['dateStr'])
if dlg.OK == False:
    core.quit()

fileName = 'data/'+expInfo['person'] + expInfo['dateStr']
dataFile = open(fileName + '.csv', 'w')
dataFile.write('DaxCharacteristics: ,'+bugCharacteristics+'\n')
dataFile.write('corrAns,bugCharacteristics,DidVPCorr,Time\n')

win = visual.Window(fullscr=True, monitor='testMonitor', units='pix')
win.colorSpace = 'rgb255'
win.color = [255, 255, 255]

instr1 = visual.TextStim(win, pos=[0, +10], text='In the following Experiments you will see Bugs with 5 different attributes.\n'
                                                  'These are: wings, legs, antenna, dots, eyes.\n'
                                                  'All of them are binary.\n'
                                                  'Below you can see 2 examples that show all possible attributes.\n'
                                                  'All other attributes does not matter.\n\n\n\n'
                                                  'Press any key to continue.')
instr1.draw()
exampleImage1 = visual.ImageStim(win, pos=[-5,-5],image='BugImages/00000.png',units='deg')
exampleImage1.draw()
exampleImage2 = visual.ImageStim(win, pos=[+5,-5],image='BugImages/11111.png',units='deg')
exampleImage2.draw()
win.flip()
event.waitKeys()

vs = VersionSpace()
solution = False

allBugs = createListOfBugs()
responseTimer = core.Clock()
correctRun = False
didAnswerCorrect = False
while not(correctRun and didAnswerCorrect):
    shuffle(allBugs)
    correctRun = True
    numCorrect = 0

    for index in range(0,32):
        event.clearEvents()
        bugName = allBugs[index]
        imagePath = 'BugImages/' + bugName + '.png'
        bug = visual.ImageStim(win, pos=[0, 0], image=imagePath, size=[288,212], units='pix')
        bug.draw()
        win.flip()
        responseTimer.reset()
        timeForThisTrial = 0.0

        wasCorrect = None
        corrAns = isThisADax(bugName)

        solution = vs.showNewBug(bugName,corrAns)
        if type(solution) is str:  # version space algorithm found the solution
            print(solution)

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
        feedbackText2 = ''
        if not corrAns:
            feedbackText2 = 'NOT '
        feedbackRect = visual.Rect(win, lineWidth=25.0, size=[1600,1200])
        if wasCorrect:
            numCorrect += 1
            correct = sound.Sound('sounds/correctAnswer.ogg')
            correct.play()
            feedbackRect.lineColor = 'green'
            feedbackText = 'correct'
        else:
            correctRun = False
            wrong = sound.Sound('sounds/wrongAnswer.ogg')
            wrong.play()
            feedbackRect.lineColor = 'red'
            feedbackText = 'wrong'
        feedback = visual.TextStim(win, pos=[0, -10], text='Your answer was ' + feedbackText+
                                                           '\n This was '+feedbackText2+' a Dax')
        feedback.colorSpace = 'rgb255'
        feedback.color = [0, 0, 0]
        feedback.draw()
        feedbackRect.draw()
        win.flip()
        core.wait(3)

    fb = visual.TextStim(win, pos=[0,0], text=str(numCorrect)+' of your last 32 answers were correct.\n\n'
                                                         'Press any key to continue.')
    fb.colorSpace = 'rgb255'
    fb.color = [0,0,0]
    fb.draw()
    win.flip()
    event.waitKeys()

    win.winHandle.set_fullscreen(False)
    win.winHandle.set_visible(False)
    didAnswerCorrect = intermediateQuestion()
    win.winHandle.set_fullscreen(True)
    win.winHandle.set_visible(True)
    win.flip()

dataFile.close()
core.quit()