import pandas as pd
import os

path = 'data_folder/'
names = ['brian', 'neal', 'novel', 'tejas']
workouts = ['bench', 'squat', 'deadlift']
c = 0
dfs = []
for root, dirs, files in os.walk(path):
    for file in files:

        if '.json' in file and '-checkpoint' not in file:
            file_lower = file.lower()
            s = file_lower.split("_")
            #person, workout, weight = 
            print(s)
            
            df = pd.read_json(path + file)
            df['name'], df['workout'], df['weight'] = s[0], s[1], str(s[2])
            df['num'] = str(c)
            c+=1

            dfs.append(df)


combined_df = pd.concat(dfs, ignore_index=False)
combined_df.set_index(['name', 'workout', 'weight', 'num'], inplace=True)

def get_list(name):
    temp = combined_df.loc[slice(None), name, slice(None), slice(None)]
    nums = list(set(temp.index.get_level_values('num').tolist()))
    temp = [(temp.loc[slice(None), slice(None), str(i)]) for i in nums]
    return temp


bench = get_list('bench')
squat = get_list('squat')
deadlift = get_list('deadlift')

