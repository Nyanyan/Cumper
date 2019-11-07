import pandas as pd
import csv

registration = []

with open('RegistrationExportedFromWCACompPage.csv', newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        registration.append(row)

wcaidcol = 0
for i in range(len(registration[0])):
    if registration[0][i] == 'WCA ID':
        wcaidcol = i

events = ['3x3x3 Cube', '2x2x2 Cube', '4x4x4 Cube', 'Pyraminx', 'Skewb']

for i in range(1,len(registration)):
    wcaId = '2016SIGG01'#registration[i][wcaidcol]
    if wcaId != '':
        url = 'https://www.worldcubeassociation.org/persons/'+wcaId

        dfs = pd.read_html(url)

        tmp = list(dfs[1][dfs[1]['Event'] == '3x3x3 Cube']['Average'])

        if len(tmp) > 0:
            bestAverage3 = tmp[0]
        else:
            bestAverage3 = 0
        
        numOfsolves = 0
        print(dfs[2])
        solves = ['Solves','Solves.1','Solves.2','Solves.3','Solves.4']
        for i in solves:
            a = list((dfs[2][i] == '') | (dfs[2][i].isin(events)))
            b = 0
            for j in range(len(a)):
                if a[j]:
                    b += 1
            numOfsolves += len(a) - b

        print(wcaId, bestAverage3,numOfsolves)