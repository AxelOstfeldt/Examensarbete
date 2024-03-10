import numpy as np
import math
from Rice import RiceCoding

class FlacModified:

    def __init__(self, sign, mics, samples, AdjacentOrder):
        self.ShortenCofficents = [[0],[1],[2, -1],[3, -3, 1],[4,-6,4,-1]]
        self.mics = mics
        self.samples = samples
        self.AdjacentOrder = AdjacentOrder
        self.sign = sign
        
        

    def In(self, Inputs, memorysIn):
        AdjacentResiduals = []
        AdjacentFirstPredictions = []
        AdjacentPredictions = []
        CodeWords = []

        for microphone in range(self.mics):
            RleCode = ""
            RleCount = 0
            currentInputs = Inputs[microphone,:]
            ShortenResiduals = [[],[],[],[],[]]
            ShortenCodeWords = ["","","","",""]
            AdjacentSampleCodeWords = ""
            #ShortenK = [0,0,0,0,0]#Not needed?
            AdjacentResiduals.append([])

            for sample in range(self.samples):
                #RLE calculations:

                #RLE predicitons, should start once sample > 0 so that memory have been updated once
                if sample > 0:
                    #If the next imput is the same as the earlier the RLE count increases by 1
                    if currentInputs[sample] == memorysIn[microphone][0]:
                        RleCount += 1
                    #If the next input is not the same as the first one in memory it means that a new value have arrived at input
                    #The old value is then encoded with its RLE count
                    else:
                        #Save the encoded Rle value in the RleCode variable
                        RleCode += self.RleEnconder(memorysIn[microphone][0], RleCount)
                        #Reset the Rle Counter
                        RleCount = 0
                    


                #Shorten calculations:

                #calculate the predicitons for the current input for all roders of Shorten, update the memory for all slots except the first one
                ShortenPredictions, new_memory = self.ShortenPredictIn(memorysIn[microphone])

                #Calculate the residuals for all orders of shorten
                for order in range(5):
                    ShortenResiduals[order].append(currentInputs[sample] - ShortenPredictions[order])

                #Uppdate the first slot in the new_memory to the current sample
                new_memory[0] = currentInputs[sample]
                memorysIn[microphone] = new_memory


                #Adjacent calculations:

                #First prediction for adjacent is saved as the first value in the begining of a new row
                #First residual for adjacent in the residual given by tge choosen order of shorten prediction 
                if microphone == 0:
                    AdjacentResiduals[microphone].append(currentInputs[sample] - ShortenPredictions[order])
                    AdjacentFirstPredictions.append(currentInputs[sample])
                    AdjacentPredictions.append(currentInputs[sample])

                #If microphone % 8 == 0 a new row for microphones have begun
                elif microphone % 8 == 0:
                    #the first value in the row is predicted using the previous row first value
                    CurrentAdjacentResidual, NewAdjacentPrediction = self.AdjacentPredictIn(currentInputs[sample], AdjacentFirstPredictions[sample])
                    #The first value in the row is then updated to the value of the first mic in the new row
                    AdjacentFirstPredictions[sample] = NewAdjacentPrediction

                else:
                    #Predict the current mic value with the previous mic value
                    CurrentAdjacentResidual, NewAdjacentPrediction = self.AdjacentPredictIn(currentInputs[sample], AdjacentPredictions[sample])

                #Save the resiudla
                AdjacentResiduals[microphone].append(CurrentAdjacentResidual)
                #Update the prediciton for the next mic
                AdjacentPredictions[sample] = NewAdjacentPrediction

            #Encode the residuals for shorten using RiceCodes
            for order in range(5):
                CurrentShortenResiduals = ShortenResiduals[order]

                #Calculate the k value
                k = self.kCalculator(CurrentShortenResiduals)
                #ShortenK[order] = k#Not needed?
                if k > 33:
                    raise ValueError(f"k can not be represented in 5 bits binary, max value for k is 32 and current value is {k}")
                #The k-value is represented in 5 bits, which allows for up to k = 33 to be represented.
                #This is becuase of k being subtracted by 1 so that k = 33 is represented by k = 32 which is max with 5 bits
                #k can never be less than 1 so k = 1 is shifted down to be represented as 0 in binary 
                
                #The first part of the codeword will be the k value
                ShortenCodeWords[order] = np.binary_repr(k-1,5)
                
                #rice code the residuals and add them to the code word
                for i in range(len(CurrentShortenResiduals)):
                    ShortenCodeWords[order] += self.RiceEncode(CurrentShortenResiduals[i], k)

            CurrentAdjacentSampleResidual = AdjacentResiduals[microphone]

             #Calculate the k value
            k = self.kCalculator(CurrentAdjacentSampleResidual)
            #ShortenK[order] = k#Not needed?
            if k > 33:
                raise ValueError(f"k can not be represented in 5 bits binary, max value for k is 32 and current value is {k}")
            #The k-value is represented in 5 bits, which allows for up to k = 33 to be represented.
            #This is becuase of k being subtracted by 1 so that k = 33 is represented by k = 32 which is max with 5 bits
            #k can never be less than 1 so k = 1 is shifted down to be represented as 0 in binary 
            
            #The first part of the codeword will be the k value
            AdjacentSampleCodeWords = np.binary_repr(k-1,5)

            #rice code the residuals and add them to the code word
            for i in range(len(CurrentAdjacentSampleResidual)):
                AdjacentSampleCodeWords += self.RiceEncode(CurrentAdjacentSampleResidual[i], k)


            #Find wich code word is shortest of RLE and the orders of shorten
            ChoosenEncoder = 0
            EncoderLength = len(RleCode)
            for order in range(5):
                if EncoderLength > len(ShortenCodeWords[order]):
                    EncoderLength = len(ShortenCodeWords[order])
                    ChoosenEncoder = order + 1
            
            #Compare the shortest code word of RLE or SHorten to adjacent codeword
            if EncoderLength > len(AdjacentSampleCodeWords):
                ChoosenEncoder = 6
            
            #Binary represent the choosen code word, this will be the first bits in the code word
            CurrentCodeWord = np.binary_repr(ChoosenEncoder,3)
            #If Choosen encoder is 0 the best code word is from RLE code
            if ChoosenEncoder == 0:
                CurrentCodeWord += RleCode
            #If choosen encoder is 6 the best code word is from adjacent when residuals are sorted by samples
            elif ChoosenEncoder == 6:
                CurrentCodeWord += AdjacentSampleCodeWords
            #else it is from shorten
            else:
                CurrentCodeWord += ShortenCodeWords[ChoosenEncoder-1]

            CodeWords.append(CurrentCodeWord)

        #Encode the adjacent residuals by sorting the resiudals based on mic
        #The theory behind this is that the reisudals based on mic will be closer together and therefore have better k-value when encoding
        #instead of encoding adjacent based on samples from one mic
        #The first slot in the AdjacentCodeWords array will represent the enocding choice for using adjacent
        AdjacentCodeWords = [np.binary_repr(7,3)]
        for sample in range(self.samples):
            
            #Save all residuals from all mics corresponding to one sample in the currentResidual array
            currentResidual = []
            for microphone in range(self.mics):
                AdjacentMicResiduals = AdjacentResiduals[microphone]
                currentResidual.append(AdjacentResiduals[sample])

            #Calculate k-value for the currentResidual array
            k = self.kCalculator(currentResidual)
            if k > 33:
                raise ValueError(f"k can not be represented in 5 bits binary, max value for k is 32 and current value is {k}")
            #The k-value is represented in 5 bits, which allows for up to k = 33 to be represented.
            #This is becuase of k being subtracted by 1 so that k = 33 is represented by k = 32 which is max with 5 bits
            #k can never be less than 1 so k = 1 is shifted down to be represented as 0 in binary 
            
            #The first part of the codeword will be the k value
            CurrentAdjacentCodeWord = np.binary_repr(k-1,5)

            #Rice code the residuals and add them to the code word
            for i in range(len(currentResidual)):
                CurrentAdjacentCodeWord += self.RiceEncode(currentResidual[i],k)

            AdjacentCodeWords.append(CurrentAdjacentCodeWord)

        #Compare the total length of the adjacent codewords based on sorting residuals by mics to the other codewords
        samplesLen = 0
        micsLen = 0
        for i in range(len(CodeWords)):
            samplesLen += len(CodeWords[i])

        for i in range(len(AdjacentCodeWords)):
            micsLen += len(AdjacentCodeWords[i])

        if samplesLen < micsLen:
            ChoosenCodeWords = CodeWords
        
        else:
            ChoosenCodeWords = AdjacentCodeWords

        return ChoosenCodeWords
        





            

            








                    

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

        return k
            
        
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

        #The amount of bits that RLE count i written in is dependent on self.samples
        #The maximum value for count is sample -1, the reason for -1 is that RLE count is countign how many times a value is reapeted
        #So for 256 values you can have 1 initial value and then reapeat it 255 times
        #It is important to round the value upwards
        BinaryRepresentation = math.ceil( math.log(self.samples, 2) )
        RleCountBinary = np.binary_repr(RleCounter, BinaryRepresentation)

        #Completes the current binary representation of the RLE
        RleBinary = s + RleValueBinary + RleCountBinary

        #Return the binary representation of the RLE
        return RleBinary                


    def ShortenPredictIn(self, memoryIn):
        #Predict shorten for order 0-4
        ShortenPredictions = [0]
        for i in range(1,5):
            ShortenPredictions.append(sum( np.array(memoryIn[:i]) * np.array(self.ShortenCofficents[i]) ))

        #All memory slots are stepped one step back and the oldest memory is dropped
        new_memory = []
        new_memory += memoryIn[:-1]

        return ShortenPredictions, new_memory
    
    def AdjacentPredictIn(self, CurrentInput, CurrentPrediction):
        #Calculate the residual by taking the current input and subtracting the residual
        CurrentResidual = CurrentInput - CurrentPrediction

        #Crate a new prediction by taking the current mic value, the next mic will be predicted with the current mic value
        NewPrediction = CurrentInput

        return CurrentResidual, NewPrediction
    



       




