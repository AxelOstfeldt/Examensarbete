import numpy as np
import math


class MetaLPC:

    def __init__(self, order, sign = True, CoefficentDecimalBits: int = 10):
        #Order have to be an integer of size 1 or larger for LPC
        #No upperlimit exist other than when the order is larger than the number of inputs the lag when caluclating autocorrelation will raise an error
        if  order < 0 or not isinstance(order, int):
            raise ValueError(f"Order can only have integer values larger than 0. Current value of is {order}")
        
        self.order = order
        self.sign = sign
        self.CoefDecBit = CoefficentDecimalBits
        self.CoeffDivisionFactor = pow(2,CoefficentDecimalBits) - 1
        


    #Function to calculate the autocorrelation of the input values
    def autocorrelation(self, x, lag):

        if lag >= len(x):
            raise ValueError(f"Lag must be shorter than array length")
        if not isinstance(lag, int) or lag < 0:
            raise ValueError(f"Lag must be an positive int")
        
 

        

        x_mean = np.mean(x)
        n = 0
        t = 0

            
        for i in range(len(x)):
            n += pow(x[i] - x_mean, 2)
            if i >= lag:
                t += (x[i] - x_mean) * (x[i-lag] - x_mean)


        #In the case where all x values are identical to each other the equation for autocorrelation dont work
        #This is beceause n will be equal to 0 and this can not be used to dicide t
        #In the case that all values are identical the autocorrelation should be =1 regardless of lag-value
        if n == 0:
            if lag == 0:
                t = 1
            else:
                t = 0
            
            n = 1
            

                       

        return t/n


    #Calculates the coefficents for LPC using the Levinson-Durbin algorithm
    #The coefficents can be calculated with matrix multiplications
    #How ever it is faster to use this algorithm
    def Coefficents(self, inputs):

        #If all inputs are constant a division by 0 error will occur
        #To handle this this if statement is created.
        #Since all values are exactly the same it is enough to predict the next value with the previous value
        #hence the first cofficent is a 1 and the rest are 0
        if all(element == inputs[0] for element in inputs):
            a = [1] + [0] * (self.order - 1)

        else:
            E = self.autocorrelation(inputs, 0)
            a = []

            for i in range(self.order):

                k = self.autocorrelation(inputs, i+1)
                if i > 0:
                    for j in range(i):
                        k -= a[j] * self.autocorrelation(inputs, i-j)

                k = k / E



                a.append(k)

                if i > 0:
                    a_old = a.copy()
                    for j in range(i):
                        a[j] = a_old[j] - k * a_old[(i-1)-j]
                E = (1 - pow(k,2)) * E







        return a


    #Calculates the prediction of the current value using the cofficents and earlier values
    def prediciton(self, memory, coef):
        prediction = 0

        for j in reversed(range(1, self.order)):
            prediction += coef[j] * memory[j]
            memory[j] = memory[j-1]#updates the memory with the earlier values taking one step in the memory array


        prediction += coef[0] * memory[0]

        return prediction, memory
    

    def In(self, inputs, memory):

        coef = self.Coefficents(inputs)



        residuals = []

        for i in range(len(inputs)):
            predict, memory = self.prediciton(memory, coef)

            memory[0] = inputs[i]#Updates the first slot in the memory array with the current value
            residual = inputs[i] - predict#caltulcates the residual

            residual = round(residual)#Since Rice and Golomb codes need to have interger the residual is rounded to closest int


            #Append current prediction and residual in array to returned
            residuals.append(residual)


        binaryCoefficents = self.CoefEncode(coef.copy())

        idealK, binaryIdealK = self.kCalculator(residuals.copy())

        CodeWord = self.RiceEncode(residuals, idealK)

        FullCodeWord = binaryIdealK + binaryCoefficents + CodeWord




        return FullCodeWord, memory, binaryCoefficents


    def kCalculator(self, residuals):
        #Calculates the ideal k_vaule
        abs_res = np.absolute(residuals.copy())
        abs_res_avg = np.mean(abs_res)
        #if abs_res_avg is less than 4.7 it would give a k value less than 1.
        #k needs tobe a int > 1. All abs_res_avg values bellow 6.64 will be set to 1 to avoid this issue
        if abs_res_avg > 6.64:
            #from testing it appears that the actual ideal k-value is larger by +1 than theory suggest,
        #atleast for larger k-value. The exact limit is unknown but it have been true for all test except for when the lowest k, k =1 is best.
        #Therefore th formula have been modified to increment k by 1 if abs_res_avg > 6.64.
            k = int(round(math.log(math.log(2,10) * abs_res_avg,2))) + 1
        else:
            k = 1

        #Binary represent k in 5 bits for metadata to be sent
        #This allows for values 0-32, since k never is less than 1 it is possible to shift down k by 1 beffore encoding,
        #allowing for k values 1-33 to be encoded
            
        binaryK = np.binary_repr(k-1,5)

        return k, binaryK
    

    def RiceEncode(self, residuals, k):
        CodeWord = ""

        for n in residuals:
            #n is the value to encode in Rice code
        
            #If the input data is signed the signed bit needs to be saved.
            #In case the input data is negative it is converted to positive beffore encoding.
            if self.sign:
                if n < 0:
                    s = "1"
                    n = -n
                else:
                    s = "0"

            
            #If statments checks if n = 0, this should be handled the same way as if n < k (see below),
            #but since math-log(0,2) does not work an extra if statement is needed
            if n == 0:
                #If n represent fewer than k bits it will be converted to a bianry value with padding.
                #The padding are zeros as MSB so that there are k bits representing the value n
                r = np.binary_repr(n,k)
                #The loop constant will detemen how long the unary code will be.
                #When n is fully represented in binary by r there is no need for unary code.
                loop = 0
            
            #If statement checks that n value is large enough to be longer than k bits when converted to binary.
            #This is done so when separating the k last bits it would create an error if there is not enoguh bits.
            elif math.log(n,2) < k:
                #If n represent fewer than k bits it will be converted to a bianry value with padding.
                #The padding are zeros as MSB so that there are k bits representing the value n
                r = np.binary_repr(n,k)
                #The loop constant will detemen how long the unary code will be.
                #When n is fully represented in binary by r there is no need for unary code.
                loop = 0
            else:
                #Convert n to a binary value
                n = bin(n)[2:]
                #Takes the k last bits of n and saves it in variable r
                r = n[len(n)-k:]
                #The remaining bits in n are converted to their interger value.
                #This interger value will be unary coded
                loop = int(n[:len(n)-k],2)
            
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

            #add r to the total codeword
            CodeWord += r
        
        return CodeWord


    #Enode the coefficents in binary code
    def CoefEncode(self, coefficent):
        #The cofficents are float numbers, usualy between -1 and 1.
        #To encode them the cofficents are multiplied by 1023 and rounded down to closest int,
        #That int is then written in binary.
        #baseline is to write this int in 10 bits binary and have 1 extra bit for sign bit.
        #This is enough when the coefficents are between -1 and 1, but if any coefficents are smaller/larger than this extra bits are needed.
        #The first bits in the Binary coefficents are run length encoded for how many extra bits are needed.
        #If the largest coefficents is 3.5 for example, multiplying this with 1023 and round down to closest in will get 3580 which needs 12 bits to be written,
        #that is 2 extra bits. It is the same amount of bits needed to write 3.5 rounded down to closest int.
        

        #The basline for how many bits should be used for decimal can be changed in the function by changing:
        #CoefficentDecimalBits in innit

        BinaryCoefficents = ""
        if np.max(np.absolute(coefficent.copy())) > 1:

            extraBits = np.max(np.absolute(coefficent.copy()))
            extraBits = math.ceil(math.log(extraBits,2))
        else:
            extraBits = 0


        
        #Run length encode how many extra bits are needed
        for RunLengthEncode in range(extraBits):
            BinaryCoefficents += "1"
        BinaryCoefficents += "0"
        

        
        #Encode each coefficent in binary
        #loop thorugh all coefficents
        for i in range(self.order):
            currentCoefficent = coefficent[i]
            #assign sign bit
            if currentCoefficent < 0:
                CurrentBinaryCoef = "1"
                currentCoefficent = -currentCoefficent
            else:
                CurrentBinaryCoef = "0"
            #Multipli coeffcient by 1023 and round down to closest int (1023 is standard value)
            currentCoefficent = int(currentCoefficent * self.CoeffDivisionFactor)
            
            #current coefficent should never be able to be larger than 2 ^ (10 + extraBits)
            #If it is it will not be possible to encode it
            if currentCoefficent > pow(2,self.CoefDecBit + extraBits):
                raise ValueError(f"current coefficent, {currentCoefficent} is larger than 2^{self.CoefDecBit+extraBits}")

            
            #Write the currentCoefficent value in binary, with 10 + extraBits lenght
            CurrentBinaryCoef +=  np.binary_repr(currentCoefficent, self.CoefDecBit + extraBits)

            #Add the current coefficent in binary to the full code word
            BinaryCoefficents += CurrentBinaryCoef

        return BinaryCoefficents


    def coefDecode(self, codeword):
        extraBits = 0
        coefficents = []

        #Recreate the extra bits from the rle code
        while codeword[0] == "1":
            extraBits +=1

            codeword = codeword[1:]

        codeword = codeword[1:]

        #loop thorugh the codeword and take out the bits representing a cofficents
        #this is done for every coefficents needed (number of coefficents = order)
        for NumberOfCoefficents in range(self.order):
            if codeword[0] == "1":
                IsNegative = True
            else:
                IsNegative = False

            codeword = codeword[1:]

            CurrentCoefficentBinary = codeword[:self.CoefDecBit+extraBits]
            codeword = codeword[self.CoefDecBit+extraBits:]
            


            CurrentCoefficent = int(CurrentCoefficentBinary, 2)

            if IsNegative:
                CurrentCoefficent = -CurrentCoefficent

            coefficents.append(CurrentCoefficent / self.CoeffDivisionFactor)

        if len(coefficents) != self.order:
            raise ValueError(f"Number of coefficents should match order, decoded coefficents are = {coefficents}")
        
        return coefficents, codeword

        
    def Out(self, codeword, memory):
        RecreatedValues = []

        kValue, codeword = self.kDecode(codeword)



        coef, codeword = self.coefDecode(codeword)



        residuals = self.RiceDecode(codeword, kValue)




        for i in range(len(residuals)):
            predict, memory = self.prediciton(memory, coef)
            

            #Recreates the current input
            #This maybe should also use round as in LPC.In
            #since the values in this project to be recreated always are int
            currentValue = residuals[i] + predict

            memory[0] = currentValue#Uppdates the first memory slot with the recreated input


            #Appends the current recreated value to be returned
            RecreatedValues.append(currentValue)

        return RecreatedValues, memory
    
    def kDecode(self, codeword):
        #5 first bits in the codeword represent the k value used to encode the residuals
        kBinary = codeword[:5]
        codeword = codeword[5:]

        #Convert k from binary to int
        #Increment k by 1 because it is shifted down by 1 when encoded
        k = int(kBinary,2) + 1

        return k, codeword
    
    def RiceDecode(self, code, k):
        
        
        decoded_values = []

        #Loops trough the code word to get all values in the code word
        while len(code) > 0:
            
            
            A = 0
            #If S is true the output should be negative
            S = False
            value = ""
            
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
            #By looping thorugh the codeword and removing k bits to the current value being decoded
            #The last bits in the code word for the current value can be decoded
            for j in range(k):
                code = code[1:]
                value += code[0]
            #Since there is a 0 separating the MSB with the LSB 1 more bit needs to be removed for the current value in the codeword
            code = code[1:]

            value = bin(A)[2:] + value

            #The original binary value is converted to an int
            value = int(value, 2)

            #In if the original value was negative sign and S will be true,
            #code will then be converted to a negative value
            if self.sign and S:
                value = -value

            #appends the decoded value in an array
            decoded_values.append(value)

        #Returns array with decoded int values
        return decoded_values


