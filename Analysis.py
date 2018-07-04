import matplotlib.pyplot as plt
from tkinter.filedialog import askopenfilename
import csv


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
    for i, c in enumerate(personID):
        if c.isdigit():
            break
    personID = personID[:i]
with open(filename, 'r') as csvfile:
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
            successes = []
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
    successes = successes[:1]

    for j in range(len(times)):
        timeTrial = times[j]
        plt.plot(range(1, len(timeTrial)+1), timeTrial)
        plt.xlabel('# of shown bug')
        plt.ylabel('time')
        timePlotName = personID+procedure[j].strip()+'time'
        plt.savefig('plots/'+timePlotName+'.pdf', format='pdf')

        plt.gcf().clear()

        successTrial = successes[j]
        plt.plot(range(1, len(successTrial) + 1), successTrial)
        plt.xlabel('# of shown bug')
        plt.ylabel('success')
        successPlotName = personID + procedure[j].strip() + 'success'
        plt.savefig('plots/' + successPlotName + '.pdf', format='pdf')

        j += 1
