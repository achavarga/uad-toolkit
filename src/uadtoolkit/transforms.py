
import numpy as np

def arcsin_sqrt(p):
    p = np.clip(p, 0.0, 1.0)
    return np.arcsin(np.sqrt(p))

def running_average(x):
    x = np.asarray(x, float)
    if x.size < 2: return x.copy()
    y = x.copy()
    y[0]  = (x[0] + 0.5*x[1]) / 1.5
    y[-1] = (x[-1] + 0.5*x[-2]) / 1.5
    if x.size > 2:
        y[1:-1] = (0.5*x[:-2] + x[1:-1] + 0.5*x[2:]) / 2.0
    return y
