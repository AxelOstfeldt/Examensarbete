import math
import numpy as np

n = 5
m = 7

print("n: ", n)
q = math.floor(n/m)
r = n % m
c = math.ceil(math.log(m,2))

print(c)


b = pow(2,c) - m


encoded = bin(0)[2:]

sign = False

if sign == True:
    if n < 0:
        s = "1"
        n = -n
    else:
        s = "0"
        

for i in range(q):
    encoded = "1" + encoded


if (math.log(m,2)).is_integer():
    encoded = encoded + np.binary_repr(r, width = c)
elif r >= pow(2,c) -m:
    encoded = encoded + np.binary_repr(r+pow(2,c)-m, width = c)
else:
    encoded = encoded + np.binary_repr(r, width = c-1)

print("encoded: ", encoded)

R= 7

Q = 0
B = pow(2,c) - m
A = 0
decoded = 0
#c = math.ceil(math.log(m,2)) for the function later
#m = 7 for the function later

sign = False

if sign == True:
    if encoded[0] == "1":
        S = "1"
    encoded = encoded[1:]

while encoded[0] == "1":
    A += 1
    encoded = encoded[1:]

encoded = encoded[1:]

if (math.log(m,2)).is_integer():
    decoded = m * A + int(encoded)

elif len(encoded) == c:
    decoded = m * A + int(encoded)
else:
    decoded = m * A + int(encoded) - B

print(A)

print("Decoded: ", decoded)

    
    

