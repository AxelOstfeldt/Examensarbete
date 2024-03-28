import numpy as np
import math
from Rice import RiceCoding

#Predcits mic value using value from previous mic

class MetaAdjacent:

    def __init__(self, order: int = 2, sign = True):
        self.order = order
        self.sign = sign
        #Coeficents for differente orders, from 0 to 4
        all_coeficents = [[0],[1],[2, -1],[3, -3, 1],[4,-6,4,-1]]
        #Assigns the coeificents to be used based on order
        self.coeficents = all_coeficents[order]


    def FirstIn(self, firstInput, memory):
        firstPrediction = 0

        if self.order > 0:
            firstPrediction = sum( np.array(self.coeficents) * np.array(memory) )

        firstResidual = firstInput - firstPrediction

        if self.order > 0:
            memory = [firstInput] + memory[:-1]


        return firstResidual, memory
    
    def In(self, inputs, memory):
        
        #Use Shorten to calculate the residual for the first microphone in the array
        firstResidual, memory = self.FirstIn(inputs[0], memory)

        #Save the first residual and prediciton in the residual and prediciton arrays
        Residuals = [firstResidual]



        #Save the first value as the previous value and previous row value
        #Previous indicates the value of the previous mice
        #PreviousRow indicates the first value of the previous row
        #The rest of the resiudals are calculated by taking the difference between the current mic value and the previous mic value
        Previous = inputs[0]
        PreviousRow = inputs[0]
        for i in range(1, len(inputs)):
            #When i modulos 8 is equal to 0 it indicates that a new row has started (8 mics per row)
            if i % 8 == 0:
                #The previous value is then taken from the previous row and not the previous mic
                #This will give a mic that is closer to the current mic
                CurrentResidual = self.PredicitorIn(inputs[i], PreviousRow)
                #A new PreviousRow value is calculculated
                #This is the first value of the new row
                PreviousRow = inputs[i]
            else:
                CurrentResidual = self.PredicitorIn(inputs[i], Previous)

            #Update the previous value
            Previous = inputs[i]

            #Save the residual and predicted value in their respective array
            Residuals.append(CurrentResidual)

        #Calculate the k value for the Rice Codes
        k_value = self.kCalculator(Residuals)
        #if k is larger than 33 it can not be encoded in 5 bits
        #33 works since k is shifted down by 1
        if k_value > 33:
            raise ValueError(f"k can not be larger than 32, current k value is {k_value}")


        #Convert the k_value to binary in 5 bits,
        #shift it down 1 step first, allowing for a range of k-values of 1-33
        k_binary = np.binary_repr(k_value - 1, 5)

        CodeWord = k_binary

        for i in range(len(Residuals)):
            Rice_coder = RiceCoding(k_value, self.sign)
            n = int(Residuals[i])
            kodOrd = Rice_coder.Encode(n)
            CodeWord += kodOrd



        #Return the residuals, memory, and predictions
        return CodeWord, memory


    def kCalculator(self, residuals):
        #Calculates the ideal k_vaule for the residuals
        abs_res = np.absolute(residuals.copy())
        abs_res_avg = np.mean(abs_res)
        #if abs_res_avg is less than 4.7 it would give a k value less than 1.
        #k needs tobe a int > 1. All abs_res_avg values bellow 6.64 will be set to 1 to avoid this issue
        if abs_res_avg > 6.64:
        #from testing it appears that the actual ideal k-value is larger by +1 than theory suggest,
        #atleast for larger k-value. The exact limit is unknown but it have been true for all test except for when the lowest k, k =1 is best.
        #Therefore th formula have been modified to increment k by 1 if abs_res_avg is larger than 6.64.
            k = int(round(math.log(math.log(2,10) * abs_res_avg,2))) +1
        else:
            k = 1

        return k


    def PredicitorIn(self, CurrentInput, PreviousInput):
        #Predicted value is the previous mic value
        Predcition = PreviousInput
        #The residual is the difference of the current mic value and the previous mic value
        Residual = CurrentInput - Predcition
        #Return the residual and prediciton
        return Residual
    

    def FirstOut(self, firstResidual, memory):
        firstPrediction = 0

        #If order is larger than 0 calculate prediciton, else prediciton is always 0
        if self.order > 0:
            firstPrediction = sum( np.array(self.coeficents) * np.array(memory) )

        #Recreate the original input by adding the residual and prediction value
        firstInput = firstResidual + firstPrediction

        #Update memory
        if self.order > 0:
            memory = [firstInput] + memory[:-1]


        return firstInput, memory
    

    def Out(self, CodeWord, memory):
        #First 5 bits of the codeword is the k-value used for Rice codes in binary
        k_binary = CodeWord[:5]
        CodeWord = CodeWord[5:]

        #k_value is decremented by 1 beffore being encoded and therefore need to be incremented by 1
        k_value = int(k_binary,2) + 1

        Rice_decoder = RiceCoding(k_value, self.sign)
        residuals = Rice_decoder.Decode(CodeWord)

        #Use Shorten to calculate the original input for the first microphone in the array
        firstInput, memory = self.FirstOut(residuals[0], memory)

        #Save the first residual and prediciton in the residual and prediciton arrays
        RecreatedValues = [firstInput]



        #Save the first value as the previous value and previous row value
        #Previous indicates the value of the previous mice
        #PreviousRow indicates the first value of the previous row
        #The original inputs are calculated unsing previous mic values and residuals
        Previous = firstInput
        PreviousRow = firstInput
        for i in range(1, len(residuals)):
            
            #When i modulos 8 is equal to 0 it indicates that a new row has started (8 mics per row)
            if i % 8 == 0:
                #The previous value is then taken from the previous row and not the previous mic
                #This will give a mic that is closer to the current mic
                CurrentInput = self.PredicitorOut(residuals[i], PreviousRow)
                #A new PreviousRow value is calculculated
                #This is the first value of the new row
                PreviousRow = CurrentInput
            else:
                CurrentInput = self.PredicitorOut(residuals[i], Previous)

            #Update previous value
            Previous = CurrentInput

            #Save the recreated input value and predicted value in their respective array
            RecreatedValues.append(CurrentInput)



        #Return recreated values and memory
        return RecreatedValues, memory
        

    def PredicitorOut(self, CurrentResidual, PreviousInput):
        #Predicted value is the previous mic value
        Predcition = PreviousInput
        #The original input value will be the residual + previous mic value
        CurrentInput = CurrentResidual + Predcition
        #Return the residual and prediciton
        return CurrentInput
        



