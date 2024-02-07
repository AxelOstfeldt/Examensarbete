import numpy as np

import cython



x = np.random.randint(0,100,10)

print(x)

def autocorrelation(x, lag):

    if lag >= len(x):
        raise ValueError(f"Lag must be shorter than array length")
    if not isinstance(lag, int) or lag < 0:
        raise ValueError(f"Lag must be an positive int")

    x_mean = np.mean(x)
    n = 0
    t = 0

        
    for i in range(len(x)):
        n += pow(x[i] - x_mean, 2)
        if i >= lag:
            t += (x[i] - x_mean) * (x[i-lag] - x_mean)

            

    return t/n


result = autocorrelation(x, 5)

print(result)

