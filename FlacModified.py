import numpy as np
import math

class FlacModified:

    def __init__(self, sign = True, mics: int = 64, samples: int = 256, AdjacentOrder: int = 2, ForceEncoder = "None"):
        self.ShortenCofficents = [[0],[1],[2, -1],[3, -3, 1],[4,-6,4,-1]]
        self.mics = mics
        self.samples = samples
        self.AdjacentOrder = AdjacentOrder
        self.sign = sign
        EncoderForced = -1
        Encoders = ["RLE", "Shorten0", "Shorten1", "Shorten2", "Shorten3", "Shorten4", "AdjacentSamples", "AdjacentMics"]
        for i in range(len(Encoders)):
            encoder = Encoders[i]
            if encoder == ForceEncoder:
                EncoderForced = i

        self.EncoderForced = EncoderForced
        #An encoder that is not in the list cant be choosen
        if self.EncoderForced < 0 and ForceEncoder != "None":
            raise ValueError(ForceEncoder," is not a possible choice of encoder, options are: ", Encoders)
        
        

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

                #For the last sample in the datablock the RLE value needs to be encoded
                if sample == self.samples - 1:
                    RleCode += self.RleEnconder(currentInputs[sample], RleCount)
                    


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
                    #CurrentAdjacentResidual = currentInputs[sample] - ShortenPredictions[order]
                    AdjacentResiduals[microphone].append(currentInputs[sample] - ShortenPredictions[self.AdjacentOrder])
                    AdjacentFirstPredictions.append(currentInputs[sample])
                    AdjacentPredictions.append(currentInputs[sample])
                
                else:
                    #If microphone % 8 == 0 a new row for microphones have begun
                    if microphone % 8 == 0:
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

            #If EncoderForced is: 0 <= EncoderForced <= 6, 
            if 0 <= self.EncoderForced <= 6:
                ChoosenEncoder = self.EncoderForced

            #Else the shortest codeword is calculated and choosen as encoder
            else:
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
                currentResidual.append(AdjacentMicResiduals[sample])#Not sure about this line?

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

        #if EncoderForced is less than 0 the shortest code words will be choosen
        if self.EncoderForced < 0:

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
        #If 0 <= EncoderForced < 7 the codeword is forced to take a value previously calculated and Choosen codewords is set to CodeWords
        elif self.EncoderForced < 7:
            ChoosenCodeWords = CodeWords

        #In other cases for EncoderForced the ChoosenCodeWords will be for Adjacent when residuals are grouped by samples
        else:
            ChoosenCodeWords = AdjacentCodeWords

        
        return ChoosenCodeWords, memorysIn
        





            

            

    def Out(self, CodeWords, MemorysOut):
        AdjacentMics = self.CheckFirst(CodeWords[0])
        DecodedValues = []
        for microphone in range(self.mics):
            DecodedValues.append([])

        if AdjacentMics:

            
            #For Adjacent Mics the first 
            for sample in range(1, len(CodeWords)):
                #Recreate the residuals from the Rice codes
                CodeWord = CodeWords[sample]
                RecreatedResiduals = self.RiceDecode(CodeWord)
                
                for i in range(len(RecreatedResiduals)):
                    CurrentRecreatedResidual = RecreatedResiduals[i]
                    #Recreate the first mic value from Shorten
                    if i == 0:
                        FirstInRowValue, MemorysOut[i] =  self.FirstAdjacentDecoder(CurrentRecreatedResidual, MemorysOut[i])
                        AdjacentValue = FirstInRowValue
                    #If i%8 == 0 then a new row have been started
                    #The mic value will be predicted from the previous row and the decoded value will be saved as the new FirstInRowValue
                    elif i % 8 == 0:
                        FirstInRowValue, MemorysOut[i] = self.AdjacentDecoder(FirstInRowValue, CurrentRecreatedResidual, MemorysOut[i])
                        AdjacentValue = FirstInRowValue
                    #The value is predicted from the previous mic value
                    else:
                        AdjacentValue, MemorysOut[i] = self.AdjacentDecoder(AdjacentValue, CurrentRecreatedResidual, MemorysOut[i])
                        
                    DecodedValues[i].append(AdjacentValue)


        else:
            for i in range(len(CodeWords)):
                CodeWord = CodeWords[i]
                #Check what encoder was used to encode the resiudals
                ChoosenEncoder, CodeWord = self.FindEncoder(CodeWord)
                #If ChoosenEncoder is 0 RLE have been used to encode the resiudals
                if ChoosenEncoder == 0:
                    #Decode the values when RLE is used to encode
                    DecodedValues[i], MemorysOut[i] = self.RleDecoder(CodeWord)

                else:
                    #Decode the residuals from Rice codes
                    RecreatedResiduals = self.RiceDecode(CodeWord)

                    #If ChossenEncoder is 6 Adjacent grouped by sampels have been encoded
                    if ChoosenEncoder == 6:
                        if i == 0:
                            DecodedValues[i], MemorysOut[i] = self.ShortenDecoder(RecreatedResiduals, self.AdjacentOrder, MemorysOut[i])
                        
                        else:
                            CurrentMicDecodedValues = []
                            if i % 8 == 0:
                                prediction = DecodedValues[i-8].copy()

                            else:
                                prediction = DecodedValues[i-1].copy()

                            for j in range(len(prediction)):
                                CurrentPrediction = prediction[j]
                                CurrentResidual = RecreatedResiduals[j]

                                CurrentDecodedValue, MemorysOut[i] = self.AdjacentDecoder(CurrentPrediction, CurrentResidual, MemorysOut[i])
                                CurrentMicDecodedValues.append(CurrentDecodedValue)

                            DecodedValues[i] = CurrentMicDecodedValues

                    #In other cases Shorten have been used
                    else:
                        #The shorten order that have been used is ChoosenEncoder - 1
                        order = ChoosenEncoder - 1

                        DecodedValues[i], MemorysOut[i] = self.ShortenDecoder(RecreatedResiduals, order, MemorysOut[i])
                        

        #Length of DecodedValues should match number of mics
        if len(DecodedValues) != self.mics:
            raise ValueError(f"DecodedValues length does not match number of mics, current length is: {len(DecodedValues)}")
        
        #Each saved slot in decodedValues should have a length that matches number of samples
        for microphone in range(len(DecodedValues)):
            if len(DecodedValues[microphone]) != self.samples:
                raise ValueError(f"Only {len(DecodedValues[microphone])} samples decoded for microphone #{microphone}")
            
        return DecodedValues, MemorysOut





    def CheckFirst(self, CodeWord):
        #The first 3 binary value
        BinaryEncoder = CodeWord[:3]
        #Change their binary value to int
        ChoosenEncoder = int(BinaryEncoder,2)

        #Checks if the encoder used is adjacent mics
        if ChoosenEncoder == 7:
            AdjacentMicsUsed = True
        
        else:
            AdjacentMicsUsed = False
    
        return AdjacentMicsUsed


    def FindEncoder(self, CodeWord):
        #The first 3 binary value
        BinaryEncoder = CodeWord[:3]
        #Change their binary value to int
        ChoosenEncoder = int(BinaryEncoder,2)

        #Return the CodeWord without the binary digits representing the Choosene encoder
        RemainingCodeWord = CodeWord[3:]

        return ChoosenEncoder, RemainingCodeWord


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
            
    
    def RiceDecode(self, CodeWord):
        #The 5 first binary digits in the codeword represnt the k value used to Rice code the residuals
        kBinary = CodeWord[:5]
        #When encoding k value it is decremented by 1 so when deocing k it have to be incremented by 1
        k = int(kBinary,2) + 1
        #k should only be able to be in value between 1 and 33
        if not (1 <= k <= 33) or not isinstance(k, int):
            raise ValueError(f"Order can only have integer values between 1 and 33. Current value of is {k}")


        CodeWord = CodeWord[5:]
        
        decoded_values = []

        #Loops trough the code word to get all values in the code word
        while len(CodeWord) > 0:
            A = 0
            #If S is true the output should be negative
            S = False
            value = ""
            
            #Checks if the data is signed
            if self.sign:
                #Checks if the MSB is "1", indicating that the value should be negative.
                if CodeWord[0] == "1":
                    #Sets S to True if the output should be negative
                    S = True
                #Removes the MSB, signed bit, from the code word.
                #This way the rest of the code word can be handled as if it was unsigned
                CodeWord = CodeWord[1:]

            
            #Decodes the unary code.
            #Unary code represents a interger value as a set of "1":s followed by a "0".
            #By incrementing A by 1 if the MSB is a one then moving the codeword one step and checking again
            #all "1" will increment A until a "0" is MSB indicating that the unary code have been decoded. 
            while CodeWord[0] == "1":
                A += 1
                CodeWord = CodeWord[1:]

            
            #After the unary code have been uncoded the remaining code will be
            #a "0" as MSB followed by the last k-bits from the original binary value as LSB
            #By looping thorugh the codeword and removing k bits to the current value being decoded
            #The last bits in the code word for the current value can be decoded
            for j in range(k):
                CodeWord = CodeWord[1:]
                value += CodeWord[0]
            #Since there is a 0 separating the MSB with the LSB 1 more bit needs to be removed for the current value in the codeword
            CodeWord = CodeWord[1:]

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

    
    def RleDecoder(self, CodeWord):
        
        DecodedValues = []
        #Loops trough all the enocded binary values with a while llop
        while len(CodeWord) > 0:
            #Raise error if there is not enough length left of code_residuals for 1 code_word
            if len(CodeWord) < 33:
                raise ValueError(f"Code_word length is {len(CodeWord)}, should  never be lower than 33")


            #The first bit in each code word is the sign bit
            #This is saved as s and then the code_residuals is stepped one step
            s = CodeWord[0]
            CodeWord = CodeWord[1:]

            #The next 24 bits represents the value that have been encoded
            #Once they been saved 24 steps trough the code_residuals are taken
            RleValue = CodeWord[:24]
            CodeWord = CodeWord[24:]

            #The next 8 bits represent how many times the value was repeated
            #Once it been saved 8 steps is taken in the code_residuals
            RleCount = CodeWord[:8]
            CodeWord = CodeWord[8:]

            #The value that have been encoded is converted to int
            IntRelValue = int(RleValue, 2)

            #If the sign bit is "1" the value is converted to negative
            if s == "1":
                IntRelValue = -IntRelValue

            #A for loop is used to append as many values as needed
            #The RleCount value is increased by 1 because even though
            #a value never was reapeted it occured once
            
            for reapeats in range(1 + int(RleCount, 2)):
                DecodedValues.append(IntRelValue)
        
        #Uppdate memory
        #Copy the decoded values to assign them to the memory array later
        RleCopy = DecodedValues.copy()
        #The last for values will be the memory array in reverse order
        
        new_memory = []
        if len(RleCopy) > 3:
            reversed_memory = RleCopy[len(RleCopy)-4:]
        #In the case that there is to few values among the decoded values pad the memory array with 0:s
        else:
            reversed_memory = RleCopy
            while len(new_memory) < 3:
                reversed_memory.insert(0,0)
        for i in reversed(reversed_memory):
            new_memory.append(i)


        #Assign the new_memory to memory
        return DecodedValues, new_memory


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


    def ShortenDecoder(self, Residuals, Order, memoryOut):
        RecreatedValues = []
        for residual in Residuals:
            if Order == 0:
                #If order = 0 preditiction is allways 0
                prediciton = 0

            else:
                #Calculate the prediciton from memory and cofficents
                prediciton = sum( np.array(memoryOut[:Order]) * np.array(self.ShortenCofficents[Order]) )

            #Recreate the original value by adding prediciton and residual value
            RecreatedValue = prediciton + residual

            #Update the memory by stepping all values one step and setting the first memory slot to the recreated value
            new_memory = [RecreatedValue]
            memoryOut = new_memory + memoryOut[:-1]

            #Save the recreated value
            RecreatedValues.append(RecreatedValue)

        return RecreatedValues, memoryOut


    def ShortenPredictIn(self, memoryIn):
        #Predict shorten for order 0-4
        ShortenPredictions = [0]
        for i in range(1,5):

            ShortenPredictions.append(sum( np.array(memoryIn[:i]) * np.array(self.ShortenCofficents[i]) ))

        #All memory slots are stepped one step back and the oldest memory is dropped
        new_memory = [0]
        new_memory += memoryIn[:-1]

        return ShortenPredictions, new_memory
    

    def AdjacentPredictIn(self, CurrentInput, CurrentPrediction):
        #Calculate the residual by taking the current input and subtracting the residual
        CurrentResidual = CurrentInput - CurrentPrediction

        #Crate a new prediction by taking the current mic value, the next mic will be predicted with the current mic value
        NewPrediction = CurrentInput

        return CurrentResidual, NewPrediction
    

    def AdjacentDecoder(self, prediction, residual, memory):
        

        #Recreate the original input value by adding prediciton and residual
        DecodedValue = prediction + residual

        #Update memory
        new_memory = [DecodedValue] + memory[:-1]
            

        return DecodedValue, new_memory

       
    def FirstAdjacentDecoder(self, residual, memory):
        Firstpredict = (sum( np.array(memory[:self.AdjacentOrder]) * np.array(self.ShortenCofficents[self.AdjacentOrder]) ))
        FirstDecodedValue = Firstpredict + residual
        new_memory = [FirstDecodedValue] + memory[:-1]

        return FirstDecodedValue, new_memory



