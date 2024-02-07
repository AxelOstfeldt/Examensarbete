import numpy as np

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



residuals = [1, 2, 20, 2, 5, 20, 100, 60, 70, 44, 20]

R =[]

for t in range(len(residuals)):
    R.append(autocorrelation(residuals,t))




order = 5

a = [0] * order

k = [0] * order

E = [0] * order

n = order

E[0] = R[0]

for i in range(1, n):


    a_old = a

    for j in range(i-1):
        k[i] = a[j] * R[i-j] + k[i]

    k[i] = ( R[i] - k[i] ) / E[i-1]

    a[i] = k[i]

    if i > 0:
        for j in range (1, i-1):
            a[j] = a_old[j] - k[i]*a_old[i-j]
        
    E[i] = (1 - pow(k[i],2) ) * E[i-1]
    
    #print("loop #i: ", i)
    #print("k = ", k)
    #print("E = ", E)
    print("a = ", a)
    

    for i in range 
    predict = a[]











