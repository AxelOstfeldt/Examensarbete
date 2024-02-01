import math

m = 2
n = 4

q = math.floor(n/m)
r = n % m
c = math.ceil(math.log(m,2))

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

if r > pow(2,c) - m:
    encoded = encoded + bin(r)[2:]

