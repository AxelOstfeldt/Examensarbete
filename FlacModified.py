import numpy as np
import math
from Rice import RiceCoding

class FlacModified:

    def __init__(self, mics, samples, AdjacentOrder):
        self.ShortenCofficents = [[0],[1],[2, -1],[3, -3, 1],[4,-6,4,-1]]
        self.mics = mics
        self.samples = samples
        self.AdjacentOrder = AdjacentOrder
        

    def In(self, Inputs, memorysIn):

        for microphone in range(self.mics):
            currentInputs = Inputs[microphone,:]
            ShortenResiduals = [[],[],[],[],[]]
            for sample in range(self.samples):
                ShortenPredictions, memorysIn[microphone] = self.PredictIn(memorysIn[microphone])

                for order in range(5):


            
                if sample == 0:
                    memoryIn = memorysIn[microphone]
                    currentInputs = Inputs[microphone,:]
                    AdjacentResidual, ShortenResiduals = (memoryIn)



                #Pick a micrphone by giving left argument, and sample by giving right arbument
    #To pick all sampels for a specific mic choose a number x for desired mic and ":" for samples:
    #data2[x,:]
                


    def PredictIn(self, memoryIn):

        
        #Predict shorten for order 0-4
        ShortenPredictions = [0]
        for i in range(1,5):
            ShortenPredictions.append(sum( np.array(memoryIn[:i]) * np.array(self.ShortenCofficents[i]) ))

        #All memory slots are stepped one step back and the oldest memory is dropped
        new_memory = []
        new_memory += memoryIn[:-1]

        return ShortenPredictions, new_memory



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




