This project can turn any tensorflow model into a tensorflow lite model 

To run the model_pipeline script (converts any tf model class .py into a .tflite file): 
script calling example: python3 model_pipeline.py --dir_name "model4" --model_name model --params "gravityX,gravityY,gravityZ"

Further data analysis is included on workout data. Several algorithms are as follows: 
1) A simple CNN is trained on the data. Input is a 92-length sequence of all the signals 
2) A probability distribution is generated from all the data points in an eye diagram for each signal. Each probability distribution is then used in a K-means clustering algorithm to determine type of excersize, and a final prediction is taken by popular vote of all the signals.

Several mathematical and visualization tools are included, including fourier transforms, eye diagrams, convolutions, and clustering. 
