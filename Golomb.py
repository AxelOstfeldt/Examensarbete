import math
import numpy as np



def Golomb_encode(n, m, sign):


    q = math.floor(n/m)
    r = n % m
    c = math.ceil(math.log(m,2))
    b = pow(2,c) - m

    encoded = bin(0)[2:]

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
    elif r < b:
        encoded = encoded + np.binary_repr(r, width = c-1)
    else:
        encoded = encoded + np.binary_repr(r+b, width = c)

    if sign == True:
        encoded = s + encoded

    return encoded



def Golomb_decode(code, m, sign):

    c = math.ceil(math.log(m,2))
    b = pow(2,c) - m
    A = 0

    if sign == True:
        if code[0] == "1":
            ss = "1"
        code = code[1:]

    while code[0] == "1":
        A += 1
        code = code[1:]
    code = code[1:]

    

    if (math.log(m,2)).is_integer():
        decoded = m * A + int(encoded, 2)
    else:
        R = int(code[:c-1],2)
        if R < b:
            decoded = m * A + int(code, 2)
        else:
            decoded = m * A + int(code, 2) - b




    if sign == True and ss == "1":
        decoded = -decoded

    return decoded



kodOrd = Golomb_encode(5, 7, False)

print("kod ord: ",kodOrd)

value = Golomb_decode(kodOrd, 7, False)

print("Value: ", value)
        
        
