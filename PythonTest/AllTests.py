import math
import numpy as np
import matplotlib.pyplot as plt
import time
import sys
sys.path.insert(0, '/home/luigi/Desktop/GIT/Examensarbete')#Change this path to where all the files with the functions are stored
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


    

    




        
        