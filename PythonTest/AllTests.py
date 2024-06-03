import math
import numpy as np
import matplotlib.pyplot as plt
import time
import sys
import os
#Hem dator:
#sys.path.insert(0, 'C:\\Users\\axelo\\OneDrive\\Skrivbord\\Exjobb\\GIT\\Examensarbete\\')
#Exjobb dator:
#sys.path.insert(0, '/home/luigi/Desktop/GIT/Examensarbete')#Change this path to where all the files with the functions are stored

# Add the parent directory to import compression classes
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)
from Rice import RiceCoding
from Golomb import GolombCoding
from Shorten import Shorten
from LPC import LPC
from FLAC import FLAC
from Adjacent import Adjacent
from FlacModified import FlacModified
from AdjacentAndShorten import DoubleCompression
from LPC_Meta import MetaLPC
from FLAC_Meta import MetaFLAC
from ShortenMeta import ShortenMeta
from AdjacentMeta import MetaAdjacent




class TestFunctions:

    def __init__(self, TestNr):
        self.TestNr = TestNr


    #TestInfo function prints info for what each test does
    def TestInfo(self):
        #Raw data tests
        if self.TestNr == 1:
            print('Test 1. This test plots data for specific microphones.')
        elif self.TestNr == 2:
            print('Test 2. Compression rate when using Rice codes on raw data.')
        elif self.TestNr == 3:
            print('Test 3. Compression rate when using Golomb codes on raw data.')

        #Shorten tests
        elif self.TestNr == 4:
            print('Test 4. Compare original input with recreated values when using Shorten with Rice codes to see if all values have been recreated correctly.')
        elif self.TestNr == 5:
            print('Test 5. Compare original input with recreated values when using Shorten with Golomb codes to see if all values have been recreated correctly.')
        elif self.TestNr == 6:
            print('Test 6. Plots compression rate for differnte k-values when using Shorten with Rice codes.')
        elif self.TestNr == 7:
            print('Test 7. Compression rate using Shorten with Rice codes.')
        elif self.TestNr == 8:
            print('Test 8. Average speed to recreate values from codewords using Shorten with Rice codes.')
        elif self.TestNr == 9:
            print('Test 9. Average speed to recreate values from codewords using Shorten with Golomb codes.')

        #LPC tests
        elif self.TestNr == 10:
            print('Test 10. Compare original input with recreated values when using LPC with Rice codes to see if all values have been recreated correctly.')
        elif self.TestNr == 11:
            print('Test 11. Compare original input with recreated values when using LPC with Golomb codes to see if all values have been recreated correctly.')
        elif self.TestNr == 12:
            print('Test 12. Plots compression rate for differnte k-values when using LPC with Rice codes.')
        elif self.TestNr == 13:
            print('Test 13. Compression rate using LPC with Rice codes.')
        elif self.TestNr == 14:
            print('Test 14. Average speed to recreate values from codewords using LPC with Rice codes.')
        elif self.TestNr == 15:
            print('Test 15. Average speed to recreate values from codewords using LPC with Golomb codes.')

        #FLAC tests
        elif self.TestNr == 16:
            print('Test 16. Test compression rate using FLAC.')
        elif self.TestNr == 17:
            print('Test 17. Average speed to recreate values from codewords using FLAC.')

        #Adjacent tests
        elif self.TestNr == 18:
            print('Test 18. Compare original input with recreated values when using Adjacent with Rice codes to see if all values have been recreated correctly.')
        elif self.TestNr == 19:
            print('Test 19. Compare original input with recreated values when using Adjacent with Golomb codes to see if all values have been recreated correctly.')
        elif self.TestNr == 20:
            print('Test 20. Plots compression rate for differnte k-values when using Adjacent with Rice codes.')
        elif self.TestNr == 21:
            print('Test 21. Compression rate using Adjacent with Rice codes.')
        elif self.TestNr == 22:
            print('Test 22. Average speed to recreate values from codewords using Adjacent with Rice codes.')
        elif self.TestNr == 23:
            print('Test 23. Average speed to recreate values from codewords using Adjacent with Golomb codes.')

        #FLAC-Modified tests
        elif self.TestNr == 24:
            print('Test 24. Test compression rate using FLAC-Modifed.')
        elif self.TestNr == 25:
            print('Test 25. Average speed to recreate values from codewords using FLAC-Modified.')

        #DoubleCompression test
        elif self.TestNr == 26:
            print('Test 26. Test compression rate using DoubleCompression.')
        elif self.TestNr == 27:
            print('Test 27. Average speed to recreate values from codewords using DoubleCompression.')

        else:
            raise ValueError(f"Test {self.TestNr} does not exist, please select a test between 1 and 27")
        
        pass

        
    def DataSelect(self, OrgData, dBlocks: int = 20, startMic: int = 64, endMic: int = 127):
        if startMic < 0 or endMic > 255 or endMic < startMic:
            raise ValueError(f"The selected mics have to be values between 0 and 255, the starting microphone have to be less or equal to the ending microphone.")
        #Array to store the selected data
        SelectedTestData = []
        #loop through all datablocks that is going to be used for testing
        for block in range(dBlocks):
            #Select the data from the current datablock
            CurrentDataBlock = OrgData[block]
            #Save the datafrom the desired mics
            SelectedTestData.append(CurrentDataBlock[startMic:endMic+1,:])
        
        return SelectedTestData
    

    def StartTest(self, OriginalData, datablocks: int = 20):
        #Raw data tests
        FlagTry = True
        if self.TestNr == 1:
            #Select what mics are going to be plotted
            start_mic = input('Select what microhpone to start plotting from: ')
            #Check if the start_mic value choosen can be converted to int
            try:
                int(start_mic)
            #If the value can not be converted to int set the FlagTry to false
            except ValueError:
                FlagTry = False

            if FlagTry:
                start_mic = int(start_mic)
            else:
                raise ValueError(f"The microphone value selected needs to be an integer.")
            

            end_mic = input('Select what microhpone to end plotting on (if only one mic is desired to plot choose the same value as start microphone): ')
            #Check if the end_mic value choosen can be converted to int
            try:
                int(end_mic)
            #If the value can not be converted to int set the FlagTry to false
            except ValueError:
                FlagTry = False

            if FlagTry:
                end_mic = int(end_mic)
            else:
                raise ValueError(f"The microphone value selected needs to be an integer.")
            
            #Store the data from the desired microphones and datablocks in TestData
            TestData = self.DataSelect(OriginalData, datablocks, start_mic, end_mic)

            
            #loop through all selected microphones
            for microhpone in range(end_mic + 1 - start_mic):
                micPlot = []
                #loop thorugh all selected datablocks
                for block in range(datablocks):
                    #Grab the data from the current datablock
                    TestDataBlock = TestData[block]
                    #Grab the data from the selected mic in the current datablock
                    CurrentTestData = TestDataBlock[microhpone,:]
                    #loop through all 256 samples in the datablock
                    for sample in CurrentTestData:
                        #Store each sample in the micPlot array
                        micPlot.append(sample)

                #Plot the data, one plot per microphone
                figure_title = "Mic #" + str(microhpone + start_mic)
                plt.figure(figure_title, layout='constrained')
                plt.plot(micPlot)
                plt.show()


        elif self.TestNr == 2:
            #Select what mics are going to be compressed
            start_mic = input('Select what microhpone to start plotting from: ')
            #Check if the start_mic value choosen can be converted to int
            try:
                int(start_mic)
            #If the value can not be converted to int set the FlagTry to false
            except ValueError:
                FlagTry = False

            if FlagTry:
                start_mic = int(start_mic)
            else:
                raise ValueError(f"The microphone value selected needs to be an integer.")
            

            end_mic = input('Select what microhpone to end plotting on (if only one mic is desired to plot choose the same value as start microphone): ')
            #Check if the end_mic value choosen can be converted to int
            try:
                int(end_mic)
            #If the value can not be converted to int set the FlagTry to false
            except ValueError:
                FlagTry = False

            if FlagTry:
                end_mic = int(end_mic)
            else:
                raise ValueError(f"The microphone value selected needs to be an integer.")
            
            

            
            #Store the data from the desired microphones and datablocks in TestData
            TestData = self.DataSelect(OriginalData, datablocks, start_mic, end_mic)

            cr_array = []
            #loop thorugh all datablocks and select the data for the current datablock
            for TestDataBlock in TestData:
                #loop thorugh all microphones and select the data for the current microphone in the current datablock
                for microhpone in range(end_mic + 1 - start_mic):
                    CurrentTestData = TestDataBlock[microhpone,:].copy()
                    #Codeword starts with 5 bits to represent the metadata needed to decode it. This represent the k-value.
                    CodeWord = np.binary_repr(0,5)
                    #Uncoded word to story 24 bit representation of input values
                    UncodedWord =""
                    #Calculates the ideal k_vaule for the data
                    abs_res = np.absolute(CurrentTestData.copy())
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

                   
                    
                    #loop thorugh all 256 samples
                    for sample in range(256):
                         #Rice code the input data and stor it in CodeWord
                        Rice_coder = RiceCoding(k, True)
                        n = int(CurrentTestData[sample])
                        kodOrd = Rice_coder.Encode(n)
                        CodeWord += kodOrd
                        #Also store the binary value of data in UncodedWord
                        UncodedWord += np.binary_repr(abs(CurrentTestData[sample]),24)

                    #Calculate compression rate by dividing the length of the codeword with the uncoded data
                    cr = len(CodeWord) / len(UncodedWord)
                    cr_array.append(cr)

            #Calculate the average CR
            avg_cr = sum(cr_array)/len(cr_array)

            print("Average compression rate is, cr = ", avg_cr)
                       

        elif self.TestNr == 3:
            #Select what mics are going to be compressed
            start_mic = input('Select what microhpone to start plotting from: ')
            #Check if the start_mic value choosen can be converted to int
            try:
                int(start_mic)
            #If the value can not be converted to int set the FlagTry to false
            except ValueError:
                FlagTry = False

            if FlagTry:
                start_mic = int(start_mic)
            else:
                raise ValueError(f"The microphone value selected needs to be an integer.")
            

            end_mic = input('Select what microhpone to end plotting on (if only one mic is desired to plot choose the same value as start microphone): ')
            #Check if the end_mic value choosen can be converted to int
            try:
                int(end_mic)
            #If the value can not be converted to int set the FlagTry to false
            except ValueError:
                FlagTry = False

            if FlagTry:
                end_mic = int(end_mic)
            else:
                raise ValueError(f"The microphone value selected needs to be an integer.")
            
            

            
            #Store the data from the desired microphones and datablocks in TestData
            TestData = self.DataSelect(OriginalData, datablocks, start_mic, end_mic)
            

            cr_array = []
            #loop thorugh all datablocks and select the data for the current datablock
            for TestDataBlock in TestData:

                #loop thorugh all microphones and select the data for the current microphone in the current datablock
                for microhpone in range(end_mic + 1 - start_mic):
                    CurrentTestData = TestDataBlock[microhpone,:].copy()
                    #Codeword starts with 2⁵=32 bits to represent the metadata needed to decode it. This represent the m-value.
                    CodeWord = np.binary_repr(0,32)
                    #Uncoded word to story 24 bit representation of input values
                    UncodedWord =""
                    #Calculates the ideal k_vaule for the data
                    abs_res = np.absolute(CurrentTestData.copy())
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

                    #Calculate m value from k value by taking 2^k
                        
                    m = pow(2,k)
                   
                    
                    #loop thorugh all 256 samples
                    for sample in range(256):
                         #Golomb code the input data and stor it in CodeWord
                        Golomb_coder = GolombCoding(m, True)
                        n = int(CurrentTestData[sample])
                        kodOrd = Golomb_coder.Encode(n)
                        CodeWord += kodOrd
                        #Also store the binary value of data in UncodedWord
                        UncodedWord += np.binary_repr(abs(CurrentTestData[sample]),24)

                    #Calculate compression rate by dividing the length of the codeword with the uncoded data
                    cr = len(CodeWord) / len(UncodedWord)
                    cr_array.append(cr)

            #Calculate the average CR
            avg_cr = sum(cr_array)/len(cr_array)

            print("Average compression rate is, cr = ", avg_cr)


        #Shorten tests
        elif self.TestNr == 4:
            #Select what mics are going to be plotted
            start_mic = input('Select what microhpone to plot: ')
            #Check if the start_mic value choosen can be converted to int
            try:
                int(start_mic)
            #If the value can not be converted to int set the FlagTry to false
            except ValueError:
                FlagTry = False

            if FlagTry:
                start_mic = int(start_mic)
            else:
                raise ValueError(f"The microphone value selected needs to be an integer.")
            
            #Store the data from the desired microphone and datablocks in TestData
            TestData = self.DataSelect(OriginalData, datablocks, start_mic, start_mic)

            ShortenOrder = input('Select Shorten order (0-3): ')
            #Check if the ShortenOrder value choosen can be converted to int
            try:
                int(ShortenOrder)
            #If the value can not be converted to int set the FlagTry to false
            except ValueError:
                FlagTry = False

            if FlagTry:
                ShortenOrder = int(ShortenOrder)
            else:
                raise ValueError(f"The Shorten order selected needs to be an integer.")
            
            ShortenAlgorithm = ShortenMeta(ShortenOrder)
            
            #Create memory array with appropriate length for selected order
            if ShortenOrder == 0:
                MemoryIn = []
                MemoryOut = []
            else:
                MemoryIn = [0]*ShortenOrder
                MemoryOut = [0]*ShortenOrder

            #Array to store all CodeWords
            CodeWords = []

            
            for CurrentBlock in range(len(TestData)):
                #Use shorten to create the code words
                CurrentTestData = TestData[CurrentBlock]
                CurrentTestData = CurrentTestData[0]#I belive this is needed because of choosing the first mic even tho it is only 1 mic
                CodeWord, MemoryIn = ShortenAlgorithm.In(CurrentTestData.copy(), MemoryIn)
                #Save each codeword
                CodeWords.append(CodeWord)

            allCorrect = 0
            #loop thorugh all CodeWords, there will be one codeword for every datablock
            for i in range(len(CodeWords)):
                zero = []
                CodeWord = CodeWords[i]
                #Decode the codeword fo every datablock
                DecodedData, MemoryOut = ShortenAlgorithm.Out(CodeWord, MemoryOut)
                #Grab the original data from every datablock
                CurrentInputData = TestData[i]
                CurrentInputData = CurrentInputData[0]#I belive the first mic needs to be choosen even though it is only 1 mic


                #Go thorugh all samples in every datablock
                for sample in range(len(CurrentInputData)):
                    #Calculate the difference between the original data and decoded data,
                    #This should be =0 if every thing has been done correctly
                    currentZero = CurrentInputData[sample] - DecodedData[sample]
                    zero.append(currentZero)
                    
                    #If the difference is not equal to 0 the code repports that there have been an error
                    if currentZero != 0:
                        allCorrect += 1
                        print("Failed to decode value at datablock ",i,"sample #",sample)

                #Plot the original, recretated, and the differential between them
                #There will be one plot for every datablock
                fig = plt.figure(i, layout = 'constrained')

                ax = fig.add_subplot(211)
                plt.plot(CurrentInputData, 'b', label = 'Original values')
                plt.plot(DecodedData, 'r-.', label = 'Decoded values')

                plt.legend(fontsize=25, loc = 'upper right')
                plt.yticks(fontsize=20)
                plt.xticks(fontsize=20)

                ax = fig.add_subplot(212)
                plt.plot(zero, label = 'Original values - Decoded values')

                plt.legend(fontsize=25, loc = 'upper right')
                plt.yticks(fontsize=20)
                plt.xticks(fontsize=20)
                
                plt.show()

            #If all values have been recreated correctly this will be printed out, 
            #else print out how many was failed to be decoded
            if allCorrect == 0:
                print("All values where decoded succesfully")
            else:
                print("Failed decoding ", allCorrect,"values")

        
        elif self.TestNr == 5:
            #Select what mics are going to be plotted
            start_mic = input('Select what microhpone to plot: ')
            #Check if the start_mic value choosen can be converted to int
            try:
                int(start_mic)
            #If the value can not be converted to int set the FlagTry to false
            except ValueError:
                FlagTry = False

            if FlagTry:
                start_mic = int(start_mic)
            else:
                raise ValueError(f"The microphone value selected needs to be an integer.")
            
            #Store the data from the desired microphone and datablocks in TestData
            TestData = self.DataSelect(OriginalData, datablocks, start_mic, start_mic)

            ShortenOrder = input('Select Shorten order (0-3): ')
            #Check if the ShortenOrder value choosen can be converted to int
            try:
                int(ShortenOrder)
            #If the value can not be converted to int set the FlagTry to false
            except ValueError:
                FlagTry = False

            if FlagTry:
                ShortenOrder = int(ShortenOrder)
            else:
                raise ValueError(f"The Shorten order selected needs to be an integer.")
            
            ShortenAlgorithm = Shorten(ShortenOrder)
            
            #Create memory array with appropriate length for selected order
            if ShortenOrder == 0:
                MemoryIn = []
                MemoryOut = []
            else:
                MemoryIn = [0]*ShortenOrder
                MemoryOut = [0]*ShortenOrder

            #Array to store all CodeWords
            CodeWords = []
            #Array to store m-values for encoding/decoding
            m_array = []
            for CurrentBlock in range(len(TestData)):
                #Use shorten to create the code words
                CurrentTestData = TestData[CurrentBlock]
                CurrentTestData = CurrentTestData[0]#I belive this is needed because of choosing the first mic even tho it is only 1 mic
                #Calculate the residuals using Shorten
                residuals, MemoryIn, predictions = ShortenAlgorithm.In(CurrentTestData.copy(), MemoryIn)
                #Calculate the ideal m value, by first calculating the ideal k value and taking 2^k
                #Calculates the ideal k_vaule for the data
                abs_res = np.absolute(residuals)
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

                #Calculate m value from k value by taking 2^k
                m = pow(2,k)
                #Store the m-value
                m_array.append(m)


               
                #Golomb codes the residuals from shorten and saves the code word in code_word
                CodeWord = ""
                for i in range(len(residuals)):
                    Golomb_coder = GolombCoding(m, True)
                    n = int(residuals[i])
                    kodOrd = Golomb_coder.Encode(n)
                    CodeWord += kodOrd

                #Saves Rice coded residuals
                CodeWords.append(CodeWord)

            #Loops through all codewords to decode them and recreate all values, and compare them to the original values
            #There is one codeword for every datablock
            allCorrect = 0
            for i in range(len(CodeWords)):
                zero = []
                #Grab the current codeword
                CodeWord = CodeWords[i]
                #Grab the m-value to decode the codeword
                m = m_array[i]
                #Decodes the residuals from the Golomb code
                Golomb_coder = GolombCoding(m, True)
                uncoded_residuals = Golomb_coder.Decode(CodeWord)
                #Decode the codeword fo every datablock
                DecodedData, MemoryOut, predictions = ShortenAlgorithm.Out(uncoded_residuals, MemoryOut)
                #Grab the original data from every datablock
                CurrentInputData = TestData[i]
                CurrentInputData = CurrentInputData[0]#I belive the first mic needs to be choosen even though it is only 1 mic


                #Go thorugh all samples in every datablock
                for sample in range(len(CurrentInputData)):
                    #Calculate the difference between the original data and decoded data,
                    #This should be =0 if every thing has been done correctly
                    currentZero = CurrentInputData[sample] - DecodedData[sample]
                    zero.append(currentZero)
                    
                    #If the difference is not equal to 0 the code repports that there have been an error
                    if currentZero != 0:
                        allCorrect += 1
                        print("Failed to decode value at datablock ",i,"sample #",sample)

                #Plot the original, recretated, and the differential between them
                #There will be one plot for every datablock
                fig = plt.figure(i, layout = 'constrained')

                ax = fig.add_subplot(211)
                plt.plot(CurrentInputData, 'b', label = 'Original values')
                plt.plot(DecodedData, 'r-.', label = 'Decoded values')

                plt.legend(fontsize=25, loc = 'upper right')
                plt.yticks(fontsize=20)
                plt.xticks(fontsize=20)

                ax = fig.add_subplot(212)
                plt.plot(zero, label = 'Original values - Decoded values')

                plt.legend(fontsize=25, loc = 'upper right')
                plt.yticks(fontsize=20)
                plt.xticks(fontsize=20)
                
                plt.show()

            #If all values have been recreated correctly this will be printed out, 
            #else print out how many was failed to be decoded
            if allCorrect == 0:
                print("All values where decoded succesfully")
            else:
                print("Failed decoding ", allCorrect,"values")


        elif self.TestNr == 6:
            #Select what mics are going to be plotted
            start_mic = input('Select what microhpone to use: ')
            #Check if the start_mic value choosen can be converted to int
            try:
                int(start_mic)
            #If the value can not be converted to int set the FlagTry to false
            except ValueError:
                FlagTry = False

            if FlagTry:
                start_mic = int(start_mic)
            else:
                raise ValueError(f"The microphone value selected needs to be an integer.")
            
            #Store the data from the desired microphone and datablocks in TestData
            TestData = self.DataSelect(OriginalData, datablocks, start_mic, start_mic)

            #Select startin k-value for the rice codes
            k_start = input('Select k-value to start compressing from: ')
            #Check if the k_start value choosen can be converted to int
            try:
                int(k_start)
            #If the value can not be converted to int set the FlagTry to false
            except ValueError:
                FlagTry = False

            if FlagTry:
                k_start = int(k_start)
                if k_start < 1:
                    raise ValueError(f"The k-value selected needs to be atleast 1.")

            else:
                raise ValueError(f"The k-value selected needs to be an integer.")
            
            #Select ending k-value for the rice codes
            k_stop = input('Select k_value to stop compressing at: ')
            #Check if the k_start value choosen can be converted to int
            try:
                int(k_stop)
            #If the value can not be converted to int set the FlagTry to false
            except ValueError:
                FlagTry = False

            if FlagTry:
                k_stop = int(k_stop)
                if k_stop < k_start:
                    raise ValueError(f"The k-value selected needs to be larger or equal to the starting k_value.")

            else:
                raise ValueError(f"The k-value selected needs to be an integer.")
            
            #crate array to store avg compression rates for all orders and k_values
            All_avg_cr_array = []
            #create array with all selected k_values
            k_array = []
            for k_values in range(k_start, k_stop+1):
                k_array.append(k_values)

            #Create array to store ideal k-value for each order
            k_ideal_array = [[],[],[],[]]

            #Array with memory for all orders of shorten
            MemorysIn=[[],[0],[0,0],[0,0,0]]
            #loop thorugh all orders of shorten
            for order in range(4):
                #Array to store compression rate for current order
                cr_array = []
                #loop thorugh all datablocks
                for block in range(len(TestData)):
                    #Grab the testdata for the current block
                    CurrentTestData = TestData[block]
                    #Need to grab from the first mic as well, even though it is only 1 mic
                    CurrentTestData = CurrentTestData[0]

                    #Calcualate the residuals with the shorten algorithm
                    ShortenAlgorithm = Shorten(order)
                    residual,  MemorysIn[order], predict = ShortenAlgorithm.In(CurrentTestData, MemorysIn[order])

                    #Calculates the ideal k_vaule acording to Rice Theory
                    abs_res = np.absolute(residual.copy())
                    abs_res_avg = np.mean(abs_res)
                    #if abs_res_avg is less than 4.7 it would give a k value less than 1.
                    #k needs tobe a int > 1 and therefore if abs_res_avg < 5 k is set to 1
                    #OBS. 4.7 < abs_res_avg < 5 would be rounded of to k=1 so setting the limit to 5 works well
                    if abs_res_avg > 5:
                        k_ideal = int(round(math.log(math.log(2,10) * abs_res_avg,2)))
                    else:
                        k_ideal = 1

                    #Appends the ideal k vaule in the array matching the correct Shorten order
                    k_ideal_array[order].append(k_ideal)

                    #loop thorug all k-values
                    for i in range(len(k_array)):
                        CodeWord = ""
                        if i == 0:
                            UncodedWord = ""
                        k = k_array[i]
                        for q in range(len(residual)):
                            #Rice code the residual for all k_values
                            Rice_coder = RiceCoding(k, True)
                            n = int(residual[q])
                            kodOrd = Rice_coder.Encode(n)
                            CodeWord += kodOrd
                            if i == 0:
                                #Represent the uncdoed word in 24 bits
                                UncodedWord += np.binary_repr(abs(n),24)
                        #calculate the compression rate for the current CodeWord
                        cr = len(CodeWord) / len(UncodedWord)

                        #Save the compression rate in an array, with cr_for specific k_values grouped together
                        if block == 0:
                            cr_array.append([])
                        cr_array[i].append(cr)
                    
                

                #Calculate the average cr for all k-value used for the current order
                avg_cr_array = []
                for current_cr_array in cr_array:
                    avg_cr = sum(current_cr_array)/len(current_cr_array)
                    avg_cr_array.append(avg_cr)

                #Save the avg cr values from the current order
                All_avg_cr_array.append(avg_cr_array)

            
            #Figure to plot all k-values in
            plt.figure("Compression order for differente k-values using Shorten with Rice codes", layout = 'constrained')
            plt_colors = ['yo', 'ro', 'bo', 'go']


            #Print the k_array, ideal k-value for each order, and average compression rate for allorders
            print("k-values: ",k_array)
            print("")
            for orders in range(4):
                print("Average ideal k-value using Shorten order ",orders," (acording to Rice theory, rounded to closest int): ", round(sum(k_ideal_array[orders])/len(k_ideal_array[orders])))
                print("Average compression rate using Shorten order ",orders,": ",All_avg_cr_array[orders])
                print("")
                plt_label = 'Order ' + str(orders)
                plt.plot(k_array, All_avg_cr_array[orders], plt_colors[orders], label = plt_label)

            plt.yticks(fontsize=25)
            plt.xticks(fontsize=25)
            plt.xlabel("k-value", fontsize=30)
            plt.ylabel("Average compression ratio", fontsize=30)
            plt.legend(fontsize=30, loc = 'upper right')
            plt.show()


        elif self.TestNr == 7:
            #Select what mics are going to be compressed
            start_mic = input('Select what microhpone to start from: ')
            #Check if the start_mic value choosen can be converted to int
            try:
                int(start_mic)
            #If the value can not be converted to int set the FlagTry to false
            except ValueError:
                FlagTry = False

            if FlagTry:
                start_mic = int(start_mic)
            else:
                raise ValueError(f"The microphone value selected needs to be an integer.")
            

            end_mic = input('Select what microhpone to end at (if only one mic is desired choose the same value as start microphone): ')
            #Check if the end_mic value choosen can be converted to int
            try:
                int(end_mic)
            #If the value can not be converted to int set the FlagTry to false
            except ValueError:
                FlagTry = False

            if FlagTry:
                end_mic = int(end_mic)
            else:
                raise ValueError(f"The microphone value selected needs to be an integer.")
            
            

            
            #Store the data from the desired microphones and datablocks in TestData
            TestData = self.DataSelect(OriginalData, datablocks, start_mic, end_mic)



            ShortenOrder = input('Select Shorten order (0-3): ')
            #Check if the ShortenOrder value choosen can be converted to int
            try:
                int(ShortenOrder)
            #If the value can not be converted to int set the FlagTry to false
            except ValueError:
                FlagTry = False

            if FlagTry:
                ShortenOrder = int(ShortenOrder)
            else:
                raise ValueError(f"The Shorten order selected needs to be an integer.")
            
            ShortenAlgorithm = ShortenMeta(ShortenOrder)


            #Create MemoryArray
            Memorys = []

            

            #Array to store all compression rates
            cr_array = []

            
            for CurrentBlock in range(len(TestData)):
                #Use shorten to create the code words
                CurrentTestData = TestData[CurrentBlock]
                for mic in range(end_mic + 1 - start_mic):
                    if CurrentBlock == 0:
                        #Create memory array with appropriate length for selected order
                        if ShortenOrder == 0:
                            Memorys.append([])
                            
                        else:
                            Memorys.append([0]*ShortenOrder)

                    #Create codeword for current mic/datablock
                    CurrentTestDataMic = CurrentTestData[mic]
                    CodeWord, Memorys[mic] = ShortenAlgorithm.In(CurrentTestDataMic.copy(), Memorys[mic])

                    #Create binary uncoded word for current input, original value represented in 24 bits
                    UncodedWord = ""
                    for sample in CurrentTestDataMic:
                        UncodedWord += np.binary_repr(sample, 24)

                    #Calculate CR for current codeword
                    cr = len(CodeWord) / len(UncodedWord)
                    #Save Cr in array
                    cr_array.append(cr)

            #Calculate average CR for all codewords
            avg_cr = sum(cr_array) / len(cr_array)

            print("Average compression rate using Shorte order ",ShortenOrder," is, CR = ",avg_cr)
                        

        elif self.TestNr == 8:
            #Select what mics are going to be compressed
            start_mic = input('Select what microhpone to start from: ')
            #Check if the start_mic value choosen can be converted to int
            try:
                int(start_mic)
            #If the value can not be converted to int set the FlagTry to false
            except ValueError:
                FlagTry = False

            if FlagTry:
                start_mic = int(start_mic)
            else:
                raise ValueError(f"The microphone value selected needs to be an integer.")
            

            end_mic = input('Select what microhpone to end at (if only one mic is desired choose the same value as start microphone): ')
            #Check if the end_mic value choosen can be converted to int
            try:
                int(end_mic)
            #If the value can not be converted to int set the FlagTry to false
            except ValueError:
                FlagTry = False

            if FlagTry:
                end_mic = int(end_mic)
            else:
                raise ValueError(f"The microphone value selected needs to be an integer.")
            
            

            
            #Store the data from the desired microphones and datablocks in TestData
            TestData = self.DataSelect(OriginalData, datablocks, start_mic, end_mic)



            ShortenOrder = input('Select Shorten order (0-3): ')
            #Check if the ShortenOrder value choosen can be converted to int
            try:
                int(ShortenOrder)
            #If the value can not be converted to int set the FlagTry to false
            except ValueError:
                FlagTry = False

            if FlagTry:
                ShortenOrder = int(ShortenOrder)
            else:
                raise ValueError(f"The Shorten order selected needs to be an integer.")
            
            ShortenAlgorithm = ShortenMeta(ShortenOrder)


            #Create MemoryArray
            MemorysIn = []
            MemorysOut = []

            

            #Array to store all CodeWords
            CodeWordArray = []



            
            
            for CurrentBlock in range(len(TestData)):
                #Use shorten to create the code words
                CurrentTestData = TestData[CurrentBlock]
                for mic in range(end_mic + 1 - start_mic):
                    if CurrentBlock == 0:
                        #Make sure all CodeWords are grouped by microphone
                        CodeWordArray.append([])

                        #Create memory array with appropriate length for selected order
                        if ShortenOrder == 0:
                            MemorysIn.append([])
                            MemorysOut.append([])
                            
                        else:
                            MemorysIn.append([0]*ShortenOrder)
                            MemorysOut.append([0]*ShortenOrder)

                    #Create codeword for current mic/datablock
                    CurrentTestDataMic = CurrentTestData[mic]
                    CodeWord, MemorysIn[mic] = ShortenAlgorithm.In(CurrentTestDataMic.copy(), MemorysIn[mic])

                    #Save Codeword in array
                    CodeWordArray[mic].append(CodeWord)

            #Array to store Decoding time
            TimeArray = []

            for i in range(datablocks):
                #Start time
                start_time = time.time()            
                for mic in range(end_mic + 1 - start_mic):
                        
            
                    #Grab all codewords for a specific microphone
                    CodeWordsMic = CodeWordArray[mic]

                    
     

                    #Select a codeword
                    CurrentCodeWord = CodeWordsMic[i]
                    
                    #Decode the codeword fo every datablock
                    DecodedData, MemorysOut[mic] = ShortenAlgorithm.Out(CurrentCodeWord, MemorysOut[mic])
                #Stop time
                stop_time = time.time()

                #Calculate totalt time
                total_time = stop_time - start_time
                
                #Store total time in array
                TimeArray.append(total_time)

            #Calculate average time
            avg_time = sum(TimeArray) / len(TimeArray)

            print("Average time (in seconds) to recreate a full datablock using Shorten order ", ShortenOrder, "with Rice codes is: ",avg_time," s")


        elif self.TestNr == 9:
            #Select what mics are going to be compressed
            start_mic = input('Select what microhpone to start from: ')
            #Check if the start_mic value choosen can be converted to int
            try:
                int(start_mic)
            #If the value can not be converted to int set the FlagTry to false
            except ValueError:
                FlagTry = False

            if FlagTry:
                start_mic = int(start_mic)
            else:
                raise ValueError(f"The microphone value selected needs to be an integer.")
            

            end_mic = input('Select what microhpone to end at (if only one mic is desired choose the same value as start microphone): ')
            #Check if the end_mic value choosen can be converted to int
            try:
                int(end_mic)
            #If the value can not be converted to int set the FlagTry to false
            except ValueError:
                FlagTry = False

            if FlagTry:
                end_mic = int(end_mic)
            else:
                raise ValueError(f"The microphone value selected needs to be an integer.")
            
            

            
            #Store the data from the desired microphones and datablocks in TestData
            TestData = self.DataSelect(OriginalData, datablocks, start_mic, end_mic)



            ShortenOrder = input('Select Shorten order (0-3): ')
            #Check if the ShortenOrder value choosen can be converted to int
            try:
                int(ShortenOrder)
            #If the value can not be converted to int set the FlagTry to false
            except ValueError:
                FlagTry = False

            if FlagTry:
                ShortenOrder = int(ShortenOrder)
            else:
                raise ValueError(f"The Shorten order selected needs to be an integer.")
            
            ShortenAlgorithm = Shorten(ShortenOrder)

            #Create MemoryArray
            MemorysIn = []
            MemorysOut = []

            #Array to store all CodeWords
            CodeWordArray = []

            #Array to store m-values
            m_array = []

            #Encode all input values
            for CurrentBlock in range(len(TestData)):
                #Use shorten to create the code words
                CurrentTestData = TestData[CurrentBlock]
                for mic in range(end_mic + 1 - start_mic):
                    if CurrentBlock == 0:
                        #Make sure all CodeWords and m_values are grouped by microphone
                        CodeWordArray.append([])
                        m_array.append([])


                        #Create memory array with appropriate length for selected order
                        if ShortenOrder == 0:
                            MemorysIn.append([])
                            MemorysOut.append([])
                            
                        else:
                            MemorysIn.append([0]*ShortenOrder)
                            MemorysOut.append([0]*ShortenOrder)

                    #Create codeword for current mic/datablock
                    CurrentTestDataMic = CurrentTestData[mic]
                    residuals, MemorysIn[mic], predictions = ShortenAlgorithm.In(CurrentTestDataMic.copy(), MemorysIn[mic])
                    
                    #Calculate the ideal m value, by first calculating the ideal k value and taking 2^k
                    #Calculates the ideal k_vaule for the data
                    abs_res = np.absolute(residuals)
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

                    #Calculate m value from k value by taking 2^k
                    m = pow(2,k)
                    #Store the m-value
                    m_array[mic].append(m)

                    #Golomb codes the residuals from shorten and saves the code word
                    CodeWord = ""
                    for i in range(len(residuals)):
                        Golomb_coder = GolombCoding(m, True)
                        n = int(residuals[i])
                        kodOrd = Golomb_coder.Encode(n)
                        CodeWord += kodOrd

                    #Save Codeword in array
                    CodeWordArray[mic].append(CodeWord)

            #Array to store Decoding time
            TimeArray = []


            for i in range(datablocks):
                #Start time
                start_time = time.time()            
                for mic in range(end_mic + 1 - start_mic):
                    #Grab all codewords and m-values for a specific microphone
                    CodeWordsMic = CodeWordArray[mic]
                    MvaluesMic = m_array[mic]
                    
                    #loop thorugh all codewords for the selected mic
                    for i in range(len(CodeWordsMic)):
                        
                        #Select a codeword and m-values
                        CurrentCodeWord = CodeWordsMic[i]
                        m_values = MvaluesMic[i]
                        
                        #Decode the residuals for every datablock
                        Golomb_coder = GolombCoding(m_values, True)
                        uncoded_residuals = Golomb_coder.Decode(CurrentCodeWord)
                        #Recreate values
                        DecodedData, MemorysOut[mic], predictions = ShortenAlgorithm.Out(uncoded_residuals, MemorysOut[mic])
                        
                        
                #Stop time
                stop_time = time.time()

                #Calculate totalt time
                total_time = stop_time - start_time
                
                #Store total time in array
                TimeArray.append(total_time)

            #Calculate average time
            avg_time = sum(TimeArray) / len(TimeArray)


            print("Average time (in seconds) to recreate a full datablock using Shorten order ", ShortenOrder, "with Golomb codes is: ",avg_time," s")


        #LPC tests
        elif self.TestNr == 10:
            #Select what mics are going to be plotted
            start_mic = input('Select what microhpone to plot: ')
            #Check if the start_mic value choosen can be converted to int
            try:
                int(start_mic)
            #If the value can not be converted to int set the FlagTry to false
            except ValueError:
                FlagTry = False

            if FlagTry:
                start_mic = int(start_mic)
            else:
                raise ValueError(f"The microphone value selected needs to be an integer.")
            
            #Store the data from the desired microphone and datablocks in TestData
            TestData = self.DataSelect(OriginalData, datablocks, start_mic, start_mic)

            LpcOrder = input('Select LPC order (1-32): ')
            #Check if the LpcOrder value choosen can be converted to int
            try:
                int(LpcOrder)
            #If the value can not be converted to int set the FlagTry to false
            except ValueError:
                FlagTry = False

            if FlagTry:
                LpcOrder = int(LpcOrder)
            else:
                raise ValueError(f"The LPC order selected needs to be an integer.")
            
            if LpcOrder > 32 or LpcOrder < 1:
                raise ValueError(f"The LPC order selected needs to be between 1 and 32.")
            
            LpcAlgorithm = MetaLPC(LpcOrder)
            
            #Create memory array with appropriate length for selected order
            MemoryIn = [0]*LpcOrder
            MemoryOut = [0]*LpcOrder

            #Array to store all CodeWords
            CodeWords = []

            
            for CurrentBlock in range(len(TestData)):
                #Use LPC to create the code words
                CurrentTestData = TestData[CurrentBlock]
                CurrentTestData = CurrentTestData[0]#I belive this is needed because of choosing the first mic even tho it is only 1 mic
                CodeWord, MemoryIn, coef = LpcAlgorithm.In(CurrentTestData.copy(), MemoryIn)
                #Save each codeword
                CodeWords.append(CodeWord)

            
            #loop thorugh all CodeWords, there will be one codeword for every datablock
            for i in range(len(CodeWords)):
                allCorrect = 0
                zero = []
                CodeWord = CodeWords[i]
                #Decode the codeword fo every datablock
                DecodedData, MemoryOut = LpcAlgorithm.Out(CodeWord, MemoryOut)
                #Grab the original data from every datablock
                CurrentInputData = TestData[i]
                CurrentInputData = CurrentInputData[0]#I belive the first mic needs to be choosen even though it is only 1 mic


                #Go thorugh all samples in every datablock
                for sample in range(len(CurrentInputData)):
                    #Calculate the difference between the original data and decoded data,
                    #This should be =0 if every thing has been done correctly
                    currentZero = CurrentInputData[sample] - DecodedData[sample]
                    zero.append(currentZero)
                    
                    #If the difference is not equal to 0 the code repports that there have been an error
                    if currentZero != 0:
                        allCorrect += 1

                #Plot the original, recretated, and the differential between them
                #There will be one plot for every datablock
                fig = plt.figure(i, layout = 'constrained')

                ax = fig.add_subplot(211)
                plt.plot(CurrentInputData, 'b', label = 'Original values')
                plt.plot(DecodedData, 'r-.', label = 'Decoded values')

                plt.legend(fontsize=25, loc = 'upper right')
                plt.yticks(fontsize=20)
                plt.xticks(fontsize=20)

                ax = fig.add_subplot(212)
                plt.plot(zero, label = 'Original values - Decoded values')

                plt.legend(fontsize=25, loc = 'upper right')
                plt.yticks(fontsize=20)
                plt.xticks(fontsize=20)
                
                plt.show()

                #If all values have been recreated correctly this will be printed out, 
                #else print out how many was failed to be decoded
                if allCorrect == 0:
                    print("All values where decoded succesfully")
                else:
                    print("Failed decoding ", allCorrect,"values")


        elif self.TestNr == 11:
            #Select what mics are going to be plotted
            start_mic = input('Select what microhpone to plot: ')
            #Check if the start_mic value choosen can be converted to int
            try:
                int(start_mic)
            #If the value can not be converted to int set the FlagTry to false
            except ValueError:
                FlagTry = False

            if FlagTry:
                start_mic = int(start_mic)
            else:
                raise ValueError(f"The microphone value selected needs to be an integer.")
            
            #Store the data from the desired microphone and datablocks in TestData
            TestData = self.DataSelect(OriginalData, datablocks, start_mic, start_mic)

            LpcOrder = input('Select LPC order (1-32): ')
            #Check if the LpcOrder value choosen can be converted to int
            try:
                int(LpcOrder)
            #If the value can not be converted to int set the FlagTry to false
            except ValueError:
                FlagTry = False

            if FlagTry:
                LpcOrder = int(LpcOrder)
            else:
                raise ValueError(f"The LPC order selected needs to be an integer.")
            
            if LpcOrder > 32 or LpcOrder < 1:
                raise ValueError(f"The LPC order selected needs to be between 1 and 32.")
            
            LpcAlgorithm = LPC(LpcOrder)
            
            #Create memory array with appropriate length for selected order
            MemoryIn = [0]*LpcOrder
            MemoryOut = [0]*LpcOrder

            #Array to store all CodeWords
            CodeWords = []
            #Array to store all Coefficents
            Coefficents = []
            #Array to store m-values for encoding/decoding
            m_array = []
            for CurrentBlock in range(len(TestData)):
                #Use LPC to create the code words
                CurrentTestData = TestData[CurrentBlock]
                CurrentTestData = CurrentTestData[0]#I belive this is needed because of choosing the first mic even tho it is only 1 mic
                #Calculate the residuals using LPC
                coef, residuals, MemoryIn, predictions = LpcAlgorithm.In(CurrentTestData.copy(), MemoryIn)
                #Calculate the ideal m value, by first calculating the ideal k value and taking 2^k
                #Calculates the ideal k_vaule for the data
                abs_res = np.absolute(residuals)
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

                #Calculate m value from k value by taking 2^k
                m = pow(2,k)
                #Store the m-value
                m_array.append(m)

                #Store coefficents
                Coefficents.append(coef)


               
                #Golomb codes the residuals from LPC and saves the code word in code_word
                CodeWord = ""
                for i in range(len(residuals)):
                    Golomb_coder = GolombCoding(m, True)
                    n = int(residuals[i])
                    kodOrd = Golomb_coder.Encode(n)
                    CodeWord += kodOrd

                #Saves Rice coded residuals
                CodeWords.append(CodeWord)

            #Loops through all codewords to decode them and recreate all values, and compare them to the original values
            #There is one codeword for every datablock
            for i in range(len(CodeWords)):
                allCorrect = 0
                zero = []
                #Grab the current codeword
                CodeWord = CodeWords[i]
                #Grab the m-value to decode the codeword
                m = m_array[i]
                #Decodes the residuals from the Golomb code
                Golomb_coder = GolombCoding(m, True)
                uncoded_residuals = Golomb_coder.Decode(CodeWord)
                #Grab current coefficents
                coef = Coefficents[i]
                #Decode the codeword fo every datablock
                DecodedData, MemoryOut, predictions = LpcAlgorithm.Out(coef, uncoded_residuals, MemoryOut)
                #Grab the original data from every datablock
                CurrentInputData = TestData[i]
                CurrentInputData = CurrentInputData[0]#I belive the first mic needs to be choosen even though it is only 1 mic


                #Go thorugh all samples in every datablock
                for sample in range(len(CurrentInputData)):
                    #Calculate the difference between the original data and decoded data,
                    #This should be =0 if every thing has been done correctly
                    currentZero = CurrentInputData[sample] - DecodedData[sample]
                    zero.append(currentZero)
                    
                    #If the difference is not equal to 0 the code records that there have been an error
                    if currentZero != 0:
                        allCorrect += 1

                #Plot the original, recretated, and the differential between them
                #There will be one plot for every datablock
                fig = plt.figure(i, layout = 'constrained')

                ax = fig.add_subplot(211)
                plt.plot(CurrentInputData, 'b', label = 'Original values')
                plt.plot(DecodedData, 'r-.', label = 'Decoded values')

                plt.legend(fontsize=25, loc = 'upper right')
                plt.yticks(fontsize=20)
                plt.xticks(fontsize=20)

                ax = fig.add_subplot(212)
                plt.plot(zero, label = 'Original values - Decoded values')

                plt.legend(fontsize=25, loc = 'upper right')
                plt.yticks(fontsize=20)
                plt.xticks(fontsize=20)
                
                plt.show()

                #If all values have been recreated correctly this will be printed out, 
                #else print out how many was failed to be decoded
                if allCorrect == 0:
                    print("All values where decoded succesfully")
                else:
                    print("Failed decoding ", allCorrect,"values")


        elif self.TestNr == 12:
            #Select what mics are going to be plotted
            start_mic = input('Select what microhpone to use: ')
            #Check if the start_mic value choosen can be converted to int
            try:
                int(start_mic)
            #If the value can not be converted to int set the FlagTry to false
            except ValueError:
                FlagTry = False

            if FlagTry:
                start_mic = int(start_mic)
            else:
                raise ValueError(f"The microphone value selected needs to be an integer.")
            
            #Store the data from the desired microphone and datablocks in TestData
            TestData = self.DataSelect(OriginalData, datablocks, start_mic, start_mic)

            #Select startin k-value for the rice codes
            k_start = input('Select k-value to start compressing from: ')
            #Check if the k_start value choosen can be converted to int
            try:
                int(k_start)
            #If the value can not be converted to int set the FlagTry to false
            except ValueError:
                FlagTry = False

            if FlagTry:
                k_start = int(k_start)
                if k_start < 1:
                    raise ValueError(f"The k-value selected needs to be atleast 1.")

            else:
                raise ValueError(f"The k-value selected needs to be an integer.")
            
            #Select ending k-value for the rice codes
            k_stop = input('Select k_value to stop compressing at: ')
            #Check if the k_start value choosen can be converted to int
            try:
                int(k_stop)
            #If the value can not be converted to int set the FlagTry to false
            except ValueError:
                FlagTry = False

            if FlagTry:
                k_stop = int(k_stop)
                if k_stop < k_start:
                    raise ValueError(f"The k-value selected needs to be larger or equal to the starting k_value.")

            else:
                raise ValueError(f"The k-value selected needs to be an integer.")
            
            #crate array to store avg compression rates for all orders and k_values
            All_avg_cr_array = []
            #create array with all selected k_values
            k_array = []
            for k_values in range(k_start, k_stop+1):
                k_array.append(k_values)

            
            #Select startin LPC order
            order_start = input('Select LPC order to start from (minimum is 1, maximum is 32): ')
            #Check if the LPC value choosen can be converted to int
            try:
                int(order_start)
            #If the value can not be converted to int set the FlagTry to false
            except ValueError:
                FlagTry = False

            if FlagTry:
                order_start = int(order_start)
                if order_start < 1:
                    raise ValueError(f"The LPC order selected needs to be atleast 1.")
                elif order_start > 32:
                    raise ValueError(f"The LPC order max order is 32.")

            else:
                raise ValueError(f"The LPC order selected needs to be an integer.")
            
            #Select ending k-value for the rice codes
            order_stop = input('Select LPC order to stop at (maximum 32): ')
            #Check if the order_stop value choosen can be converted to int
            try:
                int(order_stop)
            #If the value can not be converted to int set the FlagTry to false
            except ValueError:
                FlagTry = False

            if FlagTry:
                order_stop = int(order_stop)
                if order_stop < order_start:
                    raise ValueError(f"The order selected needs to be larger or equal to the starting order value.")
                elif order_stop > 32:
                    raise ValueError(f"The LPC order max order is 32.")
                

            else:
                raise ValueError(f"The order selected needs to be an integer.")


            k_ideal_array = []
            MemorysIn = []
                


            #loop thorugh all orders of LPC
            for order in range(order_start, order_stop+1):
                #Create array to store memory for each order
                MemorysIn.append([0]*order)
                #Create array to store ideal k-value for each order
                k_ideal_array.append([])
                #Array to store compression rate for current order
                cr_array = []
                #loop thorugh all datablocks
                for block in range(len(TestData)):
                    #Grab the testdata for the current block
                    CurrentTestData = TestData[block]
                    #Need to grab from the first mic as well, even though it is only 1 mic
                    CurrentTestData = CurrentTestData[0]

                    #Calcualate the residuals with the LPC algorithm
                    LpcAlgorithm = LPC(order)
                    coef, residual, MemorysIn[order-order_start], predict = LpcAlgorithm.In(CurrentTestData, MemorysIn[order-order_start])

                    #Calculates the ideal k_vaule acording to Rice Theory
                    abs_res = np.absolute(residual.copy())
                    abs_res_avg = np.mean(abs_res)
                    #if abs_res_avg is less than 4.7 it would give a k value less than 1.
                    #k needs tobe a int > 1 and therefore if abs_res_avg < 5 k is set to 1
                    #OBS. 4.7 < abs_res_avg < 5 would be rounded of to k=1 so setting the limit to 5 works well
                    if abs_res_avg > 5:
                        k_ideal = int(round(math.log(math.log(2,10) * abs_res_avg,2)))
                    else:
                        k_ideal = 1

                    #Appends the ideal k vaule in the array matching the correct LPC order
                    k_ideal_array[order-order_start].append(k_ideal)

                    #loop thorug all k-values
                    for i in range(len(k_array)):
                        CodeWord = ""
                        if i == 0:
                            UncodedWord = ""
                        k = k_array[i]
                        for q in range(len(residual)):
                            #Rice code the residual for all k_values
                            Rice_coder = RiceCoding(k, True)
                            n = int(residual[q])
                            kodOrd = Rice_coder.Encode(n)
                            CodeWord += kodOrd
                            if i == 0:
                                #Represent the uncdoed word in 24 bits
                                UncodedWord += np.binary_repr(abs(n),24)
                        #calculate the compression rate for the current CodeWord
                        cr = len(CodeWord) / len(UncodedWord)

                        #Save the compression rate in an array, with cr_for specific k_values grouped together
                        if block == 0:
                            cr_array.append([])
                        cr_array[i].append(cr)
                    
                

                #Calculate the average cr for all k-value used for the current order
                avg_cr_array = []
                for current_cr_array in cr_array:
                    avg_cr = sum(current_cr_array)/len(current_cr_array)
                    avg_cr_array.append(avg_cr)

                #Save the avg cr values from the current order
                All_avg_cr_array.append(avg_cr_array)

            
            #Figure to plot all k-values in
            plt.figure("Compression order for differente k-values using LPC with Rice codes", layout = 'constrained')
            plt_colors = ['yo', 'ro', 'bo', 'go', 'co', 'ko', 'mo',
                          'yv', 'rv', 'bv', 'gv', 'cv', 'kv', 'mv',
                          'ys', 'rs', 'bs', 'gs', 'cs', 'ks', 'ms',
                          'y*', 'r*', 'b*', 'g*', 'c*', 'k*', 'm*',
                          'yD', 'rD', 'bD', 'gD', 'cD', 'kD', 'mD']


            #Print the k_array, ideal k-value for each order, and average compression rate for allorders
            print("k-values: ",k_array)
            print("")
            for orders in range(order_start, order_stop+1):
                print("Average ideal k-value using LPC order ",orders," (acording to Rice theory, rounded to closest int): ", round(sum(k_ideal_array[orders-order_start])/len(k_ideal_array[orders-order_start])))
                print("Average compression rate using LPC order ",orders,": ",All_avg_cr_array[orders-order_start])
                print("")
                plt_label = 'Order ' + str(orders)
                plt.plot(k_array, All_avg_cr_array[orders-order_start], plt_colors[orders-order_start], label = plt_label)

            plt.yticks(fontsize=25)
            plt.xticks(fontsize=25)
            plt.xlabel("k-value", fontsize=30)
            plt.ylabel("Average compression ratio", fontsize=30)
            plt.legend(fontsize=30, loc = 'upper right')
            plt.show()


        elif self.TestNr == 13:
            #Select what mics are going to be compressed
            start_mic = input('Select what microhpone to start from: ')
            #Check if the start_mic value choosen can be converted to int
            try:
                int(start_mic)
            #If the value can not be converted to int set the FlagTry to false
            except ValueError:
                FlagTry = False

            if FlagTry:
                start_mic = int(start_mic)
            else:
                raise ValueError(f"The microphone value selected needs to be an integer.")
            

            end_mic = input('Select what microhpone to end at (if only one mic is desired choose the same value as start microphone): ')
            #Check if the end_mic value choosen can be converted to int
            try:
                int(end_mic)
            #If the value can not be converted to int set the FlagTry to false
            except ValueError:
                FlagTry = False

            if FlagTry:
                end_mic = int(end_mic)
            else:
                raise ValueError(f"The microphone value selected needs to be an integer.")
            
            

            
            #Store the data from the desired microphones and datablocks in TestData
            TestData = self.DataSelect(OriginalData, datablocks, start_mic, end_mic)



            LpcOrder = input('Select LPC order (1-32): ')
            #Check if the LpcOrder value choosen can be converted to int
            try:
                int(LpcOrder)
            #If the value can not be converted to int set the FlagTry to false
            except ValueError:
                FlagTry = False

            if FlagTry:
                LpcOrder = int(LpcOrder)
                if LpcOrder < 1:
                    raise ValueError(f"The LPC order selected needs to be an atleast 1.")
                elif LpcOrder > 32:
                    raise ValueError(f"The LPC order can not be larger than 32.")

            else:
                raise ValueError(f"The LPC order selected needs to be an integer.")
            
            LpcAlgorithm = MetaLPC(LpcOrder)


            #Create MemoryArray
            Memorys = []

            

            #Array to store all compression rates
            cr_array = []

            for CurrentBlock in range(len(TestData)):
                #Use LPC to create the code words
                CurrentTestData = TestData[CurrentBlock]
                for mic in range(end_mic + 1 - start_mic):
                    if CurrentBlock == 0:
                        #Create memory array with appropriate length for selected order
                        Memorys.append([0]*LpcOrder)
                        

                    #Create codeword for current mic/datablock
                    CurrentTestDataMic = CurrentTestData[mic]
                    CodeWord, Memorys[mic], coef = LpcAlgorithm.In(CurrentTestDataMic.copy(), Memorys[mic])

                    #Create binary uncoded word for current input, original value represented in 24 bits
                    UncodedWord = ""
                    for sample in CurrentTestDataMic:
                        UncodedWord += np.binary_repr(sample, 24)

                    #Calculate CR for current codeword
                    cr = len(CodeWord) / len(UncodedWord)
                    #Save Cr in array
                    cr_array.append(cr)

            #Calculate average CR for all codewords
            avg_cr = sum(cr_array) / len(cr_array)

            print("Average compression rate using LPC order ",LpcOrder," is, CR = ",avg_cr)
                        

        elif self.TestNr == 14:
            #Select what mics are going to be compressed
            start_mic = input('Select what microhpone to start from: ')
            #Check if the start_mic value choosen can be converted to int
            try:
                int(start_mic)
            #If the value can not be converted to int set the FlagTry to false
            except ValueError:
                FlagTry = False

            if FlagTry:
                start_mic = int(start_mic)
            else:
                raise ValueError(f"The microphone value selected needs to be an integer.")
            

            end_mic = input('Select what microhpone to end at (if only one mic is desired choose the same value as start microphone): ')
            #Check if the end_mic value choosen can be converted to int
            try:
                int(end_mic)
            #If the value can not be converted to int set the FlagTry to false
            except ValueError:
                FlagTry = False

            if FlagTry:
                end_mic = int(end_mic)
            else:
                raise ValueError(f"The microphone value selected needs to be an integer.")
            
            

            
            #Store the data from the desired microphones and datablocks in TestData
            TestData = self.DataSelect(OriginalData, datablocks, start_mic, end_mic)

            LpcOrder = input('Select LPC order (1-32): ')
            #Check if the LpcOrder value choosen can be converted to int
            try:
                int(LpcOrder)
            #If the value can not be converted to int set the FlagTry to false
            except ValueError:
                FlagTry = False

            if FlagTry:
                LpcOrder = int(LpcOrder)
                if LpcOrder < 1:
                    raise ValueError(f"The LPC order selected needs to be an atleast 1.")
                elif LpcOrder > 32:
                    raise ValueError(f"The LPC order can not be larger than 32.")

            else:
                raise ValueError(f"The LPC order selected needs to be an integer.")
            
            LpcAlgorithm = MetaLPC(LpcOrder)



            #Create MemoryArray
            MemorysIn = []
            MemorysOut = []

            

            #Array to store all CodeWords
            CodeWordArray = []



            
            
            for CurrentBlock in range(len(TestData)):
                #Use LPC to create the code words
                CurrentTestData = TestData[CurrentBlock]
                for mic in range(end_mic + 1 - start_mic):
                    if CurrentBlock == 0:
                        #Make sure all CodeWords are grouped by microphone
                        CodeWordArray.append([])

                        #Create memory array with appropriate length for selected order
                        MemorysIn.append([0]*LpcOrder)
                        MemorysOut.append([0]*LpcOrder)

                    #Create codeword for current mic/datablock
                    CurrentTestDataMic = CurrentTestData[mic]
                    CodeWord, MemorysIn[mic], coef = LpcAlgorithm.In(CurrentTestDataMic.copy(), MemorysIn[mic])

                    #Save Codeword in array
                    CodeWordArray[mic].append(CodeWord)

            #Array to store Decoding time
            TimeArray = []

            for i in range(datablocks):
                #Start time
                start_time = time.time()            
                for mic in range(end_mic + 1 - start_mic):
                        
            
                    #Grab all codewords for a specific microphone
                    CodeWordsMic = CodeWordArray[mic]

                    
     

                    #Select a codeword
                    CurrentCodeWord = CodeWordsMic[i]
                    
                    #Decode the codeword fo every datablock
                    DecodedData, MemorysOut[mic] = LpcAlgorithm.Out(CurrentCodeWord, MemorysOut[mic])
                #Stop time
                stop_time = time.time()

                #Calculate totalt time
                total_time = stop_time - start_time
                
                #Store total time in array
                TimeArray.append(total_time)

            #Calculate average time
            avg_time = sum(TimeArray) / len(TimeArray)

            print("Average time (in seconds) to recreate a full datablock using LPC order ", LpcOrder, "with Rice codes is: ",avg_time," s")

        elif self.TestNr == 15:
            #Select what mics are going to be compressed
            start_mic = input('Select what microhpone to start from: ')
            #Check if the start_mic value choosen can be converted to int
            try:
                int(start_mic)
            #If the value can not be converted to int set the FlagTry to false
            except ValueError:
                FlagTry = False

            if FlagTry:
                start_mic = int(start_mic)
            else:
                raise ValueError(f"The microphone value selected needs to be an integer.")
            

            end_mic = input('Select what microhpone to end at (if only one mic is desired choose the same value as start microphone): ')
            #Check if the end_mic value choosen can be converted to int
            try:
                int(end_mic)
            #If the value can not be converted to int set the FlagTry to false
            except ValueError:
                FlagTry = False

            if FlagTry:
                end_mic = int(end_mic)
            else:
                raise ValueError(f"The microphone value selected needs to be an integer.")
            
            

            
            #Store the data from the desired microphones and datablocks in TestData
            TestData = self.DataSelect(OriginalData, datablocks, start_mic, end_mic)



            LpcOrder = input('Select LPC order (1-32): ')
            #Check if the LpcOrder value choosen can be converted to int
            try:
                int(LpcOrder)
            #If the value can not be converted to int set the FlagTry to false
            except ValueError:
                FlagTry = False

            if FlagTry:
                LpcOrder = int(LpcOrder)
                if LpcOrder < 1:
                    raise ValueError(f"The LPC order selected needs to be an atleast 1.")
                elif LpcOrder > 32:
                    raise ValueError(f"The LPC order can not be larger than 32.")

            else:
                raise ValueError(f"The LPC order selected needs to be an integer.")
            
            LpcAlgorithm = LPC(LpcOrder)

            #Create MemoryArray
            MemorysIn = []
            MemorysOut = []

            #Array to store all CodeWords
            CodeWordArray = []

            #Array to store coefficents
            Coefficents = []

            #Array to store m-values
            m_array = []

            #Encode all input values
            for CurrentBlock in range(len(TestData)):
                #Use LPC to create the code words
                CurrentTestData = TestData[CurrentBlock]
                for mic in range(end_mic + 1 - start_mic):
                    if CurrentBlock == 0:
                        #Make sure all CodeWords and m_values are grouped by microphone
                        CodeWordArray.append([])
                        m_array.append([])


                        #Create memory array with appropriate length for selected order
                        MemorysIn.append([0]*LpcOrder)
                        MemorysOut.append([0]*LpcOrder)

                        Coefficents.append([])
                            

                    #Create codeword for current mic/datablock
                    CurrentTestDataMic = CurrentTestData[mic]
                    coef, residuals, MemorysIn[mic], predictions = LpcAlgorithm.In(CurrentTestDataMic.copy(), MemorysIn[mic])
                    
                    Coefficents[mic].append(coef)


                    #Calculate the ideal m value, by first calculating the ideal k value and taking 2^k
                    #Calculates the ideal k_vaule for the data
                    abs_res = np.absolute(residuals)
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

                    #Calculate m value from k value by taking 2^k
                    m = pow(2,k)
                    #Store the m-value
                    m_array[mic].append(m)

                    #Golomb codes the residuals from LPC and saves the code word
                    CodeWord = ""
                    for i in range(len(residuals)):
                        Golomb_coder = GolombCoding(m, True)
                        n = int(residuals[i])
                        kodOrd = Golomb_coder.Encode(n)
                        CodeWord += kodOrd

                    #Save Codeword in array
                    CodeWordArray[mic].append(CodeWord)

            #Array to store Decoding time
            TimeArray = []


            for i in range(datablocks):
                #Start time
                start_time = time.time()            
                for mic in range(end_mic + 1 - start_mic):
                    #Grab all codewords and m-values for a specific microphone
                    CodeWordsMic = CodeWordArray[mic]
                    MvaluesMic = m_array[mic]
                    CurrentCoefficents = Coefficents[mic]
                    
                    #loop thorugh all codewords for the selected mic
                    for i in range(len(CodeWordsMic)):
                        
                        #Select a codeword and m-values
                        CurrentCodeWord = CodeWordsMic[i]
                        m_values = MvaluesMic[i]

                        #Grab coefficents
                        coef = CurrentCoefficents[i]
                        
                        #Decode the residuals for every datablock
                        Golomb_coder = GolombCoding(m_values, True)
                        uncoded_residuals = Golomb_coder.Decode(CurrentCodeWord)
                        #Recreate values
                        DecodedData, MemorysOut[mic], predictions = LpcAlgorithm.Out(coef, uncoded_residuals, MemorysOut[mic])
                        
                        
                #Stop time
                stop_time = time.time()

                #Calculate totalt time
                total_time = stop_time - start_time
                
                #Store total time in array
                TimeArray.append(total_time)

            #Calculate average time
            avg_time = sum(TimeArray) / len(TimeArray)


            print("Average time (in seconds) to recreate a full datablock using LPC order ", LpcOrder, "with Golomb codes is: ",avg_time," s")


        #FLAC tests
        elif self.TestNr == 16:
            #Select what mics are going to be compressed
            start_mic = input('Select what microhpone to start from: ')
            #Check if the start_mic value choosen can be converted to int
            try:
                int(start_mic)
            #If the value can not be converted to int set the FlagTry to false
            except ValueError:
                FlagTry = False

            if FlagTry:
                start_mic = int(start_mic)
            else:
                raise ValueError(f"The microphone value selected needs to be an integer.")
            

            end_mic = input('Select what microhpone to end at (if only one mic is desired choose the same value as start microphone): ')
            #Check if the end_mic value choosen can be converted to int
            try:
                int(end_mic)
            #If the value can not be converted to int set the FlagTry to false
            except ValueError:
                FlagTry = False

            if FlagTry:
                end_mic = int(end_mic)
            else:
                raise ValueError(f"The microphone value selected needs to be an integer.")
            
            

            
            #Store the data from the desired microphones and datablocks in TestData
            TestData = self.DataSelect(OriginalData, datablocks, start_mic, end_mic)



            
            FlacAlgorithm = MetaFLAC()


            #Create MemoryArray
            Memorys = []

            

            #Array to store all compression rates
            cr_array = []

            
            for CurrentBlock in range(len(TestData)):
                #Use FLAC to create the code words
                CurrentTestData = TestData[CurrentBlock]
                for mic in range(end_mic + 1 - start_mic):
                    if CurrentBlock == 0:
                        #Create memory array with appropriate length for selected order
                        Memorys.append([0]*32)

                    #Create codeword for current mic/datablock
                    CurrentTestDataMic = CurrentTestData[mic]
                    CodeWord, Memorys[mic] = FlacAlgorithm.In(CurrentTestDataMic.copy(), Memorys[mic])

                    #Create binary uncoded word for current input, original value represented in 24 bits
                    UncodedWord = ""
                    for sample in CurrentTestDataMic:
                        UncodedWord += np.binary_repr(sample, 24)

                    #Calculate CR for current codeword
                    cr = len(CodeWord) / len(UncodedWord)
                    #Save Cr in array
                    cr_array.append(cr)

            #Calculate average CR for all codewords
            avg_cr = sum(cr_array) / len(cr_array)

            print("Average compression rate using FLAC is, CR = ",avg_cr)
               
        elif self.TestNr == 17:
            #Select what mics are going to be compressed
            start_mic = input('Select what microhpone to start from: ')
            #Check if the start_mic value choosen can be converted to int
            try:
                int(start_mic)
            #If the value can not be converted to int set the FlagTry to false
            except ValueError:
                FlagTry = False

            if FlagTry:
                start_mic = int(start_mic)
            else:
                raise ValueError(f"The microphone value selected needs to be an integer.")
            

            end_mic = input('Select what microhpone to end at (if only one mic is desired choose the same value as start microphone): ')
            #Check if the end_mic value choosen can be converted to int
            try:
                int(end_mic)
            #If the value can not be converted to int set the FlagTry to false
            except ValueError:
                FlagTry = False

            if FlagTry:
                end_mic = int(end_mic)
            else:
                raise ValueError(f"The microphone value selected needs to be an integer.")
            
            

            
            #Store the data from the desired microphones and datablocks in TestData
            TestData = self.DataSelect(OriginalData, datablocks, start_mic, end_mic)



            
            FlacAlgorithm = MetaFLAC()


            #Create MemoryArray
            MemorysIn = []
            MemorysOut = []

            

            #Array to store all CodeWords
            CodeWordArray = []



            
            
            for CurrentBlock in range(len(TestData)):
                #Use FLAC to create the code words
                CurrentTestData = TestData[CurrentBlock]
                for mic in range(end_mic + 1 - start_mic):
                    if CurrentBlock == 0:
                        #Make sure all CodeWords are grouped by microphone
                        CodeWordArray.append([])

                        #Create memory array with appropriate length for selected order
                        MemorysIn.append([0]*32)
                        MemorysOut.append([0]*32)
                            

                    #Create codeword for current mic/datablock
                    CurrentTestDataMic = CurrentTestData[mic]
                    CodeWord, MemorysIn[mic] = FlacAlgorithm.In(CurrentTestDataMic.copy(), MemorysIn[mic])

                    #Save Codeword in array
                    CodeWordArray[mic].append(CodeWord)

            #Array to store Decoding time
            TimeArray = []

            for i in range(datablocks):
                #Start time
                start_time = time.time()            
                for mic in range(end_mic + 1 - start_mic):
                        
            
                    #Grab all codewords for a specific microphone
                    CodeWordsMic = CodeWordArray[mic]

                    
     

                    #Select a codeword
                    CurrentCodeWord = CodeWordsMic[i]
                    
                    #Decode the codeword fo every datablock
                    DecodedData, MemorysOut[mic], coding_choice = FlacAlgorithm.Out(CurrentCodeWord, MemorysOut[mic])
                #Stop time
                stop_time = time.time()

                #Calculate totalt time
                total_time = stop_time - start_time
                
                #Store total time in array
                TimeArray.append(total_time)

            #Calculate average time
            avg_time = sum(TimeArray) / len(TimeArray)

            print("Average time (in seconds) to recreate a full datablock using FLAC is: ",avg_time," s")


        #Adjacent tests
        elif self.TestNr == 18:
            #Select what mics are going to be plotted
            start_mic = input('Select what microhpone to use: ')
            #Check if the start_mic value choosen can be converted to int
            try:
                int(start_mic)
            #If the value can not be converted to int set the FlagTry to false
            except ValueError:
                FlagTry = False

            if FlagTry:
                start_mic = int(start_mic)
            else:
                raise ValueError(f"The microphone value selected needs to be an integer.")
            
            end_mic = input('Select what microhpone to end at (if only one mic is desired choose the same value as start microphone): ')
            #Check if the end_mic value choosen can be converted to int
            try:
                int(end_mic)
            #If the value can not be converted to int set the FlagTry to false
            except ValueError:
                FlagTry = False

            if FlagTry:
                end_mic = int(end_mic)
            else:
                raise ValueError(f"The microphone value selected needs to be an integer.")
            
            

            
            #Store the data from the desired microphones and datablocks in TestData
            TestData = self.DataSelect(OriginalData, datablocks, start_mic, end_mic)

            AdjacentAlgorithm = MetaAdjacent(order=1)
            MemoryIn = [0]
            MemoryOut = [0]
            code_words = []
            AllInputs = []

            for block in range(len(TestData)):
                #Grab the testdata for the current block
                CurrentTestData = TestData[block]

                for sample in range(256):
                    
                    #create an array to save all mic values for current data sample
                    testInputs = []
                    for microphone in range(end_mic + 1 - start_mic):
                        testIn = CurrentTestData[microphone,sample]
                        testInputs.append(testIn)

                    CurrentCodeWord, MemoryIn = AdjacentAlgorithm.In(testInputs, MemoryIn)


                    #Saves codewords
                    code_words.append(CurrentCodeWord)
                    AllInputs.append(testInputs)


            #Recreate inputs
            recreatedInputs = []
            for i in range(len(code_words)):

                #Recreate the original inputs
                CurrentRecreatedInputs, MemoryOut = AdjacentAlgorithm.Out(code_words[i], MemoryOut)
                recreatedInputs.append(CurrentRecreatedInputs)

            #Store original and recreated inputs from each mic in an array
            #Start by creating the arrays
            mics_og = []#Original inputs
            mics_re = []#Recreated inputs
            mics_zero = []#Original inputs - recreated inputs (Hopefully equals 0)
            for i in range(end_mic + 1 - start_mic):
                mics_og.append([])
                mics_re.append([])
                mics_zero.append([])
            
            allCorrect = 0#Tacks how many values was failed to be recreated

            #loops thorugh each input/recreated input block
            for i in range(len(recreatedInputs)):
                #Loop thorugh each mic for the current block
                currentRe = recreatedInputs[i]
                currentOg = AllInputs[i]
                for microphone in range(len(currentRe)):
                    currentMicOg = currentOg[microphone]
                    currentMicRe = currentRe[microphone]
                    currentMicZero = currentMicOg - currentMicRe

                    #While looping throug each recreated value also check if any value was failed to be recreated:
                    if currentMicOg != currentMicRe:
                        #Increament the amount of errors by 1
                        allCorrect +=1
                        #Print out where the failed recreaten where
                        print("Failed recrating value at mic ",microphone,"at data block ",i,"Original value = ",currentMicOg,"Recreated value = ",currentMicRe)


                    mics_og[microphone].append(currentMicOg)
                    mics_re[microphone].append(currentMicRe)
                    mics_zero[microphone].append(currentMicZero)
            
            if allCorrect == 0:
                print("All values where recreated succesfully")
            else:
                print("Failed to recreate ",allCorrect,"values")

            for Plotted_Mic in range(start_mic, end_mic+1):


                figure_title = "Mic #" + str(Plotted_Mic)
                fig = plt.figure(figure_title, layout = 'constrained')
                ax = fig.add_subplot(211)
                plt.plot(mics_og[Plotted_Mic - start_mic], 'b', label = "Original values")
                plt.plot(mics_re[Plotted_Mic - start_mic], 'r-.', label = "Recreated values")
                plt.legend(fontsize=25, loc = 'upper right')
                plt.yticks(fontsize=20)
                plt.xticks(fontsize=20)

                ax = fig.add_subplot(212)
                plt.plot(mics_zero[Plotted_Mic - start_mic], 'g', label = "Original values - Recreated values")
                plt.legend(fontsize=25, loc = 'upper right')
                plt.yticks(fontsize=20)
                plt.xticks(fontsize=20)
                plt.show()


        elif self.TestNr == 19:
            #Select what mics are going to be plotted
            start_mic = input('Select what microhpone to use: ')
            #Check if the start_mic value choosen can be converted to int
            try:
                int(start_mic)
            #If the value can not be converted to int set the FlagTry to false
            except ValueError:
                FlagTry = False

            if FlagTry:
                start_mic = int(start_mic)
            else:
                raise ValueError(f"The microphone value selected needs to be an integer.")
            
            end_mic = input('Select what microhpone to end at (if only one mic is desired choose the same value as start microphone): ')
            #Check if the end_mic value choosen can be converted to int
            try:
                int(end_mic)
            #If the value can not be converted to int set the FlagTry to false
            except ValueError:
                FlagTry = False

            if FlagTry:
                end_mic = int(end_mic)
            else:
                raise ValueError(f"The microphone value selected needs to be an integer.")
            
            

            
            #Store the data from the desired microphones and datablocks in TestData
            TestData = self.DataSelect(OriginalData, datablocks, start_mic, end_mic)

            AdjacentAlgorithm = Adjacent(1)
            MemoryIn = [0]
            MemoryOut = [0]
            AllInputs = []
            AllCodeWords = []
            AllMvalues = []
    

            for block in range(len(TestData)):
                #Grab the testdata for the current block
                CurrentTestData = TestData[block]

                for sample in range(256):

                    if block == 0:
                        AllCodeWords.append([])
                        AllMvalues.append([])
                    
                    #create an array to save all mic values for current data sample
                    testInputs = []
                    for microphone in range(end_mic + 1 - start_mic):
                        testIn = CurrentTestData[microphone,sample]
                        testInputs.append(testIn)

                    CurrentResiduals, MemoryIn, CurrentPredictions = AdjacentAlgorithm.In(testInputs, MemoryIn)

                    AllInputs.append(testInputs)

                    #Calculates the ideal k_vaule for the residuals
                    abs_res = np.absolute(CurrentResiduals)
                    abs_res_avg = np.mean(abs_res)
                    #if abs_res_avg is less than 4.7 it would give a k value less than 1.
                    #k needs tobe a int > 1. All abs_res_avg values bellow 6.64 will be set to 1 to avoid this issue
                    if abs_res_avg > 6.64:

                        k = int(round(math.log(math.log(2,10) * abs_res_avg,2))) + 1
                    else:
                        k = 1

                    #calculating the m value by taking 2 to the power of k
                        
                    m = pow(2,k)

                    #Golomb code the resiudals
                    
                    CodeWord = ""
                    for i in range(len(CurrentResiduals)):
                        Golomb_coder = GolombCoding(m, True)
                        n = int(CurrentResiduals[i])
                        kodOrd = Golomb_coder.Encode(n)
                        CodeWord += kodOrd
                    
                    #Save the ricecoded residuals and k-values to later decode
                    AllCodeWords[sample].append(CodeWord)
                    AllMvalues[sample].append(m)




            #Recreate inputs
            recreatedInputs = []
            #Loop thorugh all data blocks
            for i in range(datablocks):

                #loop thorugh all samples
                for sample in range(256):

                    #Grab data from the current sample
                    CodeWordsDataSample = AllCodeWords[sample]
                    MvaluesSample = AllMvalues[sample]


                    #Grab data from the current datablock
                    CodeWord = CodeWordsDataSample[i]
                    mValue = MvaluesSample[i]


                    Golomb_decoder = GolombCoding(mValue, True)
                    residuals = Golomb_decoder.Decode(CodeWord)

                    #Recreate the original inputs
                    CurrentRecreatedInputs, MemoryOut, predictions = AdjacentAlgorithm.Out(residuals, MemoryOut)
                    recreatedInputs.append(CurrentRecreatedInputs)

            #Store original and recreated inputs from each mic in an array
            #Start by creating the arrays
            mics_og = []#Original inputs
            mics_re = []#Recreated inputs
            mics_zero = []#Original inputs - recreated inputs (Hopefully equals 0)
            for i in range(end_mic + 1 - start_mic):
                mics_og.append([])
                mics_re.append([])
                mics_zero.append([])
            
            allCorrect = 0#Tacks how many values was failed to be recreated

            #loops thorugh each input/recreated input block
            for i in range(len(recreatedInputs)):
                #Loop thorugh each mic for the current block
                currentRe = recreatedInputs[i]
                currentOg = AllInputs[i]
                for microphone in range(len(currentRe)):
                    currentMicOg = currentOg[microphone]
                    currentMicRe = currentRe[microphone]
                    currentMicZero = currentMicOg - currentMicRe

                    #While looping throug each recreated value also check if any value was failed to be recreated:
                    if currentMicOg != currentMicRe:
                        #Increament the amount of errors by 1
                        allCorrect +=1
                        #Print out where the failed recreaten where
                        print("Failed recrating value at mic ",microphone,"at data block ",i,"Original value = ",currentMicOg,"Recreated value = ",currentMicRe)


                    mics_og[microphone].append(currentMicOg)
                    mics_re[microphone].append(currentMicRe)
                    mics_zero[microphone].append(currentMicZero)
            
            if allCorrect == 0:
                print("All values where recreated succesfully")
            else:
                print("Failed to recreate ",allCorrect,"values")

            for Plotted_Mic in range(start_mic, end_mic+1):


                figure_title = "Mic #" + str(Plotted_Mic)
                fig = plt.figure(figure_title, layout = 'constrained')
                ax = fig.add_subplot(211)
                plt.plot(mics_og[Plotted_Mic - start_mic], 'b', label = "Original values")
                plt.plot(mics_re[Plotted_Mic - start_mic], 'r-.', label = "Recreated values")
                plt.legend(fontsize=25, loc = 'upper right')
                plt.yticks(fontsize=20)
                plt.xticks(fontsize=20)

                ax = fig.add_subplot(212)
                plt.plot(mics_zero[Plotted_Mic - start_mic], 'g', label = "Original values - Recreated values")
                plt.legend(fontsize=25, loc = 'upper right')
                plt.yticks(fontsize=20)
                plt.xticks(fontsize=20)
                plt.show()


        elif self.TestNr == 20:
            #Select what mics are going to be plotted
            start_mic = input('Select what microhpone to use: ')
            #Check if the start_mic value choosen can be converted to int
            try:
                int(start_mic)
            #If the value can not be converted to int set the FlagTry to false
            except ValueError:
                FlagTry = False

            if FlagTry:
                start_mic = int(start_mic)
            else:
                raise ValueError(f"The microphone value selected needs to be an integer.")
            
            end_mic = input('Select what microhpone to end at (if only one mic is desired choose the same value as start microphone): ')
            #Check if the end_mic value choosen can be converted to int
            try:
                int(end_mic)
            #If the value can not be converted to int set the FlagTry to false
            except ValueError:
                FlagTry = False

            if FlagTry:
                end_mic = int(end_mic)
            else:
                raise ValueError(f"The microphone value selected needs to be an integer.")
            
            

            
            #Store the data from the desired microphones and datablocks in TestData
            TestData = self.DataSelect(OriginalData, datablocks, start_mic, end_mic)

            


            #Select startin k-value for the rice codes
            k_start = input('Select k-value to start compressing from: ')
            #Check if the k_start value choosen can be converted to int
            try:
                int(k_start)
            #If the value can not be converted to int set the FlagTry to false
            except ValueError:
                FlagTry = False

            if FlagTry:
                k_start = int(k_start)
                if k_start < 1:
                    raise ValueError(f"The k-value selected needs to be atleast 1.")

            else:
                raise ValueError(f"The k-value selected needs to be an integer.")
            
            #Select ending k-value for the rice codes
            k_stop = input('Select k_value to stop compressing at: ')
            #Check if the k_start value choosen can be converted to int
            try:
                int(k_stop)
            #If the value can not be converted to int set the FlagTry to false
            except ValueError:
                FlagTry = False

            if FlagTry:
                k_stop = int(k_stop)
                if k_stop < k_start:
                    raise ValueError(f"The k-value selected needs to be larger or equal to the starting k_value.")

            else:
                raise ValueError(f"The k-value selected needs to be an integer.")
            

            AdjacentAlgorithm = Adjacent(1)
            MemoryIn = [0]

            #crate array to store avg compression rates for all orders and k_values
            k_array = []
            cr_array = []
            for k_values in range(k_start, k_stop+1):
                k_array.append(k_values)
                cr_array.append([])

            #Create array to store ideal k-value for each order and codewords
            k_ideal_array = []
            
            for block in range(len(TestData)):
                #Grab the testdata for the current block
                CurrentTestData = TestData[block]
                for sample in range(256):
                    
                    #create an array to save all mic values for current data sample
                    testInputs = []
                    for microphone in range(end_mic+1-start_mic):
                        testIn = CurrentTestData[microphone,sample]
                        testInputs.append(testIn)

                    CurrentResiduals, memoryIn, CurrentPredictions = AdjacentAlgorithm.In(testInputs, MemoryIn)
                

                    
                    #Rice codes the residuals from Adjacent
                    uncoded_word = ""
                    for j in range(len(k_array)):
                        k = k_array[j]
                        Rice_coder = RiceCoding(k, True)
                        CodeWord = ""
                        CurrentResidualsCopy = CurrentResiduals.copy()
                        for i in range(len(CurrentResiduals)):

                            if j == 0:
                                #Saves binary value of input, represented in 24 bits
                                uncoded_word += np.binary_repr(abs(testInputs[i]),24)


                            
                        
                            kodOrd = Rice_coder.Encode(CurrentResidualsCopy[i])
                            CodeWord += kodOrd
                            
                            
                        cr = len(CodeWord) / len(uncoded_word)

                        cr_array[j].append(cr)
                        



                    #Calculates the ideal k-value according to Rice theory
                    abs_res = np.absolute(CurrentResiduals.copy())
                    abs_res_avg = np.mean(abs_res)
                    
                    #if abs_res_avg is less than 4.7 it would give a k value less than 1.
                    #k needs tobe a int > 1 and therefore if abs_res_avg < 5 k is set to 1
                    #OBS. 4.7 < abs_res_avg < 5 would be rounded of to k=1 so setting the limit to 5 works well
                    if abs_res_avg > 5:
                        k = int(round(math.log(math.log(2,10) * abs_res_avg,2)))
                    else:
                        k = 1
                    #Saves the current ideal k value to later use for decoding
                    
                    k_ideal_array.append(k)


            avg_k_ideal = round(sum(k_ideal_array) / len(k_ideal_array))

            avg_cr_array = []

            for itter in range(len(cr_array)):
                avg_cr = sum(cr_array[itter]) / len(cr_array[itter])
                avg_cr_array.append(avg_cr)

            print("Ideal k value using Adjacent is: ", avg_k_ideal)
            print("")
            print("K-values: ", k_array)
            print("Average compression rates: ", avg_cr_array)

            #Figure to plot all k-values in
            plt.figure("Compression rate for differente k-values using Adjacent with Rice codes", layout = 'constrained')

            plt.plot(k_array, avg_cr_array, 'bo')

            plt.yticks(fontsize=25)
            plt.xticks(fontsize=25)
            plt.xlabel("k-value", fontsize=30)
            plt.ylabel("Average compression ratio", fontsize=30)

            plt.show()


        elif self.TestNr == 21:
            #Select what mics are going to be plotted
            start_mic = input('Select what microhpone to use: ')
            #Check if the start_mic value choosen can be converted to int
            try:
                int(start_mic)
            #If the value can not be converted to int set the FlagTry to false
            except ValueError:
                FlagTry = False

            if FlagTry:
                start_mic = int(start_mic)
            else:
                raise ValueError(f"The microphone value selected needs to be an integer.")
            
            end_mic = input('Select what microhpone to end at (if only one mic is desired choose the same value as start microphone): ')
            #Check if the end_mic value choosen can be converted to int
            try:
                int(end_mic)
            #If the value can not be converted to int set the FlagTry to false
            except ValueError:
                FlagTry = False

            if FlagTry:
                end_mic = int(end_mic)
            else:
                raise ValueError(f"The microphone value selected needs to be an integer.")
            
            

            
            #Store the data from the desired microphones and datablocks in TestData
            TestData = self.DataSelect(OriginalData, datablocks, start_mic, end_mic)

            AdjacentAlgorithm = MetaAdjacent(order=1)
            MemoryIn = [0]
            cr_array = []



            for block in range(len(TestData)):
                #Grab the testdata for the current block
                CurrentTestData = TestData[block]

                for sample in range(256):
                    
                    #create an array to save all mic values for current data sample
                    testInputs = []
                    for microphone in range(end_mic + 1 - start_mic):
                        testIn = CurrentTestData[microphone,sample]
                        testInputs.append(testIn)

                    CurrentCodeWord, MemoryIn = AdjacentAlgorithm.In(testInputs, MemoryIn)

                    
                    uncoded_word = ""
                    for i in range(len(testInputs)):
                        #Saves binary value of input, represented in 24 bits
                        uncoded_word += np.binary_repr(testInputs[i],24)

                    cr = len(CurrentCodeWord) / len(uncoded_word)

                    cr_array.append(cr)

            avg_cr = sum(cr_array) / len(cr_array)

            print("Average compression rate using Adjacent is: ", avg_cr)


        elif self.TestNr == 22:
            #Select what mics are going to be plotted
            start_mic = input('Select what microhpone to use: ')
            #Check if the start_mic value choosen can be converted to int
            try:
                int(start_mic)
            #If the value can not be converted to int set the FlagTry to false
            except ValueError:
                FlagTry = False

            if FlagTry:
                start_mic = int(start_mic)
            else:
                raise ValueError(f"The microphone value selected needs to be an integer.")
            
            end_mic = input('Select what microhpone to end at (if only one mic is desired choose the same value as start microphone): ')
            #Check if the end_mic value choosen can be converted to int
            try:
                int(end_mic)
            #If the value can not be converted to int set the FlagTry to false
            except ValueError:
                FlagTry = False

            if FlagTry:
                end_mic = int(end_mic)
            else:
                raise ValueError(f"The microphone value selected needs to be an integer.")
            
            

            
            #Store the data from the desired microphones and datablocks in TestData
            TestData = self.DataSelect(OriginalData, datablocks, start_mic, end_mic)

            AdjacentAlgorithm = MetaAdjacent(order=1)
            MemoryIn = [0]
            MemoryOut = [0]
            code_words = []
            AllInputs = []

            for block in range(len(TestData)):
                #Grab the testdata for the current block
                CurrentTestData = TestData[block]

                for sample in range(256):
                    
                    #create an array to save all mic values for current data sample
                    testInputs = []
                    for microphone in range(end_mic + 1 - start_mic):
                        testIn = CurrentTestData[microphone,sample]
                        testInputs.append(testIn)

                    CurrentCodeWord, MemoryIn = AdjacentAlgorithm.In(testInputs, MemoryIn)


                    #Saves codewords
                    code_words.append(CurrentCodeWord)
                    AllInputs.append(testInputs)


            #Recreate inputs
            TimeArray = []
            for i in range(len(code_words)):

                #Recreate the original inputs
                start_time = time.time()
                CurrentRecreatedInputs, MemoryOut = AdjacentAlgorithm.Out(code_words[i], MemoryOut)
                end_time = time.time()
                total_time = end_time - start_time
                TimeArray.append(total_time)

            #This is time for one value
            avg_time = sum(TimeArray) / len(TimeArray)
            #To get it for an entire datablock take it times 256
            avg_time = avg_time * 256
            

            print("Average time (in seconds) for Adjacent to reacreate a datablock of values while using Rice codes: ", avg_time,"s")


        elif self.TestNr == 23:
            #Select what mics are going to be plotted
            start_mic = input('Select what microhpone to use: ')
            #Check if the start_mic value choosen can be converted to int
            try:
                int(start_mic)
            #If the value can not be converted to int set the FlagTry to false
            except ValueError:
                FlagTry = False

            if FlagTry:
                start_mic = int(start_mic)
            else:
                raise ValueError(f"The microphone value selected needs to be an integer.")
            
            end_mic = input('Select what microhpone to end at (if only one mic is desired choose the same value as start microphone): ')
            #Check if the end_mic value choosen can be converted to int
            try:
                int(end_mic)
            #If the value can not be converted to int set the FlagTry to false
            except ValueError:
                FlagTry = False

            if FlagTry:
                end_mic = int(end_mic)
            else:
                raise ValueError(f"The microphone value selected needs to be an integer.")
            
            

            
            #Store the data from the desired microphones and datablocks in TestData
            TestData = self.DataSelect(OriginalData, datablocks, start_mic, end_mic)

            AdjacentAlgorithm = Adjacent(1)
            MemoryIn = [0]
            MemoryOut = [0]
            AllInputs = []
            AllCodeWords = []
            AllMvalues = []
    

            for block in range(len(TestData)):
                #Grab the testdata for the current block
                CurrentTestData = TestData[block]

                for sample in range(256):

                    if block == 0:
                        AllCodeWords.append([])
                        AllMvalues.append([])
                    
                    #create an array to save all mic values for current data sample
                    testInputs = []
                    for microphone in range(end_mic + 1 - start_mic):
                        testIn = CurrentTestData[microphone,sample]
                        testInputs.append(testIn)

                    CurrentResiduals, MemoryIn, CurrentPredictions = AdjacentAlgorithm.In(testInputs, MemoryIn)

                    AllInputs.append(testInputs)

                    #Calculates the ideal k_vaule for the residuals
                    abs_res = np.absolute(CurrentResiduals)
                    abs_res_avg = np.mean(abs_res)
                    #if abs_res_avg is less than 4.7 it would give a k value less than 1.
                    #k needs tobe a int > 1. All abs_res_avg values bellow 6.64 will be set to 1 to avoid this issue
                    if abs_res_avg > 6.64:

                        k = int(round(math.log(math.log(2,10) * abs_res_avg,2))) + 1
                    else:
                        k = 1

                    #calculating the m value by taking 2 to the power of k
                        
                    m = pow(2,k)

                    #Golomb code the resiudals
                    
                    CodeWord = ""
                    for i in range(len(CurrentResiduals)):
                        Golomb_coder = GolombCoding(m, True)
                        n = int(CurrentResiduals[i])
                        kodOrd = Golomb_coder.Encode(n)
                        CodeWord += kodOrd
                    
                    #Save the ricecoded residuals and k-values to later decode
                    AllCodeWords[sample].append(CodeWord)
                    AllMvalues[sample].append(m)



            
            

            

            #Recreate inputs
            TimeArray = []
            #Loop thorugh all data blocks
            for i in range(datablocks):
                start_time = time.time()
                #loop thorugh all samples
                for sample in range(256):

                    #Grab data from the current sample
                    CodeWordsDataSample = AllCodeWords[sample]
                    MvaluesSample = AllMvalues[sample]


                    #Grab data from the current datablock
                    CodeWord = CodeWordsDataSample[i]
                    mValue = MvaluesSample[i]


                    Golomb_decoder = GolombCoding(mValue, True)
                    residuals = Golomb_decoder.Decode(CodeWord)

                    #Recreate the original inputs
                    CurrentRecreatedInputs, MemoryOut, predictions = AdjacentAlgorithm.Out(residuals, MemoryOut)
                
                end_time = time.time()
                total_time = end_time - start_time
                TimeArray.append(total_time)

            avg_time = sum(TimeArray) / len(TimeArray)

            print("Average time (in seconds) for Adjacent to reacreate a datablock of values while using Golomb codes: ", avg_time,"s")


        #FLAC-Modified tests
        elif self.TestNr == 24:
            #Select what mics are going to be compressed
            start_mic = input('Select what microhpone to start from: ')
            #Check if the start_mic value choosen can be converted to int
            try:
                int(start_mic)
            #If the value can not be converted to int set the FlagTry to false
            except ValueError:
                FlagTry = False

            if FlagTry:
                start_mic = int(start_mic)
            else:
                raise ValueError(f"The microphone value selected needs to be an integer.")
            

            end_mic = input('Select what microhpone to end at (if only one mic is desired choose the same value as start microphone): ')
            #Check if the end_mic value choosen can be converted to int
            try:
                int(end_mic)
            #If the value can not be converted to int set the FlagTry to false
            except ValueError:
                FlagTry = False

            if FlagTry:
                end_mic = int(end_mic)
            else:
                raise ValueError(f"The microphone value selected needs to be an integer.")
            
            

            
            #Store the data from the desired microphones and datablocks in TestData
            TestData = self.DataSelect(OriginalData, datablocks, start_mic, end_mic)


            microhpones = end_mic - start_mic
            
            FlacAlgorithm = FlacModified(mics= microhpones)


            #Create MemoryArray
            Memorys = []
            for j in range(end_mic + 1 - start_mic):
                    Memorys.append([0]*4)

            

            #Array to store all compression rates
            cr_array = []

            
            for CurrentBlock in range(len(TestData)):
                #Use FLAC Modified to create the code words
                CurrentTestData = TestData[CurrentBlock]
                #Grabs codewords for all mics in the current datablock
                CodeWords, Memorys = FlacAlgorithm.In(CurrentTestData.copy(), Memorys)
                for mic in range(end_mic - start_mic):
                    
                    #Grab codeword for current mic
                    CodeWord = CodeWords[mic]    

                    #Create codeword for current mic/datablock
                    CurrentTestDataMic = CurrentTestData[mic]
                    

                    #Create binary uncoded word for current input, original value represented in 24 bits
                    UncodedWord = ""
                    for sample in CurrentTestDataMic:
                        UncodedWord += np.binary_repr(sample, 24)

                    #Calculate CR for current codeword
                    cr = len(CodeWord) / len(UncodedWord)
                    #Save Cr in array
                    cr_array.append(cr)

            #Calculate average CR for all codewords
            avg_cr = sum(cr_array) / len(cr_array)

            print("Average compression rate using FLAC Modified is, CR = ",avg_cr)
            
        elif self.TestNr == 25:
            #Select what mics are going to be compressed
            start_mic = input('Select what microhpone to start from: ')
            #Check if the start_mic value choosen can be converted to int
            try:
                int(start_mic)
            #If the value can not be converted to int set the FlagTry to false
            except ValueError:
                FlagTry = False

            if FlagTry:
                start_mic = int(start_mic)
            else:
                raise ValueError(f"The microphone value selected needs to be an integer.")
            

            end_mic = input('Select what microhpone to end at (if only one mic is desired choose the same value as start microphone): ')
            #Check if the end_mic value choosen can be converted to int
            try:
                int(end_mic)
            #If the value can not be converted to int set the FlagTry to false
            except ValueError:
                FlagTry = False

            if FlagTry:
                end_mic = int(end_mic)
            else:
                raise ValueError(f"The microphone value selected needs to be an integer.")
            
            

            
            #Store the data from the desired microphones and datablocks in TestData
            TestData = self.DataSelect(OriginalData, datablocks, start_mic, end_mic)



            
            microhpones = end_mic - start_mic
            
            FlacAlgorithm = FlacModified(mics= microhpones)


            #Create MemoryArray
            MemorysIn = []
            MemorysOut = []
            for j in range(end_mic + 1 - start_mic):
                    MemorysIn.append([0]*4)
                    MemorysOut.append([0]*4)


            
            

            

            #Array to store all CodeWords
            CodeWordArray = []


            
            for CurrentBlock in range(len(TestData)):
                #Use FLAC Modified to create the code words
                CurrentTestData = TestData[CurrentBlock]
                CodeWords, MemorysIn = FlacAlgorithm.In(CurrentTestData.copy(), MemorysIn)
                CodeWordArray.append(CodeWords)



            #Array to store Decoding time
            TimeArray = []

            for i in range(datablocks):
                #Start time
                start_time = time.time()
                CodeWords = CodeWordArray[i]
                            
                
                    
                
                #Decode the codeword fo every datablock
                DecodedData, MemorysOut = FlacAlgorithm.Out(CodeWords, MemorysOut)

                #Stop time
                stop_time = time.time()

                #Calculate totalt time
                total_time = stop_time - start_time
                
                #Store total time in array
                TimeArray.append(total_time)

            #Calculate average time
            avg_time = sum(TimeArray) / len(TimeArray)

            print("Average time (in seconds) to recreate a full datablock using FLAC Modified is: ",avg_time," s")

        #DoubleCompression test
        elif self.TestNr == 26:
            #Select what mics are going to be compressed
            start_mic = input('Select what microhpone to start from: ')
            #Check if the start_mic value choosen can be converted to int
            try:
                int(start_mic)
            #If the value can not be converted to int set the FlagTry to false
            except ValueError:
                FlagTry = False

            if FlagTry:
                start_mic = int(start_mic)
            else:
                raise ValueError(f"The microphone value selected needs to be an integer.")
            

            end_mic = input('Select what microhpone to end at: ')
            #Check if the end_mic value choosen can be converted to int
            try:
                int(end_mic)
            #If the value can not be converted to int set the FlagTry to false
            except ValueError:
                FlagTry = False

            if FlagTry:
                end_mic = int(end_mic)
            else:
                raise ValueError(f"The microphone value selected needs to be an integer.")
            

            
            #Store the data from the desired microphones and datablocks in TestData
            TestData = self.DataSelect(OriginalData, datablocks, start_mic, end_mic)


            Order = input('Select order (0-4): ')
            #Check if the Order value choosen can be converted to int
            try:
                int(Order)
            #If the value can not be converted to int set the FlagTry to false
            except ValueError:
                FlagTry = False

            if FlagTry:
                Order = int(Order)
                if Order < 0 or Order > 4:
                    raise ValueError(f"The order selected needs to be between 0 and 4.")

            else:
                raise ValueError(f"The order selected needs to be an integer.")
            
            microhpones = end_mic - start_mic
            
            #Create memory array with appropriate length for selected order
            MemoryIn = []
            for j in range(microhpones):

                MemoryIn.append([0]*4)
                
            

            AdjacentMemory = [0] * 4


            

            DoubleCompressionAlgorithm = DoubleCompression(ShortenOrder=Order, mics=microhpones)

             #Array to store all compression rates
            cr_array = []

            
            for CurrentBlock in range(len(TestData)):
                #Use FLAC Modified to create the code words
                CurrentTestData = TestData[CurrentBlock]
                #Grabs codewords for all mics in the current datablock
                CodeWords, MemoryIn, AdjacentMemory, currentAllSorted = DoubleCompressionAlgorithm.In(CurrentTestData.copy(), MemoryIn, AdjacentMemory)
                for mic in range(end_mic - start_mic):
                    
                    #Grab codeword for current mic
                    CodeWord = CodeWords[mic]    

                    #Create codeword for current mic/datablock
                    CurrentTestDataMic = CurrentTestData[mic]
                    

                    #Create binary uncoded word for current input, original value represented in 24 bits
                    UncodedWord = ""
                    for sample in CurrentTestDataMic:
                        UncodedWord += np.binary_repr(sample, 24)

                    #Calculate CR for current codeword
                    cr = len(CodeWord) / len(UncodedWord)
                    #Save Cr in array
                    cr_array.append(cr)

            #Calculate average CR for all codewords
            avg_cr = sum(cr_array) / len(cr_array)

            print("Average compression rate using DoubleCompression is, CR = ",avg_cr)
            

        elif self.TestNr == 27:
            #Select what mics are going to be compressed
            start_mic = input('Select what microhpone to start from: ')
            #Check if the start_mic value choosen can be converted to int
            try:
                int(start_mic)
            #If the value can not be converted to int set the FlagTry to false
            except ValueError:
                FlagTry = False

            if FlagTry:
                start_mic = int(start_mic)
            else:
                raise ValueError(f"The microphone value selected needs to be an integer.")
            

            end_mic = input('Select what microhpone to end at: ')
            #Check if the end_mic value choosen can be converted to int
            try:
                int(end_mic)
            #If the value can not be converted to int set the FlagTry to false
            except ValueError:
                FlagTry = False

            if FlagTry:
                end_mic = int(end_mic)
            else:
                raise ValueError(f"The microphone value selected needs to be an integer.")
            

            
            #Store the data from the desired microphones and datablocks in TestData
            TestData = self.DataSelect(OriginalData, datablocks, start_mic, end_mic)


            Order = input('Select order (0-4): ')
            #Check if the Order value choosen can be converted to int
            try:
                int(Order)
            #If the value can not be converted to int set the FlagTry to false
            except ValueError:
                FlagTry = False

            if FlagTry:
                Order = int(Order)
                if Order < 0 or Order > 4:
                    raise ValueError(f"The order selected needs to be between 0 and 4.")

            else:
                raise ValueError(f"The order selected needs to be an integer.")
            
            microhpones = end_mic - start_mic
            
            #Create memory array with appropriate length for selected order
            MemoryIn = []
            MemoryOut= []
            for j in range(microhpones):

                MemoryIn.append([0]*4)
                MemoryOut.append([0]*4)
                
            

            AdjacentMemoryIn = [0] * 4
            AdjacentMemoryOut = [0] * 4


            

            DoubleCompressionAlgorithm = DoubleCompression(ShortenOrder=Order, mics=microhpones)

            #Array to store all CodeWords
            CodeWordArray = []


            
            for CurrentBlock in range(len(TestData)):
                #Use FLAC Modified to create the code words
                CurrentTestData = TestData[CurrentBlock]
                CodeWords, MemoryIn, AdjacentMemoryIn, AllSortedResiduals = DoubleCompressionAlgorithm.In(CurrentTestData.copy(), MemoryIn, AdjacentMemoryIn)
                CodeWordArray.append(CodeWords)



            #Array to store Decoding time
            TimeArray = []

            for i in range(datablocks):
                #Start time
                start_time = time.time()
                CodeWords = CodeWordArray[i]
                            
                
                    
                
                #Decode the codeword fo every datablock
                Decodedvalues, MemoryOut, AdjacentMemoryOut = DoubleCompressionAlgorithm.Out(CodeWords, MemoryOut, AdjacentMemoryOut)
                stop_time = time.time()

                #Calculate totalt time
                total_time = stop_time - start_time
                
                #Store total time in array
                TimeArray.append(total_time)

            #Calculate average time
            avg_time = sum(TimeArray) / len(TimeArray)

            print("Average time (in seconds) to recreate a full datablock using DoubleCompression is: ",avg_time," s")

            
        
            

        else:
            raise ValueError(f"Test {self.TestNr} does not exist, please select a test between 1 and 27")
        
        pass


    

    




        
        