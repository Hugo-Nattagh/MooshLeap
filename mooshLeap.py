import tkinter as tk
import tkinter.ttk as ttk
from tkinter import font
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.patches as mpatches
import seaborn as sns
import numpy as np
import pandas as pd
import csv
from glob import glob
import os
import time
matplotlib.use('TkAgg')
pd.set_option('display.max_colwidth', 1000)

now = datetime.now()

# À modifier lors de l'implémentation sur cabine Q: Chemin d'accès line 32
# À modifier lorsque les cabines seront reliées: checkbox line 1425, 1428, 1431 -> effacer "state='disabled'"   + Modif chemin d'accès line 33, 34, 35

window = tk.Tk()
window.title('Moosh Leap')

# Selection Functions____________________________________________________________________________


ogpath = os.getcwd()

pathD = "SampleD"
pathG = "SampleG"
pathK = "SampleK"
pathQ = "SampleQ"


def whichCabins():
    cab1value = cab1var.get()
    cab2value = cab2var.get()
    cab3value = cab3var.get()
    cab4value = cab4var.get()
    cabTot = cab1value + cab2value + cab3value + cab4value
    if cabTot > 0:
        AllFiles = []
        cabList = []
        if cab1value == 1:
            filesD = selectFiles(pathD)
            AllFiles.append(filesD)
            cabList += 'D'
        if cab2value == 1:
            filesG = selectFiles(pathG)
            AllFiles.append(filesG)
            cabList += 'G'
        if cab3value == 1:
            filesK = selectFiles(pathK)
            AllFiles.append(filesK)
            cabList += 'K'
        if cab4value == 1:
            filesQ = selectFiles(pathQ)
            AllFiles.append(filesQ)
            cabList += 'Q'
    return AllFiles, cabList


def selectFiles(path):
    os.chdir(ogpath)
    os.chdir(path)
    spBoxVar1 = int(spBoxPass1.get())
    spBoxVar2 = int(spBoxPass2.get())
    spBoxVar3 = int(spBoxPass3.get())
    radButtVar = int(rbvar.get())
    nbDay1 = int(spBoxDay1.get())
    nbDay2 = int(spBoxDay2.get())
    nbMonth1 = int(spBoxMonth1.get())
    nbMonth2 = int(spBoxMonth2.get())
    nbYear1 = int(spBoxYear1.get())
    nbYear2 = int(spBoxYear2.get())
    fromDateTemp = time.strptime(str(nbDay1) + " " + str(nbMonth1) + " " + str(nbYear1), "%d %m %Y")
    toDateTemp = time.strptime(str(nbDay2) + " " + str(nbMonth2) + " " + str(nbYear2), "%d %m %Y")
    fromDate = time.mktime(fromDateTemp)
    toDate = time.mktime(toDateTemp)
    if fromDate > toDate:
        Error('Date Error: A valid date entry is needed')

    if radButtVar == 1:
        files = [fn for fn in glob('*.csv')
                 if not os.path.basename(fn).endswith('errors.csv')
                 and not os.path.basename(fn).endswith('IQ.csv')
                 and not os.path.basename(fn).endswith('Data.csv')
                 and os.path.getmtime(fn) > fromDate
                 and os.path.getmtime(fn) < toDate]
    elif radButtVar == 2:
        if spBoxVar1 == 1:
            files = [fn for fn in glob('*.csv')
                     if not os.path.basename(fn).endswith('errors.csv')
                     and not os.path.basename(fn).endswith('IQ.csv')
                     and not os.path.basename(fn).endswith('Data.csv')
                     and not '-' in fn
                     and os.path.getmtime(fn) > fromDate
                     and os.path.getmtime(fn) < toDate]
        else:
            files = [fn for fn in glob('*.csv')
                     if os.path.basename(fn).endswith('-' + str(spBoxVar1 - 1) + '.csv')
                     and os.path.getmtime(fn) > fromDate
                     and os.path.getmtime(fn) < toDate]
    elif radButtVar == 3:
        files = []
        if spBoxVar2>spBoxVar3:
            Error('Runs Error: A valid run entry is needed')
        if spBoxVar2 == 1:
            files = [fn for fn in glob('*.csv')
                     if not os.path.basename(fn).endswith('errors.csv')
                     and not os.path.basename(fn).endswith('IQ.csv')
                     and not os.path.basename(fn).endswith('Data.csv')
                     and not '-' in fn
                     and os.path.getmtime(fn) > fromDate
                     and os.path.getmtime(fn) < toDate]
            spBoxVar2 += 1
        while spBoxVar2 <= spBoxVar3:
            files = files + [fn for fn in glob('*.csv')
                             if os.path.basename(fn).endswith('-' + str(spBoxVar2 - 1) + '.csv')
                             and os.path.getmtime(fn) > fromDate
                             and os.path.getmtime(fn) < toDate]
            spBoxVar2 += 1
    return files

# Graph Functions____________________________________________________________________________

# PASS/ERRORS FUNCTION


def passErrors(liste, cabine_name):
    os.chdir(ogpath)
    os.chdir('Sample' + cabine_name)
    succesVar = 0
    fail01Var = 0
    fail02Var = 0
    fail03Var = 0
    fail04Var = 0
    for file in liste:
        with open(file, "r") as f:
            reader = csv.reader(f)
            i = next(reader)
            j = next(reader)
            k = next(reader)
            l = next(reader)
        if cabine_name == 'D':
            dft = pd.read_csv(file, skiprows=3, usecols=l[1:], encoding='utf8', engine='python')
        elif cabine_name == 'G':
            dft = pd.read_csv(file, skiprows=3, usecols=l[1:], encoding='utf8', engine='c')
        elif cabine_name == 'K':
            dft = pd.read_csv(file, skiprows=3, usecols=l[1:], encoding='ISO-8859-1', engine='c')
        elif cabine_name == 'Q':
            dft = pd.read_csv(file, skiprows=3, usecols=l[1:], encoding='utf8', engine='python')
        try:
            if 'Test Completed.  Result:  PASS' in dft['Protocol Name'].tail(1).to_string():
                succesVar += 1
            elif 'Test Completed.  Result:  FAIL (Test failed due to total spits being greater than the spits allowed in the protocol.)' in dft['Protocol Name'].tail(1).to_string():
                fail01Var += 1
            elif 'Test Stopped!  Generator Error!  No more resumes allowed.' in dft['Protocol Name'].tail(1).to_string():
                fail02Var += 1
            elif 'Test Stopped!  Generator Error!  Resumes not allowed.' in dft['Protocol Name'].tail(1).to_string():
                fail03Var += 1
            elif 'Test Stopped!  Too many spits!  No more reruns allowed.' in dft['Protocol Name'].tail(1).to_string():
                fail04Var += 1
        except Exception:
            pass
    tots = len(liste)
    if tots > 0:
        percentPass = round((succesVar / tots) * 100, 1)
        percentFail01 = round((fail01Var / tots) * 100, 1)
        percentFail02 = round((fail02Var / tots) * 100, 1)
        percentFail03 = round((fail03Var / tots) * 100, 1)
        percentFail04 = round((fail04Var / tots) * 100, 1)
        percentFailRest = round(100 - (percentPass + percentFail01 + percentFail02 + percentFail03 + percentFail04), 1)

        percentList = [percentPass, percentFail01, percentFail02, percentFail03, percentFail04, percentFailRest]
        bars = ['PASS', 'FAIL', 'GenErr1', 'GenErr2', 'TMS', 'Misc']

        fig = plt.figure()
        sns.set(style="darkgrid")
        if cabine_name == 'D':
            ax = sns.barplot(x=bars, y=percentList, color='#004d99')
        elif cabine_name == 'G':
            ax = sns.barplot(x=bars, y=percentList, color='#4747d1')
        elif cabine_name == 'K':
            ax = sns.barplot(x=bars, y=percentList, color='#4d1919')
        elif cabine_name == 'Q':
            ax = sns.barplot(x=bars, y=percentList, color='#194d33')
        y_pos = np.arange(len(bars))
        plt.xticks(y_pos, bars)
        plt.ylabel('%')
        plt.suptitle("Results Cabin " + cabine_name)

        typicalString = "PASS: 'Test Completed.  Result:  PASS'\n-> " + str(percentPass) + " %\n\nFAIL: 'Test Completed.  Result:  FAIL (Test failed due to total spits being greater than the spits allowed in the protocol.)'\n-> " + str(percentFail01) + " %\n\n"
        typicalString += "GenErr1: 'Test Stopped!  Generator Error!  No more resumes allowed.'\n-> " + str(percentFail02) + " %\n\nGenErr2: 'Test Stopped!  Generator Error!  Resumes not allowed.'\n-> " + str(percentFail03) + " %\n\n"
        typicalString += "TMS: 'Test Stopped!  Too many spits!  No more reruns allowed.'\n-> " + str(percentFail04) + " %\n\nMisc: Other Errors\n-> " + str(percentFailRest) + " %\n"
    elif tots == 0:
        fig = plt.figure()
        sns.set(style="darkgrid")

        typicalString = 'No file found'

    return fig, typicalString


# REUSSITE PROGRESSION

# More Steps:

# def tauxProgress(liste, cabine_name):
#     os.chdir(ogpath)
#     os.chdir('Sample' + cabine_name)
#     totVar = 0
#     passVar = 0
#     failVar = 0

