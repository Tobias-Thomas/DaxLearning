import matplotlib.pyplot as plt
from tkinter.filedialog import askopenfilename
import csv
import codecs

def isFloat(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


filename = askopenfilename()
personID = ''
if isinstance(filename, str):
    personID = filename.split('/')
    personID = personID[len(personID)-1]
    n = 0
    for i, c in enumerate(personID):
        if c.isdigit():
            n += 1
            if n == 3:
                break
    personID = personID[:i]
with codecs.open(filename, 'r',encoding='utf-8',errors='ignore') as csvfile:
    reader = csv.reader(csvfile)
    procedure = []
    successes = []
    successesForOneTrial = []
    times = []
    timesForOneTrial = []
    for row in reader:
        if len(row) == 1:
            procedure = row[0]
            if isinstance(procedure, str):
                procedureParts = procedure.split(':')
                procedureParts = procedureParts[1]
                procedure = procedureParts.split(';')
        if len(row) == 2:
            successes.append(successesForOneTrial)
            successesForOneTrial = []
            times.append(timesForOneTrial)
            timesForOneTrial = []
        elif len(row) == 4:
            if isFloat(row[3]):
                timesForOneTrial.append(float(row[3]))
            if row[2].isdigit():
                successesForOneTrial.append(int(row[2]))
    times.append(timesForOneTrial)
    times = times[1:]
    successes.append(successesForOneTrial)
    successes = successes[1:]

    for j in range(len(times)):
        timeTrial = times[j]
        plt.plot(range(1, len(timeTrial)+1), timeTrial)
        plt.xlabel('# of shown bug')
        plt.ylabel('time')
        timePlotName = personID + str(j+1) + '-' + procedure[j].strip() +'time'
        plt.savefig('plots/'+timePlotName+'.pdf', format='pdf')

        plt.gcf().clear()

        successTrial = successes[j]
        plt.plot(range(1, len(successTrial) + 1), successTrial)
        plt.xlabel('# of shown bug')
        plt.ylabel('success')
        successPlotName = personID + str(j+1) + '-' + procedure[j].strip() + 'success'
        plt.savefig('plots/' + successPlotName + '.pdf', format='pdf')

        plt.gcf().clear()
        j += 1
