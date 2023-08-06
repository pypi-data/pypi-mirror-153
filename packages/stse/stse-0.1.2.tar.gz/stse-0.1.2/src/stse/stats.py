import numpy as np
from statistics import mean, stdev


def z_norm(iter):
    iter = np.array(iter).astype(float)
    return (iter - mean(iter))/stdev(iter)
