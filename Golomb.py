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
        #The largest possible residual will allways be m-1.
        #To easily get the correct binary value it is possible to take r + c² - m = r + b and then convert to binary
        else:
            encoded = encoded + np.binary_repr(r+b, width = c)

        
        #If the data is signed the signed bit is added
        if self.sign == True:
            encoded = s + encoded

        #returns the encoded value
        return encoded



    def Decode(self, code):

        cc = math.log(self.m,2)
        c = math.ceil(cc)
        b = pow(2,c) - self.m
        A = 0
        S = "0"
        
        #Used later to check that the data is correctly decoded
        LengthCheck = len(code)
        
        #Checks if the data is signed
        if self.sign == True:
            #if the sign bit is "1" the result should be negative,
            #to ensure this S is set to "1"
            if code[0] == "1":
                S = "1"
            #The sign bit is removed and the rest of the code word can be decoded as if it was unsigned
            code = code[1:]

        #Decodes the unary part of the codeword by staying in the while loop aslong as the MSB is "1"
        while code[0] == "1":
            #for every "1" in the code word A is incremented by one
            A += 1
            #Removes the MSB of the codeword
            code = code[1:]
        #After the unary code is decoded the MSB will be a "0".
        #This zero exist to indicate that the unary code is done and can be removed
        code = code[1:]

        #The c-1 last bits are converted to integer and denoted R
        R = int(code[:c-1],2)


        #There are 3 cases when decoding, reflecting the 3 cases for encoding

        #Case 1. m is a power of 2, then cc will be an interger.
        if (cc).is_integer():
            #In this case the remoning bits should be of lenght c, else and error will be raised
            if len(code) != c:
                raise ValueError(f"Size error, length of code remaining should match c. Current values are: code = {code}, c = {c}")
            #The remaining bits are converted to int and added to the unary decoded A times m
            decoded = self.m * A + int(code, 2)
        else:
            
            #Case 2. if R is less than c² - m 
            if R < b:
                #In these cases the remaning code should be length c-1. Else and error will be raised
                if len(code) != c-1:
                    raise ValueError(f"Size error. code = {code}, should have length: {c-1}")
                #The remaining bits are converted to int and added to the unary decoded A times m
                decoded = self.m * A + int(code, 2)
            #Case 3. if R is greater or equal to c² - m
            else:
                #in this case the remaining code should be of length c. Else and error will be raised
                if len(code) != c:
                    raise ValueError(f"Size error. code = {code}, should have length: {c}")
                #to decode in case the unary decoded A is multiplied with m and added to the interger valued code as the previous cases.
                #But in this case b is subtracted (b = c² - m). This is the deconding of the encoding case where the largest remainder is encoded in "1" bits with length c.
                decoded = self.m * A + int(code, 2) - b

        

        #Checks if the data is signed and if S ="1" the decoded value should be negative
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

        #Returns the decoded int value
        return decoded


sign = True
n = -7
m = 8

Golomb_coder = GolombCoding(m, sign)

kodOrd = Golomb_coder.Encode(n)

print("kod ord: ",kodOrd)

value = Golomb_coder.Decode(kodOrd)

print("Value: ", value)
        
        
