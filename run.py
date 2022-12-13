def trim(df, col):
    df[col] = df[col].apply(lambda x: x[-4:])
    return df

import pandas as pd
df = pd.read_csv("ethplorer.csv", sep=";")
df = df.replace(',','.', regex=True)
df = df.replace('',0, regex=True)
### format ###
df["date"] = pd.to_datetime(df["date"]) +  pd.DateOffset(hours=8)
df["value"] = pd.to_numeric(df["value"])
df["usdPrice"] = pd.to_numeric(df["usdPrice"])
df["ans"] = df[["value"]].multiply(df["usdPrice"], axis="index")

df_na = df[ df['usdPrice'].isna() ]
print(df.shape)
df = df[ df['usdPrice'].notna() ] # 拿掉沒有美金計價的


print(df.shape)
### filter range ###
df = df[ (df["date"]>"2022-11-1 00:00:00") & (df["date"]<"2022-12-1 00:00:00") ]
df = trim(df, "fromAddress")
df = trim(df, "toAddress")
df = df[["date", "fromAddress", "toAddress", "tokenName", "value", "usdPrice", "ans"]]
df.to_csv("out.csv")

import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt


graph = nx.from_pandas_edgelist(df, source = 'fromAddress', target = 'toAddress',
    edge_attr = 'ans',create_using = nx.DiGraph())
    
plt.figure(figsize = (10,9))
nx.draw_networkx(graph)
lookup = ["8d16", "fd45", "0e2a", "f07c"]
for l in lookup:
    print(df[ df["toAddress"]==l ])