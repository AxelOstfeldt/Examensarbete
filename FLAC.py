import numpy as np
import math
from Rice import RiceCoding



class FLAC:

    def __init__(self, LpcOrder):
        self.LpcOrder = LpcOrder
        self.ShortCoff = [[0],[1],[2, -1],[3, -3, 1],[4,-6,4,-1]]


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
        
            


        
        return valueChoice, np.binary_repr(k_Choice,5), np.binary_repr(codeChoice,6), memory, LpcCoffChoosen

    
    def Out(self, code_residuals, memory, k_value, code_choose, LpcCoff):
        DecodedValues = []#Array to save decoded values
        k_value = int(k_value,2)
        code_choose = int(code_choose,2)
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
            #In cases where RLE encoding is not used, the resiudals have been encoded using Rice codes
            #Decodes the Residuals with Rice.Decode
            Rice_decoder = RiceCoding(k_value, True)
            Residuals = Rice_decoder.Decode(code_residuals)
            #The Shorten order will be 1 less than code_choose since code_choice 0 is for RLE
            ShortenOrder = code_choose - 1
            #The LPC order will be 5 less than code_choose since code_choice 0 is for RLE and 1-5 is for Shorten
            CurrentLpcOrder = code_choose - 5

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
        return DecodedValues, memory
                

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

        




#Test FLAC out
if 1 < 0:
    LPC_Order = 9
    FLAC_prediction = FLAC(LPC_Order)

    testInput = [1,3,5,7,9,8,9,10,9,20,9,21,9,22,9]

    if LPC_Order > 4:
        testMemory = [0]*LPC_Order
    else:
        testMemory = [0]*4

    Encoded_inputs, k_value, Encoding_choice, mem, LPC_Cofficents = FLAC_prediction.In(testInput, testMemory)

    print("k_value: ", k_value)
    print("Encoding choice: ", Encoding_choice)

    int_choice = int(Encoding_choice, 2)
    if LPC_Order > 4:
        mem_out = [0]*LPC_Order
    else:
        mem_out = [0]*4

    

    decodedInputs, mem_out = FLAC_prediction.Out(Encoded_inputs, mem_out, k_value, Encoding_choice, LPC_Cofficents)

    print("Original input = ",testInput)
    print("Decoded inputs = ", decodedInputs)
    print("mem_out = ", mem_out)



#Test to see that FLAC can perform aswell as Shorten and LPC
#Aswell as test output from FLAC
from Shorten import Shorten
from LPC import LPC
if 1 < 0:

    LPC_Order = 8
    FLAC_prediction = FLAC(LPC_Order)

    testInput = [1,2,3,4,5,5,5,5,5,5,5,6,7,8,9,9,9,9]

    if LPC_Order > 4:
        testMemory = [0]*LPC_Order
    else:
        testMemory = [0]*4

    Encoded_inputs, k_value, Encoding_choice, mem, LPC_Cofficents = FLAC_prediction.In(testInput, testMemory)
    #print("Encoded_inputs: ", Encoded_inputs)
    #print("k_value: ", k_value)
    #print("Encoding choice: ", Encoding_choice)
    #print("New memory: ", mem)
    #print("LPC cofficents from FLAC:")
    for i in range(len(LPC_Cofficents)):
        i
        
        #print("LPC order ",i+1,": ",LPC_Cofficents[i])

    S_order = 3
    L_order = 1
    for i in range(1, 8):
        L_order = i
        S_memory = [0]*S_order
        L_memory = [0]*L_order
        Shorten_predictor = Shorten(S_order)
        LPC_predictor = LPC(L_order)

        res_s, mem_s, pred_s = Shorten_predictor.In(testInput, S_memory)
        cof_l, res_l, mem_l, pred_l = LPC_predictor.In(testInput, L_memory)
        for j in range(L_order):
            curr_flac_cofs = LPC_Cofficents[i-1]
            if cof_l[j] != curr_flac_cofs[j]:
                print("Wrong cofficents at: ", cof_l[j],"=! ", curr_flac_cofs[j])


        #Calculates the ideal k_vaule for the LPC residuals
        abs_res = np.absolute(res_s)
        abs_res_avg = np.mean(abs_res)
        #if abs_res_avg is less than 4.7 it would give a k value less than 1.
        #k needs tobe a int > 1 and therefore if abs_res_avg < 5 k is set to 1
        #OBS. 4.7 < abs_res_avg < 5 would be rounded of to k=1 so setting the limit to 5 works well
        if abs_res_avg > 5:
            k_s = int(round(math.log(math.log(2,10) * abs_res_avg,2)))
        else:
            k_s = 1

        #Calculates the ideal k_vaule for the LPC residuals
        abs_res = np.absolute(res_l)
        abs_res_avg = np.mean(abs_res)
        #if abs_res_avg is less than 4.7 it would give a k value less than 1.
        #k needs tobe a int > 1 and therefore if abs_res_avg < 5 k is set to 1
        #OBS. 4.7 < abs_res_avg < 5 would be rounded of to k=1 so setting the limit to 5 works well
        if abs_res_avg > 5:
            k_l = int(round(math.log(math.log(2,10) * abs_res_avg,2)))
        else:
            k_l = 1


        #calculates the Rice code word for the residual
        code_word =""
        for q in range(len(res_s)):
            
            Rice_coder = RiceCoding(k_s, True)
            n = int(res_s[q])
            kodOrd = Rice_coder.Encode(n)
            code_word += kodOrd
        #print("Lenght for Shorten order ",S_order," = ",len(code_word))


        #calculates the Rice code word for the residual
        code_word =""
        for q in range(len(res_l)):
            Rice_coder = RiceCoding(k_l, True)
            n = int(res_l[q])
            kodOrd = Rice_coder.Encode(n)
            code_word += kodOrd
        print("Lenght for LPC order ",L_order," = ",len(code_word))

    

    
    #auto_Corr = FLAC_prediction.autocorrelation(testInput, 2)#Works
    #print(auto_Corr)

    #Lpc_coff = FLAC_prediction.LpcCoefficentsCalc(testInput)#Works
    #print(Lpc_coff[8])

    RleCode, ShortResiduals, LpcResiduals, memory, LpcCoff, SPred, LPred = FLAC_prediction.ResidualCalculation(testInput,testMemory)

    for i in range(len(LpcResiduals)):
        print((LpcResiduals[i]))
    

    

    



