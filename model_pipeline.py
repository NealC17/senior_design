import tensorflow as tf
import numpy as np 
import pandas as pd 
from data_loader import bench, squat, deadlift
from model import Model
import argparse
import importlib
from tqdm import tqdm
from time import time


#parameter handling
parser = argparse.ArgumentParser(description='model name')
parser.add_argument('--dir_name', required=True, help='directory name should be in models/ eg "models/model1", in quotes')
parser.add_argument('--model_name', required=True, help='model name eg if the class is "model.py" model_name should be "model", not in quotes')
parser.add_argument('--params', required=True, help="formatted parameters eg \"gravityX,gravityY,gravityZ\", in quotes")
args = parser.parse_args()

params = args.params.split(',')


#importing model
module = importlib.import_module(args.model_name)
cls = getattr(module, "Model")
model = cls()

#generating input for model and model itself
dummy_input = model.preprocessing((bench[1][params]).dropna().to_numpy())
inp = dummy_input[0]
output = model(inp)

#msaving model
saved_model_dir = f"models/{args.dir_name}"
tf.saved_model.save(model, saved_model_dir)
converter = tf.lite.TFLiteConverter.from_saved_model(saved_model_dir)
tflite_model = converter.convert()


#opening tflite model
with open("rep_count_model.tflite", "wb") as f:
    f.write(tflite_model)

#settings for tflite
interpreter = tf.lite.Interpreter(model_path="rep_count_model.tflite")
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

print("Input details:", input_details)
print("Output details:", output_details)

#output of tflite model
interpreter.set_tensor(input_details[0]['index'], dummy_input[0])
interpreter.invoke()
output_data = interpreter.get_tensor(output_details[0]['index'])
print("Model output:", output_data)


#speed test:
start = time()
for e in dummy_input:
    interpreter.set_tensor(input_details[0]['index'], e)
    interpreter.invoke()
    output_data = interpreter.get_tensor(output_details[0]['index'])
    print("Model output:", output_data)
end = time()
print(f"total time for one example: {end - start}")



