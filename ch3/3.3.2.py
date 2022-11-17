import pandas as pd

kospi = pd.Series([1915, 1961, 2026, 2467, 2041],
                  index=[2014, 2015, 2016, 2017, 2018],
                  name='KOSPI')
print((kospi))