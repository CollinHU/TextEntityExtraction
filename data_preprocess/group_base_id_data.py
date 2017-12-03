import pandas as pd
import csv

df = pd.read_csv('data/parsed_sent.csv',index_col = 0)

course_id_list = df['course_id'].unique()
print(len(course_id_list))

for id in course_id_list:
    course = df[df['course_id']==id]
#    print(len(course.index.values))
    course.to_csv('data/course/course_{}.csv'.format(id))
print('finished')