#     prescriptions = {'Calibration 1' : 0, 'Calibration 2' : 0, 'Calibration 3' : 0, 'Calibration 4' : 0, 'Calibration 5' : 0, 'Calibration 6' : 0, 'WarmUp' : 0, 'NG HVIS 110' : 0, 'NG HVIS 115' : 0, 'NG HVIS 120' : 0, 'NG HVIS 125' : 0, 'NG HVIS 130' : 0, 'NG HVIS 135' : 0, 'NG HVIS 140' : 0, 'SHVIS 2 80' : 0, 'SHVIS 2 85' : 0, 'SHVIS 2 90' : 0, 'SHVIS 2 95' : 0, 'SHVIS 2 100' : 0, 'SHVIS 2 105' : 0, 'SHVIS 2 110' : 0, 'SHVIS 2 115' : 0, 'SHVIS 2 120' : 0, 'SHVIS 2 125' : 0, 'SHVIS 2 130' : 0, 'SHVIS 2 135' : 0, 'SHVIS 2 140' : 0, 'FT step 1' : 0, 'FT step 2' : 0, 'FT step 3' : 0, 'FT step 4' : 0, 'FT step 5' : 0, 'FT step 6' : 0, 'FT step 7' : 0, 'FT step 8' : 0, 'FT step 9' : 0, 'FT step 10' : 0, 'FT step 11' : 0, 'FT step 12' : 0, 'FT step 13' : 0, 'FT step 14' : 0, 'FT step 15' : 0, 'FT step 16' : 0, 'FT step 17' : 0, 'FT step 18' : 0, 'FT step 19' : 0, 'FT step 20' : 0}
#     StepList = list(prescriptions.keys())

#     for file in liste:
#         try:
#             with open(file, "r") as f:
#                 reader = csv.reader(f)
#                 i = next(reader)
#                 j = next(reader)
#                 k = next(reader)
#                 l = next(reader)
#             if cabine_name == 'D':
#                 dft = pd.read_csv(file, skiprows=3, usecols=l[1:], encoding='utf8', engine='python')
#             elif cabine_name == 'G':
#                 dft = pd.read_csv(file, skiprows=3, usecols=l[1:], encoding='utf8', engine='c')
#             elif cabine_name == 'K':
#                 dft = pd.read_csv(file, skiprows=3, usecols=l[1:], encoding='ISO-8859-1', engine='c')
#             elif cabine_name == 'Q':
#                 dft = pd.read_csv(file, skiprows=3, usecols=l[0:], encoding='utf8', engine='c')
#             for step in reversed(StepList):
#                 if step in dft['Prescription Name'].to_string():
#                     lastPres = step
#                     break
#             for value in prescriptions:
#                 prescriptions[value] += 1
#                 if value == lastPres:
#                     break
#             if lastPres == 'FT step 20':
#                 if 'Test Completed.  Result:  PASS' in dft['Protocol Name'].to_string():
#                     passVar += 1
#                 else:
#                     failVar += 1
#             totVar += 1
#         except Exception:
#             pass

#     typicalString = ''
#     if totVar > 0:
#         pourcentagePrev = 100
#         plotList = []
#         typicalString += "Progression par étape pour la cabine " + cabine_name + "\n\n        __________\n\n"
#         typicalString += "Commence à l'étape Calibration 1: 100%\n\n"
#         for key in prescriptions:
#             if key == 'Calibration 1':
#                 pass
#             percent = round((prescriptions[key] / totVar) * 100, 1)
#             plotList.append(percent)
#             typicalString += "Restant à l'étape " + key + ": %.2f"  % percent + " %"
#             typicalString += "          (N'ont pas passé l'étape précédente: %.2f" % (pourcentagePrev-percent) + " %)\n\n"
#             pourcentagePrev = percent
#             percentPassTot = round((passVar / totVar) * 100, 1)
#         typicalString += "Du début à la dernière étape, le taux de réussite est de %.1f" % (percentPassTot) + " %"
#         typicalString += "\nÀ la dernière étape, le taux de réussite est de %.1f" % (round((passVar / (passVar + failVar)) * 100, 1)) + " %"

#     fig = plt.figure(figsize=(5, 8))
#     sns.set(style="darkgrid")
#     if totVar > 0:
#         plt.plot(StepList, plotList, color='#004d00')
#     plt.xlabel('Étapes')
#     plt.ylabel('%')
#     plt.xticks(rotation='vertical')
#     plt.suptitle("Progression pour la cabine " + cabine_name)
#     plt.subplots_adjust(bottom=0.20)

#     return fig, typicalString

# Less Steps

def tauxProgress(liste, cabine_name):
    os.chdir(ogpath)
    os.chdir('Sample' + cabine_name)
    totVar = 0
    passVar = 0
    failVar = 0

    prescriptions = {'Calibration': 0, 'Tube Warm Up': 0, 'NG HVIS #1': 0, 'NG HVIS #2': 0, 'NG HVIS #3': 0, 'NG HVIS #4': 0, 'SHVIS 2 A': 0, 'SHVIS 2 B': 0, 'SHVIS 2 C': 0, 'SHVIS 2 D': 0, 'SHVIS 2 E': 0, 'SHVIS 2 F': 0}
    prescriptionsFT = {'FT step 1': 0, 'FT step 2': 0, 'FT step 3': 0, 'FT step 4': 0, 'FT step 5': 0, 'FT step 6': 0, 'FT step 7': 0, 'FT step 8': 0, 'FT step 9': 0, 'FT step 10': 0, 'FT step 11': 0, 'FT step 12': 0, 'FT step 13': 0, 'FT step 14': 0, 'FT step 15': 0, 'FT step 16': 0, 'FT step 17': 0, 'FT step 18': 0, 'FT step 19': 0, 'FT step 20': 0}
    StepList = list(prescriptions.keys())
    StepListFT = list(prescriptionsFT.keys())

    for file in liste:
        try:
            with open(file, "r") as f:
                reader = csv.reader(f)
                i = next(reader)
                j = next(reader)
                k = next(reader)
                l = next(reader)
            if cabine_name == 'D':
                dft = pd.read_csv(file, skiprows=3, usecols=l[1:], encoding='utf8', engine='python')
            elif cabine_name == 'G':
                dft = pd.read_csv(file, skiprows=3, usecols=l[1:], encoding='utf8', engine='c')
            elif cabine_name == 'K':
                dft = pd.read_csv(file, skiprows=3, usecols=l[1:], encoding='ISO-8859-1', engine='c')
            elif cabine_name == 'Q':
                dft = pd.read_csv(file, skiprows=3, usecols=l[0:], encoding='utf8', engine='c')
            lastPres = 'empty'
            FTorNot = 0
            for step in reversed(StepListFT):
                if step in dft['Prescription Name'].to_string():
                    lastPres = step
                    break
            if lastPres == 'empty':
                for sstep in reversed(StepList):
                    if sstep in dft['Protocol Name'].to_string():
                        lastPres = sstep
                        FTorNot = 1
                        break
            for value in prescriptions:
                prescriptions[value] += 1
                if value == lastPres:
                    break
            if FTorNot == 0:
                for value in prescriptionsFT:
                    prescriptionsFT[value] += 1
                    if value == lastPres:
                        break
            if lastPres == 'FT step 20':
                if 'Test Completed.  Result:  PASS' in dft['Protocol Name'].to_string():
                    passVar += 1
                else:
                    failVar += 1
            totVar += 1
        except Exception:
            pass

    allPrescriptions = dict(prescriptions, **prescriptionsFT)
    APList = list(allPrescriptions.keys())
    typicalString = ''
    if totVar > 0:
        pourcentagePrev = 100
        plotList = []
        typicalString += "Progress per step for cabin " + cabine_name + "\n\n        __________\n\n"
        typicalString += "Starting at the 'Calibration' step: 100%\n\n"
        for key in allPrescriptions:
            if key == 'Calibration':
                pass
            percent = round((allPrescriptions[key] / totVar) * 100, 1)
            plotList.append(percent)
            typicalString += "Remaining at the step '" + key + "': %.2f" % percent + " %"
            typicalString += "          (Did not pass the previous step: %.2f" % (pourcentagePrev - percent) + " %)\n\n"
            pourcentagePrev = percent
            percentPassTot = round((passVar / totVar) * 100, 1)
        typicalString += "From the first to the last step, the succes rate is %.1f" % (percentPassTot) + " %"
        if (passVar + failVar) != 0:
            typicalString += "\nAt the last step, the succes rate is %.1f" % (round((passVar / (passVar + failVar)) * 100, 1)) + " %"

    fig = plt.figure(figsize=(5, 8))
    sns.set(style="darkgrid")
    if totVar > 0:
        plt.plot(APList, plotList, color='#004d00')
    plt.xlabel('Steps')
    plt.ylabel('%')
    plt.xticks(rotation='vertical')
    plt.suptitle("Progress - Cabin " + cabine_name)
    plt.subplots_adjust(bottom=0.20)

    if totVar == 0:
        fig = plt.figure()
        sns.set(style="darkgrid")

        typicalString = 'No file found'

        plotList = []

    return fig, typicalString, plotList


