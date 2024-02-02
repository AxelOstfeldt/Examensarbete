import math
import numpy as np

class GolombCoding:

    def __init__(self, m, sign):
        self.m = m
        self.sign = sign

    def Encode(self, n):

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

        q = math.floor(n/ self.m)
        r = n % self.m
        
                

        for i in range(q):
            encoded = "1" + encoded

        if len(encoded) != q+1:
            raise ValueError(f"Unary code size does not match q value. Current values are: encoded = {encoded}, q = {q}")

        if cc.is_integer():
            encoded = encoded + np.binary_repr(r, width = c)
        elif r < b:
            encoded = encoded + np.binary_repr(r, width = c-1)
        else:
            encoded = encoded + np.binary_repr(r+b, width = c)

        

        if self.sign == True:
            encoded = s + encoded

        return encoded



    def Decode(self, code):

        cc = math.log(self.m,2)
        c = math.ceil(cc)
        b = pow(2,c) - self.m
        A = 0
        S = "0"
        LengthCheck = len(code)
        

        if self.sign == True:
            if code[0] == "1":
                S = "1"
            code = code[1:]

        while code[0] == "1":
            A += 1
            code = code[1:]
        code = code[1:]

        

        if (cc).is_integer():
            if len(code) != c:
                raise ValueError(f"Size error, length of code remaining should match c. Current values are: code = {code}, c = {c}")
            decoded = self.m * A + int(code, 2)
            print("Case 1")
        else:
            R = int(code[:c-1],2)
            if R < b:
                if len(code) != c-1:
                    raise ValueError(f"Size error. code = {code}, should have length: {c-1}")
                decoded = self.m * A + int(code, 2)
                print("Case 2")
            else:
                if len(code) != c:
                    raise ValueError(f"Size error. code = {code}, should have length: {c}")
                decoded = self.m * A + int(code, 2) - b
                print("Case 3")

        


        if self.sign and S == "1":
            decoded = -decoded
            if ((cc).is_integer() or R >= b) and LengthCheck != A+c+2:
                raise ValueError(f"Size error. Input code length, {LengthCheck}, should be equal to A+c+2 = {A+c+2}")
            elif LengthCheck != A+c+1:
                raise ValueError(f"Size error. Input code length, {LengthCheck}, should be equal to A+c+2 = {A+c+1}")
        else:
            if ((cc).is_integer() or R >= b) and LengthCheck != A+c+1:
                raise ValueError(f"Size error. Input code length, {LengthCheck}, should be equal to A+c+2 = {A+c+1}")
            elif LengthCheck != A+c:
                raise ValueError(f"Size error. Input code length, {LengthCheck}, should be equal to A+c+2 = {A+c}")


        return decoded


sign = True
n = -10
m = 7

Golomb_coder = GolombCoding(m, sign)

kodOrd = Golomb_coder.Encode(n)

print("kod ord: ",kodOrd)

value = Golomb_coder.Decode(kodOrd)

print("Value: ", value)
        
        
