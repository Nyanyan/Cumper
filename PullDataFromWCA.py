import pandas as pd

wcaId = str(input())
url = 'https://www.worldcubeassociation.org/persons/'+wcaId

#print(url)

numOfComps = 0
bestAverage3 = 0

dfs = pd.read_html(url)
bestAverage3 = dfs[1].at[0, 'Average']
print(bestAverage3)