def spitFreq(liste, cabine_name):
    os.chdir(ogpath)
    os.chdir('Sample' + cabine_name)
    FTstep1TotSpit = 0
    FTstep1Pos = 0
    FTstep1Tot = 0
    FTstep2TotSpit = 0
    FTstep2Pos = 0
    FTstep2Tot = 0
    FTstep3TotSpit = 0
    FTstep3Pos = 0
    FTstep3Tot = 0
    FTstep4TotSpit = 0
    FTstep4Pos = 0
    FTstep4Tot = 0
    FTstep5TotSpit = 0
    FTstep5Pos = 0
    FTstep5Tot = 0
    FTstep6TotSpit = 0
    FTstep6Pos = 0
    FTstep6Tot = 0
    FTstep7TotSpit = 0
    FTstep7Pos = 0
    FTstep7Tot = 0
    FTstep8TotSpit = 0
    FTstep8Pos = 0
    FTstep8Tot = 0
    FTstep9TotSpit = 0
    FTstep9Pos = 0
    FTstep9Tot = 0
    FTstep10TotSpit = 0
    FTstep10Pos = 0
    FTstep10Tot = 0
    FTstep11TotSpit = 0
    FTstep11Pos = 0
    FTstep11Tot = 0
    FTstep12TotSpit = 0
    FTstep12Pos = 0
    FTstep12Tot = 0
    FTstep13TotSpit = 0
    FTstep13Pos = 0
    FTstep13Tot = 0
    FTstep14TotSpit = 0
    FTstep14Pos = 0
    FTstep14Tot = 0
    FTstep15TotSpit = 0
    FTstep15Pos = 0
    FTstep15Tot = 0
    FTstep16TotSpit = 0
    FTstep16Pos = 0
    FTstep16Tot = 0
    FTstep17TotSpit = 0
    FTstep17Pos = 0
    FTstep17Tot = 0
    FTstep18TotSpit = 0
    FTstep18Pos = 0
    FTstep18Tot = 0
    FTstep19TotSpit = 0
    FTstep19Pos = 0
    FTstep19Tot = 0
    FTstep20TotSpit = 0
    FTstep20Pos = 0
    FTstep20Tot = 0

    # prescriptions = {'Calibration 1' : 0, 'Calibration 2' : 0, 'Calibration 3' : 0, 'Calibration 4' : 0, 'Calibration 5' : 0, 'Calibration 6' : 0, 'WarmUp' : 0, 'NG HVIS 110' : 0, 'NG HVIS 115' : 0, 'NG HVIS 120' : 0, 'NG HVIS 125' : 0, 'NG HVIS 130' : 0, 'NG HVIS 135' : 0, 'NG HVIS 140' : 0, 'SHVIS 2 80' : 0, 'SHVIS 2 85' : 0, 'SHVIS 2 90' : 0, 'SHVIS 2 95' : 0, 'SHVIS 2 100' : 0, 'SHVIS 2 105' : 0, 'SHVIS 2 110' : 0, 'SHVIS 2 115' : 0, 'SHVIS 2 120' : 0, 'SHVIS 2 125' : 0, 'SHVIS 2 130' : 0, 'SHVIS 2 135' : 0, 'SHVIS 2 140' : 0, 'FT step 1' : 0, 'FT step 2' : 0, 'FT step 3' : 0, 'FT step 4' : 0, 'FT step 5' : 0, 'FT step 6' : 0, 'FT step 7' : 0, 'FT step 8' : 0, 'FT step 9' : 0, 'FT step 10' : 0, 'FT step 11' : 0, 'FT step 12' : 0, 'FT step 13' : 0, 'FT step 14' : 0, 'FT step 15' : 0, 'FT step 16' : 0, 'FT step 17' : 0, 'FT step 18' : 0, 'FT step 19' : 0, 'FT step 20' : 0}
    # StepList = list(prescriptions.keys())

    for file in liste:
        try:
            with open(file, "r") as f:
                reader = csv.reader(f)
                i = next(reader)
                j = next(reader)
                k = next(reader)
                l = next(reader)
            if cabine_name == 'D':
                dft = pd.read_csv(file, skiprows=3, usecols=l[1:], encoding='utf8', engine='python')
            elif cabine_name == 'G':
                dft = pd.read_csv(file, skiprows=3, usecols=l[1:], encoding='utf8', engine='c')
            elif cabine_name == 'K':
                dft = pd.read_csv(file, skiprows=3, usecols=l[1:], encoding='ISO-8859-1', engine='c')
            elif cabine_name == 'Q':
                dft = pd.read_csv(file, skiprows=3, usecols=l[0:], encoding='utf8', engine='c')
            for row in dft['Prescription Name']:
                if row == "FT step 1":
                    if int(dft['Total Spits'].loc[dft['Prescription Name'] == "FT step 1"]) > 0:
                        FTstep1Pos += 1
                    FTstep1TotSpit += int(dft['Total Spits'].loc[dft['Prescription Name'] == "FT step 1"])
                    FTstep1Tot += 1
                elif row == "FT step 2":
                    if int(dft['Total Spits'].loc[dft['Prescription Name'] == "FT step 2"]) > 0:
                        FTstep2Pos += 1
                    FTstep2TotSpit += int(dft['Total Spits'].loc[dft['Prescription Name'] == "FT step 2"])
                    FTstep2Tot += 1
                elif row == "FT step 3":
                    if int(dft['Total Spits'].loc[dft['Prescription Name'] == "FT step 3"]) > 0:
                        FTstep3Pos += 1
                    FTstep3TotSpit += int(dft['Total Spits'].loc[dft['Prescription Name'] == "FT step 3"])
                    FTstep3Tot += 1
                elif row == "FT step 4":
                    if int(dft['Total Spits'].loc[dft['Prescription Name'] == "FT step 4"]) > 0:
                        FTstep4Pos += 1
                    FTstep4TotSpit += int(dft['Total Spits'].loc[dft['Prescription Name'] == "FT step 4"])
                    FTstep4Tot += 1
                elif row == "FT step 5":
                    if int(dft['Total Spits'].loc[dft['Prescription Name'] == "FT step 5"]) > 0:
                        FTstep5Pos += 1
                    FTstep5TotSpit += int(dft['Total Spits'].loc[dft['Prescription Name'] == "FT step 5"])
                    FTstep5Tot += 1
                elif row == "FT step 6":
                    if int(dft['Total Spits'].loc[dft['Prescription Name'] == "FT step 6"]) > 0:
                        FTstep6Pos += 1
                    FTstep6TotSpit += int(dft['Total Spits'].loc[dft['Prescription Name'] == "FT step 6"])
                    FTstep6Tot += 1
                elif row == "FT step 7":
                    if int(dft['Total Spits'].loc[dft['Prescription Name'] == "FT step 7"]) > 0:
                        FTstep7Pos += 1
                    FTstep7TotSpit += int(dft['Total Spits'].loc[dft['Prescription Name'] == "FT step 7"])
                    FTstep7Tot += 1
                elif row == "FT step 8":
                    if int(dft['Total Spits'].loc[dft['Prescription Name'] == "FT step 8"]) > 0:
                        FTstep8Pos += 1
                    FTstep8TotSpit += int(dft['Total Spits'].loc[dft['Prescription Name'] == "FT step 8"])
                    FTstep8Tot += 1
                elif row == "FT step 9":
                    if int(dft['Total Spits'].loc[dft['Prescription Name'] == "FT step 9"]) > 0:
                        FTstep9Pos += 1
                    FTstep9TotSpit += int(dft['Total Spits'].loc[dft['Prescription Name'] == "FT step 9"])
                    FTstep9Tot += 1
                elif row == "FT step 10":
                    if int(dft['Total Spits'].loc[dft['Prescription Name'] == "FT step 10"]) > 0:
                        FTstep10Pos += 1
                    FTstep10TotSpit += int(dft['Total Spits'].loc[dft['Prescription Name'] == "FT step 10"])
                    FTstep10Tot += 1
                elif row == "FT step 11":
                    if int(dft['Total Spits'].loc[dft['Prescription Name'] == "FT step 11"]) > 0:
                        FTstep11Pos += 1
                    FTstep11TotSpit += int(dft['Total Spits'].loc[dft['Prescription Name'] == "FT step 11"])
                    FTstep11Tot += 1
                elif row == "FT step 12":
                    if int(dft['Total Spits'].loc[dft['Prescription Name'] == "FT step 12"]) > 0:
                        FTstep12Pos += 1
                    FTstep12TotSpit += int(dft['Total Spits'].loc[dft['Prescription Name'] == "FT step 12"])
                    FTstep12Tot += 1
                elif row == "FT step 13":
                    if int(dft['Total Spits'].loc[dft['Prescription Name'] == "FT step 13"]) > 0:
                        FTstep13Pos += 1
                    FTstep13TotSpit += int(dft['Total Spits'].loc[dft['Prescription Name'] == "FT step 13"])
                    FTstep13Tot += 1
                elif row == "FT step 14":
                    if int(dft['Total Spits'].loc[dft['Prescription Name'] == "FT step 14"]) > 0:
                        FTstep14Pos += 1
                    FTstep14TotSpit += int(dft['Total Spits'].loc[dft['Prescription Name'] == "FT step 14"])
                    FTstep14Tot += 1
                elif row == "FT step 15":
                    if int(dft['Total Spits'].loc[dft['Prescription Name'] == "FT step 15"]) > 0:
                        FTstep15Pos += 1
                    FTstep15TotSpit += int(dft['Total Spits'].loc[dft['Prescription Name'] == "FT step 15"])
                    FTstep15Tot += 1
                elif row == "FT step 16":
                    if int(dft['Total Spits'].loc[dft['Prescription Name'] == "FT step 16"]) > 0:
                        FTstep16Pos += 1
                    FTstep16TotSpit += int(dft['Total Spits'].loc[dft['Prescription Name'] == "FT step 16"])
                    FTstep16Tot += 1
                elif row == "FT step 17":
                    if int(dft['Total Spits'].loc[dft['Prescription Name'] == "FT step 17"]) > 0:
                        FTstep17Pos += 1
                    FTstep17TotSpit += int(dft['Total Spits'].loc[dft['Prescription Name'] == "FT step 17"])
                    FTstep17Tot += 1
                elif row == "FT step 18":
                    if int(dft['Total Spits'].loc[dft['Prescription Name'] == "FT step 18"]) > 0:
                        FTstep18Pos += 1
                    FTstep18TotSpit += int(dft['Total Spits'].loc[dft['Prescription Name'] == "FT step 18"])
                    FTstep18Tot += 1
                elif row == "FT step 19":
                    if int(dft['Total Spits'].loc[dft['Prescription Name'] == "FT step 19"]) > 0:
                        FTstep19Pos += 1
                    FTstep19TotSpit += int(dft['Total Spits'].loc[dft['Prescription Name'] == "FT step 19"])
                    FTstep19Tot += 1
                elif row == "FT step 20":
                    if int(dft['Total Spits'].loc[dft['Prescription Name'] == "FT step 20"]) > 0:
                        FTstep20Pos += 1
                    FTstep20TotSpit += int(dft['Total Spits'].loc[dft['Prescription Name'] == "FT step 20"])
                    FTstep20Tot += 1
        except Exception:
            pass

    freqList = []
    if FTstep1Tot != 0:
        FTstep1Moy = round((FTstep1TotSpit / FTstep1Tot), 1)
        FTstep1Freq = round((FTstep1Pos / FTstep1Tot) * 100, 1)
        freqList.append(FTstep1Freq)
    else:
        FTstep1Moy = 1
        FTstep1Freq = 1
        freqList.append(FTstep1Freq)
    if FTstep2Tot != 0:
        FTstep2Moy = round((FTstep2TotSpit / FTstep2Tot), 1)
        FTstep2Freq = round((FTstep2Pos / FTstep2Tot) * 100, 1)
        freqList.append(FTstep2Freq)
    else:
        FTstep2Moy = 1
        FTstep2Freq = 1
        freqList.append(FTstep2Freq)
    if FTstep3Tot != 0:
        FTstep3Moy = round((FTstep3TotSpit / FTstep3Tot), 1)
        FTstep3Freq = round((FTstep3Pos / FTstep3Tot) * 100, 1)
        freqList.append(FTstep3Freq)
    else:
        FTstep3Moy = 1
        FTstep3Freq = 1
        freqList.append(FTstep3Freq)
    if FTstep4Tot != 0:
        FTstep4Moy = round((FTstep4TotSpit / FTstep4Tot), 1)
        FTstep4Freq = round((FTstep4Pos / FTstep4Tot) * 100, 1)
        freqList.append(FTstep4Freq)
    else:
        FTstep4Moy = 1
        FTstep4Freq = 1
        freqList.append(FTstep4Freq)
    if FTstep5Tot != 0:
        FTstep5Moy = round((FTstep5TotSpit / FTstep5Tot), 1)
        FTstep5Freq = round((FTstep5Pos / FTstep5Tot) * 100, 1)
        freqList.append(FTstep5Freq)
    else:
        FTstep5Moy = 1
        FTstep5Freq = 1
        freqList.append(FTstep5Freq)
    if FTstep6Tot != 0:
        FTstep6Moy = round((FTstep6TotSpit / FTstep6Tot), 1)
        FTstep6Freq = round((FTstep6Pos / FTstep6Tot) * 100, 1)
        freqList.append(FTstep6Freq)
    else:
        FTstep6Moy = 1
        FTstep6Freq = 1
        freqList.append(FTstep6Freq)
    if FTstep7Tot != 0:
        FTstep7Moy = round((FTstep7TotSpit / FTstep7Tot), 1)
        FTstep7Freq = round((FTstep7Pos / FTstep7Tot) * 100, 1)
        freqList.append(FTstep7Freq)
    else:
        FTstep7Moy = 1
        FTstep7Freq = 1
        freqList.append(FTstep7Freq)
    if FTstep8Tot != 0:
        FTstep8Moy = round((FTstep8TotSpit / FTstep8Tot), 1)
        FTstep8Freq = round((FTstep8Pos / FTstep8Tot) * 100, 1)
        freqList.append(FTstep8Freq)
    else:
        FTstep8Moy = 1
        FTstep8Freq = 1
        freqList.append(FTstep8Freq)
    if FTstep9Tot != 0:
        FTstep9Moy = round((FTstep9TotSpit / FTstep9Tot), 1)
        FTstep9Freq = round((FTstep9Pos / FTstep9Tot) * 100, 1)
        freqList.append(FTstep9Freq)
    else:
        FTstep9Moy = 1
        FTstep9Freq = 1
        freqList.append(FTstep9Freq)
    if FTstep10Tot != 0:
        FTstep10Moy = round((FTstep10TotSpit / FTstep10Tot), 1)
        FTstep10Freq = round((FTstep10Pos / FTstep10Tot) * 100, 1)
        freqList.append(FTstep10Freq)
    else:
        FTstep10Moy = 1
        FTstep10Freq = 1
        freqList.append(FTstep10Freq)
    if FTstep11Tot != 0:
        FTstep11Moy = round((FTstep11TotSpit / FTstep11Tot), 1)
        FTstep11Freq = round((FTstep11Pos / FTstep11Tot) * 100, 1)
        freqList.append(FTstep11Freq)
    else:
        FTstep11Moy = 1
        FTstep11Freq = 1
        freqList.append(FTstep11Freq)
    if FTstep12Tot != 0:
        FTstep12Moy = round((FTstep12TotSpit / FTstep12Tot), 1)
        FTstep12Freq = round((FTstep12Pos / FTstep12Tot) * 100, 1)
        freqList.append(FTstep12Freq)
    else:
        FTstep12Moy = 1
        FTstep12Freq = 1
        freqList.append(FTstep12Freq)
    if FTstep13Tot != 0:
        FTstep13Moy = round((FTstep13TotSpit / FTstep13Tot), 1)
        FTstep13Freq = round((FTstep13Pos / FTstep13Tot) * 100, 1)
        freqList.append(FTstep13Freq)
    else:
        FTstep13Moy = 1
        FTstep13Freq = 1
        freqList.append(FTstep13Freq)
    if FTstep14Tot != 0:
        FTstep14Moy = round((FTstep14TotSpit / FTstep14Tot), 1)
        FTstep14Freq = round((FTstep14Pos / FTstep14Tot) * 100, 1)
        freqList.append(FTstep14Freq)
    else:
        FTstep14Moy = 1
        FTstep14Freq = 1
        freqList.append(FTstep14Freq)
    if FTstep15Tot != 0:
        FTstep15Moy = round((FTstep15TotSpit / FTstep15Tot), 1)
        FTstep15Freq = round((FTstep15Pos / FTstep15Tot) * 100, 1)
        freqList.append(FTstep15Freq)
    else:
        FTstep15Moy = 1
        FTstep15Freq = 1
        freqList.append(FTstep15Freq)
    if FTstep16Tot != 0:
        FTstep16Moy = round((FTstep16TotSpit / FTstep16Tot), 1)
        FTstep16Freq = round((FTstep16Pos / FTstep16Tot) * 100, 1)
        freqList.append(FTstep16Freq)
    else:
        FTstep16Moy = 1
        FTstep16Freq = 1
        freqList.append(FTstep16Freq)
    if FTstep17Tot != 0:
        FTstep17Moy = round((FTstep17TotSpit / FTstep17Tot), 1)
        FTstep17Freq = round((FTstep17Pos / FTstep17Tot) * 100, 1)
        freqList.append(FTstep17Freq)
    else:
        FTstep17Moy = 1
        FTstep17Freq = 1
        freqList.append(FTstep17Freq)
    if FTstep18Tot != 0:
        FTstep18Moy = round((FTstep18TotSpit / FTstep18Tot), 1)
        FTstep18Freq = round((FTstep18Pos / FTstep18Tot) * 100, 1)
        freqList.append(FTstep18Freq)
    else:
        FTstep18Moy = 1
        FTstep18Freq = 1
        freqList.append(FTstep18Freq)
    if FTstep19Tot != 0:
        FTstep19Moy = round((FTstep19TotSpit / FTstep19Tot), 1)
        FTstep19Freq = round((FTstep19Pos / FTstep19Tot) * 100, 1)
        freqList.append(FTstep19Freq)
    else:
        FTstep19Moy = 1
        FTstep19Freq = 1
        freqList.append(FTstep19Freq)
    if FTstep20Tot != 0:
        FTstep20Moy = round((FTstep20TotSpit / FTstep20Tot), 1)
        FTstep20Freq = round((FTstep20Pos / FTstep20Tot) * 100, 1)
        freqList.append(FTstep20Freq)
    else:
        FTstep20Moy = 1
        FTstep20Freq = 1
        freqList.append(FTstep20Freq)

    bars = ['FT step 1', 'FT step 2', 'FT step 3', 'FT step 4', 'FT step 5', 'FT step 6', 'FT step 7', 'FT step 8', 'FT step 9', 'FT step 10', 'FT step 11', 'FT step 12', 'FT step 13', 'FT step 14', 'FT step 15', 'FT step 16', 'FT step 17', 'FT step 18', 'FT step 19', 'FT step 20']
    dvar = 0
    for freq in freqList:
        dvar += freq

    fig = plt.figure()
    sns.set(style="darkgrid")
    if cabine_name == 'D':
        ax = sns.barplot(x=bars, y=freqList, color='#004d99')
    elif cabine_name == 'G':
        ax = sns.barplot(x=bars, y=freqList, color='#4747d1')
    elif cabine_name == 'K':
        ax = sns.barplot(x=bars, y=freqList, color='#4d1919')
    elif cabine_name == 'Q':
        ax = sns.barplot(x=bars, y=freqList, color='#194d33')
    y_pos = np.arange(len(bars))
    plt.xticks(y_pos, bars)
    plt.ylabel('%')
    plt.xticks(rotation='vertical')
    plt.subplots_adjust(bottom=0.20)
    plt.suptitle("Spits Frequency - Cabin " + cabine_name)

    typicalString = "The 'FT step 1' has a {0} %  probability of inducing at least 1 spit.\nThe average number of spits at this step is {1}".format(FTstep1Freq, FTstep1Moy)
    typicalString += "\n\nThe 'FT step 2' has a {0} %  probability of inducing at least 1 spit.\nThe average number of spits at this step is {1}".format(FTstep2Freq, FTstep2Moy)
    typicalString += "\n\nThe 'FT step 3' has a {0} %  probability of inducing at least 1 spit.\nThe average number of spits at this step is {1}".format(FTstep3Freq, FTstep3Moy)
    typicalString += "\n\nThe 'FT step 4' has a {0} %  probability of inducing at least 1 spit.\nThe average number of spits at this step is {1}".format(FTstep4Freq, FTstep4Moy)
    typicalString += "\n\nThe 'FT step 5' has a {0} %  probability of inducing at least 1 spit.\nThe average number of spits at this step is {1}".format(FTstep5Freq, FTstep5Moy)
    typicalString += "\n\nThe 'FT step 6' has a {0} %  probability of inducing at least 1 spit.\nThe average number of spits at this step is {1}".format(FTstep6Freq, FTstep6Moy)
    typicalString += "\n\nThe 'FT step 7' has a {0} %  probability of inducing at least 1 spit.\nThe average number of spits at this step is {1}".format(FTstep7Freq, FTstep7Moy)
    typicalString += "\n\nThe 'FT step 8' has a {0} %  probability of inducing at least 1 spit.\nThe average number of spits at this step is {1}".format(FTstep8Freq, FTstep8Moy)
    typicalString += "\n\nThe 'FT step 9' has a {0} %  probability of inducing at least 1 spit.\nThe average number of spits at this step is {1}".format(FTstep9Freq, FTstep9Moy)
    typicalString += "\n\nThe 'FT step 10' has a {0} % probability of inducing at least 1 spit.\nThe average number of spits at this step is {1}".format(FTstep10Freq, FTstep10Moy)
    typicalString += "\n\nThe 'FT step 11' has a {0} % probability of inducing at least 1 spit.\nThe average number of spits at this step is {1}".format(FTstep11Freq, FTstep11Moy)
    typicalString += "\n\nThe 'FT step 12' has a {0} % probability of inducing at least 1 spit.\nThe average number of spits at this step is {1}".format(FTstep12Freq, FTstep12Moy)
    typicalString += "\n\nThe 'FT step 13' has a {0} % probability of inducing at least 1 spit.\nThe average number of spits at this step is {1}".format(FTstep13Freq, FTstep13Moy)
    typicalString += "\n\nThe 'FT step 14' has a {0} % probability of inducing at least 1 spit.\nThe average number of spits at this step is {1}".format(FTstep14Freq, FTstep14Moy)
    typicalString += "\n\nThe 'FT step 15' has a {0} % probability of inducing at least 1 spit.\nThe average number of spits at this step is {1}".format(FTstep15Freq, FTstep15Moy)
    typicalString += "\n\nThe 'FT step 16' has a {0} % probability of inducing at least 1 spit.\nThe average number of spits at this step is {1}".format(FTstep16Freq, FTstep16Moy)
    typicalString += "\n\nThe 'FT step 17' has a {0} % probability of inducing at least 1 spit.\nThe average number of spits at this step is {1}".format(FTstep17Freq, FTstep17Moy)
    typicalString += "\n\nThe 'FT step 18' has a {0} % probability of inducing at least 1 spit.\nThe average number of spits at this step is {1}".format(FTstep18Freq, FTstep18Moy)
    typicalString += "\n\nThe 'FT step 19' has a {0} % probability of inducing at least 1 spit.\nThe average number of spits at this step is {1}".format(FTstep19Freq, FTstep19Moy)
    typicalString += "\n\nThe 'FT step 20' has a {0} % probability of inducing at least 1 spit.\nThe average number of spits at this step is {1}".format(FTstep20Freq, FTstep20Moy)

    if dvar == 20:
        typicalString = 'No run found'

    return fig, typicalString


