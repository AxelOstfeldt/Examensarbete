import numpy as np

x = [1,2,3,4,5]

def autocorrelation(x, lag):
    x_mean = np.mean(x)
    n = 0
    t = 0
    for i in range(lag, len(x)):
        t += (x[t] - x_mean) * (x[t-lag] - x_mean)
    for i in range(len(x)):
        n += pow(x[i] - x_mean, 2)
