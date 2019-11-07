import pandas as pd
import csv
import pprint

registration = []

with open('RegistrationExportedFromWCACompPage.csv', newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        registration.append(row)

wcaidcol = 0
for i in range(len(registration[0])):
    if registration[0][i] == 'WCA ID':
        wcaidcol = i


for i in range(1,len(registration)):
    wcaId = registration[i][wcaidcol]
    if wcaId != '':
        url = 'https://www.worldcubeassociation.org/persons/'+wcaId
        numOfComps = 0
        bestAverage3 = 0

        dfs = pd.read_html(url)

        tmp = list(dfs[1][dfs[1]['Event'] == '3x3x3 Cube']['Average'])

        if len(tmp) > 0:
            bestAverage3 = tmp[0]
        else:
            bestAverage3 = 0

        print(wcaId, bestAverage3)