def values(liste, cabine_name):
    os.chdir(ogpath)
    os.chdir('Sample' + cabine_name)
    casings = []
    divider = 0
    totLength = 0
    for file in liste:
        if file[:9] not in casings:
            casings.append(file[:9])
        with open(file, "r") as f:
            reader = csv.reader(f)
            i = next(reader)
            j = next(reader)
            k = next(reader)
            l = next(reader)
        if cabine_name == 'D':
            dft = pd.read_csv(file, skiprows=3, usecols=l[0:], encoding='utf8', engine='python')
        elif cabine_name == 'G':
            dft = pd.read_csv(file, skiprows=3, usecols=l[0:], encoding='utf8', engine='c')
        elif cabine_name == 'K':
            dft = pd.read_csv(file, skiprows=3, usecols=l[0:], encoding='ISO-8859-1', engine='c')
        elif cabine_name == 'Q':
            dft = pd.read_csv(file, skiprows=3, usecols=l[0:], encoding='utf8', engine='python')
        beg = dft.iloc[:, 0].head(1).to_string().split(' ')
        fin = dft.iloc[:, 0].tail(1).to_string().split(' ')
        if 'PM' in beg:
            pmbvar = 1
            ambvar = 0
        elif 'AM' in beg:
            pmbvar = 0
            ambvar = 1
        else:
            ambvar = 0
            pmbvar = 0
        if 'PM' in fin:
            amfvar = 0
            pmfvar = 1
        elif 'AM' in fin:
            amfvar = 1
            pmfvar = 0
        else:
            pmfvar = 0
            amfvar = 0
        beg = [s for s in beg if ":" in s]
        fin = [s for s in fin if ":" in s]
        if (beg != []) and (fin != []):
            if (beg[0].count(":") == 2) and (fin[0].count(":") == 2):
                beg = beg[0].split(':')
                fin = fin[0].split(':')
                hrsb = int(beg[0])
                hrsf = int(fin[0])
                if ambvar == 1:
                    if hrsb == 12:
                        hrsb = 24
                    elif hrsb < 5:
                        hrsb = hrsb +24
                if pmbvar == 1:
                    if hrsb != 12:
                        hrsb = hrsb + 12
                if amfvar == 1:
                    if hrsf == 12:
                        hrsf = 24
                    elif hrsf < 5:
                        hrsf = hrsf +24
                if pmfvar == 1:
                    if hrsf != 12:
                        hrsf = hrsf + 12
                begSec = (hrsb*3600) + (int(beg[1])*60) + int(beg[2])
                finSec = (hrsf*3600) + (int(fin[1])*60) + int(fin[2])
                length = finSec - begSec
                totLength += length
                divider += 1
            else:
                totLength = 0
    if divider != 0:
        meanTimeSec = totLength / divider
    else:
        meanTimeSec = 0
    mtHours = meanTimeSec / 3600
    meanTimeSec %= 3600
    mtMinutes = meanTimeSec / 60
    meanTimeSec %= 60
    mtSeconds = meanTimeSec

    tlHours = totLength / 3600
    totLength %= 3600
    tlMinutes = totLength / 60
    totLength %= 60
    tlSeconds = totLength
    nbCasings = len(casings)
    typicalString = '\n\nCabine ' + cabine_name + ':'
    typicalString += '\n\nTotal Length: %d' % tlHours + ' hours %d' % tlMinutes + ' minutes %d' % tlSeconds + ' seconds'
    typicalString += '\n\nAverage Length: %d' % mtHours + ' hours %d' % mtMinutes + ' minutes %d' % mtSeconds + ' seconds'
    typicalString += '\n\nNumber of casings: %d' % nbCasings + '\n\n      ________________'

    return typicalString

