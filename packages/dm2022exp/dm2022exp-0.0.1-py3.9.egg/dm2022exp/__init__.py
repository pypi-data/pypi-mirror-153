import os
import numpy as _np

def load_ex4_data():
    print(os.getcwd())
    data = _np.load("./kmeansdata.npz")
    return data['X'], data['y']
