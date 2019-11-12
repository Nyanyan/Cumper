import pandas as pd
import csv
from selenium import webdriver

thisYear = 2019
birththreshold = 12
compthreshold = 3
judgeMargin = 1


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
        dfnum = 0
        for j in range(0,len(dfs)):
            if 'Competition' in dfs[j].columns:
                dfnum = j
                break
        for j in range(len(dfs[dfnum])):
            if not pd.isnull(dfs[dfnum]['Competition'][j]) and not dfs[dfnum]['Competition'][j] in events:
                #print(dfs[dfnum]['Competition'][j])
                numOfComps += 1
            if numOfComps > compthreshold:
                break

        birthstr = registration[i][5]
        birth = 0
        for j in range(len(birthstr)):
            if birthstr[j] == '/':
                break
            else:
                birth *= 10
                birth += int(birthstr[j])

        judgeability = False
        if numOfComps > compthreshold and thisYear - birth > birththreshold:
            judgeability = True

        print(wcaId, bestAverage3, judgeability)
        registration[i].append(bestAverage3)
        registration[i].append(numOfComps)
        registration[i].append(judgeability)
    else:
        registration[i].append(100000000000)
        registration[i].append(0)
        registration[i].append(False)


numOfGroups = 3
sortedRegistration = registration[1:]
sortedRegistration.sort(key=lambda x:x[28])
i = 0
'''
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
'''
'''
for i in range(len(sortedRegistration)):
    print(sortedRegistration[i])
'''
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
for i in range(numOfGroups):
    for j in range(len(group[i])):
        print(group[i][j])
    print('')
print('')

flag = True
while flag:
    judgecnt = []
    for i in range(numOfGroups):
        tmp = 0
        for j in range(numOfGroups):
            if i != j:
                for k in range(len(group[j])):
                    if group[j][k][len(group[j][k]) - 1] == True:
                        tmp += 1
        judgecnt.append(tmp)
    print(judgecnt)

    judgelack = []
    for i in range(numOfGroups):
        judgelack.append(len(group[i]) + judgeMargin - judgecnt[i])
    print(judgelack)

    flag = False
    flag2 = False
    for i in range(numOfGroups):
        if judgelack[i] < 0:
            flag2 = True
            break

    if flag2 == True:
        for i in range(numOfGroups):
            if judgelack[i] > 0:
                flag = True
                tmp1 = []
                tmp1index = 0
                for k in reversed(range(len(group[i]))):
                    if group[i][k][len(group[i][k]) - 1] == True:
                        tmp1 = group[i][k]
                        tmp1index = k
                if tmp1 == []:
                    tmp1 = group[i][0]
                for j in range(numOfGroups):
                    if i != j and judgelack[j] < 0:
                        tmp2 = []
                        tmp2index = 0
                        for k in reversed(range(len(group[j]))):
                            if group[j][k][len(group[j][k]) - 1] == False:
                                tmp2 = group[j][k]
                                tmp2index = k
                        if tmp2 == []:
                            tmp2 = group[j][0]
                        del group[i][tmp1index]
                        del group[j][tmp2index]
                        group[i].append(tmp2)
                        group[j].append(tmp1)
                        break

    print('')
    for i in range(numOfGroups):
        for j in range(len(group[i])):
            print(group[i][j])
        print('')