def passErrButt():

    status.config(text='Loading...')
    pBar.step(1)
    window.update()
    AllFiles, cabList = whichCabins()
    pBar.step(9)
    window.update()
    nbCabins = len(AllFiles)

    if nbCabins == 1:
        fig, typicalString = passErrors(AllFiles[0], cabList[0])
        pBar.step(90)
        window.update()
        newWindowSingle(fig, typicalString)
    elif nbCabins == 2:
        fig1, typicalString1 = passErrors(AllFiles[0], cabList[0])
        pBar.step(40)
        window.update()
        fig2, typicalString2 = passErrors(AllFiles[1], cabList[1])
        pBar.step(50)
        window.update()
        newWindowDouble(fig1, fig2, typicalString1, typicalString2)
    elif nbCabins == 3:
        fig1, typicalString1 = passErrors(AllFiles[0], cabList[0])
        pBar.step(30)
        window.update()
        fig2, typicalString2 = passErrors(AllFiles[1], cabList[1])
        pBar.step(30)
        window.update()
        fig3, typicalString3 = passErrors(AllFiles[2], cabList[2])
        pBar.step(30)
        window.update()
        newWindowTriple(fig1, fig2, fig3, typicalString1, typicalString2, typicalString3)
    elif nbCabins == 4:
        fig1, typicalString1 = passErrors(AllFiles[0], cabList[0])
        pBar.step(30)
        window.update()
        fig2, typicalString2 = passErrors(AllFiles[1], cabList[1])
        pBar.step(20)
        window.update()
        fig3, typicalString3 = passErrors(AllFiles[2], cabList[2])
        pBar.step(20)
        window.update()
        fig4, typicalString4 = passErrors(AllFiles[3], cabList[3])
        pBar.step(20)
        window.update()
        newWindowQuadr(fig1, fig2, fig3, fig4, typicalString1, typicalString2, typicalString3, typicalString4)
    pBar.stop()
    status.config(text='Choose your settings and test')


def tauxProButt():

    status.config(text='Loading...')
    pBar.step(1)
    window.update()
    AllFiles, cabList = whichCabins()
    pBar.step(9)
    window.update()
    nbCabins = len(AllFiles)

    if nbCabins == 1:
        fig, typicalString, plotList = tauxProgress(AllFiles[0], cabList[0])
        pBar.step(90)
        window.update()
        newWindowSingleProg(fig, typicalString)
    elif nbCabins == 2:
        fig1, typicalString1, plotList1 = tauxProgress(AllFiles[0], cabList[0])
        pBar.step(50)
        window.update()
        fig2, typicalString2, plotList2 = tauxProgress(AllFiles[1], cabList[1])
        pBar.step(40)
        window.update()
        newWindowSingleProg(fig1, typicalString1)
        newWindowSingleProg(fig2, typicalString2)
        newWindowMashProg(cabList, plotList1, plotList2)
    elif nbCabins == 3:
        fig1, typicalString1, plotList1 = tauxProgress(AllFiles[0], cabList[0])
        pBar.step(30)
        window.update()
        fig2, typicalString2, plotList2 = tauxProgress(AllFiles[1], cabList[1])
        pBar.step(30)
        window.update()
        fig3, typicalString3, plotList3 = tauxProgress(AllFiles[2], cabList[2])
        pBar.step(30)
        window.update()
        newWindowSingleProg(fig1, typicalString1)
        newWindowSingleProg(fig2, typicalString2)
        newWindowSingleProg(fig3, typicalString3)
        newWindowMashProg(cabList, plotList1, plotList2, plotList3)
    elif nbCabins == 4:
        fig1, typicalString1, plotList1 = tauxProgress(AllFiles[0], cabList[0])
        pBar.step(30)
        window.update()
        fig2, typicalString2, plotList2 = tauxProgress(AllFiles[1], cabList[1])
        pBar.step(25)
        window.update()
        fig3, typicalString3, plotList3 = tauxProgress(AllFiles[2], cabList[2])
        pBar.step(25)
        window.update()
        fig4, typicalString4, plotList4 = tauxProgress(AllFiles[3], cabList[3])
        pBar.step(10)
        window.update()
        newWindowSingleProg(fig1, typicalString1)
        newWindowSingleProg(fig2, typicalString2)
        newWindowSingleProg(fig3, typicalString3)
        newWindowSingleProg(fig4, typicalString4)
        newWindowMashProg(cabList, plotList1, plotList2, plotList3, plotList4)
    pBar.stop()
    status.config(text='Choose your settings and test')


