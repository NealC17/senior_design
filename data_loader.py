import os 
import pandas as pd 

path = 'data/'
bench, squat, deadlift = [], [], []
b, s, d = [], [], []


for root, dirs, files in os.walk(path):
    for file in files:
        file_path = os.path.join(root, file)
        print(root, dirs, file)
        l = bench if 'Bench' in root else (squat if 'Squat' in root else deadlift)
        if '.json' in file_path:
            l.append(pd.read_json(file_path))

