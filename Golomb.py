import math

m = 4
n = 4

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
    encoded = encoded + bin(r + pow(2,c) - m)[2:]
    print("hej")



Q = 0
B = pow(2,c) - m

if sign == True:
    if encoded[0] == "1":
        S = "1"
    else:
        S = "0"
    encoded = encoded[1:]

if (math.log(m,2)).is_integer() or R < pow(2,c) -m :
    print("hej")


else:
    encoded = encoded + bin(r + pow(2,c) - m)[2:]
    
    