def spitFreqButt():

    status.config(text='Loading...')
    pBar.step(9)
    window.update()
    AllFiles, cabList = whichCabins()
    pBar.step(9)
    window.update()
    nbCabins = len(AllFiles)

    if nbCabins == 1:
        fig, typicalString = spitFreq(AllFiles[0], cabList[0])
        pBar.step(90)
        window.update()
        newWindowSingle(fig, typicalString)
    elif nbCabins == 2:
        fig1, typicalString1 = spitFreq(AllFiles[0], cabList[0])
        pBar.step(50)
        window.update()
        fig2, typicalString2 = spitFreq(AllFiles[1], cabList[1])
        pBar.step(40)
        window.update()
        newWindowDouble(fig1, fig2, typicalString1, typicalString2)
    elif nbCabins == 3:
        fig1, typicalString1 = spitFreq(AllFiles[0], cabList[0])
        pBar.step(30)
        window.update()
        fig2, typicalString2 = spitFreq(AllFiles[1], cabList[1])
        pBar.step(30)
        window.update()
        fig3, typicalString3 = spitFreq(AllFiles[2], cabList[2])
        pBar.step(30)
        window.update()
        newWindowTriple(fig1, fig2, fig3, typicalString1, typicalString2, typicalString3)
    elif nbCabins == 4:
        fig1, typicalString1 = spitFreq(AllFiles[0], cabList[0])
        pBar.step(30)
        window.update()
        fig2, typicalString2 = spitFreq(AllFiles[1], cabList[1])
        pBar.step(25)
        window.update()
        fig3, typicalString3 = spitFreq(AllFiles[2], cabList[2])
        pBar.step(25)
        window.update()
        fig4, typicalString4 = spitFreq(AllFiles[3], cabList[3])
        pBar.step(10)
        window.update()
        newWindowQuadr(fig1, fig2, fig3, fig4, typicalString1, typicalString2, typicalString3, typicalString4)
    pBar.stop()
    status.config(text='Choose your settings and test')


def valuesButt():

    status.config(text='Loading...')
    pBar.step(1)
    window.update()
    AllFiles, cabList = whichCabins()
    pBar.step(9)
    window.update()
    nbCabins = len(AllFiles)

    if nbCabins == 1:
        typicalString = values(AllFiles[0], cabList[0])
        pBar.step(90)
        window.update()
        newWindowTxt(typicalString)
    elif nbCabins == 2:
        typicalString1 = values(AllFiles[0], cabList[0])
        pBar.step(40)
        window.update()
        typicalString2 = values(AllFiles[1], cabList[1])
        pBar.step(50)
        window.update()
        typicalString = typicalString1 + typicalString2
        newWindowTxt(typicalString)
    elif nbCabins == 3:
        typicalString1 = values(AllFiles[0], cabList[0])
        pBar.step(30)
        window.update()
        typicalString2 = values(AllFiles[1], cabList[1])
        pBar.step(30)
        window.update()
        typicalString3 = values(AllFiles[2], cabList[2])
        pBar.step(30)
        window.update()
        typicalString = typicalString1 + typicalString2 + typicalString3
        newWindowTxt(typicalString)
    elif nbCabins == 4:
        typicalString1 = values(AllFiles[0], cabList[0])
        pBar.step(30)
        window.update()
        typicalString2 = values(AllFiles[1], cabList[1])
        pBar.step(20)
        window.update()
        typicalString3 = values(AllFiles[2], cabList[2])
        pBar.step(20)
        window.update()
        typicalString4 = values(AllFiles[3], cabList[3])
        pBar.step(20)
        window.update()
        typicalString = typicalString1 + typicalString2 + typicalString3 + typicalString4
        newWindowTxt(typicalString)
    pBar.stop()
    status.config(text='Choose your settings and test')

# NEW WINDOW FUNCTION

def Error(textst):
    myFont = font.Font(family="Cambria", size=11)
    errorW = tk.Toplevel(window)
    errorW.title('Error')
    PEmainFrame = tk.Frame(errorW)
    PEmainFrame.pack()
    errLab = tk.Label(PEmainFrame, text=textst, font=myFont)
    errLab.grid(column=0, row=0, sticky="NSEW", pady=15)

def theAbout():

    myFont = font.Font(family="Cambria", size=15)
    aboutW = tk.Toplevel(window)
    aboutW.title('About')
    aboutFrame = tk.Frame(aboutW)
    aboutFrame.pack()
    aboutTitleLab = tk.Label(aboutFrame, text='Moosh Leap', font=myFont)
    aboutTitleLab.grid(column=0, row=0, sticky="NSEW", pady=15)
    aboutCR = tk.Label(aboutFrame, text="©GE 2018 - hugo-nattagh@protonmail.com")
    aboutCR.grid(column=0, row=1, sticky="NSEW", pady=15, padx=15)

def newWindowTxt(text):

    newW = tk.Toplevel(window)

    PEmainFrame = tk.Frame(newW)
    PEmainFrame.pack(fill=tk.BOTH, expand=1)

    PEFrametxt = tk.Frame(PEmainFrame, bd=2, relief="flat")
    PEFrametxt.pack(fill=tk.BOTH, expand=1)

    myFont = font.Font(family="Cambria", size=11)

    txtDisplay1 = tk.Text(PEFrametxt, background='#edf2f8')
    txtDisplay1.pack(fill=tk.BOTH, expand=1)
    txtDisplay1.insert('1.0', text)
    txtDisplay1.config(state='disabled', font=myFont, wrap=tk.WORD)


def newWindowSingle(figure, text):

    newW = tk.Toplevel(window)
    newW.state('zoomed')

    PEmainFrame = tk.Frame(newW)
    PEmainFrame.pack(fill=tk.BOTH, expand=1)

    PEFrame1gph = tk.Frame(PEmainFrame)
    PEFrame1gph.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

    PEFrame1txt = tk.Frame(PEmainFrame, bd=2, relief="flat")
    PEFrame1txt.pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)

    myFont = font.Font(family="Cambria", size=11)

    canvas1 = FigureCanvasTkAgg(figure, master=PEFrame1gph)
    canvas1.draw()
    canvas1.get_tk_widget().pack(fill=tk.BOTH, expand=1)

    toolbar = NavigationToolbar2Tk(canvas1, PEFrame1gph)
    toolbar.update()
    canvas1._tkcanvas.pack(fill=tk.BOTH, expand=1)

    txtDisplay1 = tk.Text(PEFrame1txt, background='#edf2f8')
    txtDisplay1.pack(fill=tk.BOTH, expand=1)
    txtDisplay1.insert('1.0', text)
    txtDisplay1.config(state='disabled', font=myFont, wrap=tk.WORD)


def newWindowSingleProg(figure, text):

    newW = tk.Toplevel(window)
    newW.state('zoomed')

    PEmainFrame = tk.Frame(newW)
    PEmainFrame.pack(fill=tk.BOTH, expand=1)
    PEmainFrame.columnconfigure(0, weight=1)
    PEmainFrame.rowconfigure(0, weight=1)
    PEmainFrame.rowconfigure(1, weight=3)

    PEFrame1gph = tk.Frame(PEmainFrame)
    PEFrame1gph.grid(row=0, sticky='EW', ipady=150)

    PEFrame1txt = tk.Frame(PEmainFrame, bd=2, relief="flat")
    PEFrame1txt.grid(row=1, sticky='EW')

    canvas = FigureCanvasTkAgg(figure, master=PEFrame1gph)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)

    toolbar = NavigationToolbar2Tk(canvas, PEFrame1gph)
    toolbar.update()
    canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    myFont = font.Font(family="Cambria", size=11)

    txtDisplay = tk.Text(PEFrame1txt, background='#edf2f8')
    txtDisplay.pack(fill=tk.BOTH, expand=1)
    txtDisplay.insert('1.0', text)
    txtDisplay.config(state='disabled', font=myFont, wrap=tk.WORD)


