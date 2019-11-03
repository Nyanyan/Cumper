import pandas as pd

wcaId = str(input())
url = 'https://www.worldcubeassociation.org/persons/'+wcaId

numOfComps = 0
bestAverage3 = 0

dfs = pd.read_html(url)
print(dfs[1][['Average']].head())
print(len(dfs))