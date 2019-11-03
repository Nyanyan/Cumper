import pandas as pd

wcaId = str(input())
url = 'https://www.worldcubeassociation.org/persons/'+wcaId

numOfComps = 0
bestAverage3 = 0

df = pd.read_html(url)
print(df[1])
print(df[1][['Average']].head())

df2 = pd.DataFrame(data=df[1], index=['3x3x3 Cube'], columns=['Average'])
print(df2)
bestAverage3 = df2.loc['3x3x3 Cube']['Average']
print(bestAverage3)