def newWindowMashProg(cabList, plot1, plot2, *args):

    newW = tk.Toplevel(window)
    newW.state('zoomed')

    PEmainFrame = tk.Frame(newW)
    PEmainFrame.pack(fill=tk.BOTH, expand=1)
    PEmainFrame.columnconfigure(0, weight=1)
    PEmainFrame.rowconfigure(0, weight=1)
    PEmainFrame.rowconfigure(1, weight=3)

    if (len(plot1) == 0 or len(plot2) == 0):
        PEErrtxt = tk.Text(PEmainFrame)
        PEErrtxt.grid(row=0, sticky='EW', ipady=50)
        PEErrtxt.insert('1.0', 'No file found')
    else:
        PEFrame1gph = tk.Frame(PEmainFrame)
        PEFrame1gph.grid(row=0, sticky='EW', ipady=50)

        prescriptions = {'Calibration': 0, 'Tube Warm Up': 0, 'NG HVIS #1': 0, 'NG HVIS #2': 0, 'NG HVIS #3': 0, 'NG HVIS #4': 0, 'SHVIS 2 A': 0, 'SHVIS 2 B': 0, 'SHVIS 2 C': 0, 'SHVIS 2 D': 0, 'SHVIS 2 E': 0, 'SHVIS 2 F': 0}
        prescriptionsFT = {'FT step 1': 0, 'FT step 2': 0, 'FT step 3': 0, 'FT step 4': 0, 'FT step 5': 0, 'FT step 6': 0, 'FT step 7': 0, 'FT step 8': 0, 'FT step 9': 0, 'FT step 10': 0, 'FT step 11': 0, 'FT step 12': 0, 'FT step 13': 0, 'FT step 14': 0, 'FT step 15': 0, 'FT step 16': 0, 'FT step 17': 0, 'FT step 18': 0, 'FT step 19': 0, 'FT step 20': 0}
        allPrescriptions = dict(prescriptions, **prescriptionsFT)
        APList = list(allPrescriptions.keys())

        fig = plt.figure(figsize=(5, 8))
        sns.set(style="darkgrid")
        plt.plot(APList, plot1, color='blue')
        plt.plot(APList, plot2, color='green')
        firstCab = mpatches.Patch(color='blue', label=cabList[0])
        secCab = mpatches.Patch(color='green', label=cabList[1])
        if len(args) == 1:
            plt.plot(APList, args[0], color='#4d1919')
            thirdCab = mpatches.Patch(color='#4d1919', label=cabList[2])
            plt.legend(handles=[firstCab, secCab, thirdCab])
        elif len(args) == 2:
            plt.plot(APList, args[0], color='#4d1919')
            plt.plot(APList, args[1], color='#001a33')
            thirdCab = mpatches.Patch(color='#4d1919', label=cabList[2])
            fourthCab = mpatches.Patch(color='#001a33', label=cabList[3])
            plt.legend(handles=[firstCab, secCab, thirdCab, fourthCab])
        else:
            plt.legend(handles=[firstCab, secCab])

        plt.xlabel('Étapes')
        plt.ylabel('%')
        plt.xticks(rotation='vertical')
        plt.suptitle("Progress")

        canvas = FigureCanvasTkAgg(fig, master=PEFrame1gph)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)

        toolbar = NavigationToolbar2Tk(canvas, PEFrame1gph)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)


def newWindowDouble(figure_1, figure_2, text_1, text_2):
    newW = tk.Toplevel(window)
    newW.state('zoomed')

    PEmainFrame = tk.Frame(newW)
    PEmainFrame.pack(fill=tk.BOTH, expand=1)
    PEmainFrame.columnconfigure(0, weight=1)
    PEmainFrame.columnconfigure(1, weight=1)
    PEmainFrame.rowconfigure(0, weight=1)
    PEmainFrame.rowconfigure(1, weight=1)

    PEFrame1gph = tk.Frame(PEmainFrame)
    PEFrame1gph.grid(column=0, row=0)

    PEFrame1txt = tk.Frame(PEmainFrame, bd=2, relief="flat")
    PEFrame1txt.grid(column=1, row=0)

    PEFrame2gph = tk.Frame(PEmainFrame)
    PEFrame2gph.grid(column=0, row=1)

    PEFrame2txt = tk.Frame(PEmainFrame, bd=2, relief="flat")
    PEFrame2txt.grid(column=1, row=1)

    myFont = font.Font(family="Cambria", size=11)

    canvas1 = FigureCanvasTkAgg(figure_1, master=PEFrame1gph)
    canvas1.draw()
    canvas1.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    toolbar = NavigationToolbar2Tk(canvas1, PEFrame1gph)
    toolbar.update()
    canvas1._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    txtDisplay1 = tk.Text(PEFrame1txt, background='#edf2f8')
    txtDisplay1.pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)
    txtDisplay1.insert('1.0', text_1)
    txtDisplay1.config(state='disabled', font=myFont, wrap=tk.WORD)

    canvas2 = FigureCanvasTkAgg(figure_2, master=PEFrame2gph)
    canvas2.draw()
    canvas2.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    toolbar2 = NavigationToolbar2Tk(canvas2, PEFrame2gph)
    toolbar2.update()
    canvas2._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    txtDisplay2 = tk.Text(PEFrame2txt, background='#edf2f8')
    txtDisplay2.pack(side=tk.RIGHT, fill=tk.BOTH, expand=0)
    txtDisplay2.insert('1.0', text_2)
    txtDisplay2.config(state='disabled', font=myFont, wrap=tk.WORD)


def newWindowTriple(figure_1, figure_2, figure_3, text_1, text_2, text_3):
    newW = tk.Toplevel(window)
    newW.state('zoomed')

    PEmainFrame = tk.Frame(newW)
    PEmainFrame.pack(fill=tk.BOTH, expand=1)
    PEmainFrame.columnconfigure(0, weight=1)
    PEmainFrame.columnconfigure(1, weight=1)
    PEmainFrame.columnconfigure(2, weight=1)
    PEmainFrame.columnconfigure(3, weight=1)
    PEmainFrame.rowconfigure(0, weight=1)
    PEmainFrame.rowconfigure(1, weight=1)

    PEFrame1gph = tk.Frame(PEmainFrame)
    PEFrame1gph.grid(column=0, row=0)

    PEFrame1txt = tk.Frame(PEmainFrame, bd=2, relief="flat")
    PEFrame1txt.grid(column=1, row=0)

    PEFrame2gph = tk.Frame(PEmainFrame)
    PEFrame2gph.grid(column=2, row=0)

    PEFrame2txt = tk.Frame(PEmainFrame, bd=2, relief="flat")
    PEFrame2txt.grid(column=3, row=0)

    PEFrame3gph = tk.Frame(PEmainFrame)
    PEFrame3gph.grid(column=1, row=1)

    PEFrame3txt = tk.Frame(PEmainFrame, bd=2, relief="flat")
    PEFrame3txt.grid(column=2, row=1)

    myFont = font.Font(family="Cambria", size=11)

    canvas1 = FigureCanvasTkAgg(figure_1, master=PEFrame1gph)
    canvas1.draw()
    canvas1.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    toolbar = NavigationToolbar2Tk(canvas1, PEFrame1gph)
    toolbar.update()
    canvas1._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    txtDisplay1 = tk.Text(PEFrame1txt, background='#edf2f8')
    txtDisplay1.pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)
    txtDisplay1.insert('1.0', text_1)
    txtDisplay1.config(state='disabled', font=myFont, wrap=tk.WORD)

    canvas2 = FigureCanvasTkAgg(figure_2, master=PEFrame2gph)
    canvas2.draw()
    canvas2.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    toolbar2 = NavigationToolbar2Tk(canvas2, PEFrame2gph)
    toolbar2.update()
    canvas2._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    txtDisplay2 = tk.Text(PEFrame2txt, background='#edf2f8')
    txtDisplay2.pack(side=tk.RIGHT, fill=tk.BOTH, expand=0)
    txtDisplay2.insert('1.0', text_2)
    txtDisplay2.config(state='disabled', font=myFont, wrap=tk.WORD)

    canvas3 = FigureCanvasTkAgg(figure_3, master=PEFrame3gph)
    canvas3.draw()
    canvas3.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    toolbar3 = NavigationToolbar2Tk(canvas3, PEFrame3gph)
    toolbar3.update()
    canvas3._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    txtDisplay3 = tk.Text(PEFrame3txt, background='#edf2f8')
    txtDisplay3.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    txtDisplay3.insert('1.0', text_3)
    txtDisplay3.config(state='disabled', font=myFont, wrap=tk.WORD)


def newWindowQuadr(figure_1, figure_2, figure_3, figure_4, text_1, text_2, text_3, text_4):
    newW = tk.Toplevel(window)
    newW.state('zoomed')

    PEmainFrame = tk.Frame(newW)
    PEmainFrame.pack(fill=tk.BOTH, expand=1)
    PEmainFrame.columnconfigure(0, weight=1)
    PEmainFrame.columnconfigure(1, weight=1)
    PEmainFrame.columnconfigure(2, weight=1)
    PEmainFrame.columnconfigure(3, weight=1)
    PEmainFrame.rowconfigure(0, weight=1)
    PEmainFrame.rowconfigure(1, weight=1)

    PEFrame1gph = tk.Frame(PEmainFrame)
    PEFrame1gph.grid(column=0, row=0)

    PEFrame1txt = tk.Frame(PEmainFrame, bd=2, relief="flat")
    PEFrame1txt.grid(column=1, row=0)

    PEFrame2gph = tk.Frame(PEmainFrame)
    PEFrame2gph.grid(column=2, row=0)

    PEFrame2txt = tk.Frame(PEmainFrame, bd=2, relief="flat")
    PEFrame2txt.grid(column=3, row=0)

    PEFrame3gph = tk.Frame(PEmainFrame)
    PEFrame3gph.grid(column=0, row=1)

    PEFrame3txt = tk.Frame(PEmainFrame, bd=2, relief="flat")
    PEFrame3txt.grid(column=1, row=1)

    PEFrame4gph = tk.Frame(PEmainFrame)
    PEFrame4gph.grid(column=2, row=1)

    PEFrame4txt = tk.Frame(PEmainFrame, bd=2, relief="flat")
    PEFrame4txt.grid(column=3, row=1)

    myFont = font.Font(family="Cambria", size=11)

    canvas1 = FigureCanvasTkAgg(figure_1, master=PEFrame1gph)
    canvas1.draw()
    canvas1.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    toolbar = NavigationToolbar2Tk(canvas1, PEFrame1gph)
    toolbar.update()
    canvas1._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    txtDisplay1 = tk.Text(PEFrame1txt, background='#edf2f8')
    txtDisplay1.pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)
    txtDisplay1.insert('1.0', text_1)
    txtDisplay1.config(state='disabled', font=myFont, wrap=tk.WORD)

    canvas2 = FigureCanvasTkAgg(figure_2, master=PEFrame2gph)
    canvas2.draw()
    canvas2.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    toolbar2 = NavigationToolbar2Tk(canvas2, PEFrame2gph)
    toolbar2.update()
    canvas2._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    txtDisplay2 = tk.Text(PEFrame2txt, background='#edf2f8')
    txtDisplay2.pack(side=tk.RIGHT, fill=tk.BOTH, expand=0)
    txtDisplay2.insert('1.0', text_2)
    txtDisplay2.config(state='disabled', font=myFont, wrap=tk.WORD)

    canvas3 = FigureCanvasTkAgg(figure_3, master=PEFrame3gph)
    canvas3.draw()
    canvas3.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    toolbar3 = NavigationToolbar2Tk(canvas3, PEFrame3gph)
    toolbar3.update()
    canvas3._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    txtDisplay3 = tk.Text(PEFrame3txt, background='#edf2f8')
    txtDisplay3.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    txtDisplay3.insert('1.0', text_3)
    txtDisplay3.config(state='disabled', font=myFont, wrap=tk.WORD)

    canvas4 = FigureCanvasTkAgg(figure_4, master=PEFrame4gph)
    canvas4.draw()
    canvas4.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    toolbar4 = NavigationToolbar2Tk(canvas4, PEFrame4gph)
    toolbar4.update()
    canvas4._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    txtDisplay4 = tk.Text(PEFrame4txt, background='#edf2f8')
    txtDisplay4.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    txtDisplay4.insert('1.0', text_4)
    txtDisplay4.config(state='disabled', font=myFont, wrap=tk.WORD)

