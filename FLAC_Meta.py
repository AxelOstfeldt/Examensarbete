import numpy as np
import math
from Rice import RiceCoding



class MetaFLAC:

    def __init__(self, LpcOrder: int = 32, CoefficentDecimalBits: int = 10, sign = True):
        self.LpcOrder = LpcOrder
        self.ShortCoff = [[0],[1],[2, -1],[3, -3, 1],[4,-6,4,-1]]
        self.CoefDecBit = CoefficentDecimalBits
        self.CoeffDivisionFactor = pow(2,CoefficentDecimalBits) - 1
        self.sign = sign


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
    def LpcCoefficentsCalc(self, inputs):

        E = self.autocorrelation(inputs, 0)
        a = []
        CoefficentsArray = []

        #Check if all the inputs are the same, this will give a divison by zero error when using levensin durbin algorithm
        if all(element == inputs[0] for element in inputs):
            AllSame = True
        else:
            AllSame = False

        for i in range(self.LpcOrder):

            #To avoid division by zero this if statement is implemented
            #Since this edge case only handels when all inputs are the same the first cofficents is set to a 1
            #and the rest is set to 0
            if AllSame == True:
                a = [1] + [0] * i

            else:
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
            CoefficentsArray.append(a.copy())

        return CoefficentsArray

    def LpcCoefficentsBinaryIn(self, LpcCoefficentArray):
        
        BinaryCoefficentArray = []
        for c in range(len(LpcCoefficentArray)):
            
            coef = LpcCoefficentArray[c]
            BinaryCoefficents = ""
            if np.max(np.absolute(coef.copy())) > 1:

                extraBits = np.max(np.absolute(coef.copy()))
                extraBits = math.ceil(math.log(extraBits,2))
            else:
                extraBits = 0

            #Run length encode how many extra bits are needed
            for RunLengthEncode in range(extraBits):
                BinaryCoefficents += "1"
            BinaryCoefficents += "0"

            #Encode each coefficent in binary
            #loop thorugh all coefficents
            for i in range(len(coef)):
                currentCoefficent = coef[i]
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

                
                #Write the currentCoefficent value in binary, with CoefDecBit + extraBits lenght
                CurrentBinaryCoef +=  np.binary_repr(currentCoefficent, self.CoefDecBit + extraBits)

                #Add the current coefficent in binary to the full code word
                BinaryCoefficents += CurrentBinaryCoef

            BinaryCoefficentArray.append(BinaryCoefficents)



        return BinaryCoefficentArray


    def ResidualCalculation(self, inputs, memory):
        LpcCoff = self.LpcCoefficentsCalc(inputs)

        ShortPredcitions = [[],[],[],[],[]]
        ShortResiduals = [[],[],[],[],[]]

        RleCode = ""
        RleCount = 0

        LpcPredictions = []
        LpcResiduals = []
        for i in range(self.LpcOrder):
            LpcPredictions.append([])
            LpcResiduals.append([])

        for i in range(len(inputs)):

            #RLE predicitons, should start once i > 0 so that memory have been updated once
            if i > 0:
                #If the next imput is the same as the earlier the RLE count increases by 1
                if inputs[i] == memory[0]:
                    RleCount += 1
                #If the next input is not the same as the first one in memory it means that a new value have arrived at input
                #The old value is then encoded with its RLE count
                else:
                    #Save the encoded Rle value in the RleCode variable
                    RleCode += self.RleEnconder(memory[0], RleCount)
                    #Reset the Rle Counter
                    RleCount = 0
                    
            #calculates the current prediction for all orders of shorten and LPC, aswell as steps the memory array
            shortCurrentPrediciton, LpcCurrentPrediction, memory = self.prediction(memory, LpcCoff)

            #Replace the first spot in the memory array with the current input
            memory[0] = inputs[i]

            #Calculates the current residual for all orders of shorten
            #By looping through all the calculated predictions by different orders for the current input 
            #and subtracting the value from the current input and saving the ressidual in an array
            for j in range(len(shortCurrentPrediciton)):
                ShortCurrentResidual = inputs[i] - shortCurrentPrediciton[j]
                ShortResiduals[j].append(ShortCurrentResidual)
                ShortPredcitions[j].append(shortCurrentPrediciton[j])

            #The same is done for all orders of LPC  
            for j in range(len(LpcCurrentPrediction)):
                LpcCurrentResidual = round(inputs[i] - LpcCurrentPrediction[j])
                LpcResiduals[j].append(LpcCurrentResidual)
                LpcPredictions[j].append(LpcCurrentPrediction[j])

        #The last value needs to be RLE encoded
        #This is done by calling the RLE function
        #Save the encoded Rle value in the RleCode variable
        RleCode += self.RleEnconder(memory[0], RleCount)
        #Reset the Rle Counter
        RleCount = 0
        
        LpcBinaryCoefficents = self.LpcCoefficentsBinaryIn(LpcCoff.copy())

        return RleCode, ShortResiduals, LpcResiduals, memory, LpcBinaryCoefficents, LpcCoff, ShortPredcitions, LpcPredictions


    def In(self, inputs, memory):

        RleCode, ShortResiduals, LpcResiduals, memory, LpcBinaryCoefficents, LpcCoff, SPred, LPred = self.ResidualCalculation(inputs, memory)

        
        #Crate an array to store all binary represented values for the residuals and RLE
        AllResidualsBinary = []
        k_array = [0]

        #Append RLE at the first place in the binary represntation array
        AllResidualsBinary.append(RleCode)

        #Crate a for - loop and use Rice codes to append all Shorten residuals
        for i in range(len(ShortResiduals)):
            #Calculates ideal k value for current residuals and RIce codes and saves them in array
            CurrentCodeWord, ideal_k = self.FlacRice(ShortResiduals[i])
            AllResidualsBinary.append(CurrentCodeWord)
            k_array.append(ideal_k)

        #Crate a for loop and use Rice codes to append all LPC residuals
        for i in range(len(LpcResiduals)):
            #Calculates ideal k value for current residuals and RIce codes and saves them in array
            CurrentCodeWord, ideal_k = self.FlacRice(LpcResiduals[i])

            #Add the coefficents for current lpc to the codeword
            CurrentCodeWord = LpcBinaryCoefficents[i] + CurrentCodeWord
            AllResidualsBinary.append(CurrentCodeWord)
            k_array.append(ideal_k)

        codeChoice = 0
        k_Choice = 0
        valueChoice = AllResidualsBinary[0]
        for i in range(1, len(AllResidualsBinary)):
            #If specific compression algorithm needs to be tested it can be done with an if statement here
            #Example, for test RLE only add the if statment "if i < 1:"
            if len(AllResidualsBinary[i]) < len(valueChoice):
                valueChoice = AllResidualsBinary[i]
                codeChoice = i
                k_Choice = k_array[i]

        #Only need to return the relevant LpcCofficents
        #If RLE or Shorten have been used the cofficents are just an empty array
        LpcCoffChoosen = []
        #If LPC have been choosen the relevant cofficents are saved in the LpcCoffChoosen variabel
        #LPC order 1 is equal to codeChoice = 6 therefore the if statement checks if codeChoice is larger than 6
        if codeChoice > 5:
            LpcCoffChoosen = LpcCoff[codeChoice-6]
        
        

        #k is encoded in 5 bits, allowing for values from 0-32, since k can never be less than 1
        #k is decremented by 1 beffore enocding it. Allowing for k values in between: 1 <= k <= 33
        if 33 < k_Choice :
            raise ValueError(f"k can not be represented in 5 bits binary, max value for k is 32 and current value is {k_Choice}")

        k_Choice = k_Choice - 1


        #Add the code choice to get final codeword
        FinalCodeWord = np.binary_repr(codeChoice,6) + valueChoice
        


        return FinalCodeWord, memory


    def LpcCoefDecode(self, codeword, CurrentLpcOrder):
        extraBits = 0
        coefficents = []

        #Recreate the extra bits from the rle code
        while codeword[0] == "1":
            extraBits +=1

            codeword = codeword[1:]

        codeword = codeword[1:]

        #loop thorugh the codeword and take out the bits representing a cofficents
        #this is done for every coefficents needed (number of coefficents = order)
        for NumberOfCoefficents in range(CurrentLpcOrder):
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

        if len(coefficents) != CurrentLpcOrder:
            raise ValueError(f"Number of coefficents should match order, decoded coefficents are = {coefficents}")
        
        return coefficents, codeword




    
    def Out(self, code_residuals, memory):
        DecodedValues = []#Array to save decoded values
        

        #the first 6 bits in the codeword indicate what encoder have been used
        code_choose_binary = code_residuals[:6]
        code_residuals = code_residuals[6:]
        code_choose = int(code_choose_binary,2)

        #If code_chosse is 0 the residual is encoded using RLE
        if code_choose == 0:
            
            #Loops trough all the enocded binary values with a while llop
            while len(code_residuals) > 0:
                #Raise error if there is not enough length left of code_residuals for 1 code_word
                if len(code_residuals) < 33:
                    raise ValueError(f"Code_word length is {len(code_residuals)}, should  never be lower than 33")


                #The first bit in each code word is the sign bit
                #This is saved as s and then the code_residuals is stepped one step
                s = code_residuals[0]
                code_residuals = code_residuals[1:]

                #The next 24 bits represents the value that have been encoded
                #Once they been saved 24 steps trough the code_residuals are taken
                RleValue = code_residuals[:24]
                code_residuals = code_residuals[24:]

                #The next 8 bits represent how many times the value was repeated
                #Once it been saved 8 steps is taken in the code_residuals
                RleCount = code_residuals[:8]
                code_residuals = code_residuals[8:]

                #The value that have been encoded is converted to int
                IntRelValue = int(RleValue, 2)

                #If the sign bit is "1" the value is converted to negative
                if s == "1":
                    IntRelValue = -IntRelValue

                #A for loop is used to append as many values as needed
                #The RleCount value is increased by 1 because even though
                #a value never was reapeted it occured once
                for i in range(1 + int(RleCount, 2)):
                    DecodedValues.append(IntRelValue)
            
            #Uppdate memory
            #Copy the decoded values to assign them to the memory array later
            RleCopy = DecodedValues.copy()

            #Assign the last values of the decoded values to the memory array
            #Important that the size of the memory array stays the same
            if len(RleCopy) > len(memory):
                new_memory = RleCopy[len(RleCopy)-len(memory):]
            #In the case that there is to few values among the decoded values pad the memory array with 0:s
            else:
                new_memory = RleCopy
                while len(new_memory) < len(memory):
                    new_memory.append(0)

            #Assign the new_memory to memory
            memory = new_memory
         

        else:
            
            

            #If code choice is larger than 5 LPC have been used to encode the residuals,
            #the first bits in the codewords are then the coffiecnts used in LPC
            if code_choose > 5:
                #The LPC order will be 5 less than code_choose since code_choice 0 is for RLE and 1-5 is for Shorten
                CurrentLpcOrder = code_choose - 5
                #Decode the first bits that represent the LPC cofficents,
                #The number of cofficents are equal to CurrentLpcOrder
                LpcCoff, code_residuals = self.LpcCoefDecode(code_residuals, CurrentLpcOrder)


            #Else if code_choose is not > 5 shorten have been used to encode it
            else:
                #The Shorten order will be 1 less than code_choose since code_choice 0 is for RLE
                ShortenOrder = code_choose - 1

            #The next 5 MSB in the codeword represnt the k-value used to encode the residuals using Rice codes  
            k_binary = code_residuals[:5]
            code_residuals = code_residuals[5:]
            k_value = int(k_binary,2) + 1




            #In cases where RLE encoding is not used, the resiudals have been encoded using Rice codes
            #Decodes the Residuals with Rice.Decode
            Rice_decoder = RiceCoding(k_value, self.sign)
            Residuals = Rice_decoder.Decode(code_residuals)
            

            #loops thorugh all the residuals to calculate the original input value
            for i in range(len(Residuals)):
                #If code_choose is 1 to 5 Shorten have been used by FLAC
                if code_choose < 6:
                    

                    #If shorten order does not match length of memeory array error should be raised
                    

                    #If Shorten order is 0 the prediciton is allways 0
                    if ShortenOrder == 0:
                        current_prediciton = 0
                    #In other cases the current predicition is calculated by multiplying the orders cofficents with the memory array
                    else:
                        current_prediciton = sum( np.array(self.ShortCoff[ShortenOrder]) * np.array(memory[:ShortenOrder]) )

                #If the code_choose is larger than 5 LPC have been used by FLAC
                else:
                   
                    #Calculated the current_prediciton by multiplying the LpcCoff with the memory
                    current_prediciton = sum( np.array(LpcCoff) * np.array(memory[:CurrentLpcOrder]) )

                #Calculating current input by taking the prediciton and adding the current residual
                current_input = current_prediciton + Residuals[i]

                #Uppdating memory by stepping all slots one step back and putting the current_input in the first slot
                memory = [current_input] + memory[:-1]

                #Append the decoded input value
                DecodedValues.append(current_input)

        #Return the decoded values and memory array
        return DecodedValues, memory, code_choose
                

    def RleEnconder(self, RleValue, RleCounter):
        #First the signed dignit is set, 0 for positive and 1 for negative
        if RleValue < 0:
            s = "1"
            #if the value was negative it is turned to positive beffore saved as value to be RLE encoded
            Rle_value = -RleValue
        else:
            s = "0"
            Rle_value = RleValue

        #The RLE value is written as a 24 bit representation since this is the largest that can be sampled by the system
        RleValueBinary = np.binary_repr(Rle_value, 24)
        #The RLE count is written as 8 bit value
        #The current block size is 256, which then is the max amount of identical sampels that can come in a row for the same block
        #It is important to note that what is RLE encoded is the amount of repitions.
        #So that if RLE count is encoded as 0 that means that the value occours once and then is repeated 0 times.
        RleCountBinary = np.binary_repr(RleCounter, 8)
        


        #Completes the current binary representation of the RLE
        RleBinary = s + RleValueBinary + RleCountBinary

        #Return the binary representation of the RLE
        return RleBinary
        

    def FlacRice(self, current_residuals):
        #calculates the ideal k-value for the current residuals
        abs_res = np.absolute(current_residuals)
        abs_res_avg = np.mean(abs_res)

        #k needs tobe a int > 1. abs_res_avg = 6.64 gives k = 1.
        #All k values for abs_res_avg above 6.64 is calculated using modified Rice Theory
        if abs_res_avg > 6.64:
            k_ideal = int(round(math.log(math.log(2,10) * abs_res_avg,2))) + 1
        else:
            k_ideal = 1

        if k_ideal < 1 :
            raise ValueError(f"k can not be less than 1, current value is {k_ideal}")


        kBinary = k_ideal - 1
        if 1 > kBinary or kBinary > 32:
            raise ValueError(f"kBinary have to be larger or equal to 1 and less or equal to 32, current value is {kBinary}")

        #Represent the k value in 5 bits
        kBinary = np.binary_repr(kBinary,5)

        #calculates the Rice code word for the residual
        code_word =kBinary
        for q in range(len(current_residuals)):
            
            Rice_coder = RiceCoding(k_ideal, self.sign)
            n = int(current_residuals[q])
            kodOrd = Rice_coder.Encode(n)
            code_word += kodOrd

        return code_word, k_ideal
            

    def prediction(self, memory, LpcCoff):
        ShortCurrentPredcition = [0]*5
        LpcCurrentPrediciton = [0]*self.LpcOrder
        new_memory = [0]


        for i in range(len(memory)):
            if i <= 3:
                ShortCurrentPredcition[i+1] = sum( np.array(memory[:i+1]) * np.array(self.ShortCoff[i+1]) )

            if i < self.LpcOrder:
                LpcCurrentPrediciton[i] = sum( np.array(memory[:i+1]) * np.array(LpcCoff[i]) )

        new_memory += memory[:-1]

        return ShortCurrentPredcition, LpcCurrentPrediciton, new_memory

        




