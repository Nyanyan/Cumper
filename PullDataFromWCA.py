import pandas as pd
import csv
from selenium import webdriver

registration = []

with open('RegistrationExportedFromWCACompPage.csv', newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        registration.append(row)

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
            bestAverage3 = tmp[0]
        else:
            bestAverage3 = 0
        
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
        for j in range(len(dfs[dfnum])):
            if not pd.isnull(dfs[dfnum]['Competition'][j]) and not dfs[dfnum]['Competition'][j] in events:
                #print(dfs[dfnum]['Competition'][j])
                numOfComps += 1
        
        print(wcaId, bestAverage3,numOfComps)