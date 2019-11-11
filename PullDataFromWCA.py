import pandas as pd
import csv
from selenium import webdriver

registration = []

with open('sample.csv', newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    i = 0
    for row in reader:
        row.insert(0,i)
        registration.append(row)
        i += 1
wcaidcol = 0
for i in range(len(registration[0])):
    if registration[0][i] == 'WCA ID':
        wcaidcol = i

events = ['3x3x3 Cube', '2x2x2 Cube', '4x4x4 Cube', '5x5x5 Cube', '6x6x6 Cube', '7x7x7 Cube', '3x3x3 Blindfolded', '3x3x3 Fewest Moves', '3x3x3 One-Handed', '3x3x3 With Feet', 'Clock', 'Megaminx', 'Pyraminx', 'Skewb', 'Square-1', '4x4x4 Blindfolded', '5x5x5 Blindfolded', '3x3x3 Multi-Blind']

for i in range(1,len(registration)):
    wcaId = registration[i][wcaidcol]
    if wcaId != '':
        url = 'https://www.worldcubeassociation.org/persons/'+wcaId

        dfs = pd.read_html(url)

        tmp = list(dfs[1][dfs[1]['Event'] == '3x3x3 Cube']['Average'])
        if len(tmp) > 0:
            bestAverage3str = str(tmp[0])
        else:
            bestAverage3str = str(0)
        
        #print(bestAverage3str)
        bestAverage3 = 0
        tmp3 = 0
        if ':' in list(bestAverage3str):
            for j in range(len(bestAverage3str)):
                if bestAverage3str[j] != ':':
                    bestAverage3 *= 10
                    bestAverage3 += float(bestAverage3str[j])
                else:
                    tmp3 = j + 1
                    break
            bestAverage3 *= 60
        tmp4 = 0
        for j in range(tmp3, len(bestAverage3str)):
            if bestAverage3str[j] != '.':
                tmp4 *= 10
                tmp4 += float(bestAverage3str[j])
            else:
                tmp3 = j + 1
                break
        bestAverage3 += tmp4
        for j in range(tmp3, len(bestAverage3str)):
            bestAverage3 += float(bestAverage3str[j]) / pow(10, (j - tmp3 + 1))

        numOfComps = 0
        #print(dfs)
        dfnum = 0
        for j in range(0,len(dfs)):
            if 'Competition' in dfs[j].columns:
                dfnum = j
                break
        #print(dfnum)
        #print(dfs)
        #print(dfs[1])
        threshold = 5
        for j in range(len(dfs[dfnum])):
            if not pd.isnull(dfs[dfnum]['Competition'][j]) and not dfs[dfnum]['Competition'][j] in events:
                #print(dfs[dfnum]['Competition'][j])
                numOfComps += 1
            if numOfComps > threshold:
                break

        judgeability = False
        if numOfComps > threshold:
            judgeability = True
        print(wcaId, bestAverage3, judgeability)
        registration[i].append(bestAverage3)
        registration[i].append(numOfComps)
        registration[i].append(judgeability)
    else:
        registration[i].append(0)
        registration[i].append(0)
        registration[i].append(False)
        #print(i, wcaId, bestAverage3,numOfComps)

numOfGroups = 3
sortedRegistration = registration[1:]
sortedRegistration.sort(key=lambda x:x[28])
i = 0
while i < len(sortedRegistration):
    if sortedRegistration[i][28] == 0:
        f = False
        for j in range(len(sortedRegistration) - i):
            if sortedRegistration[i+j][28] != 0:
                f = True
                break
        if f == True:
            tmp = sortedRegistration[i]
            del sortedRegistration[i]
            sortedRegistration.append(tmp)
            i -= 1
    i += 1
for i in range(len(sortedRegistration)):
    print(sortedRegistration[i])

groupPeople = len(sortedRegistration) // numOfGroups
fraction = len(sortedRegistration) - groupPeople * numOfGroups
groupNum = []
for i in range(numOfGroups):
    if fraction != 0:
        groupNum.append(groupPeople + 1)
        fraction -= 1
    else:
        groupNum.append(groupPeople)

group = []
for i in range(numOfGroups):
    tmp = 0
    for j in range(len(group)):
        tmp += len(group[j])
    group.append(sortedRegistration[tmp:tmp + groupNum[i]])

print('')
for i in range(len(group)):
    for j in range(len(group[i])):
        print(group[i][j])
    print('')