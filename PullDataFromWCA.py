import pandas as pd

wcaId = str(input())
url = 'https://www.worldcubeassociation.org/persons/'+wcaId

#print(url)

numOfComps = 0
bestAverage3 = 0

dfs = pd.read_html(url)

tmp = list(dfs[1][dfs[1]['Event'] == '3x3x3 Cube']['Average'])

if len(tmp) > 0:
    bestAverage3 = tmp[0]
else:
    bestAverage3 = 0

print(bestAverage3)