import numpy as np



residuals = [1, 2, 20, 2, 5, 20, 100, 60, 70, 44, 20]

R =[]

for t in range (residuals):
    R.append()


R = [10,20,30,40,50]





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
    
    print("loop #i: ", i)
    print("k = ", k)
    print("E = ", E)
    print("a = ", a)
    













def autocorrelation(s, t, i):
    """
    Calculate autocorrelation Rs(i) = E[s(t) * s(t + i)]

    Parameters:
    - s: numpy array, input sequence
    - t: int, starting index
    - i: int, lag

    Returns:
    - Autocorrelation at lag i
    """
    n = len(s)
    
    # Check if the given indices are within the valid range
    if t < 0 or t >= n or (t + i) < 0 or (t + i) >= n:
        raise ValueError("Invalid indices for the given sequence")

    # Calculate the autocorrelation
    Rs_i = np.mean(s[t:] * s[t + i:])

    return Rs_i

# Example usage:
#s = np.array([1, 2, 3, 4, 5])
#t = 0
#i = 2

#result = autocorrelation(s, t, i)
#print(f"Autocorrelation at lag {i}: {result}")
