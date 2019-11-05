import pandas as pd

wcaId = str(input())
url = 'https://www.worldcubeassociation.org/persons/'+wcaId

print(url)

numOfComps = 0
bestAverage3 = 0

dfs = pd.read_html(url)
print(dfs[1])
print(dfs[1][['Average']].head())


'''
df2 = pd.DataFrame(data=dfs[1], index=['3x3x3 Cube'], columns=['Average'])
print(df2)
bestAverage3 = df2.loc['3x3x3 Cube']['Average']
print(bestAverage3)
'''
'''
df = dfs[1][['Average']].head()
df.head()
'''
print(dfs[dfs.Event == '3x3x3 Cube'])