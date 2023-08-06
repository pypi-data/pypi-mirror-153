
import numpy as _np

def load_ex4_data():
    data = _np.load("kmeansdata.npz")
    return data['X'], data['y']
