import pandas as pd

s_list = pd.read_csv('data.csv')

size = int(s_list.count().values[0])
print type(size)
count = 0
for i in xrange(size):
    
    if i == 10:
        print s_list.iloc[i,1]
    count += 1
print count
