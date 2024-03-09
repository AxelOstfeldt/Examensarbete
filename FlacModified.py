import numpy as np
import math
from Rice import RiceCoding

class FlacModified:

    def __init__(self, mics, samples):
        self.ShortCoff = [[0],[1],[2, -1],[3, -3, 1],[4,-6,4,-1]]
        self.mics = mics
        self.samples = samples

    def In(self, Inputs, memorysIn):
        
        for sample in range(self.samples):
            for microphone in range(self.mics):
                if sample == 0:
                    memoryIn = memorysIn[microphone]
                    currentInputs = Inputs[microphone,:]
                    AdjacentResidual, ShortenResiduals = (currentInputs, memoryIn)


                #Pick a micrphone by giving left argument, and sample by giving right arbument
    #To pick all sampels for a specific mic choose a number x for desired mic and ":" for samples:
    #data2[x,:]
                


    def PredictIn(self, currentInputs, memoryIn):
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




