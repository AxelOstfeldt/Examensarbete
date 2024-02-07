import math
import numpy as np

class GolombCoding:

    #m is a constant that affects the length of the code word.
    #For larger residuals m should be larger.
    #m have to be an int
    #sign is True if the input data can be signed

    def __init__(self, m, sign):
        self.m = m
        self.sign = sign

    def Encode(self, n):


        
        cc = math.log(self.m,2)
        c = math.ceil(cc)
        b = pow(2,c) - self.m

        #encoded is started with a binary "0".
        #This is to be able to add the unary coded 1's on the left side
        #and the bianry coded remainder on the right side
        encoded = bin(0)[2:]

        #Checks if the input data is signed in order to save a signed bit
        if self.sign == True:
            if n < 0:
                s = "1"
                #in cases where the input data is negative it is converted to positive before encoded.
                #The sign bit is saved as a "1" beffore to remember that the value should be negative
                n = -n
                
            else:
                s = "0"

        #q is caled the quotient
        #this value will be unary coded in "1's" followed by a 0
        #r is called the remainder
        #this value will be binary coded.
        #in some cases the binary coding will differ (More bellow)
        q = math.floor(n/ self.m)
        r = n % self.m
        
        
                
        #Unary codes the quotient.
        #The int value q is represented in a number of "1's" followed by a 0
        #this is achived by assining a 1 as the MSB to encoded for every iteation of the loop
        #with length q
        for i in range(q):
            encoded = "1" + encoded

        #checks that the encoded length is correct
        if len(encoded) != q+1:
            raise ValueError(f"Unary code size does not match q value. Current values are: encoded = {encoded}, q = {q}")


        #There are three differente cases for how r can be encoded:

        #Case 1. if cc is an interger that means that m is a power of 2.
        #in this case r can be encoded in binary in c bits
        if cc.is_integer():
            encoded = encoded + np.binary_repr(r, width = c)
        #Case 2. if r is less than c² - m it can be encoded in binary using c-1 bits
        elif r < b:
            encoded = encoded + np.binary_repr(r, width = c-1)
        #Case 3. if r is larger or equal to c² - m it will be encoded so that the largest residual
        #is encoded in all "1" with length c, for example if c = 2 then the largest residual will be "11".
        # 
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

        
        R = int(code[:c-1],2)

        if (cc).is_integer():
            if len(code) != c:
                raise ValueError(f"Size error, length of code remaining should match c. Current values are: code = {code}, c = {c}")
            decoded = self.m * A + int(code, 2)
            print("Case 1")
        else:
            
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
            elif (R < b) and LengthCheck != A+c+1:
                raise ValueError(f"Size error. Input code length, {LengthCheck}, should be equal to A+c+1 = {A+c+1}")
        else:
            if ((cc).is_integer() or R >= b) and LengthCheck != A+c+1:
                raise ValueError(f"Size error. Input code length, {LengthCheck}, should be equal to A+c+1 = {A+c+1}")
            elif (R < b) and LengthCheck != A+c:
                raise ValueError(f"Size error. Input code length, {LengthCheck}, should be equal to A+c = {A+c}")


        return decoded


sign = True
n = -7
m = 8

Golomb_coder = GolombCoding(m, sign)

kodOrd = Golomb_coder.Encode(n)

print("kod ord: ",kodOrd)

value = Golomb_coder.Decode(kodOrd)

print("Value: ", value)
        
        
