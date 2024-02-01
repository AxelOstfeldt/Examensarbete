import math

m = 3
n = 3

q = math.floor(n/m)
r = n % m
c = math.ceil(math.log(m,2))

print("r = ", r)
b = pow(2,c) - m
print("b = ",b)

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

if (math.log(m,2)).is_integer() or r < pow(2,c) -m :
    encoded = encoded + bin(r)[2:]
else:
    encoded = encoded + "12345"

print((math.log(m,2)).is_integer())
print(encoded)