#  GUI_______________________________________________________________________________________

# Menu


leMenu = tk.Menu(window)
window.config(menu=leMenu)
submenu = tk.Menu(leMenu, tearoff=0)
leMenu.add_cascade(label='?', menu=submenu)
submenu.add_command(label='About', command=theAbout)

# Frame contenant tous les paramètres


settingFrame0 = tk.Frame(window, bd=4, relief="ridge")
settingFrame0.grid(column=0, row=0)

settingTitle = tk.Label(settingFrame0, text="Settings", font=("Times New Roman", 20, "bold"))
settingTitle.grid(column=0, row=0, columnspan=2, pady=20)

sepTitle = ttk.Separator(settingFrame0, orient="horizontal")
sepTitle.grid(column=0, row=1, sticky="EW", columnspan=2)

# Frame contenant les paramètres à gauche (Passage, Année Cabine)
settingFrameLeft = tk.Frame(settingFrame0)
settingFrameLeft.grid(column=0, row=2, padx=10)

# Frame Passage--------------------------------------------------------------
settingFrame1 = tk.Frame(settingFrameLeft)
settingFrame1.grid(column=0, row=0)

labelPass1 = tk.Label(settingFrame1, text="Runs")
labelPass1.configure(font=("Times New Roman", 12, "bold"))
labelPass1.grid(column=0, row=0, columnspan=4)

rbvar = tk.IntVar()

radButtPass1 = tk.Radiobutton(settingFrame1, text="All Runs", value=1, variable=rbvar)
radButtPass1.grid(column=0, row=1, sticky="W")
radButtPass1.select()

radButtPass2 = tk.Radiobutton(settingFrame1, text="Run N° ", value=2, variable=rbvar)
radButtPass2.grid(column=0, row=2, sticky="W")
radButtPass2.deselect()

spBoxPass1 = tk.Spinbox(settingFrame1, from_=1, to=50, width=2)
spBoxPass1.grid(column=1, row=2)

radButtPass3 = tk.Radiobutton(settingFrame1, text="Runs ", value=3, variable=rbvar)
radButtPass3.grid(column=0, row=3, sticky="W")
radButtPass3.deselect()

spBoxPass2 = tk.Spinbox(settingFrame1, from_=1, to=50, width=2)
spBoxPass2.grid(column=1, row=3)

labelPass2 = tk.Label(settingFrame1, text=" to ")
labelPass2.grid(column=2, row=3)

spBoxPass3 = tk.Spinbox(settingFrame1, from_=1, to=50, width=2)
spBoxPass3.grid(column=3, row=3)

sep1 = ttk.Separator(settingFrame1, orient="horizontal")
sep1.grid(row=4, sticky="EW", columnspan=4, pady=15)

# Frame Année---------------------------------------------------------
settingFrame2 = tk.Frame(settingFrameLeft)
settingFrame2.grid(column=0, row=1)

labelYear1 = tk.Label(settingFrame2, text="Date")
labelYear1.configure(font=("Times New Roman", 12, "bold"))
labelYear1.grid(column=0, row=0, columnspan=7)

spBoxDay1 = tk.Spinbox(settingFrame2, from_=1, to=31, width=2)
spBoxDay1.grid(column=0, row=1)

spBoxMonth1 = tk.Spinbox(settingFrame2, from_=1, to=12, width=2)
spBoxMonth1.grid(column=1, row=1)

spBoxYear1 = tk.Spinbox(settingFrame2, from_=2009, to=2500, width=4)
spBoxYear1.grid(column=2, row=1)

labelYear2 = tk.Label(settingFrame2, text=" to ")
labelYear2.grid(column=3, row=1)

currentDay = tk.StringVar(settingFrame2)
currentDay.set(now.day)
spBoxDay2 = tk.Spinbox(settingFrame2, from_=1, to=31, width=2, textvariable=currentDay)
spBoxDay2.grid(column=4, row=1)

currentMonth = tk.StringVar(settingFrame2)
currentMonth.set(now.month)
spBoxMonth2 = tk.Spinbox(settingFrame2, from_=1, to=12, width=2, textvariable=currentMonth)
spBoxMonth2.grid(column=5, row=1)

currentYear = tk.StringVar(settingFrame2)
currentYear.set(now.year)
spBoxYear2 = tk.Spinbox(settingFrame2, from_=2009, to=2500, width=4, textvariable=currentYear)
spBoxYear2.grid(column=6, row=1)

sep2 = ttk.Separator(settingFrame2, orient="horizontal")
sep2.grid(column=0, row=2, sticky="EW", columnspan=7, pady=15)

# Frame Cabine-------------------------------------------------------------
settingFrame3 = tk.Frame(settingFrameLeft)
settingFrame3.grid(column=0, row=2)

labelCab1 = tk.Label(settingFrame3, text="Cabin")
labelCab1.configure(font=("Times New Roman", 12, "bold"))
labelCab1.grid(column=0, row=0, columnspan=3)

cab1var = tk.IntVar()
cab2var = tk.IntVar()
cab3var = tk.IntVar()
cab4var = tk.IntVar()

chBoxCab1 = tk.Checkbutton(settingFrame3, text="JEDIFT.D01", variable=cab1var)
chBoxCab1.grid(column=0, row=1)

chBoxCab2 = tk.Checkbutton(settingFrame3, text="JEDIFT.G01", variable=cab2var)
chBoxCab2.grid(column=1, row=1)

chBoxCab3 = tk.Checkbutton(settingFrame3, text="JEDIFT.K01", variable=cab3var)
chBoxCab3.grid(column=0, row=2)

chBoxCab4 = tk.Checkbutton(settingFrame3, text="JEDIFT.Q01", variable=cab4var)
chBoxCab4.grid(column=1, row=2)
chBoxCab4.select()

# FIN DES SETTINGS -> RESULTS _____________________________________________________________________________________________________

resultFrame = tk.Frame(window, bd=4, relief="ridge")
resultFrame.grid(column=1, row=0)

resultTitle = tk.Label(resultFrame, text="Results", font=("Times New Roman", 20, "bold"))
resultTitle.grid(column=0, row=0, columnspan=2, pady=20)

resultSepTitle = ttk.Separator(resultFrame, orient="horizontal")
resultSepTitle.grid(column=0, row=1, sticky="EW", columnspan=2)

resultFrame0 = tk.Frame(resultFrame)
resultFrame0.grid(column=0, row=2)

#  frame colonne de ----------------------
resultFrame1 = tk.Frame(resultFrame0)
resultFrame1.grid(column=0, row=0)

resLab1 = tk.Label(resultFrame1, text="Frequency Fail/Pass")
resLab1.grid(column=0, row=0, pady=3)

resButt1 = tk.Button(resultFrame1, text="Search", command=passErrButt)
resButt1.grid(column=0, row=1, pady=3)

resSep1 = ttk.Separator(resultFrame1, orient="horizontal")
resSep1.grid(column=0, row=2, sticky="EW", pady=15)

resLab2 = tk.Label(resultFrame1, text="Progress")
resLab2.grid(column=0, row=3, pady=3)

resButt2 = tk.Button(resultFrame1, text="Search", command=tauxProButt)
resButt2.grid(column=0, row=4, pady=3)

resSep2 = ttk.Separator(resultFrame1, orient="horizontal")
resSep2.grid(column=0, row=5, sticky="EW", pady=15)

resLab3 = tk.Label(resultFrame1, text="Spits per Steps")
resLab3.grid(column=0, row=6, pady=3)

resButt3 = tk.Button(resultFrame1, text="Search", command=spitFreqButt)
resButt3.grid(column=0, row=7, pady=3)

resSep3 = ttk.Separator(resultFrame1, orient="horizontal")
resSep3.grid(column=0, row=8, sticky="EW", pady=15)

resLab4 = tk.Label(resultFrame1, text="Values")
resLab4.grid(column=0, row=9, pady=3)

resButt4 = tk.Button(resultFrame1, text="Search", command=valuesButt)
resButt4.grid(column=0, row=10, pady=3)

# Status Bar
status = tk.Label(window, text='Choose your settings and test', bd=1, relief='sunken', anchor='w')
status.grid(column=0, row=1, columnspan=2, sticky='EW')
pBar = ttk.Progressbar(window)
pBar.grid(column=1, row=1, sticky='EW')

window.mainloop()
