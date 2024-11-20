import os 
import pandas as pd 

path = 'data/'
bench, squat, deadlift = [], [], []
b, s, d = [], [], []
workouts = ['bench', 'squat', 'deadlift']
names = ['brian', 'novel', 'tejas', 'neal']
counts = {e: {n: 0 for n in names} for e in workouts}
big = {n : {w: {} for w in workouts} for n in names}
for root, dirs, files in os.walk(path):
    for file in files:
        file_path = os.path.join(root, file)
        path_lower = file_path.lower()
        l = bench if 'Bench' in root else (squat if 'Squat' in root else deadlift)
        
        if '.json' in file_path:
            df = pd.read_json(file_path)
            name = 'brian' if 'brian' in path_lower else ('neal' if 'neal' in path_lower else ('novel' if 'novel' in path_lower else 'tejas'))
            workout = 'bench' if 'Bench' in root else ('squat' if 'Squat' in root else 'deadlift')
            
            # Get the next set_number for this person-workout
            set_num = counts[workout][name]
            counts[workout][name] += 1  # Increment for the next file
            
            df['name'] = name
            df['workout'] = workout
            df['set_number'] = set_num  # Apply this as a constant for the entire DataFrame

            big[name][workout][set_num] = df
            
            print(name, workout, set_num)
            l.append(df)


print(counts)
data_frames = []

for name, workouts in big.items():
    for workout, sets in workouts.items():
        for set_num, df in sets.items():
            # Flatten any nested columns, if present
            for col in df.columns:
                # If any column contains a list/Series, expand it (as an example)
                if df[col].apply(lambda x: isinstance(x, (list, pd.Series))).any():
                    df = df.explode(col)  # Expand lists/Series into rows

            # Ensure 'name', 'workout', and 'set_number' columns are added
            df['name'] = name
            df['workout'] = workout
            df['set_number'] = set_num
            data_frames.append(df)

# Concatenate all DataFrames into one and set the multi-level index
result_df = pd.concat(data_frames, ignore_index=True)
result_df.set_index(['name', 'workout', 'set_number'], inplace=True)

# Display the resulting DataFrame
print(result_df)
