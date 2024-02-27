import numpy as np
import math
from Rice import RiceCoding


class FLAC:

    def __init__(self, LpcOrder):
        self.LpcOrder = LpcOrder

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
            t = 1
            n = 1
                
        return t/n


    #Calculates the coefficents for LPC using the Levinson-Durbin algorithm
    #The coefficents can be calculated with matrix multiplications
    #How ever it is faster to use this algorithm
    def LpcCoefficentsCalc(self, inputs):

        E = self.autocorrelation(inputs, 0)
        a = []
        CoefficentsArray = []

        for i in range(self.LpcOrder):

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


    def ResidualCalculation(self, inputs, memory):
        LpcCoff = self.LpcCoefficentsCalc(inputs)
        ShortCoff = [[0],[1],[2, -1],[3, -3, 1],[4,-6,4,-1]]

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
                    #First the signed dignit is set, 0 for positive and 1 for negative
                    if memory[0] < 0:
                        s = "1"
                        #if the value was negative it is turned to positive beffore saved as value to be RLE encoded
                        Rle_value = -memory[0]
                    else:
                        s = "0"
                        Rle_value = memory[0]

                    #The RLE value is written as a 24 bit representation since this is the largest that can be sampled by the system
                    RleValueBinary = np.binary_repr(Rle_value, 24)
                    #The RLE count is written as 8 bit value
                    #The current block size is 256, which then is the max amount of identical sampels that can come in a row for the same block
                    #It is important to note that what is RLE encoded is the amount of repitions.
                    #So that if RLE count is encoded as 0 that means that the value occours once and then is repeated 0 times.
                    RleCountBinary = np.binary_repr(RleCount, 8)
                    RleCount = 0

                    #Completes the current binary representation of the RLE
                    RleBinary = s + RleValueBinary + RleCountBinary
                    #Saves the current representation of the RLE in array
                    RleCode += RleBinary


            #calculates the current prediction for all orders of shorten and LPC, aswell as steps the memory array
            shortCurrentPrediciton, LpcCurrentPrediction, memory = self.prediction(memory, LpcCoff, ShortCoff)

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
                LpcCurrentResidual = inputs[i] - LpcCurrentPrediction[j]
                LpcResiduals[j].append(LpcCurrentResidual)
                LpcPredictions[j].append(LpcCurrentPrediction[j])

        return RleCode, ShortResiduals, LpcResiduals, memory, LpcCoff, ShortPredcitions, LpcPredictions

    def In(self, inputs, memory):

        RleCode, ShortResiduals, LpcResiduals, memory, LpcCoff, SPred, LPred = self.ResidualCalculation(inputs, memory)

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
            AllResidualsBinary.append(CurrentCodeWord)
            k_array.append(ideal_k)

        codeChoice = 0
        k_Choice = 0
        valueChoice = AllResidualsBinary[0]

        for i in range(1, len(AllResidualsBinary)):
            
            if len(AllResidualsBinary[i]) < len(valueChoice):
                valueChoice = AllResidualsBinary[i]
                codeChoice = i
                k_Choice = k_array[i]

        return valueChoice, np.binary_repr(k_Choice,5), np.binary_repr(codeChoice, 6), memory, LpcCoff

            





    def FlacRice(self, current_residuals):
        #calculates the ideal k-value for the current residuals
        abs_res = np.absolute(current_residuals)
        abs_res_avg = np.mean(abs_res)

        #if abs_res_avg is less than 4.7 it would give a k value less than 1.
        #k needs tobe a int > 1 and therefore if abs_res_avg < 5 k is set to 1
        #OBS. 4.7 < abs_res_avg < 5 would be rounded of to k=1 so setting the limit to 5 works well
        if abs_res_avg > 5:
            k_ideal = int(round(math.log(math.log(2,10) * abs_res_avg,2)))
        else:
            k_ideal = 1

        #calculates the Rice code word for the residual
        code_word =""
        for q in range(len(current_residuals)):
            
            Rice_coder = RiceCoding(k_ideal, True)
            n = int(current_residuals[q])
            kodOrd = Rice_coder.Encode(n)
            code_word += kodOrd

        return code_word, k_ideal
            


    def prediction(self, memory, LpcCoff, ShortCoff):
        ShortCurrentPredcition = [0]*5
        LpcCurrentPrediciton = [0]*self.LpcOrder
        new_memory = [0]


        for i in range(len(memory)):
            if i <= 3:
                ShortCurrentPredcition[i+1] = sum( np.array(memory[:i+1]) * np.array(ShortCoff[i+1]) )

            if i < self.LpcOrder:
                LpcCurrentPrediciton[i] = sum( np.array(memory[:i+1]) * np.array(LpcCoff[i]) )

        new_memory += memory[:-1]

        return ShortCurrentPredcition, LpcCurrentPrediciton, new_memory

        


        
#Test FLAC
if 1 > 0:

    LPC_Order = 8
    FLAC_prediction = FLAC(LPC_Order)

    testInput = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0]

    if LPC_Order > 4:
        testMemory = [0]*LPC_Order
    else:
        testMemory = [0]*4

    
    #auto_Corr = FLAC_prediction.autocorrelation(testInput, 2)#Works
    #print(auto_Corr)

    #Lpc_coff = FLAC_prediction.LpcCoefficentsCalc(testInput)#Works
    #print(Lpc_coff[8])

    #RleCode, ShortResiduals, LpcResiduals, memory, LpcCoff, SPred, LPred = FLAC_prediction.ResidualCalculation(testInput,testMemory)

    

    Encoded_inputs, k_value, Encoding_choice, mem, LPC_Cofficents = FLAC_prediction.In(testInput, testMemory)

    print("Encoded_inputs: ", Encoded_inputs)
    print("k_value: ", k_value)
    print("Encoding choice: ", Encoding_choice)
    print("New memory: ", mem)
    print("LPC cofficents: ", LPC_Cofficents)
