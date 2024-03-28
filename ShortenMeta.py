import numpy as np
import math
from Rice import RiceCoding

class ShortenMeta:

    def __init__(self, order: int = 3, sign = True):
        #Order can only be between 0 and 3 for Shorten, and have to be an in
        if not (0 <= order <= 3) or not isinstance(order, int):
            raise ValueError(f"Order can only have integer values between 0 and 3. Current value of is {order}")

        self.order = order
        #Coeficents for differente orders, from 0 to 3
        all_coeficents = [[0],[1],[2, -1],[3, -3, 1]]
        #Assigns the coeificents to be used based on order
        self.coeficents = all_coeficents[order]
        self.sign = sign

    def predict(self, memory):
        prediction = 0

        if self.order > 1:
            #this forloop is reversed so that memory values needed are not overwritten when values are shuffled one index back
            for j in reversed(range(1, self.order)):
                prediction = prediction + self.coeficents[j] * memory[j]
                memory[j] = memory[j-1]

            prediction = prediction + self.coeficents[0] * memory[0]

        elif self.order == 1:
            #in case of order 1 the current prediction is the last input
            prediction = memory[0]

        elif self.order == 0:
            #in case of order zero the prediciton is allways zero.
            #in this case the full current value is sent as residual
            prediction = 0

        else:
            raise ValueError(f"Order can only have integer values between 0 and 3. Current value of is {self.order}")
        return prediction, memory


    def In(self, input, memory: list = [0] * 3):


        
        
        #raises error if memory is not the length of order
        if self.order != len(memory):
            raise ValueError(f"Order and memory length should match. Current values are: order = {self.order}, memory length = {len(memory)}")
        
        residuals = []
        

        
        #loops through the input array 
        for i in range(len(input)):
            prediction, memory = self.predict(memory)


            #calculates residual by taking the current value and subtract the predicted value
            residual = input[i] - prediction

            #update the first memory slot with the current input value
            #This should not be done for order 0 since that have an empty memory
            if self.order > 0:
                memory[0] = input[i]
            
            
            #saves residuals 
            residuals.append(residual)

        #Calculate the k value to use for the Rice codes
        k_value = self.kCalculator(residuals.copy())

        if k_value > 33:
            raise ValueError(f"k can not be larger than 32, current k value is {k_value}")


        #Represent the k value in 5 bits
        k_binary = np.binary_repr(k_value - 1, 5)

        CodeWord = k_binary

        for i in range(len(residuals)):
            Rice_coder = RiceCoding(k_value, self.sign)
            n = int(residuals[i])
            kodOrd = Rice_coder.Encode(n)
            CodeWord += kodOrd



        #returns residual. memory. and prediction array
        #The memory array can then be used for the next set of data inputs if the come in blocks
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


    def Out(self, CodeWord, memory: list = [0] * 3):
        

        #The first 5 bits in the codeword is the k-value for the rice codes
        k_binary = CodeWord[:5]
        CodeWord = CodeWord[5:]
        #k_value is decremented by 1 beffore being encoded and therefore need to be incremented by 1
        k_value = int(k_binary,2) + 1
        
        Rice_decoder = RiceCoding(k_value, self.sign)
        residuals = Rice_decoder.Decode(CodeWord)

        RecreatedValues = []
        
        #loops through the residuals array 
        for i in range(len(residuals)):
            prediction, memory = self.predict(memory)


            #calculates original input by taking the current residual and adding the predicted value
            current_input = residuals[i] + prediction

            #update the first memory slot with the current input value
            #This should not be done for order 0 since that have an empty memory
            if self.order > 0:
                memory[0] = current_input
            
            #saves residuals 
            RecreatedValues.append(current_input)


        return RecreatedValues, memory