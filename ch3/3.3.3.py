import pandas as pd

columns = ['KOSPI', 'KOSDAQ']
index = [2014, 2015]
rows = []
rows.append([1915, 542])
rows.append([1961, 682])
df = pd.DataFrame(rows, columns=columns, index=index)
# print(df)

for i in df.index:
    print(i, df['KOSPI'][i], df['KOSDAQ'][i])