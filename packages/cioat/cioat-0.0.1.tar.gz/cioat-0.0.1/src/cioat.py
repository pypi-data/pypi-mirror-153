import subprocess as sp
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import openpyxl
import sys,os

sp.call("wget https://github.com/jiaoyang-x/covidT/blob/main/covid_impact_on_airport_traffic.csv",shell=True)
df = pd.read_csv("covid_impact_on_airport_traffic.csv")


df = df.dropna()
df['Date'] = pd.to_datetime(df['Date'])
d_of_col = {i: i.lower() for i in df.columns}

df.rename(columns=d_of_col, inplace=True)
percentofbaseline_by_date = df.groupby('date', as_index=False).agg({'percentofbaseline': 'mean'})
fig, ax = plt.subplots(1,1, figsize=(15,8))
ax = sns.lineplot(x='date', y='percentofbaseline', data=percentofbaseline_by_date)
ax.set_ylabel('Percent of baseline')
ax.set_xlabel('Date')
ax.set_title('Percent of baseline by date')
sns.despine()

def main():
 plt.legend()
 plt.savefig('result.png')
 plt.show()

if __name__ == "__main__":
    main()
