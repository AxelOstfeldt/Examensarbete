import numpy as np
import math

class DoubleCompression:

    def __init__(self, ShortenOrder, sign = True, mics: int = 64, samples: int = 256, AdjacentOrder: int = 2):
        self.ShortenCofficents = [[0],[1],[2, -1],[3, -3, 1],[4,-6,4,-1]]
        self.mics = mics
        self.samples = samples
        self.AdjacentOrder = AdjacentOrder
        self.sign = sign
        self.ShortenOrder = ShortenOrder

    def In(self, Inputs, MemoryShorten, MemoryAdjacent):
        UnsortedResiduals = []
        AllCodeWords = []
        #loop thorugh all inputs and calculate their residuals using Adjacentpredictor
        for sample in range(self.samples):
            CurrentInputs = Inputs[:,sample]
            
            AdjacentResiduals, MemoryAdjacent = self.AdjacentResiduals(CurrentInputs, MemoryAdjacent)
            UnsortedResiduals.append(AdjacentResiduals)

        #Sort the residuals so that they are grouped by mic and not by sample
        SortedResiduals = self.SortResiduals(UnsortedResiduals)

        #Loop though each residual and compress it again by using shorten
        #The shorten predictor now predict the residual between two mic for all sampels
        for mic in range(self.mics):
            ShortenResiduals, MemoryShorten = self.ShortenResiduals(SortedResiduals[mic], MemoryShorten)

            #Calculate what k-value is best to encode the Shorten residuals using Rice Codes.
            #Modified k equation is used where k-values that are not rounded up to one are incremented by 1

            k = self.kCaulculator(ShortenResiduals)

            #The first value in the CodeWord will be the k-value for the residual in binary code
            #k is encoded in 5 bits, allowing for values from 0-32, since k can never be less than 1
            #k is decremented by 1 beffore enocding it. Allowing for k values in between: 1 <= k <= 33
            if 33 < k :
                raise ValueError(f"k can not be represented in 5 bits binary, max value for k is 32 and current value is {k}")

            kBinary = np.binary_repr(k-1,5)
            CodeWord = kBinary
            #encode all residuals using RiceCode
            for residual in ShortenResiduals:
                CodeWord += self.RiceEncode(residual, k)

            AllCodeWords.append(CodeWord)

        return AllCodeWords, MemoryShorten, MemoryAdjacent
                


    #n is the value to encode in Rice code
    def RiceEncode(self, n, k):
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

        #Returns the code word in r
        return r


    #Calculates the ideal k-value according to modified Rice theory
    #Take the Rice Theory value and if it is larger than 1 increment it by 1 (Best from test results)
    def kCalculator(self, residuals):

        #Convert all values to positive, since the will be positive when encoding
        abs_res = np.absolute(residuals)
        #Calculate the mean value
        abs_res_avg = np.mean(abs_res)
        
        #k needs tobe a int > 1. abs_res_avg = 6.64 gives k = 1.
        #All k values for abs_res_avg above 6.64 is calculated using modified Rice Theory
        if abs_res_avg > 6.64:
            k = int(round(math.log(math.log(2,10) * abs_res_avg,2))) + 1
        else:
            k = 1

        if k < 1 :
            raise ValueError(f"k can not be less than 1, current value is {k}")

        return k

    #Sort the residuals so that they are grouped by mic and not sample
    def SortResiduals(self, UnsortedResiduals):
        SortedResiduals = []
        for mic in range(self.mics):
            SortedResiduals.append([])
            for sample in range(self.samples):
                SampleResiduals = UnsortedResiduals[sample]
                SortedResiduals[mic].append(SampleResiduals[mic])

        return SortedResiduals
                
    #Predict the next mic using the previous mic, save the residual
    def AdjacentResiduals(self, Inputs, memory):
        #Use Shorten to calculate the residual for the first microphone in the array
        firstPrediction = self.ShortenPredictor(memory, self.AdjacentOrder)
        firstResidual = Inputs[0] - firstPrediction
        #Save the first residual and prediciton in the residual and prediciton arrays
        Residuals = [firstResidual]
        new_memory = [Inputs[0]] + memory[:-1].copy()

        #Save the first value as the previous value and previous row value
        #Previous indicates the value of the previous mice
        #PreviousRow indicates the first value of the previous row
        #The rest of the resiudals are calculated by taking the difference between the current mic value and the previous mic value
        Previous = Inputs[0]
        PreviousRow = Inputs[0]
        for mic in range(1, len(Inputs)):
            #When i modulos 8 is equal to 0 it indicates that a new row has started (8 mics per row)
            if mic % 8 == 0:
                #The previous value is then taken from the previous row and not the previous mic
                #This will give a mic that is closer to the current mic
                CurrentResidual = self.AdjacentPredictor(Inputs[mic], PreviousRow)
                #A new PreviousRow value is calculculated
                #This is the first value of the new row
                PreviousRow = Inputs[mic]
            else:
                CurrentResidual = self.AdjacentPredictor(Inputs[mic], Previous)

            #Update the previous value
            Previous = Inputs[mic]

            #Save the residual 
            Residuals.append(CurrentResidual)


        #Return the residuals, memory
        return Residuals, new_memory
    
    def AdjacentPredictor(self, input, Prediction):
        #The residual is the difference of the current mic value and the previous mic value
        Residual = input - Prediction
        #Return the residual
        return Residual
    
    def ShortenResiduals(self, inputs, memory):
        residuals = []
        for i in range(len(inputs)):
            currentPrediction = self.ShortendPredictor(memory, self.ShortenOrder)
            currentResidual = inputs[i] - currentPrediction
            residuals.append(currentResidual)
            memory = [inputs[i]] + memory[:-1]

        return residuals, memory


        
        

    #Prediction using Shorten, predict the value using Shorten cofficents of the correct order and 
    def ShortenPredictor(self, memory, order):
        if order == 0:
            prediction = 0
        else:
            prediction = sum( np.array(memory[:order]) * np.array(self.ShortenCofficents[order]) )

        return prediction


        





    