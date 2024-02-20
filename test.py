import numpy as np
import statsmodels.tsa.api as smt
import random




#LPC testing 
if 1 < 0:
    order = 3
    for i in range(order):
        print("i = ",i)
        if i > 0:
            for j in range(i):
                print("j = ", j)
                print("i-j = ", i-j-1)


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

max_val = 8
test_array = []

for i in range(max_val):
    test_array.append(random.randint(-10,10))
    
#test autocorre functions
if 1 > 0:
    test_array = [1,2,3,4,5]

    test_lag = 5

    print("Lag = ", test_lag)
    print("Array = ", test_array)


    acf_f = autocorrelation(test_array, test_lag)

    acf_i = smt.acf(test_array)[:4]

    print("My function for autocorrelation: ", acf_f)
    print("Result from imported autocorrelation: ", acf_i)