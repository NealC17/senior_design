import os 
import pandas as pd 

path = 'data/'
bench, squat, deadlift = [], [], []
b, s, d = [], [], []
workouts = ['bench', 'squat', 'deadlift']
names = ['brian', 'novel', 'tejas', 'neal']
counts = {e: {n: 0 for n in names} for e in workouts}

for root, dirs, files in os.walk(path):
    
    for file in files:
        file_path = (os.path.join(root, file))
        path_lower = file_path.lower()
        #print(root, dirs, file)
        l = bench if 'Bench' in root else (squat if 'Squat' in root else deadlift)
        if '.json' in file_path:
            df = pd.read_json(file_path)
            df['name'] = 'brian' if 'brian' in path_lower else ('neal' if 'neal' in path_lower else ('novel' if 'novel' in path_lower else 'tejas'))
            df['workout'] =  'bench' if 'Bench' in root else ('squat' if 'Squat' in root else 'deadlift')
            df['set_number'] = counts[df['workout'][0]][df['name'][0]]
            counts[df['workout'][0]][df['name'][0]] += 1
            l.append(df)
            print(df['name'][0], df['workout'][0], df['set_number'][0])
