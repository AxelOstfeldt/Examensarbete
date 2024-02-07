import numpy as np
import math

class RiceCoding:

    #k should be an interger based on expected values calculated from previous sampel residuals.
    #larger k values for largerresiduals.
    # sign is if the input data is signed or unsigen
    def __init__(self, k, sign):
        self.k = k
        self.sign = sign

    #n is the value to encode in Rice code
    def Encode(self, n):
        #If the input data is signed the signed bit needs to be saved.
        #In case the input data is negative it is converted to positive beffore encoding.
        if self.sign:
            if n < 0:
                s = "1"
                n = -n
            else:
                s = "0"

        #If statement checks that n value is large enough to be longer than k bits when converted to binary.
        #This is done so when separating the k last bits it would create an error if there is not enoguh bits.
        if math.log(n,2) < self.k:
            #If n represent fewer than k bits it will be converted to a bianry value with padding.
            #The padding are zeros as MSB so that there are k bits representing the value n
            r = np.binary_repr(n,self.k)
            #The loop constant will detemen how long the unary code will be.
            #When n is fully represented in binary by r there is no need for unary code.
            loop = 0
        else:
            #Convert n to a binary value
            n = bin(n)[2:]
            #Takes the k last bits of n and saves it in variable r
            r = n[len(n)-self.k:]
            #The remaining bits in n are converted to their interger value.
            #This interger value will be unary coded
            loop = int(n[:len(n)-self.k],2)
           
        #Append a "0" bit as MSB in the code word r.
        #This will later show where the unary code ends.
        r = "0" + r


        #for loop with "loop" number of iteration.
        #Each iteration adds a "1" as MSB to r,
        #This way the unary code is created.
        for i in range(loop):
            r = "1" + r

        #In the case for signed data the sign bit is added to r.
        if self.sign:
            r = s + r

        #Returns the code word in r
        return r
    
    def Decode(self, code):
        
        A = 0
        #If S is true the output should be negative
        S = False

        #Checks if the data is signed
        if self.sign:
            #Checks if the MSB is "1", indicating that the value should be negative.
            if code[0] == "1":
                #Sets S to True if the output should be negative
                S = True
            #Removes the MSB, signed bit, from the code word.
            #This way the rest of the code word can be handled as if it was unsigned
            code = code[1:]
        
        #Decodes the unary code.
        #Unary code represents a interger value as a set of "1":s followed by a "0".
        #By incrementing A by 1 if the MSB is a one then moving the codeword one step and checking again
        #all "1" will increment A until a "0" is MSB indicating that the unary code have been decoded. 
        while code[0] == "1":
            A += 1
            code = code[1:]
        
        #After the unary code have been uncoded the remaining code will be
        #a "0" as MSB followed by the last k-bits from the original binary value as LSB
        #Removing the MSB only the k LSB remain.
        #By converting the interger value A from the unary code to binary and 
        #appending the k LSB to it the original binary value is arrived at.
        code = bin(A)[2:] + code[1:]

        #The original binary value is converted to an int
        code = int(code, 2)

        #In if the original value was negative sign and S will be true,
        #code will then be converted to a negative value
        if self.sign and S:
            code = -code

        #Returns the decoded value as an int
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