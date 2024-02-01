import math
import numpy as np

n = 7
m = 11

print("n: ", n)
q = math.floor(n/m)
r = n % m
c = math.ceil(math.log(m,2))



b = pow(2,c) - m


encoded = bin(0)[2:]

sign = False

if sign:
    if n < 0:
        s = "1"
        n = -n
    else:
        s = "0"
        

for i in range(q):
    encoded = "1" + encoded
    print("for loop: ", encoded)


if (math.log(m,2)).is_integer():
    encoded = encoded + np.binary_repr(r, width = c)
elif r < b:
    encoded = encoded + np.binary_repr(r, width = c-1)
else:
    encoded = encoded + np.binary_repr(r+b, width = c)

if sign == True:
    encoded = s + encoded


print("encoded: ", encoded)



qq = 0
bb = pow(2,c) - m
aa = 0
decoded = 0
#c = math.ceil(math.log(m,2)) for the function later
#m = 7 for the function later

sign = False

if sign == True:
    if encoded[0] == "1":
        ss = "1"
    encoded = encoded[1:]

while encoded[0] == "1":
    aa += 1
    encoded = encoded[1:]

encoded = encoded[1:]

#if (math.log(m,2)).is_integer():
#    decoded = m * aa + int(encoded, 2)
#elif len(encoded) == c-1:
#    decoded = m * aa + int(encoded, 2)
#else:
#    decoded = m * aa + int(encoded, 2) - bb

R = int(encoded[:c-1],2)

if (math.log(m,2)).is_integer():
    decoded = m * aa + int(encoded, 2)
elif R < bb:
    decoded = m * aa + int(encoded, 2)
else:
    decoded = m * aa + int(encoded, 2) - bb




if sign == True and ss == "1":
    decoded = -decoded


print("Decoded: ", decoded)

    
    

