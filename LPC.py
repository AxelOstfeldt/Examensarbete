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



residuals = [1, 2, 3, 4, 5, 4, 3, 2, 1, 0, -1, -2, -3, -4, -5]

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
    


prediction = [0] * (len(residuals)-4)

for i in range(len(residuals)-4):
    print(i)
    
    
    #pred += 

    prediction[i] = int(pred)


print("Original values: ", residuals)
print("Predicted values: ", prediction)
        








