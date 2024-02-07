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


print(R)

order = 5

a = [0]

k = [0]

n = order+1

E = [R[0]]

for i in range(1, n):


    a_old = a
    k_temp = 0



    for j in range(i-1):
        k_temp = a[j] * R[i-j] + k_temp

    k_temp = ( R[i] - k_temp ) / E[i-1]


    k.append(k_temp)

    a.append(k[i])
    #print("i = ",i)
    if i > 1:
        for j in range (1, i):
            #print("j = ", j)
            a[j] = a_old[j] - k[i]*a_old[i-j]
        
        
    E.append((1 - pow(k[i],2)) * E[i-1])
    
    #print("loop #i: ", i)
    #print("k = ", k)
    #print("E = ", E)
    print("a = ", a)
    


prediction = [0] * (len(residuals))
diff = [0] * len(residuals)

#for i in range(4, len(residuals)):

    
    
    #pred = a[1] * residuals[i-1] + a[2] * residuals[i-2] + a[3] * residuals[i-3] + a[4] * residuals[i-4]

    #prediction[i] = int(pred)

for i in range(len(residuals)):
    diff[i] = residuals[i] - prediction[i]


#print("Original values: ", residuals)
#print("Predicted values: ", prediction)
#print("Residuals: ", diff)
        








