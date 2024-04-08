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
            print('Test 16. Compare original input with recreated values when using FLAC to see if all values have been recreated correctly.')
        elif self.TestNr == 17:
            print('Test 17. Test compression rate using FLAC.')
        elif self.TestNr == 18:
            print('Test 18. Average speed to recreate values from codewords using FLAC.')

        #Adjacent tests
        elif self.TestNr == 19:
            print('Test 19. Compare original input with recreated values when using Adjacent with Rice codes to see if all values have been recreated correctly.')
        elif self.TestNr == 20:
            print('Test 20. Compare original input with recreated values when using Adjacent with Golomb codes to see if all values have been recreated correctly.')
        elif self.TestNr == 21:
            print('Test 21. Plots compression rate for differnte k-values when using Adjacent with Rice codes.')
        elif self.TestNr == 22:
            print('Test 22. Compression rate using Adjacent with Rice codes.')
        elif self.TestNr == 23:
            print('Test 23. Average speed to recreate values from codewords using Adjacent with Rice codes.')
        elif self.TestNr == 24:
            print('Test 24. Average speed to recreate values from codewords using Adjacent with Golomb codes.')

        #FLAC-Modified tests
        elif self.TestNr == 25:
            print('Test 25. Compare original input with recreated values when using FLAC-Modified to see if all values have been recreated correctly.')
        elif self.TestNr == 26:
            print('Test 26. Test compression rate using FLAC-Modifed.')
        elif self.TestNr == 27:
            print('Test 27. Average speed to recreate values from codewords using FLAC-Modified.')

        #DoubleCompression test
        elif self.TestNr == 28:
            print('Test 28. Compare original input with recreated values when using DoubleCompression to see if all values have been recreated correctly.')
        elif self.TestNr == 29:
            print('Test 29. Test compression rate using DoubleCompression.')
        elif self.TestNr == 30:
            print('Test 30. Average speed to recreate values from codewords using DoubleCompression.')

        else:
            raise ValueError(f"Test {self.TestNr} does not exist, please select a test between 1 and 30")
        
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
            print('Test 16. Compare original input with recreated values when using FLAC to see if all values have been recreated correctly.')
        elif self.TestNr == 17:
            print('Test 17. Test compression rate using FLAC.')
        elif self.TestNr == 18:
            print('Test 18. Average speed to recreate values from codewords using FLAC.')

        #Adjacent tests
        elif self.TestNr == 19:
            print('Test 19. Compare original input with recreated values when using Adjacent with Rice codes to see if all values have been recreated correctly.')
        elif self.TestNr == 20:
            print('Test 20. Compare original input with recreated values when using Adjacent with Golomb codes to see if all values have been recreated correctly.')
        elif self.TestNr == 21:
            print('Test 21. Plots compression rate for differnte k-values when using Adjacent with Rice codes.')
        elif self.TestNr == 22:
            print('Test 22. Compression rate using Adjacent with Rice codes.')
        elif self.TestNr == 23:
            print('Test 23. Average speed to recreate values from codewords using Adjacent with Rice codes.')
        elif self.TestNr == 24:
            print('Test 24. Average speed to recreate values from codewords using Adjacent with Golomb codes.')

        #FLAC-Modified tests
        elif self.TestNr == 25:
            print('Test 25. Compare original input with recreated values when using FLAC-Modified to see if all values have been recreated correctly.')
        elif self.TestNr == 26:
            print('Test 26. Test compression rate using FLAC-Modifed.')
        elif self.TestNr == 27:
            print('Test 27. Average speed to recreate values from codewords using FLAC-Modified.')

        #DoubleCompression test
        elif self.TestNr == 28:
            print('Test 28. Compare original input with recreated values when using DoubleCompression to see if all values have been recreated correctly.')
        elif self.TestNr == 29:
            print('Test 29. Test compression rate using DoubleCompression.')
        elif self.TestNr == 30:
            print('Test 30. Average speed to recreate values from codewords using DoubleCompression.')

        else:
            raise ValueError(f"Test {self.TestNr} does not exist, please select a test between 1 and 30")
        
        pass


    

    




        
        