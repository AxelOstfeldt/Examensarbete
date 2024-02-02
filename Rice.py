import numpy as np
import math

class RiceCoding:

    def __init__(self, k, sign):
        self.k = k
        self.sign = sign

    def Encode(self, n):

        if self.sign:
            if n < 0:
                s = "1"
                n = -n
            else:
                s = "0"
        if math.log(n,2) < self.k:
            r = np.binary_repr(n,self.k)
            loop = 0
        else:
            n = bin(n)[2:]
            r = n[len(n)-self.k:]
            loop = int(n[:len(n)-self.k],2)
           
        r = "0" + r

        for i in range(loop):
            r = "1" + r

        if self.sign:
            r = s + r

        return r
    
    def Decode(self, code):
        
        A = 0
        S = False
        if self.sign:
            if code[0] == "1":
                S = True
            code = code[1:]
        
        while code[0] == "1":
            A += 1
            code = code[1:]
        
        code = bin(A)[2:] + code[1:]

        code = int(code, 2)

        if self.sign and S:
            code = -code

        return code
    


#Test
    
sign = True
n = -7
k = 2

Rice_coder = RiceCoding(k, sign)

kodOrd = Rice_coder.Encode(n)

print("kod ord: ",kodOrd)

value = Rice_coder.Decode(kodOrd)

print("Value: ", value)