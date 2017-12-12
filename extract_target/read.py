import pandas as pd

df = pd.read_csv('transactions.csv',index_col = 0)

def dict_process(x):
    D = eval(x)
    for key in D.keys():
        print(key)

df['opinion'].apply(dict_process)
df['target'].apply(dict_process)

