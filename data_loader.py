import os 
import pandas as pd 

path = 'data/'
bench, squat, deadlift = [], [], []
b, s, d = [], [], []
workouts = ['Bench', 'Squat', 'Deadlift']

for root, dirs, files in os.walk(path):
    for file in files:
        file_path = (os.path.join(root, file))
        path_lower = file_path.lower()
        print(root, dirs, file)
        l = bench if 'Bench' in root else (squat if 'Squat' in root else deadlift)
        if '.json' in file_path:
            df = pd.read_json(file_path)
            df['name'] = 'brian' if 'brian' in path_lower else ('neal' if 'neal' in path_lower else ('novel' if 'novel' in path_lower else 'tejas'))
            df['workout'] =  'bench' if 'Bench' in root else ('squat' if 'Squat' in root else 'deadlift')
 
            l.append(df)
            print(df['name'])
