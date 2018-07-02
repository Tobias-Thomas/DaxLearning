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
    questions = {'Flügel': ['Spielt keine Rolle', 'Ja', 'Nein'],
                 'Beine': ['Spielt keine Rolle', 'Vier', 'Sechs'],
                 'Antenne': ['Spielt keine Rolle', 'gerade', 'gekrümmt'],
                 'Punkte': ['Spielt keine Rolle', 'klein', 'dick'],
                 'Augen': ['Spielt keine Rolle', 'Weiß', 'Schwarz']}
    guess = gui.DlgFromDict(questions, title='Gib deine Hypothese ab', sort_keys=False)
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
    zeroWords = ['Nein','Vier','gerade','klein','Weiß']
    oneWords = ['Ja','Sechs','gekrümmt','dick','Schwarz']
    if word in zeroWords:
        return '0'
    elif word in oneWords:
        return '1'
    elif word == 'Spielt keine Rolle':
        return 'x'
    else:
        print('illegal word')

def getTestProcedure():
    possiblities = [[1,3,1,3,4,2,5],[1,3,3,4,2,5,1],[1,3,5,2,1,4,3],[1,3,2,1,5,3,4],[1,3,4,5,3,1,2]]
    return sample(possiblities,1)[0]

procedure = getTestProcedure()

expInfo = {'person': '', 'dateStr': data.getDateStr()}

dlg = gui.DlgFromDict(expInfo, title='Learning Experiment', fixed=['dateStr'])
if dlg.OK == False:
    core.quit()

fileName = 'data/'+expInfo['person'] + expInfo['dateStr']
dataFile = open(fileName + '.csv', 'w')
dataFile.write('procedure: '+';'.join(map(str,procedure))+'\n')
dataFile.write('corrAns,bugCharacteristics,DidVPCorr,Time\n')

win = visual.Window(fullscr=True, monitor='testMonitor', units='pix')
win.colorSpace = 'rgb255'
win.color = [255, 255, 255]
win.mouseVisible = False

instr1 = visual.TextStim(win, pos=[0, +15], text='In diesem Experiment werden Sie Käfer mit 5 verschiedenen Eigenschaften sehen\n'
                                                'Die verschiedenen eigenschaften sind: Flügel, Punkte, Beine, Antennen und Augen\n'
                                                'Alle Eigenschaften gibt es nur in 2 Varianten.\n'
                                                'Die unterschiedlichen Varianten der Variablen kannst du unten beispielhaft sehen.\n'
                                                'Es gibt alle Kombinationen der Eigenschaften.'
                                                'Ihre Aufgabe ist es herauszufinden welche Eigenschaften einen Dax ausmachen'
                                                'Ein Dax kann beliebig viele Eigenschaften haben.'
                                                'Dieses Experiment beschäftigt sich mit Lösungsstrategien.'
                                                'Falls Sie noch Fragen haben stellen sie diese bitte jetzt.\n\n\n\n'
                                                'Zum Starten drücke eine beliebige Taste.')
instr1.draw()
exampleImage1 = visual.ImageStim(win, pos=[-5,-8],image='BugImages/00000.png',units='deg')
exampleImage1.draw()
exampleImage2 = visual.ImageStim(win, pos=[+5,-8],image='BugImages/11111.png',units='deg')
exampleImage2.draw()
win.flip()
event.waitKeys()

vs = VersionSpace()
solution = False

allBugs = createListOfBugs()

for amountOfAttributes in procedure:
    bugCharacteristics = createBugCharacteristics(amountOfAttributes)
    dataFile.write('DaxCharacteristics: ,' + bugCharacteristics + '\n')
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

            while wasCorrect == None:
                allKeys = event.waitKeys()
                for thisKey in allKeys:
                    if thisKey in ['q', 'escape']:
                        dataFile.close()
                        core.quit()
                    elif thisKey in ['n', 'y']:
                        wasCorrect = (thisKey == 'y' and corrAns) or (thisKey == 'n' and (not corrAns))
                event.clearEvents()

            dataFile.write('%i,%s,%i,' % (corrAns, bugName, wasCorrect))
            feedbackText = ''
            feedbackText2 = ''
            if not corrAns:
                feedbackText2 = 'KEIN'
            else:
                feedbackText2 = 'EIN'
            feedbackRect = visual.Rect(win, lineWidth=25.0, size=[1600,1200])
            if wasCorrect:
                numCorrect += 1
                correct = sound.Sound('sounds/correctAnswer.ogg')
                correct.play()
                feedbackRect.lineColor = 'green'
                feedbackText = 'richtig'
            else:
                correctRun = False
                wrong = sound.Sound('sounds/wrongAnswer.ogg')
                wrong.play()
                feedbackRect.lineColor = 'red'
                feedbackText = 'falsch'
            feedback = visual.TextStim(win, pos=[0, -100], text='Deine Antwort war ' + feedbackText+
                                                               '\nDas war '+feedbackText2+' Dax')
            feedback.colorSpace = 'rgb255'
            feedback.color = [0, 0, 0]
            feedback.draw()
            feedbackRect.draw()
            bug.pos = [0,100]
            bug.draw()
            win.flip()
            event.clearEvents()
            core.wait(0.5)
            feedbackTimer = core.CountdownTimer(2.5)
            while feedbackTimer.getTime() > 0:
                keysPressed = event.getKeys()
                if 'space' in keysPressed:
                    break
                else:
                    continue
            timeForThisTrial = responseTimer.getTime()
            dataFile.write('%.4f\n'%(timeForThisTrial))



        fb = visual.TextStim(win, pos=[0,0], text=str(numCorrect)+' deiner letzten 32 Antworten waren korrekt\n\n'
                                                             'Beliebige Taste drücken zum Fortsetzen.')
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

    intermediateFeedback = visual.TextStim(win, pos=[0,0], text='Super! Du hast dieses Rätsel gelöst.\n'
                                                                'Wenn du dich bereit für das nächste Rätsel fühlst drücke eine beliebige Tasten zum Fortfahren')
    intermediateFeedback.colorSpace = 'rgb255'
    intermediateFeedback.color = [0,0,0]
    intermediateFeedback.draw()
    win.flip()
    event.waitKeys()

dataFile.close()
core.quit()