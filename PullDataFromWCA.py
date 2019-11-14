import pandas as pd
import csv
from selenium import webdriver

thisYear = 2019
birththreshold = 12
compthreshold = 5
judgeMargin = 1
country = 'Japan'
countryindex = 3
birthindex = 5
numOfGroups = [8, 4, 4, 4, 4, 4, 4, 2, 4, 2, 2, 2, 4, 4, 4, 2, 2, 1]
events = ['3x3x3 Cube', '2x2x2 Cube', '4x4x4 Cube', '5x5x5 Cube', '6x6x6 Cube', '7x7x7 Cube', '3x3x3 Blindfolded', '3x3x3 Fewest Moves', '3x3x3 One-Handed', '3x3x3 With Feet', 'Clock', 'Megaminx', 'Pyraminx', 'Skewb', 'Square-1', '4x4x4 Blindfolded', '5x5x5 Blindfolded', '3x3x3 Multi-Blind']


registration = []

with open('RegistrationExportedFromWCACompPage.csv', newline='', encoding='utf-8') as f:
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


eventindex = []
for i in events:
    for j in range(len(registration[0])):
        if registration[0][j] == i:
            eventindex.append(j)




for i in range(1,len(registration)):
    wcaId = registration[i][wcaidcol]
    if wcaId != '':
        url = 'https://www.worldcubeassociation.org/persons/'+wcaId

        dfs = pd.read_html(url)

        numOfComps = 0
        dfnum = 0
        for j in range(0,len(dfs)):
            if 'Competition' in dfs[j].columns:
                dfnum = j
                break
        for j in range(len(dfs[dfnum])):
            if not pd.isnull(dfs[dfnum]['Competition'][j]) and not dfs[dfnum]['Competition'][j] in events:
                numOfComps += 1
            if numOfComps > compthreshold:
                break

        birthstr = registration[i][birthindex]
        birth = 0
        for j in range(len(birthstr)):
            if birthstr[j] == '/':
                break
            else:
                birth *= 10
                birth += int(birthstr[j])

        judgeability = False
        if numOfComps > compthreshold and thisYear - birth > birththreshold and registration[i][countryindex] == 'Japan':
            judgeability = True
        
        print(wcaId, judgeability)

        registration[i].append(judgeability)
    else:
        registration[i].append(False)

judgeabilityindex = len(registration[1])

timeindex = len(registration[1])


#print(registration)


for eventnum in range(len(events)):
    print('\n\n')
    print(events[eventnum])
    eventregistration = []
    eventTF = 0
    for i in range(len(registration[0])):
        if registration[0][i] == events[eventnum]:
            eventTF = i
            break
    #print(eventTF)
    
    for i in range(1,len(registration)):
        if int(registration[i][eventTF]) == 1:
            eventregistration.append(registration[i])
    for i in range(1,len(eventregistration)):
        wcaId = eventregistration[i][wcaidcol]
        if wcaId != '':
            url = 'https://www.worldcubeassociation.org/persons/'+wcaId

            dfs = pd.read_html(url)

            tmp = list(dfs[1][dfs[1]['Event'] == events[eventnum]]['Average'])
            if len(tmp) > 0 and not pd.isnull(tmp[0]):
                bestAveragestr = str(tmp[0])
            else:
                bestAveragestr = str(1000000000)
            
            #print(bestAveragestr)

            bestAverage = 0
            tmp3 = 0
            if ':' in list(bestAveragestr):
                for j in range(len(bestAveragestr)):
                    if bestAveragestr[j] != ':':
                        bestAverage *= 10
                        bestAverage += float(bestAveragestr[j])
                    else:
                        tmp3 = j + 1
                        break
                bestAverage *= 60
            tmp4 = 0
            for j in range(tmp3, len(bestAveragestr)):
                if bestAveragestr[j] != '.':
                    tmp4 *= 10
                    tmp4 += float(bestAveragestr[j])
                else:
                    tmp3 = j + 1
                    break
            bestAverage += tmp4
            for j in range(tmp3, len(bestAveragestr)):
                bestAverage += float(bestAveragestr[j]) / pow(10, (j - tmp3 + 1))
            bestAverage = round(bestAverage, 2)

            print(wcaId, bestAverage)

            eventregistration[i].append(bestAverage)
        else:
            eventregistration[i].append(100000000000)

    sortedRegistration = eventregistration[1:]
    sortedRegistration.sort(key=lambda x:x[timeindex])
    i = 0


    groupPeople = len(sortedRegistration) // numOfGroups[eventnum]
    fraction = len(sortedRegistration) - groupPeople * numOfGroups[eventnum]
    groupNum = []
    for i in range(numOfGroups[eventnum]):
        if fraction != 0:
            groupNum.append(groupPeople + 1)
            fraction -= 1
        else:
            groupNum.append(groupPeople)

    group = []
    for i in range(numOfGroups[eventnum]):
        tmp = 0
        for j in range(len(group)):
            tmp += len(group[j])
        group.append(sortedRegistration[tmp:tmp + groupNum[i]])

    '''
    print('')
    for i in range(numOfGroups):
        for j in range(len(group[i])):
            print(group[i][j])
        print('')
    print('')
    '''

    flag = True
    while flag:
        judgecnt = []
        for i in range(numOfGroups[eventnum]):
            tmp = 0
            for j in range(numOfGroups[eventnum]):
                if i != j:
                    for k in range(len(group[j])):
                        if group[j][k][judgeabilityindex] == True:
                            tmp += 1
            judgecnt.append(tmp)
        print(judgecnt)

        judgelack = []
        for i in range(numOfGroups[eventnum]):
            judgelack.append(len(group[i]) + judgeMargin - judgecnt[i])
        print(judgelack)

        flag = False
        flag2 = False
        for i in range(numOfGroups[eventnum]):
            if judgelack[i] < 0:
                flag2 = True
                break

        if flag2 == True:
            for i in range(numOfGroups[eventnum]):
                if judgelack[i] > 0:
                    flag = True
                    tmp1 = []
                    tmp1index = 0
                    for k in reversed(range(len(group[i]))):
                        if group[i][k][judgeabilityindex] == True:
                            tmp1 = group[i][k]
                            tmp1index = k
                    if tmp1 == []:
                        tmp1 = group[i][0]
                    for j in range(numOfGroups[eventnum]):
                        if i != j and judgelack[j] < 0:
                            tmp2 = []
                            tmp2index = 0
                            for k in reversed(range(len(group[j]))):
                                if group[j][k][judgeabilityindex] == False:
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
        for i in range(numOfGroups[eventnum]):
            for j in range(len(group[i])):
                print(group[i][j])
            print('')