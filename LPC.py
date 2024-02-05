import numpy as np

E = [1,2,3,4,5,6,7,8]

k_array = []

a = []

n = len(E) - 2

for i in range(n):

    for j in range(i-1):
        












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
s = np.array([1, 2, 3, 4, 5])
t = 0
i = 2

result = autocorrelation(s, t, i)
print(f"Autocorrelation at lag {i}: {result}")
