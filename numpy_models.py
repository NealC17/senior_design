import numpy as np
import pandas as pd 
import tensorflow as tf 




#INPUT: one of gravityX, gravityY, gravityZ
def count_reps(count):
    count = count.dropna()
    count = count.to_numpy()
    count -= np.mean(count)
    t = (np.where(count > 0, 0, 1))
    b = t[1:] - t[:-1]
    return np.sum(b[b==1])


#INPUT: tensor of [gravityX, gravityY, gravityZ]
def count_reps_2(tens):
    tens -= np.mean(tens, axis=0)
    t = (np.where(tens > 0, 0, 1))
    b = t[1:] - t[:-1]
    b = b[np.any(b, 1)]
    b[b==-1] = 0
    return np.sum(b, axis=0)

#same input as above
def get_periodic(tens):
    pass

