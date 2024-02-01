import math
import numpy as np

class GolombCoding:

    def __init__(self, m, sign):
        self.m = m
        self.sign = sign

    def Golomb_encode(self, n):


        q = math.floor(n/ self.m)
        r = n % self.m
        cc = math.log(self.m,2)
        c = math.ceil(cc)
        b = pow(2,c) - self.m

        encoded = bin(0)[2:]

        if self.sign == True:
            if n < 0:
                s = "1"
                n = -n
            else:
                s = "0"
                

        for i in range(q):
            encoded = "1" + encoded

        if cc.is_integer():
            encoded = encoded + np.binary_repr(r, width = c)
        elif r < b:
            encoded = encoded + np.binary_repr(r, width = c-1)
        else:
            encoded = encoded + np.binary_repr(r+b, width = c)

        if self.sign == True:
            encoded = s + encoded

        return encoded



    def Golomb_decode(self, code):

        cc = math.log(self.m,2)
        c = math.ceil(cc)
        b = pow(2,c) - self.m
        A = 0

        if self.sign == True:
            if code[0] == "1":
                ss = "1"
            code = code[1:]

        while code[0] == "1":
            A += 1
            code = code[1:]
        code = code[1:]

        

        if (cc).is_integer():
            decoded = self.m * A + int(code, 2)
        else:
            R = int(code[:c-1],2)
            if R < b:
                decoded = self.m * A + int(code, 2)
            else:
                decoded = self.m * A + int(code, 2) - b




        if self.sign == True and ss == "1":
            decoded = -decoded

        return decoded


Golomb_coder = GolombCoding(7, False)

kodOrd = Golomb_coder.Golomb_encode(5)

print("kod ord: ",kodOrd)

value = Golomb_coder.Golomb_decode(kodOrd)

print("Value: ", value)
        
        
