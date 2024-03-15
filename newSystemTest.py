from lib.beamformer import *
import config as config
import numpy as np
import math
from Rice import RiceCoding
from Golomb import GolombCoding
from Shorten import Shorten
from LPC import LPC
from FLAC import FLAC
from Adjacent import Adjacent
from FlacModified import FlacModified
from AdjacentAndShorten import DoubleCompression

import matplotlib.pyplot as plt
import time




connect()


#Some general inital values for testing
NORM_FACTOR = 16777216
input_new = 0#Used to check if new data is available
w_limit = 0#Is incremented in while loop until limit is reached
best_mic = 79#From looking at the plots in test 1
blasted_mic = 217#From looking at the plots in test 1, seems to have realy high values
silent_mic_1 = 20#From looking at the plots in test 1, allways 0
silent_mic_2 = 19#From looking at the plots in test 1, allways [-1, 0]

#Some inital values for Shorten
memorys = [[],[0],[0,0],[0,0,0]]




#Choose what test to do:
test = 45

#General tests
#Test 1. This test plots microphone data
#Test 2. This test checks average binary len and max length of input data if every data point was written with minimal amount of bits
#Test 4. Try Rice and Golom codes on original inputs

#Shorten tests
#Test 11. Test if Shorten using Rice code can correctly decode the input values
#Test 12. Plots results for differente orders of Shorten
#Test 13. This test tries different k-values in Rice codes for all orders of shorten over several data blocks. (Fixed to compare to original as 24bit)(no meta data taken into acount)
#Test 14. Test if Shorten using Golomb code can correctly decode the input values
#Test 15. This test tries different m-values in Golomb codes for all orders of shorten. (Fixed to compare to original as 24bit)(No meta data taken into acount)
#Test 16. Test what order of Shorten with Rice codes gives best compression rate over a full array of mics.(Fixed to compare to original as 24bit)(added meta data if needed)
#Test 17. Test how long time it takes Shorten to decompress a full array of mics and recreate original inputs when using Rice codes
#Test 18. Test how long time it takes Shorten to decompress a full array of mics and recreate original inputs when using Golomb codes

#LPC tests
#Test 21. Test if LPC using Rice code can correctly decode the input values
#Test 22. Test if LPC using Golomb code can correctly decode the input values
#Test 23. Test what order of LPC gives best result, also test how large of an order it is possible to try
#Test 24. Test what k-value gives the best compression rate when using LPC and Rice codes for different orders of LPC (Fixed to compare to original as 24bit)
#Test 25. Test what m-value gives the best compression rate when using LPC and Golomb codes for different order of LPC(Fixed to compare to original as 24bit)
#Test 26. Test what order of LPC with rice codes gives the best compression rate over a full array of mics(Fixed to compare to original as 24bit)
#Test 27. Test how long time it takes LPC to decompress a full array of mics and recreate original inputs when using Rice codes
#Test 28. Test how long time it takes LPC to decompress a full array of mics and recreate original inputs when using Golomb codes

#FLAC tests
#Test 31. Runs several itteration of FLAC and prints out what gave the best compression rate for that itteration. 
#Along with the compression rate and plotting the recreated signal(Fixed to compare to original as 24bit)
#Test 32. Test the performans of RLE. Need to modify the FLAC function to force the choice of RLE
#Test 33. Test FLAC compression rate for a full array of mics(Possible to compare with and without metadata acounted for)(Comparing to 24 bit data )
#Test 34. Time how long time it takes for FLAC to recreate a full array off microphone values

#Adjacant tests
#Test 41. Plot Residuals using adjacent for some set of mic
#Test 42. Recreate the original input, no encoding for residuals
#Test 43. See how well the Original inputs can be recreated usign Adjacant and Rice codes
#Test 44. Test different k-values to encode residuals from adjacent with Rice codes.
#Test 45. Test different m-values to encode residuals from adjacent with Golomb codes.
#Test 46. Test differente orders for Adjacent with Rice codes
#Test 47. Time how long time it takes for Adhacent to recreate a full array off microphone values using Rice codes
#Test 48. Time how long time it takes for Adhacent to recreate a full array off microphone values using Golomb codes
#Test 49. Compression rate for full array of mics using Adjacent (Comparing to 24 bit data )

#Test that compare all algorithms(Shorten, LPC, FLAC, Adjacent)
#Test 51. Compare compression rate of all algorithms over 1 array of 64 mics, adjusted formula for k-value by incrementing it by 1
#Test 52. Compare compression rate of all algorithms over 1 array of 64 mics, (using original formula for k-value)
#Test 53. Compare compression rate of all algorithms over 1 array but 1 k vale for 256*64 samples

#FlacModified tests
#Test 61. Test if FlacModifed can recreate inputs correctly, with options to plot original inputs, recreated input, and orgiginal input - recreated input
#Test 62. Test Compression rate for FlacModified. Compare with orignal input values as binary 24 bit
#Test 63. Test Decoding speed for FlacModified

#DoubleCompression test
#Test 71. Test if DoubleCompression can ecreate inputs correctly, with options to plot original inputs, recreated input, and orgiginal input - recreated input
#Test 62. Test Compression rate for DoubleCompression. Compare with orignal input values as binary 24 bit
#Test 63. Test Decoding speed for DoubleCompression



#Initial values for tests
if test == 73:
    mic_start = 64
    mic_end = 127
    AllCodeWords = []


    Order = 4
    DoubleCompression_predictor = DoubleCompression(ShortenOrder = Order, mics = (mic_end + 1 - mic_start))

    AdjacentMemoryIn = [0]*4
    ShortenMemoryIn = []
    for i in range(mic_end + 1 - mic_start):
        ShortenMemoryIn.append([0]*4)


if test == 72:
    mic_start = 64
    mic_end = 127
    AllCodeWords = []
    OriginalInputsBinary = []

    Order = 4
    DoubleCompression_predictor = DoubleCompression(ShortenOrder = Order, mics = (mic_end + 1 - mic_start))

    AdjacentMemoryIn = [0]*4
    ShortenMemoryIn = []
    for i in range(mic_end + 1 - mic_start):
        ShortenMemoryIn.append([0]*4)
        

if test == 71:
    mic_start = 64
    mic_end = 127
    AllCodeWords = []
    OriginalInputs = []

    Order = 0
    DoubleCompression_predictor = DoubleCompression(ShortenOrder = Order, mics = (mic_end + 1 - mic_start))

    AdjacentMemoryIn = [0]*4
    ShortenMemoryIn = []
    for i in range(mic_end + 1 - mic_start):
        ShortenMemoryIn.append([0]*4)
        OriginalInputs.append([])


if test == 63:
    mic_start = 64
    mic_end = 127
    FlacMod_predictor = FlacModified(mics = mic_end+1-mic_start)
    memorysIn = []
    AllCodeWords = []
    for i in range(mic_end + 1 - mic_start):
        memorysIn.append([0]*4)


if test == 62:
    mic_start = 64
    mic_end = 127
    FlacMod_predictor = FlacModified(mics = mic_end+1-mic_start)
    memorysIn = []
    AllCodeWords = []
    OriginalInputsBinary = []
    for i in range(mic_end + 1 - mic_start):
        memorysIn.append([0]*4)
        OriginalInputsBinary.append([])
        

if test == 61:
    mic_start = 64
    mic_end = 127
    FlacMod_predictor = FlacModified(mics = mic_end+1-mic_start)
    memorysIn = []
    AllCodeWords = []
    OriginalInputs = []
    for i in range(mic_end + 1 - mic_start):
        memorysIn.append([0]*4)
        OriginalInputs.append([])

    
if test == 53:

    #Shorten initial values
    ShortenOrder = 1
    ShortenResiduals = []
    Shorten_predictor = Shorten(ShortenOrder)
    memoryShorten = []
    CodeWordsShorten = []
    k_Shorten = []

    #LPC initial values
    LpcOrder = 5
    LPC_predictor = LPC(LpcOrder)
    LpcResiduals = []
    #Lpc meta data is cofficents represented in 10 bits for each coefficent
    MetaLpc = np.binary_repr(0,10*LpcOrder)
    memoryLpc = []
    CodeWordsLPC = []
    k_Lpc = []

    #FLAC initial values
    FlacOrder = 10
    FlacResiduals = []
    #Meta data for flac is what type of predictor have benn used, represented in binary values up to 16 (When flac is up to orde 10 LPC),
    #And cofficents (Represented in binary values of 10 bits for each coefficent)
    #And the k-value for each code words, 5 bits 
    MetaFlac = np.binary_repr(0,5+16+(FlacOrder*10))
    FLAC_predictor = FLAC(FlacOrder)
    memoryFlac = []
    codeWordsFLAC = []
    k_Flac = []


    #Adjacent initial values
    AdjacentOrder = 1
    AdjacentResiduals = [0]*256
    Adjacent_predictor = Adjacent(AdjacentOrder)
    memoryAdjacent = []
    CodeWordsAdjacent = []
    UncodedWordsAdjacent = []
    k_Adjacent = []
    Encoding_choice = []



    #Generatl initial values
    UncodedWords = []
    sign = True
    mic_start = 64
    mic_end = 127

    for i in range(mic_start, mic_end+1):
        ShortenResiduals.append(0)
        LpcResiduals.append(0)
        FlacResiduals.append(0)

        k_Flac.append([])

        CodeWordsShorten.append([])
        CodeWordsLPC.append([])
        codeWordsFLAC.append([])

        memoryShorten.append([0]*ShortenOrder)
        memoryLpc.append([0]*LpcOrder)
        memoryFlac.append([0]*FlacOrder)

        UncodedWords.append([])
        Encoding_choice.append([])


if test == 52:

    #Shorten initial values
    ShortenOrder = 1
    Shorten_predictor = Shorten(ShortenOrder)
    memoryShorten = []
    CodeWordsShorten = []
    k_Shorten = []
    #Shorten meta data is only 5 bits for k-value
    ShortenMeta = np.binary_repr(0,5)

    #LPC initial values
    LpcOrder = 5
    LPC_predictor = LPC(LpcOrder)
    #Lpc meta data is cofficents represented in 10 bits for each coefficent, and 5 bits for k-value
    MetaLpc = np.binary_repr(0,5+(10*LpcOrder))
    memoryLpc = []
    CodeWordsLPC = []
    k_Lpc = []

    #FLAC initial values
    FlacOrder = 10
    #Meta data for flac is what type of predictor have benn used, represented in binary values up to 16 (When flac is up to orde 10 LPC),
    #And cofficents (Represented in binary values of 10 bits for each coefficent)
    #And 5 bits for k-value
    MetaFlac = np.binary_repr(0,5+16+(FlacOrder*10))
    FLAC_predictor = FLAC(FlacOrder)
    memoryFlac = []
    codeWordsFLAC = []
    k_Flac = []

    #Adjacent initial values
    AdjacentOrder = 1
    Adjacent_predictor = Adjacent(AdjacentOrder)
    memoryAdjacent = []
    CodeWordsAdjacent = []
    UncodedWordsAdjacent = []
    k_Adjacent = []
    Encoding_choice = []
    #Adjacent meta data is only 5 bits for k-value
    AdjacentMeta = np.binary_repr(0,5)



    #Generatl initial values
    UncodedWords = []
    sign = True
    mic_start = 64
    mic_end = 127

    for i in range(mic_start, mic_end+1):
        k_Shorten.append([])
        k_Lpc.append([])
        k_Flac.append([])

        CodeWordsShorten.append([])
        CodeWordsLPC.append([])
        codeWordsFLAC.append([])

        memoryShorten.append([0]*ShortenOrder)
        memoryLpc.append([0]*LpcOrder)
        memoryFlac.append([0]*FlacOrder)

        UncodedWords.append([])
        Encoding_choice.append([])


if test == 51:

    #Shorten initial values
    ShortenOrder = 1
    Shorten_predictor = Shorten(ShortenOrder)
    memoryShorten = []
    CodeWordsShorten = []
    k_Shorten = []
    #Shorten meta data is only 5 bits for k-value
    ShortenMeta = np.binary_repr(0,5)

    #LPC initial values
    LpcOrder = 5
    LPC_predictor = LPC(LpcOrder)
    #Lpc meta data is cofficents represented in 10 bits for each coefficent, and 5 bits for k-value
    MetaLpc = np.binary_repr(0,5+(10*LpcOrder))
    memoryLpc = []
    CodeWordsLPC = []
    k_Lpc = []

    #FLAC initial values
    FlacOrder = 10
    #Meta data for flac is what type of predictor have benn used, represented in binary values up to 16 (When flac is up to orde 10 LPC),
    #And cofficents (Represented in binary values of 10 bits for each coefficent)
    #And 5 bits for k-value
    MetaFlac = np.binary_repr(0,5+16+(FlacOrder*10))
    FLAC_predictor = FLAC(FlacOrder)
    memoryFlac = []
    codeWordsFLAC = []
    k_Flac = []

    #Adjacent initial values
    AdjacentOrder = 1
    Adjacent_predictor = Adjacent(AdjacentOrder)
    memoryAdjacent = []
    CodeWordsAdjacent = []
    UncodedWordsAdjacent = []
    k_Adjacent = []
    Encoding_choice = []
    #Adjacent meta data is only 5 bits for k-value
    AdjacentMeta = np.binary_repr(0,5)



    #Generatl initial values
    UncodedWords = []
    sign = True
    mic_start = 64
    mic_end = 127

    for i in range(mic_start, mic_end+1):
        k_Shorten.append([])
        k_Lpc.append([])
        k_Flac.append([])

        CodeWordsShorten.append([])
        CodeWordsLPC.append([])
        codeWordsFLAC.append([])

        memoryShorten.append([0]*ShortenOrder)
        memoryLpc.append([0]*LpcOrder)
        memoryFlac.append([0]*FlacOrder)

        UncodedWords.append([])
        Encoding_choice.append([])


if test == 49:
    order = 0
    if order == 0:
        memorysIn = []
    else:
        memorysIn = [0]*order
    uncoded_words = []
    mic_start = 64#sugested 64
    mic_end = 127#Sugested 127
    AllInputsBinary = []
    AllCodeWords = []
    sign = True
    Adjacent_predictor = Adjacent(order)
    #Meta data for Adjacent is only k-value in 5 bits, it is added to every codeword
    #There is one code word for every sample in every datablock, no mather how many mics
    #For a datablock with all 256 samples there are 256 codewords
    MetaData = np.binary_repr(0,5)


if test == 48:
    order = 2
    if order == 0:
        memorysIn = []
    else:
        memorysIn = [0]*order
    mic_start = 64#sugested 64
    mic_end = 127#Sugested 127
    AllInputs = []
    AllCodeWords = []
    AllMvalues = []
    for sample in range(256):
        AllCodeWords.append([])
        AllMvalues.append([])
        AllInputs.append([])
    sign = True
    Adjacent_predictor = Adjacent(order)


if test == 47:
    order = 2
    if order == 0:
        memorysIn = []
    else:
        memorysIn = [0]*order
    mic_start = 64#sugested 64
    mic_end = 127#Sugested 127
    AllInputs = []
    AllCodeWords = []
    AllKvalues = []
    for sample in range(256):
        AllCodeWords.append([])
        AllKvalues.append([])
        AllInputs.append([])
    sign = True
    Adjacent_predictor = Adjacent(order)


if test == 46:
    memorysIn = [[],[0],[0,0],[0,0,0],[0,0,0,0]]
    uncoded_words = []
    mic_start = 64#sugested 64
    mic_end = 127#Sugested 127
    AllInputs = []
    sign = True
    AllResiduals = []
    abs_res = []
    

    for i in range(5):
        AllResiduals.append([])
        abs_res.append([])


if test == 45:
    order = 2
    memoryIn = [0] * order
    Adjacant_predictor = Adjacent(order)
    code_words = []
    uncoded_words = []
    mic_start = 64#sugested 64
    mic_end = 127#Sugested 127
    m_array = []
    AllInputs = []
    sign = True
    AllResiduals = []
    m_start = 43900
    m_end = 44700
    magnitude = 1

    for i in range(m_start, m_end+1):
        code_words.append([])
        m_array.append(i*magnitude)


if test == 44:
    order = 2
    memoryIn = [0] * order
    Adjacant_predictor = Adjacent(order)
    code_words = []
    uncoded_words = []
    mic_start = 64#sugested 64
    mic_end = 127#Sugested 127
    k_array = []
    AllInputs = []
    sign = True
    AllResiduals = []
    k_start = 12
    k_end = 20
    k_ideal_array = []
    abs_res = []

    for i in range(k_start, k_end+1):
        code_words.append([])
        k_array.append(i)


if test == 43:
    order = 2
    memorysIn = [[],[0],[0,0],[0,0,0],[0,0,0,0]]
    memoryIn = memorysIn[order]
    Adjacant_predictor = Adjacent(order)
    code_words = []
    uncoded_words = []
    mic_start = 64#sugested 64
    mic_end = 127#Sugested 127
    k_array = []
    AllInputs = []
    sign = True


if test == 42:
    order = 2
    memoryIn = [0] * order
    Adjacant_predictor = Adjacent(order)
    mic_start = 64#sugested 64
    mic_end = 127#Sugested 127
    AllInputs = []
    AllResiduals = []
    AllPredictions = []


if test == 41:
    order = 2
    memoryIn = [0] * order
    Adjacant_predictor = Adjacent(order)
    mic_residuals = []
    mic_predictions = []
    mic_start = 64#sugested 64
    mic_end = 127#Sugested 127
    for i in range(mic_start, mic_end+1):
        mic_residuals.append([])
        mic_predictions.append([])


if test == 34:
    LPC_Order = 32
    start_mic = 64
    end_mic = 127
    FLAC_prediction = FLAC(LPC_Order)
    MemorysIn = []
    AllCodeWords = []
    AllKvalues = []
    AllEncodingChoices = []
    AllCofficents = []
    AllOriginalInputs = []


    for mic in range(end_mic + 1 - start_mic):
        AllCodeWords.append([])
        AllKvalues.append([])
        AllEncodingChoices.append([])
        AllCofficents.append([])
        AllOriginalInputs.append([])

        if LPC_Order > 4:
            MemorysIn.append([0]*LPC_Order)
        else:
            MemorysIn.append([0]*4)


if test == 33:
    LPC_Order = 32
    start_mic = 64
    end_mic = 127
    FLAC_prediction = FLAC(LPC_Order)
    MemorysIn = []
    AllCodeWords = []

    #Meta data for FLAC is: k-value in 5 bits, enoding choice in 6 bits, and LPC Cofficents in 10 bits each. This is meta data for every codeword
    #(One code word for every data block and mic)
    MetaData = np.binary_repr(0, (5 + 6 + (10 * LPC_Order)))
    for mic in range(end_mic + 1 - start_mic):

        if LPC_Order > 4:
            MemorysIn.append([0]*LPC_Order)
        else:
            MemorysIn.append([0]*4)

    AllEncodingChoices = [0] * (6+LPC_Order)
    OriginalInputsBinary = []


if test == 32:
    LPC_Order = 1
    FLAC_prediction = FLAC(LPC_Order)
    if LPC_Order > 4:
        testMemory = [0]*LPC_Order
    else:
        testMemory = [0]*4

    Encoded_inputs = [] 
    k_value = []
    Encoding_choice = []
    AllMemorys = []
    LPC_Cofficents = []
    AllTestInputs = []


if test == 31:
    LPC_Order = 32
    FLAC_prediction = FLAC(LPC_Order)
    if LPC_Order > 4:
        testMemory = [0]*LPC_Order
    else:
        testMemory = [0]*4

    Encoded_inputs = [] 
    k_value = []
    Encoding_choice = []
    AllMemorys = []
    LPC_Cofficents = []
    AllTestInputs = []


if test == 28:
    Order = 1
    AllCodeWords = []
    AllCofficents = []
    UncodedWords = []
    OriginalInputs = []
    memorysIn = []
    sign = True
    m_array = []
    mic_start = 64
    mic_end = 127
    LPC_predictor = LPC(Order)
    for i in range(mic_start, mic_end+1):
        AllCodeWords.append([])
        memorysIn.append([0]*Order)
        m_array.append([])
        UncodedWords.append([])


if test == 27:
    Order = 1
    AllCodeWords = []
    AllCofficents = []
    UncodedWords = []
    OriginalInputs = []
    memorysIn = []
    sign = True
    k_array = []
    mic_start = 64
    mic_end = 127
    LPC_predictor = LPC(Order)
    for i in range(mic_start, mic_end+1):
        AllCodeWords.append([])
        memorysIn.append([0]*Order)
        k_array.append([])
        UncodedWords.append([])

    
if test == 26:
    Order = 1
    #Metadata for LPC is 5 bits of encoding k value, and 10 bits per cofficent needed to be encoded.
    #The amount of cofficents corresponds to what order of lpc is used
    metaData = np.binary_repr(0,5+(10*Order))
    AllCodeWords = []
    UncodedWords = []
    memorysIn = []
    sign = True
    k_array = []
    mic_start = 64
    mic_end = 127
    all_k = []
    LPC_predictor = LPC(Order)
    for i in range(mic_start, mic_end+1):
        AllCodeWords.append([])
        memorysIn.append([0]*Order)
        k_array.append([])
        UncodedWords.append([])


if test == 25:
    uncoded_words = []
    orders = []
    order_start = 1
    order_stop = 1
    order_array = []
    memorys = []
    for i in range(order_start, order_stop+1):
        orders.append(i)
        order_array.append([])
        memorys.append([0]*i)
    
    #m starting and stop value will be their assigned values times factorr
    #m will increment by step factor each time
    factorr = 1
    m_start = 61000
    m_stop = 67000
    m_array = []

    for i in range(m_start, m_stop+1):
        m_array.append(int(i*factorr))
        for j in range(len(order_array)):
            order_array[j].append([])


if test == 24:
    uncoded_words = []
    orders = []
    order_start = 1
    order_stop = 5
    order_array = []
    k_ideal_array = []
    memorys = []
    for i in range(order_start, order_stop+1):
        orders.append(i)
        order_array.append([])
        k_ideal_array.append([])
        memorys.append([0]*i)
    
    k_start = 1
    k_stop = 8
    k_array = []
    for i in range(k_start, k_stop+1):
        k_array.append(i)
        for j in range(len(order_array)):
            order_array[j].append([])

   
if test == 23:
    data_points = 256#How many samples for each block is gonna be plotted, lower value gives a more zoomed in picture.
    #Can only be changed if recomdended limit = 1
    order_start = 1#Should never be bellow 1
    order_stop = 8#Tested upper limit with 32 as start was =1
    orders = []
    plot_residuals = []
    plot_predict = []
    plot_sig = []
    plot_zero = []
    cof_array = []
    memorys = []

    for i in range(order_start, order_stop+1):
        orders.append(i)
        plot_residuals.append([])
        plot_predict.append([])
        plot_zero.append([])
        memorys.append([0]*i)


if test == 22:
    inputs = []
    code_words = []
    uncoded_words = []
    order = 5
    memory = [0] * order
    LPC_predictor = LPC(order)
    cof_array = []
    m_array = []
    sign = True


if test == 21:
    inputs = []
    code_words = []
    uncoded_words = []
    order = 5
    memory = [0] * order
    LPC_predictor = LPC(order)
    cof_array = []
    k_array = []
    sign = True


if test == 18:
    Order = 3
    AllCodeWords = []
    UncodedWords = []
    OriginalInputs = []
    memorysIn = []
    sign = True
    m_array = []
    mic_start = 64
    mic_end = 127
    Shorten_predictor = Shorten(Order)
    for i in range(mic_start, mic_end+1):
        AllCodeWords.append([])
        if Order > 0:
            memorysIn.append([0]*Order)
        else:
            memorysIn.append([])
        m_array.append([])
        UncodedWords.append([])


if test == 17:
    Order = 3
    AllCodeWords = []
    UncodedWords = []
    OriginalInputs = []
    memorysIn = []
    sign = True
    k_array = []
    mic_start = 64
    mic_end = 127
    Shorten_predictor = Shorten(Order)
    for i in range(mic_start, mic_end+1):
        AllCodeWords.append([])
        if Order > 0:
            memorysIn.append([0]*Order)
        else:
            memorysIn.append([])
        k_array.append([])
        UncodedWords.append([])


if test == 16:
    #Meta data in the case for shorten algorithm would only be the k value.
    #This is encoded in 5 bits, to acount for it when calculating cr 5 bits are added to each codeword
    metaData = np.binary_repr(0,5)
    Order = 3
    AllInputs = []
    AllCodeWords = []
    UncodedWords = []
    memorysIn = []
    sign = True
    k_array = []
    mic_start = 64
    mic_end = 127
    all_k = []
    Shorten_predictor = Shorten(Order)
    for i in range(mic_start, mic_end+1):
        AllCodeWords.append([])
        if Order > 0:
            memorysIn.append([0]*Order)
        else:
            memorysIn.append([])
        k_array.append([])
        UncodedWords.append([])

   
if test == 15:
    uncoded_words = []
    m_start = 164000
    m_stop = 170000
    m_array = []
    order_0_array = []
    order_1_array = []
    order_2_array = []
    order_3_array = []
    for i in range(m_start, m_stop+1):
        m_array.append(i)
        order_0_array.append([])
        order_1_array.append([])
        order_2_array.append([])
        order_3_array.append([])


if test == 14:
    inputs = []
    code_words = []
    uncoded_words = []
    order = 3
    memory = memorys[order].copy()
    Shorten_predictor = Shorten(order)
    m_array = []
    sign = True


if test == 13:
    uncoded_words = []
    k_ideal_array = [[],[],[],[]]
    k_start = 9
    k_stop = 10
    k_array = []
    order_0_array = []
    order_1_array = []
    order_2_array = []
    order_3_array = []
    for i in range(k_start, k_stop+1):
        k_array.append(i)
        order_0_array.append([])
        order_1_array.append([])
        order_2_array.append([])
        order_3_array.append([])


if test == 12:
    
    data_points = 256#How many samples for each block is gonna be plotted, lower value gives a more zoomed in picture.
    #Can only be changed if recomdended limit = 1
    
    plot_residuals = [[],[],[],[]]
    plot_predict = [[],[],[],[]]
    plot_sig = []
    plot_zero = [[],[],[],[]]


if test == 11:
    inputs = []
    code_words = []
    uncoded_words = []
    order = 0
    memory = memorys[order].copy()
    Shorten_predictor = Shorten(order)
    k_array = []
    sign = True


if test == 4:
    sign = True
    code_words_r = []
    code_words_g = []
    uncoded_words_24 = []
    uncoded_words_smal = []
    uncoded_smal_max_array = []


if test == 3:
    loop_time = []


if test == 2:
    code_words_len = []


if test == 1:
    plot_sig = []
    data_points = 256#How many samples for each block is gonna be plotted, lower value gives a more zoomed in picture
    #(Recomended limit should be set to =1 if this is used)



#Grabs one package from the sound file
#Each packet contains 256 smples from all 256 microphones

#The data from the while loop is appended in the test_data array
#It loops recomended_limit amount of time, this depends on the size of the sound file
#23 was found to be a good number to use
recomnded_limit = 20

test_data = []
data = np.empty((config.N_MICROPHONES, config.N_SAMPLES), dtype=np.float32)
while w_limit < recomnded_limit:

    
    receive(data)

    #Multyply by NORM_FACTOR to remove decimals
    data2 = data * NORM_FACTOR


    #convert data into integer
    data2 = data2.astype(int)


    if np.all(data2[best_mic,:]) != np.all(input_new):
        if w_limit == 0:
            print("Start gathering data")
            print("")
        input_new = data2[best_mic,:]#This data choice is only to make sure to wait for a new available data value
        
        
        w_limit +=1
        test_data.append(data2)
    
    

    
    #Pick a micrphone by giving left argument, and sample by giving right arbument
    #To pick all sampels for a specific mic choose a number x for desired mic and ":" for samples:
    #data2[x,:]


print("Data gathered")
print("")
for itter in range(len(test_data)):
    current_data = test_data[itter]
    print("Itteration #", itter)

    if test == 73:
        input_data = current_data[mic_start:mic_end+1,:].copy()
        #Encode the input data for the datablock
        CodeWords, ShortenMemoryIn, AdjacentMemoryIn = DoubleCompression_predictor.In(input_data, ShortenMemoryIn, AdjacentMemoryIn)
        AllCodeWords.append(CodeWords)


    if test == 72:
        input_data = current_data[mic_start:mic_end+1,:].copy()
        #Encode the input data for the datablock
        CodeWords, ShortenMemoryIn, AdjacentMemoryIn = DoubleCompression_predictor.In(input_data, ShortenMemoryIn, AdjacentMemoryIn)
        AllCodeWords.append(CodeWords)

        #Save the original data as 24 bit binary to later compare against the decoded data
        UncodedWords = ""
        for mic in range(mic_start, mic_end+1):
            mic_data = current_data[mic,:]
            for value in mic_data:
                BinaryValue = np.binary_repr(abs(value), 24)

                UncodedWords += BinaryValue

        OriginalInputsBinary.append(UncodedWords)


    if test == 71:
        input_data = current_data[mic_start:mic_end+1,:].copy()

        #Encode the input data for the datablock
        CodeWords, ShortenMemoryIn, AdjacentMemoryIn = DoubleCompression_predictor.In(input_data, ShortenMemoryIn, AdjacentMemoryIn)
        AllCodeWords.append(CodeWords)

        #Save the original data to later compare against the decoded data
        for mic in range(mic_start, mic_end+1):
            mic_data = current_data[mic,:]
            for value in mic_data:
                OriginalInputs[mic-mic_start].append(value)


    if test == 63:
        input_data = current_data[mic_start:mic_end+1,:].copy()

        #Encode the residuals
        CodeWords, memorysIn = FlacMod_predictor.In(input_data, memorysIn)
        #Store the encoded residuals
        AllCodeWords.append(CodeWords)


    if test == 62:
        input_data = current_data[mic_start:mic_end+1,:].copy()

        #Encode the residuals
        CodeWords, memorysIn = FlacMod_predictor.In(input_data, memorysIn)
        #Store the encoded residuals
        AllCodeWords.append(CodeWords)



        #Save the original mic values to later plot
        for mic in range(mic_start, mic_end+1):
            UncodedWord = ""
            OgData = current_data[mic,:].copy()
            for CurrentData in OgData:
               UncodedWord += np.binary_repr(abs(CurrentData),24)
            
            OriginalInputsBinary[mic-mic_start].append(UncodedWord)


    if test == 61:
        input_data = current_data[mic_start:mic_end+1,:].copy()

        #Encode the residuals
        CodeWords, memorysIn = FlacMod_predictor.In(input_data, memorysIn)
        #Store the encoded residuals
        AllCodeWords.append(CodeWords)

        #Save the original mic values to later plot
        for mic in range(mic_start, mic_end+1):
            OgData = current_data[mic,:].copy()
            for CurrentData in OgData:
               OriginalInputs[mic-mic_start].append(CurrentData)
        

    if test == 53:
        inputs = []
        for microphone in range(mic_start, mic_end + 1):
            inputNow = current_data[microphone,:]
            #Save the data for all the microphones of the array to be examined
            inputs.append(inputNow)

            uncoded_word = ""
            for i in range(len(inputNow)):
                #Saves binary value of input, represented in 32 bits
                uncoded_word += np.binary_repr(abs(inputNow[i]),32)
            #Saves the full binary value of the uncoded word in an array
            UncodedWords[microphone-mic_start].append(uncoded_word)

        
        #Shorten calculations:
        abs_res = []
        for mic in range(len(inputs)):
            currentInput = inputs[mic]
            currentResidual, memoryShorten[mic], currentPrediction = Shorten_predictor.In(currentInput, memoryShorten[mic])
            ShortenResiduals[mic] = currentResidual
            #Calculate the sum of the absolute values of all residuals for the current mic and datablock
            total_abs_res = 0
            for i in range(len(currentResidual)):
                total_abs_res += abs(currentResidual[i])
            #Save the current sum of the absolute residuals for the current mic and datablock
            abs_res.append(total_abs_res)
            

        #Calculates the ideal k_vaule for the Shorten residuals off all mics from one data block of 256 samples
        abs_res_avg = np.mean(abs_res)
        #if abs_res_avg is less than 4.7 it would give a k value less than 1.
        #k needs tobe a int > 1. All abs_res_avg values bellow 6.64 will be set to 1 to avoid this issue
        #(the ideal k equation gives k = 1 when abs_res_avg is 6.64)
        if abs_res_avg > 6.64:
            #from testing it appears that the actual ideal k-value is larger by +1 than theory suggest,
        #atleast for larger k-value. The exact limit is unknown but it have been true for all test except for when the lowest k, k =1 is best.
        #Therefore th formula have been modified to increment k by 1 if k is larger than 1.
            k = int(round(math.log(math.log(2,10) * abs_res_avg,2))) + 1
        else:
            k = 1

        #Appends the ideal k vaule in the array matching the correct Shorten order
        k_Shorten.append(k)

        #calculate the rice codes for all mics of a data block of 256 samples
        for mic in range(len(ShortenResiduals)):
            currentResidual = ShortenResiduals[mic]
            #Rice code the residuals using the calculated k-value
            code_word = ""
            for i in range(len(currentResidual)):
                Rice_coder = RiceCoding(k, sign)
                n = int(currentResidual[i])
                kodOrd = Rice_coder.Encode(n)
                code_word += kodOrd
                
            #Saves Rice coded residuals
            CodeWordsShorten[mic].append(code_word)

        

        #LPC calculations
        abs_res = []
        for mic in range(len(inputs)):
            currentInput = inputs[mic]
            currentCofficents, currentResidual, memoryLpc[mic], currentPrediction = LPC_predictor.In(currentInput, memoryLpc[mic])
            #Save the current residual to later encode
            LpcResiduals[mic] = currentResidual
            #Calculate the sum of the absolute values of all residuals for the current mic and datablock
            total_abs_res = 0
            for i in range(len(currentResidual)):
                total_abs_res += abs(currentResidual[i])
            #Save the current sum of the absolute residuals for the current mic and datablock
            abs_res.append(total_abs_res)

        #Calculates the ideal k_vaule for the Shorten residuals off all mics from one data block of 256 samples
        abs_res_avg = np.mean(abs_res)
        #if abs_res_avg is less than 4.7 it would give a k value less than 1.
        #k needs to be a int > 1. All abs_res_avg values bellow 6.64 will be set to 1 to avoid this issue
        #(the ideal k equation gives k = 1 when abs_res_avg is 6.64)
        if abs_res_avg > 6.64:
            #from testing it appears that the actual ideal k-value is larger by +1 than theory suggest,
        #atleast for larger k-value. The exact limit is unknown but it have been true for all test except for when the lowest k, k =1 is best.
        #Therefore th formula have been modified to increment k by 1 if k is larger than 1.
            k = int(round(math.log(math.log(2,10) * abs_res_avg,2)))# + 1
        else:
            k = 1

        #Appends the ideal k vaule in the array matching the correct Shorten order
        k_Lpc.append(k)

        #calculate the rice codes for all mics of a data block of 256 samples
        for mic in range(len(LpcResiduals)):
            currentResidual = LpcResiduals[mic]
            #Rice code the residuals using the calculated k-value
            code_word = MetaLpc
            for i in range(len(currentResidual)):
                Rice_coder = RiceCoding(k, sign)
                n = int(currentResidual[i])
                kodOrd = Rice_coder.Encode(n)
                code_word += kodOrd
                
            #Saves Rice coded residuals
            CodeWordsLPC[mic].append(code_word)
            


        #FLAC calculations
        for mic in range(len(inputs)):
            currentInput = inputs[mic]
            
            Current_Encoded_inputs, Current_k_value, Current_Encoding_choice, memoryFlac[mic], Current_LPC_Cofficents = FLAC_predictor.In(currentInput, memoryFlac[mic])
            code_word = MetaFlac + Current_Encoded_inputs
            
            codeWordsFLAC[mic].append(code_word)
            k_Flac[mic].append(Current_k_value)
            Encoding_choice[mic].append(Current_Encoding_choice)




        #Adjacent calculations
        abs_res = []
        for sample in range(256):
            #print(sample)
            #create an array to save all mic values for current data sample
            testInputs = []
            for microphone in range(mic_start, mic_end+1):
                testIn = current_data[microphone,sample]
                testInputs.append(testIn)

            CurrentResidual, memoryAdjacent, CurrentPredictions = Adjacent_predictor.In(testInputs, memoryAdjacent)
            #Save the current residual to later encode
            AdjacentResiduals[sample] = CurrentResidual
            #Calculate the sum of the absolute values of all residuals for the current mic and datablock
            total_abs_res = 0
            #Calculate the length of uncoded word
            uncoded_word = ""
            for i in range(len(CurrentResidual)):
                total_abs_res += abs(CurrentResidual[i])

                #Saves binary value of input, represented in 32 bits
                uncoded_word += np.binary_repr(abs(testInputs[i]),32)

            #Save the current sum of the absolute residuals for the current mic and datablock
            abs_res.append(total_abs_res)
            #Save the uncoded_word
            UncodedWordsAdjacent.append(uncoded_word)

        
        #Calculates the ideal k-value according to Rice theory
        abs_res_avg = np.mean(abs_res)
        
        #if abs_res_avg is less than 4.7 it would give a k value less than 1.
        #k needs tobe a int > 1. All abs_res_avg values bellow 6.64 will be set to 1 to avoid this issue
        #(the ideal k equation gives k = 1 when abs_res_avg is 6.64)
        if abs_res_avg > 6.64:
            k = int(round(math.log(math.log(2,10) * abs_res_avg,2)))# + 1
        else:
            k = 1
        #Saves the current ideal k value to later use for decoding
        
        k_Adjacent.append(k)

        for sample in range(len(AdjacentResiduals)):
            #Rice codes the residuals from Adjacent and saves the code word in code_word
            code_word = ""
            CurrentResidual = AdjacentResiduals[sample]
            for i in range(len(CurrentResidual)):
                Rice_coder = RiceCoding(k, sign)
                n = int(CurrentResidual[i])
                kodOrd = Rice_coder.Encode(n)
                code_word += kodOrd

            #Saves Rice coded residuals
            CodeWordsAdjacent.append(code_word)

     
    if test == 52:
        inputs = []
        for microphone in range(mic_start, mic_end + 1):
            inputNow = current_data[microphone,:]
            #Save the data for all the microphones of the array to be examined
            inputs.append(inputNow)

            uncoded_word = ""
            for i in range(len(inputNow)):
                #Saves binary value of input, represented in 32 bits
                uncoded_word += np.binary_repr(abs(inputNow[i]),32)
            #Saves the full binary value of the uncoded word in an array
            UncodedWords[microphone-mic_start].append(uncoded_word)

        #Shorten calculations:
        for mic in range(len(inputs)):
            currentInput = inputs[mic]
            currentResidual, memoryShorten[mic], currentPrediction = Shorten_predictor.In(currentInput, memoryShorten[mic])

            #Calculates the ideal k_vaule for the Shorten residuals
            abs_res = np.absolute(currentResidual)
            abs_res_avg = np.mean(abs_res)
            #if abs_res_avg is less than 4.7 it would give a k value less than 1.
            #k needs tobe a int > 1. All abs_res_avg values bellow 6.64 will be set to 1 to avoid this issue
            if abs_res_avg > 6.64:
          
                k = int(round(math.log(math.log(2,10) * abs_res_avg,2)))
            else:
                k = 1

        
            #Appends the ideal k vaule in the array matching the correct Shorten order
            k_Shorten[mic].append(k)

            #Rice code the residuals using the calculated k-value
            code_word = ShortenMeta
            for i in range(len(currentResidual)):
                Rice_coder = RiceCoding(k, sign)
                n = int(currentResidual[i])
                kodOrd = Rice_coder.Encode(n)
                code_word += kodOrd
                
            #Saves Rice coded residuals
            CodeWordsShorten[mic].append(code_word)

        #LPC calculations
        for mic in range(len(inputs)):
            currentInput = inputs[mic]
            currentCofficents, currentResidual, memoryLpc[mic], currentPrediction = LPC_predictor.In(currentInput, memoryLpc[mic])

            #Calculates the ideal k_vaule for the LPC residuals
            abs_res = np.absolute(currentResidual)
            abs_res_avg = np.mean(abs_res)
            #if abs_res_avg is less than 4.7 it would give a k value less than 1.
            #k needs tobe a int > 1. All abs_res_avg values bellow 6.64 will be set to 1 to avoid this issue
            if abs_res_avg > 6.64:
                k = int(round(math.log(math.log(2,10) * abs_res_avg,2)))
            else:
                k = 1

            
            

            #Appends the ideal k vaule in the array matching the correct LPC order
            k_Lpc[mic].append(k)
            

            #Rice code the residuals using the calculated k-value
            
            #Each code word will start with the cofficents
            #This takes into account that higher order of LPC will need more meta data sent
            code_word = MetaLpc
            
            for i in range(len(currentResidual)):
                Rice_coder = RiceCoding(k, sign)
                n = int(currentResidual[i])
                kodOrd = Rice_coder.Encode(n)
                code_word += kodOrd
                
            #Saves Rice coded residuals
            CodeWordsLPC[mic].append(code_word)

        #FLAC calculations
        for mic in range(len(inputs)):
            currentInput = inputs[mic]
            
            Current_Encoded_inputs, Current_k_value, Current_Encoding_choice, memoryFlac[mic], Current_LPC_Cofficents = FLAC_predictor.In(currentInput, memoryFlac[mic])

            code_word = MetaFlac + Current_Encoded_inputs
            
            codeWordsFLAC[mic].append(code_word)
            k_Flac[mic].append(Current_k_value)
            Encoding_choice[mic].append(Current_Encoding_choice)

        #Adjacent calculations
            
        for sample in range(256):
            #print(sample)
            #create an array to save all mic values for current data sample
            testInputs = []
            for microphone in range(mic_start, mic_end+1):
                testIn = current_data[microphone,sample]
                testInputs.append(testIn)

            CurrentResiduals, memoryAdjacent, CurrentPredictions = Adjacent_predictor.In(testInputs, memoryAdjacent)

            #Calculates the ideal k-value according to Rice theory
            abs_res = np.absolute(CurrentResiduals)
            abs_res_avg = np.mean(abs_res)
            
            #if abs_res_avg is less than 4.7 it would give a k value less than 1.
            #k needs tobe a int > 1 and therefore if abs_res_avg < 5 k is set to 1
            #OBS. 4.7 < abs_res_avg < 5 would be rounded of to k=1 so setting the limit to 5 works well
            if abs_res_avg > 6.64:
                k = int(round(math.log(math.log(2,10) * abs_res_avg,2)))
            else:
                k = 1
            #Saves the current ideal k value to later use for decoding
            
            k_Adjacent.append(k)

            #Rice codes the residuals from Adjacent and saves the code word in code_word
            code_word = AdjacentMeta
            uncoded_word = ""
            for i in range(len(CurrentResiduals)):
                Rice_coder = RiceCoding(k, sign)
                n = int(CurrentResiduals[i])
                kodOrd = Rice_coder.Encode(n)
                code_word += kodOrd

                #Saves binary value of input, represented in 32 bits
                uncoded_word += np.binary_repr(abs(testInputs[i]),32)
                


            #Saves Rice coded residuals
            CodeWordsAdjacent.append(code_word)
            UncodedWordsAdjacent.append(uncoded_word)

   
    if test == 51:
        inputs = []
        for microphone in range(mic_start, mic_end + 1):
            inputNow = current_data[microphone,:]
            #Save the data for all the microphones of the array to be examined
            inputs.append(inputNow)

            uncoded_word = ""
            for i in range(len(inputNow)):
                #Saves binary value of input, represented in 32 bits
                uncoded_word += np.binary_repr(abs(inputNow[i]),32)
            #Saves the full binary value of the uncoded word in an array
            UncodedWords[microphone-mic_start].append(uncoded_word)

        #Shorten calculations:
        for mic in range(len(inputs)):
            currentInput = inputs[mic]
            currentResidual, memoryShorten[mic], currentPrediction = Shorten_predictor.In(currentInput, memoryShorten[mic])

            #Calculates the ideal k_vaule for the Shorten residuals
            abs_res = np.absolute(currentResidual)
            abs_res_avg = np.mean(abs_res)
            #if abs_res_avg is less than 4.7 it would give a k value less than 1.
            #k needs tobe a int > 1. All abs_res_avg values bellow 6.64 will be set to 1 to avoid this issue
            if abs_res_avg > 6.64:
                #from testing it appears that the actual ideal k-value is larger by +1 than theory suggest,
            #atleast for larger k-value. The exact limit is unknown but it have been true for all test except for when the lowest k, k =1 is best.
            #Therefore th formula have been modified to increment k by 1 if k is larger than 1.
                k = int(round(math.log(math.log(2,10) * abs_res_avg,2))) + 1
            else:
                k = 1

        
            #Appends the ideal k vaule in the array matching the correct Shorten order
            k_Shorten[mic].append(k)

            #Rice code the residuals using the calculated k-value
            code_word = ShortenMeta
            for i in range(len(currentResidual)):
                Rice_coder = RiceCoding(k, sign)
                n = int(currentResidual[i])
                kodOrd = Rice_coder.Encode(n)
                code_word += kodOrd
                
            #Saves Rice coded residuals
            CodeWordsShorten[mic].append(code_word)

        #LPC calculations
        for mic in range(len(inputs)):
            currentInput = inputs[mic]
            currentCofficents, currentResidual, memoryLpc[mic], currentPrediction = LPC_predictor.In(currentInput, memoryLpc[mic])

            #Calculates the ideal k_vaule for the LPC residuals
            abs_res = np.absolute(currentResidual)
            abs_res_avg = np.mean(abs_res)
            #if abs_res_avg is less than 4.7 it would give a k value less than 1.
            #k needs tobe a int > 1. All abs_res_avg values bellow 6.64 will be set to 1 to avoid this issue
            if abs_res_avg > 6.64:
                #from testing it appears that the actual ideal k-value is larger by +1 than theory suggest,
                #atleast for larger k-value. The exact limit is unknown but it have been true for all test except for when the lowest k, k =1 is best.
                #Therefore th formula have been modified to increment k by 1 if k is larger than 1.
                k = int(round(math.log(math.log(2,10) * abs_res_avg,2))) + 1
            else:
                k = 1

            
            

            #Appends the ideal k vaule in the array matching the correct LPC order
            k_Lpc[mic].append(k)
            

            #Rice code the residuals using the calculated k-value
            
            #Each code word will start with the cofficents
            #This takes into account that higher order of LPC will need more meta data sent
            code_word = MetaLpc
            
            for i in range(len(currentResidual)):
                Rice_coder = RiceCoding(k, sign)
                n = int(currentResidual[i])
                kodOrd = Rice_coder.Encode(n)
                code_word += kodOrd
                
            #Saves Rice coded residuals
            CodeWordsLPC[mic].append(code_word)

        #FLAC calculations
        for mic in range(len(inputs)):
            currentInput = inputs[mic]
            
            Current_Encoded_inputs, Current_k_value, Current_Encoding_choice, memoryFlac[mic], Current_LPC_Cofficents = FLAC_predictor.In(currentInput, memoryFlac[mic])

            code_word = MetaFlac + Current_Encoded_inputs
            
            codeWordsFLAC[mic].append(code_word)
            k_Flac[mic].append(Current_k_value)
            Encoding_choice[mic].append(Current_Encoding_choice)

        #Adjacent calculations
            
        for sample in range(256):
            #print(sample)
            #create an array to save all mic values for current data sample
            testInputs = []
            for microphone in range(mic_start, mic_end+1):
                testIn = current_data[microphone,sample]
                testInputs.append(testIn)

            CurrentResiduals, memoryAdjacent, CurrentPredictions = Adjacent_predictor.In(testInputs, memoryAdjacent)

            #Calculates the ideal k-value according to Rice theory
            abs_res = np.absolute(CurrentResiduals)
            abs_res_avg = np.mean(abs_res)
            
            #if abs_res_avg is less than 4.7 it would give a k value less than 1.
            #k needs tobe a int > 1 and therefore if abs_res_avg < 5 k is set to 1
            #OBS. 4.7 < abs_res_avg < 5 would be rounded of to k=1 so setting the limit to 5 works well
            if abs_res_avg > 6.64:
                k = int(round(math.log(math.log(2,10) * abs_res_avg,2))) + 1
            else:
                k = 1
            #Saves the current ideal k value to later use for decoding
            
            k_Adjacent.append(k)

            #Rice codes the residuals from Adjacent and saves the code word in code_word
            code_word = AdjacentMeta
            uncoded_word = ""
            for i in range(len(CurrentResiduals)):
                Rice_coder = RiceCoding(k, sign)
                n = int(CurrentResiduals[i])
                kodOrd = Rice_coder.Encode(n)
                code_word += kodOrd

                #Saves binary value of input, represented in 32 bits
                uncoded_word += np.binary_repr(abs(testInputs[i]),32)
                


            #Saves Rice coded residuals
            CodeWordsAdjacent.append(code_word)
            UncodedWordsAdjacent.append(uncoded_word)


    if test == 49:
        #Crate an loop that determines how many sampels that are going to be looked at
        for sample in range(256):
            #create an array to save all mic values for current data sample
            testInputs = []
            uncoded_word = ""
            for microphone in range(mic_start, mic_end+1):
                testIn = current_data[microphone,sample]
                testInputs.append(testIn)
                #represent original value in 24 bits
                uncoded_word += np.binary_repr(abs(testIn),24)
            
            AllInputsBinary.append(uncoded_word)

            CurrentResiduals, memorysIn, CurrentPredictions = Adjacent_predictor.In(testInputs, memorysIn)

            #Calculates the ideal k_vaule for the residuals
            abs_res = np.absolute(CurrentResiduals)
            abs_res_avg = np.mean(abs_res)
            #if abs_res_avg is less than 4.7 it would give a k value less than 1.
            #k needs tobe a int > 1. All abs_res_avg values bellow 6.64 will be set to 1 to avoid this issue
            if abs_res_avg > 6.64:
                #from testing it appears that the actual ideal k-value is larger by +1 than theory suggest,
            #atleast for larger k-value. The exact limit is unknown but it have been true for all test except for when the lowest k, k =1 is best.
            #Therefore th formula have been modified to increment k by 1 if abs_res_avg > 6.64.
                k = int(round(math.log(math.log(2,10) * abs_res_avg,2))) + 1
            else:
                k = 1

            #Rice code the resiudals
            #The codeword can either be ="" or =MetaData depending on if cr is tested with or without meta data
            
            CodeWord = ""#MetaData
            for i in range(len(CurrentResiduals)):
                Rice_coder = RiceCoding(k, sign)
                n = int(CurrentResiduals[i])
                kodOrd = Rice_coder.Encode(n)
                CodeWord += kodOrd

            AllCodeWords.append(CodeWord)


    if test == 48:
        #Crate an loop that determines how many sampels that are going to be looked at
        for sample in range(256):
            #create an array to save all mic values for current data sample
            testInputs = []

            for microphone in range(mic_start, mic_end+1):
                testIn = current_data[microphone,sample]
                testInputs.append(testIn)
                
            
            AllInputs[sample].append(testInputs)

            CurrentResiduals, memorysIn, CurrentPredictions = Adjacent_predictor.In(testInputs, memorysIn)

            #Calculates the ideal k_vaule for the residuals
            abs_res = np.absolute(CurrentResiduals)
            abs_res_avg = np.mean(abs_res)
            #if abs_res_avg is less than 4.7 it would give a k value less than 1.
            #k needs tobe a int > 1. All abs_res_avg values bellow 6.64 will be set to 1 to avoid this issue
            if abs_res_avg > 6.64:

                k = int(round(math.log(math.log(2,10) * abs_res_avg,2)))
            else:
                k = 1

            #calculating the m value by taking 2 to the power of k
                
            m = pow(2,k)

            #Golomb code the resiudals
            
            CodeWord = ""#
            for i in range(len(CurrentResiduals)):
                Golomb_coder = GolombCoding(m, sign)
                n = int(CurrentResiduals[i])
                kodOrd = Golomb_coder.Encode(n)
                CodeWord += kodOrd
            
            #Save the ricecoded residuals and k-values to later decode
            AllCodeWords[sample].append(CodeWord)
            AllMvalues[sample].append(m)


    if test == 47:
        #Crate an loop that determines how many sampels that are going to be looked at
        for sample in range(256):
            #create an array to save all mic values for current data sample
            testInputs = []

            for microphone in range(mic_start, mic_end+1):
                testIn = current_data[microphone,sample]
                testInputs.append(testIn)
                
            
            AllInputs[sample].append(testInputs)

            CurrentResiduals, memorysIn, CurrentPredictions = Adjacent_predictor.In(testInputs, memorysIn)

            #Calculates the ideal k_vaule for the residuals
            abs_res = np.absolute(CurrentResiduals)
            abs_res_avg = np.mean(abs_res)
            #if abs_res_avg is less than 4.7 it would give a k value less than 1.
            #k needs tobe a int > 1. All abs_res_avg values bellow 6.64 will be set to 1 to avoid this issue
            if abs_res_avg > 6.64:

                k = int(round(math.log(math.log(2,10) * abs_res_avg,2)))
            else:
                k = 1

            #Rice code the resiudals
            
            CodeWord = ""#
            for i in range(len(CurrentResiduals)):
                Rice_coder = RiceCoding(k, sign)
                n = int(CurrentResiduals[i])
                kodOrd = Rice_coder.Encode(n)
                CodeWord += kodOrd
            
            #Save the ricecoded residuals and k-values to later decode
            AllCodeWords[sample].append(CodeWord)
            AllKvalues[sample].append(k)           


    if test == 46:
        #Crate an loop that determines how many sampels that are going to be looked at
        for sample in range(256):
            #create an array to save all mic values for current data sample
            testInputs = []
            uncoded_word = ""
            for microphone in range(mic_start, mic_end+1):
                testIn = current_data[microphone,sample]
                testInputs.append(testIn)
                uncoded_word += np.binary_repr(abs(testIn),32)
            
            uncoded_words.append(uncoded_word)
            AllInputs.append(testInputs)

            for order in range(5):
                Adjacent_predictor = Adjacent(order)
                CurrentResiduals, memorysIn[order], CurrentPredictions = Adjacent_predictor.In(testInputs, memorysIn[order])
                AllResiduals[order].append(CurrentResiduals)

                for i in range(len(CurrentResiduals)):
                    abs_res[order].append(abs(CurrentResiduals[i]))


    if test == 45:
        #Crate an loop that determines how many sampels that are going to be looked at
        for sample in range(256):
            #create an array to save all mic values for current data sample
            testInputs = []
            for microphone in range(mic_start, mic_end+1):
                testIn = current_data[microphone,sample]
                testInputs.append(testIn)

            CurrentResiduals, memoryIn, CurrentPredictions = Adjacant_predictor.In(testInputs, memoryIn)
            

            #Golomb codes the residuals from shorten and saves the code word in code_word
            code_word = []
            for j in range(len(m_array)):
                code_word.append("")
            uncoded_word = ""

            for i in range(len(CurrentResiduals)):
                n = int(CurrentResiduals[i])
                for j in range(len(m_array)):
                    m = m_array[j]

                    Golomb_coder = GolombCoding(m, sign)
                    kodOrd = Golomb_coder.Encode(n)
                    code_word[j] += kodOrd
                
                #Saves binary value of input, represented in 24 bits
                uncoded_word += np.binary_repr(abs(testInputs[i]),24)

            #Saves Rice coded residuals and binary input values arrays
            for j in range(len(m_array)):
                code_words[j].append(code_word[j])

            uncoded_words.append(uncoded_word)
            AllInputs.append(testInputs)


    if test == 44:
        #Crate an loop that determines how many sampels that are going to be looked at
        for sample in range(256):
            #print(sample)
            #create an array to save all mic values for current data sample
            testInputs = []
            for microphone in range(mic_start, mic_end+1):
                testIn = current_data[microphone,sample]
                testInputs.append(testIn)

            CurrentResiduals, memoryIn, CurrentPredictions = Adjacant_predictor.In(testInputs, memoryIn)
            

            
            

            #Rice codes the residuals from shorten and saves the code word in code_word
            code_word = []
            for j in range(len(k_array)):
                code_word.append("")
            uncoded_word = ""
            for i in range(len(CurrentResiduals)):
                abs_res.append(abs(CurrentResiduals[i]))
                n = int(CurrentResiduals[i])
                for j in range(len(k_array)):
                    k = k_array[j]

                    Rice_coder = RiceCoding(k, sign)
                    kodOrd = Rice_coder.Encode(n)
                    code_word[j] += kodOrd
                
                #Saves binary value of input, represented in 24 bits
                uncoded_word += np.binary_repr(abs(testInputs[i]),24)

            #Saves Rice coded residuals and binary input values arrays
            for j in range(len(k_array)):
                code_words[j].append(code_word[j])

            uncoded_words.append(uncoded_word)
            AllInputs.append(testInputs)
     
 
    if test == 43:
        #Crate an loop that determines how many sampels that are going to be looked at
        for sample in range(256):
            #print(sample)
            #create an array to save all mic values for current data sample
            testInputs = []
            for microphone in range(mic_start, mic_end+1):
                testIn = current_data[microphone,sample]
                testInputs.append(testIn)

            CurrentResiduals, memoryIn, CurrentPredictions = Adjacant_predictor.In(testInputs, memoryIn)

            #Calculates the ideal k-value according to Rice theory
            abs_res = np.absolute(CurrentResiduals)
            abs_res_avg = np.mean(abs_res)
            
            #if abs_res_avg is less than 4.7 it would give a k value less than 1.
            #k needs tobe a int > 1 and therefore if abs_res_avg < 5 k is set to 1
            #OBS. 4.7 < abs_res_avg < 5 would be rounded of to k=1 so setting the limit to 5 works well
            if abs_res_avg > 5:
                k = int(round(math.log(math.log(2,10) * abs_res_avg,2)))
            else:
                k = 1
            #Saves the current ideal k value to later use for decoding
            
            k_array.append(k)

            #Rice codes the residuals from shorten and saves the code word in code_word
            code_word = ""
            uncoded_word = ""
            for i in range(len(CurrentResiduals)):
                Rice_coder = RiceCoding(k, sign)
                n = int(CurrentResiduals[i])
                kodOrd = Rice_coder.Encode(n)
                code_word += kodOrd
                
                #Saves binary value of input, represented in 32 bits
                uncoded_word += np.binary_repr(testInputs[i],32)

            #Saves Rice coded residuals and binary input values arrays
            code_words.append(code_word)
            uncoded_words.append(uncoded_word)
            AllInputs.append(testInputs)
            

    if test == 42:
        #Crate an loop that determines how many sampels that are going to be looked at
        for sample in range(256):
            #print(sample)
            #create an array to save all mic values for current data sample
            testInputs = []
            for microphone in range(mic_start, mic_end+1):
                testIn = current_data[microphone,sample]
                testInputs.append(testIn)

            CurrentResiduals, memoryIn, CurrentPredictions = Adjacant_predictor.In(testInputs, memoryIn)
            AllPredictions.append(CurrentPredictions)
            AllResiduals.append(CurrentResiduals)
            AllInputs.append(testInputs)
            

    if test == 41:
        #Crate an loop that determines how many sampels that are going to be looked at
        for sample in range(100):
            #print(sample)
            #create an array to save all mic values for current data sample
            testInputs = []
            for microphone in range(mic_start, mic_end+1):
                testIn = current_data[microphone,sample]
                testInputs.append(testIn)

            CurrentResiduals, memoryIn, CurrentPredictions = Adjacant_predictor.In(testInputs, memoryIn)

            for i in range(len(CurrentResiduals)):
                mic_residuals[i].append(CurrentResiduals[i])
                mic_predictions[i].append(CurrentPredictions[i])


    if test == 34:
        TestInputs = []
        for microphone in range(start_mic, end_mic+1):
            inputNow = current_data[microphone,:].copy()
            TestInputs.append(inputNow)
            #Save the inputs for the corresponding mic to later check that it was decoded correctly
            AllOriginalInputs[microphone-start_mic].append(inputNow)

            
        for mic in range(len(TestInputs)):
            #Encode the inputs corresponding to a specific mic
            CurrentTestInput = TestInputs[mic]
            Current_Encoded_inputs, Current_k_value, Current_Encoding_choice, MemorysIn[mic], Current_LPC_Cofficents = FLAC_prediction.In(CurrentTestInput, MemorysIn[mic])


            #Save relevant data for each mic
            AllCodeWords[mic].append(Current_Encoded_inputs)
            AllKvalues[mic].append(Current_k_value)
            AllEncodingChoices[mic].append(Current_Encoding_choice)
            AllCofficents[mic].append(Current_LPC_Cofficents)


    if test == 33:
        TestInputs = []
        for microphone in range(start_mic, end_mic+1):
            inputNow = current_data[microphone,:].copy()
            TestInputs.append(inputNow)
            #Save the input value as a binary representation in 24 bits
            UncodedWord = ""
            for value in inputNow:
                UncodedWord += np.binary_repr(abs(value),24)

            #Save the full uncoded word
            OriginalInputsBinary.append(UncodedWord)

        for i in range(len(TestInputs)):
            CurrentTestInput = TestInputs[i]
            Current_Encoded_inputs, Current_k_value, Current_Encoding_choice, MemorysIn[i], Current_LPC_Cofficents = FLAC_prediction.In(CurrentTestInput, MemorysIn[i])

            #Code word can either be set to = MetaData or ="" depending if the test is comparing with our without meta data
            CodeWord = MetaData
            #Save the current codeword
            CodeWord += Current_Encoded_inputs
            AllCodeWords.append(CodeWord)

            #Save the current encoding choice
            EncodingChoice = int(Current_Encoding_choice, 2)
            AllEncodingChoices[EncodingChoice] += 1


    if test == 32:
        testInput = current_data[silent_mic_2,:]#Input data used in test

        
        Current_Encoded_inputs, Current_k_value, Current_Encoding_choice, testMemory, Current_LPC_Cofficents = FLAC_prediction.In(testInput, testMemory)
        
        Encoded_inputs.append(Current_Encoded_inputs)
        k_value.append(Current_k_value)
        Encoding_choice.append(Current_Encoding_choice)
        AllMemorys.append(testMemory)
        LPC_Cofficents.append(Current_LPC_Cofficents)
        AllTestInputs.append(testInput)


    if test == 31:
        testInput = current_data[best_mic,:]#Input data used in test

        
        Current_Encoded_inputs, Current_k_value, Current_Encoding_choice, testMemory, Current_LPC_Cofficents = FLAC_prediction.In(testInput, testMemory)
        
        Encoded_inputs.append(Current_Encoded_inputs)
        k_value.append(Current_k_value)
        Encoding_choice.append(Current_Encoding_choice)
        AllMemorys.append(testMemory)
        LPC_Cofficents.append(Current_LPC_Cofficents)
        AllTestInputs.append(testInput)


    if test == 28:
        inputs = []
        OriginalInputs.append([])
        AllCofficents.append([])
        for microphone in range(mic_start, mic_end + 1):
            inputNow = current_data[microphone,:]
            #Save the data for all the microphones of the array to be examined
            inputs.append(inputNow)
            OriginalInputs[itter].append(inputNow)
            

            uncoded_word = ""
            for i in range(len(inputNow)):
                #Saves binary value of input, represented in 32 bits
                uncoded_word += np.binary_repr(abs(inputNow[i]),32)
            #Saves the full binary value of the uncoded word in an array
            UncodedWords[microphone-mic_start].append(uncoded_word)
            


        for mic in range(len(inputs)):
            currentInput = inputs[mic]
            currentCofficents, currentResidual, memorysIn[mic], currentPrediction = LPC_predictor.In(currentInput, memorysIn[mic])
            #Save the cofficents for the current itteration and mic
            AllCofficents[itter].append(currentCofficents)
            #Calculates the ideal k_vaule for the LPC residuals
            abs_res = np.absolute(currentResidual)
            abs_res_avg = np.mean(abs_res)
            #if abs_res_avg is less than 4.7 it would give a k value less than 1.
            #k needs tobe a int > 1. All abs_res_avg values bellow 6.64 will be set to 1 to avoid this issue
            #(abs_res_avg = 6.64 gives to k = 1)
            if abs_res_avg > 6.64:
                k = int(round(math.log(math.log(2,10) * abs_res_avg,2)))
            else:
                k = 1

            
            #Calulcate the ideal m value from the ideal k value
            m = pow(k,2)

            m_array[mic].append(m)


            #Rice code the residuals using the calculated k-value
            code_word = ""
            for i in range(len(currentResidual)):
                Golomb_coder = GolombCoding(m, sign)
                n = int(currentResidual[i])
                kodOrd = Golomb_coder.Encode(n)
                code_word += kodOrd
                
            #Saves Rice coded residuals
            AllCodeWords[mic].append(code_word)


    if test == 27:
        inputs = []
        OriginalInputs.append([])
        AllCofficents.append([])
        for microphone in range(mic_start, mic_end + 1):
            inputNow = current_data[microphone,:]
            #Save the data for all the microphones of the array to be examined
            inputs.append(inputNow)
            OriginalInputs[itter].append(inputNow)
            

            uncoded_word = ""
            for i in range(len(inputNow)):
                #Saves binary value of input, represented in 32 bits
                uncoded_word += np.binary_repr(abs(inputNow[i]),32)
            #Saves the full binary value of the uncoded word in an array
            UncodedWords[microphone-mic_start].append(uncoded_word)
            


        for mic in range(len(inputs)):
            currentInput = inputs[mic]
            currentCofficents, currentResidual, memorysIn[mic], currentPrediction = LPC_predictor.In(currentInput, memorysIn[mic])
            #Save the cofficents for the current itteration and mic
            AllCofficents[itter].append(currentCofficents)
            #Calculates the ideal k_vaule for the LPC residuals
            abs_res = np.absolute(currentResidual)
            abs_res_avg = np.mean(abs_res)
            #if abs_res_avg is less than 4.7 it would give a k value less than 1.
            #k needs tobe a int > 1. All abs_res_avg values bellow 6.64 will be set to 1 to avoid this issue
            #(abs_res_avg = 6.64 gives to k = 1)
            if abs_res_avg > 6.64:
                k = int(round(math.log(math.log(2,10) * abs_res_avg,2)))
            else:
                k = 1

            
            #Appends the ideal k vaule in the array matching the correct Shorten order
            k_array[mic].append(k)


            #Rice code the residuals using the calculated k-value
            code_word = ""
            for i in range(len(currentResidual)):
                Rice_coder = RiceCoding(k, sign)
                n = int(currentResidual[i])
                kodOrd = Rice_coder.Encode(n)
                code_word += kodOrd
                
            #Saves Rice coded residuals
            AllCodeWords[mic].append(code_word)


    if test == 26:
        inputs = []
        for microphone in range(mic_start, mic_end + 1):
            inputNow = current_data[microphone,:]
            #Save the data for all the microphones of the array to be examined
            inputs.append(inputNow)

            uncoded_word = ""
            for i in range(len(inputNow)):
                #Saves binary value of input, represented in 24 bits
                uncoded_word += np.binary_repr(abs(inputNow[i]),24)
            #Saves the full binary value of the uncoded word in an array
            UncodedWords[microphone-mic_start].append(uncoded_word)
            
        

        for mic in range(len(inputs)):
            currentInput = inputs[mic]
            currentCofficents, currentResidual, memorysIn[mic], currentPrediction = LPC_predictor.In(currentInput, memorysIn[mic])

            #Calculates the ideal k_vaule for the Shorten residuals
            abs_res = np.absolute(currentResidual)
            abs_res_avg = np.mean(abs_res)
            #if abs_res_avg is less than 4.7 it would give a k value less than 1.
            #k needs tobe a int > 1. All abs_res_avg values bellow 6.64 will be set to 1 to avoid this issue
            if abs_res_avg > 6.64:
                #from testing it appears that the actual ideal k-value is larger by +1 than theory suggest,
            #atleast for larger k-value. The exact limit is unknown but it have been true for all test except for when the lowest k, k =1 is best.
            #Therefore th formula have been modified to increment k by 1 if abs_res_avg > 6.64.
                k = int(round(math.log(math.log(2,10) * abs_res_avg,2))) + 1
            else:
                k = 1

            
            #Appends the ideal k vaule in the array matching the correct Shorten order
            k_array[mic].append(k)
            all_k.append(k)

            #Rice code the residuals using the calculated k-value
            
            #Each code word will start with the metadata, it is possible to set code_word = "" to find CR with no meta data taken into acount
            #This takes into account that higher order of LPC will need more meta data sent
            code_word = metaData
            for i in range(len(currentResidual)):
                Rice_coder = RiceCoding(k, sign)
                n = int(currentResidual[i])
                kodOrd = Rice_coder.Encode(n)
                code_word += kodOrd
                
            #Saves Rice coded residuals
            AllCodeWords[mic].append(code_word)

        
    if test == 25:
    

        input = current_data[best_mic,:]#Input data used in test

        
        #loops though all k values in k_array.

        for j in range(len(m_array)):
            m = m_array[j]

            #loops thorugh all order
            for i in range(len(orders)):
                #Does the LPC calculations and updates memory
                LPC_predictor = LPC(orders[i])
                cof, residual, memorys[i], predict = LPC_predictor.In(input, memorys[i])



                #calculates the Rice code word for the residual
                code_word =""
                for q in range(len(input)):
                    
                    Golomb_coder = GolombCoding(m, True)
                    n = int(residual[q])
                    kodOrd = Golomb_coder.Encode(n)
                    code_word += kodOrd
                #The rice code word is saved in the array matching both order and k-value
                order_array[i][j].append(code_word)
                
        
        #Calculates size of uncoded input.
        #Assuming each vaule is repsented in 24 bits.
        uncoded_word = ""              
        for j in range(len(input)):
            uncoded_word += np.binary_repr(abs(input[j]),24)



        #Saves uncoded binary input in array
        uncoded_words.append(uncoded_word)


    if test == 24:
        input = current_data[silent_mic_1,:]#Input data used in test

        
        #loops though all k values in k_array.

        for j in range(len(k_array)):
            k = k_array[j]

            #loops thorugh all order, i = 0-3
            for i in range(len(orders)):
                #Does the LPC calculations and updates memory
                LPC_predictor = LPC(orders[i])
                cof, residual, memorys[i], predict = LPC_predictor.In(input, memorys[i])

                #Calculates the ideal k_vaule for the LPC residuals
                abs_res = np.absolute(residual)
                abs_res_avg = np.mean(abs_res)
                #if abs_res_avg is less than 4.7 it would give a k value less than 1.
                #k needs tobe a int > 1 and therefore if abs_res_avg < 5 k is set to 1
                #OBS. 4.7 < abs_res_avg < 5 would be rounded of to k=1 so setting the limit to 5 works well
                if abs_res_avg > 5:
                    k_ideal = int(round(math.log(math.log(2,10) * abs_res_avg,2)))
                else:
                    k_ideal = 1

                #Appends the ideal k vaule in the array matching the correct Shorten order
                k_ideal_array[i].append(k_ideal)


                #calculates the Rice code word for the residual
                code_word =""
                for q in range(len(input)):
                    
                    Rice_coder = RiceCoding(k, True)
                    n = int(residual[q])
                    kodOrd = Rice_coder.Encode(n)
                    code_word += kodOrd
                #The rice code word is saved in the array matching both order and k-value
                order_array[i][j].append(code_word)
                
        
        #Calculates size of uncoded input.
        #Assuming each vaule is repsented in 24 bits.
        uncoded_word = ""              
        for j in range(len(input)):
            uncoded_word += np.binary_repr(abs(input[j]),24)



        #Saves uncoded binary input in array
        uncoded_words.append(uncoded_word)


    #Plot LPC
    if test == 23:
        input = current_data[best_mic,:]#data used in test
        
        #Saves the amount of data points thats going to be plotted in plot_sig_temp from input data
        plot_sig_temp = []
        if recomnded_limit == 1:
            for j in range(data_points):
                plot_sig_temp.append(input[j])
        else:
            plot_sig_temp = input
        
        #Calculates LPC for some orders for input data
        for i in range(len(orders)):
            LPC_predictor = LPC(orders[i])

            cof, residual, memorys[i], predict = LPC_predictor.In(plot_sig_temp, memorys[i])
            
            cof_array.append(cof)

            #Saves results of shorten for all orders to later be plotted
            for j in range(len(residual)):
                plot_residuals[i].append(residual[j])
                plot_predict[i].append(predict[j])
                plot_zero[i].append(plot_sig_temp[j] - ( predict[j] + residual[j]))
                #Input singla only needs sot be saved once
                if i == 0:
                    plot_sig.append(plot_sig_temp[j])


    #Test LPC and Golomb coding if it can recreate the input data on the decompressed side
    #It saves all input data in inputs array, all coded words in coded_words array and the inputs as binary values in 32 bits
    #It also saves the m-values used and coeficents used for the differente data blocks 
    if test == 22:
    
        input = current_data[best_mic,:]#This mic choice is the mic that will be sent over channel
        code_word =""
        uncoded_word = ""
        #Saves current input values in inputs array
        inputs.append(input)
        
        #uses LPC to calculate residuals
        cof, residuals, memory, predictions = LPC_predictor.In(input, memory)

        #Saves the coefficents to later be used for decoding
        cof_array.append(cof)

        #Calculates the ideal k-value according to Rice theory
        abs_res = np.absolute(residuals)
        abs_res_avg = np.mean(abs_res)
        
        #if abs_res_avg is less than 4.7 it would give a k value less than 1.
        #k needs tobe a int > 1 and therefore if abs_res_avg < 5 k is set to 1
        #OBS. 4.7 < abs_res_avg < 5 would be rounded of to k=1 so setting the limit to 5 works well
        if abs_res_avg > 5:
            k = int(round(math.log(math.log(2,10) * abs_res_avg,2)))
        else:
            k = 1
        #Saves the current ideal k value to later use for decoding
        m = pow(2,k)
        m_array.append(m)

        #Rice codes the residuals from shorten and saves the code word in code_word
        for i in range(len(residuals)):
            Golomb_coder = GolombCoding(m, sign)
            n = int(residuals[i])
            kodOrd = Golomb_coder.Encode(n)
            code_word += kodOrd
            
            #Saves binary value of input, represented in 32 bits
            uncoded_word += np.binary_repr(input[i],32)

        #Saves Rice coded residuals and binary input values arrays
        code_words.append(code_word)
        uncoded_words.append(uncoded_word)


    #Test LPC and Rice coding if it can recreate the input data on the decompressed side
    #It saves all input data in inputs array, all coded words in coded_words array and the inputs as binary values in 32 bits
    #It also saves the k-values used and coeficents used for the differente data blocks   
    if test == 21:
        
        input = current_data[best_mic,:]#This mic choice is the mic that will be sent over channel
        code_word =""
        uncoded_word = ""
        #Saves current input values in inputs array
        inputs.append(input)
        
        #uses LPC to calculate residuals
        cof, residuals, memory, predictions = LPC_predictor.In(input, memory)

        #Saves the coefficents so that they later can be sued when decoding
        cof_array.append(cof)

        #Calculates the ideal k-value according to Rice theory
        abs_res = np.absolute(residuals)
        abs_res_avg = np.mean(abs_res)
        
        #if abs_res_avg is less than 4.7 it would give a k value less than 1.
        #k needs tobe a int > 1 and therefore if abs_res_avg < 5 k is set to 1
        #OBS. 4.7 < abs_res_avg < 5 would be rounded of to k=1 so setting the limit to 5 works well
        if abs_res_avg > 5:
            k = int(round(math.log(math.log(2,10) * abs_res_avg,2)))
        else:
            k = 1
        #Saves the current ideal k value to later use for decoding
        
        k_array.append(k)

        #Rice codes the residuals from shorten and saves the code word in code_word
        for i in range(len(residuals)):
            Rice_coder = RiceCoding(k, sign)
            n = int(residuals[i])
            kodOrd = Rice_coder.Encode(n)
            code_word += kodOrd
            
            #Saves binary value of input, represented in 32 bits
            uncoded_word += np.binary_repr(input[i],32)

        #Saves Rice coded residuals and binary input values arrays
        code_words.append(code_word)
        uncoded_words.append(uncoded_word)


    if test == 18:
        inputs = []
        OriginalInputs.append([])
        for microphone in range(mic_start, mic_end + 1):
            inputNow = current_data[microphone,:]
            #Save the data for all the microphones of the array to be examined
            inputs.append(inputNow)
            OriginalInputs[itter].append(inputNow)
            

            uncoded_word = ""
            for i in range(len(inputNow)):
                #Saves binary value of input, represented in 32 bits
                uncoded_word += np.binary_repr(abs(inputNow[i]),32)
            #Saves the full binary value of the uncoded word in an array
            UncodedWords[microphone-mic_start].append(uncoded_word)
            


        for mic in range(len(inputs)):
            currentInput = inputs[mic]
            currentResidual, memorysIn[mic], currentPrediction = Shorten_predictor.In(currentInput, memorysIn[mic])

            #Calculates the ideal k_vaule for the Shorten residuals
            abs_res = np.absolute(currentResidual)
            abs_res_avg = np.mean(abs_res)
            #if abs_res_avg is less than 4.7 it would give a k value less than 1.
            #k needs tobe a int > 1. All abs_res_avg values bellow 6.64 will be set to 1 to avoid this issue
            #(abs_res_avg = 6.64 gives to k = 1)
            if abs_res_avg > 6.64:
                k = int(round(math.log(math.log(2,10) * abs_res_avg,2)))
            else:
                k = 1

            
            #Calulcate the ideal m value from the ideal k value
            m = pow(k,2)

            m_array[mic].append(m)


            #Rice code the residuals using the calculated k-value
            code_word = ""
            for i in range(len(currentResidual)):
                Golomb_coder = GolombCoding(m, sign)
                n = int(currentResidual[i])
                kodOrd = Golomb_coder.Encode(n)
                code_word += kodOrd
                
            #Saves Rice coded residuals
            AllCodeWords[mic].append(code_word)


    if test == 17:
        inputs = []
        OriginalInputs.append([])
        for microphone in range(mic_start, mic_end + 1):
            inputNow = current_data[microphone,:]
            #Save the data for all the microphones of the array to be examined
            inputs.append(inputNow)
            OriginalInputs[itter].append(inputNow)
            

            uncoded_word = ""
            for i in range(len(inputNow)):
                #Saves binary value of input, represented in 32 bits
                uncoded_word += np.binary_repr(abs(inputNow[i]),32)
            #Saves the full binary value of the uncoded word in an array
            UncodedWords[microphone-mic_start].append(uncoded_word)
            


        for mic in range(len(inputs)):
            currentInput = inputs[mic]
            currentResidual, memorysIn[mic], currentPrediction = Shorten_predictor.In(currentInput, memorysIn[mic])

            #Calculates the ideal k_vaule for the Shorten residuals
            abs_res = np.absolute(currentResidual)
            abs_res_avg = np.mean(abs_res)
            #if abs_res_avg is less than 4.7 it would give a k value less than 1.
            #k needs tobe a int > 1. All abs_res_avg values bellow 6.64 will be set to 1 to avoid this issue
            #(abs_res_avg = 6.64 gives to k = 1)
            if abs_res_avg > 6.64:
                k = int(round(math.log(math.log(2,10) * abs_res_avg,2)))
            else:
                k = 1

            
            #Appends the ideal k vaule in the array matching the correct Shorten order
            k_array[mic].append(k)


            #Rice code the residuals using the calculated k-value
            code_word = ""
            for i in range(len(currentResidual)):
                Rice_coder = RiceCoding(k, sign)
                n = int(currentResidual[i])
                kodOrd = Rice_coder.Encode(n)
                code_word += kodOrd
                
            #Saves Rice coded residuals
            AllCodeWords[mic].append(code_word)


    if test == 16:
        inputs = []
        for microphone in range(mic_start, mic_end + 1):
            inputNow = current_data[microphone,:]
            #Save the data for all the microphones of the array to be examined
            inputs.append(inputNow)

            uncoded_word = ""
            for i in range(len(inputNow)):
                #Saves binary value of input, represented in 24 bits
                uncoded_word += np.binary_repr(abs(inputNow[i]),24)
            #Saves the full binary value of the uncoded word in an array
            UncodedWords[microphone-mic_start].append(uncoded_word)
            
        AllInputs.append(inputs)

        for mic in range(len(inputs)):
            currentInput = inputs[mic]
            currentResidual, memorysIn[mic], currentPrediction = Shorten_predictor.In(currentInput, memorysIn[mic])

            #Calculates the ideal k_vaule for the Shorten residuals
            abs_res = np.absolute(currentResidual)
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

            
            
            #Appends the ideal k vaule in the array matching the correct Shorten order
            k_array[mic].append(k)
            all_k.append(k)

            #Rice code the residuals using the calculated k-value
            
            #Can either set to "" or to metaData if test want to take meta data into acount or not
            code_word = metaData
            for i in range(len(currentResidual)):
                Rice_coder = RiceCoding(k, sign)
                n = int(currentResidual[i])
                kodOrd = Rice_coder.Encode(n)
                code_word += kodOrd
                
            #Saves Rice coded residuals
            AllCodeWords[mic].append(code_word)


    #Tries different m-values in Golob codes for all orders of shorten in order to find which gives the best cr
    if test == 15:

        input = current_data[best_mic,:]#Input data used in test

        
        #loops though all k values in k_array.

        for j in range(len(m_array)):
            m = m_array[j]


            #loops thorugh all order, i = 0-3
            for i in range(4):
                #Does the shorten calculations and updates memory
                Shorten_predictor = Shorten(i)
                residual, memorys[i], predict = Shorten_predictor.In(input, memorys[i])

                #calculates the Golomb code word for the residual
                code_word =""
                for q in range(len(input)):
                    
                    Golomb_coder = GolombCoding(m, True)
                    n = int(residual[q])
                    kodOrd = Golomb_coder.Encode(n)
                    code_word += kodOrd
                #The rice code word is saved in the array matching both order and k-value
                if i == 0:
                    order_0_array[j].append(code_word)

                elif i == 1:
                    order_1_array[j].append(code_word)

                elif i == 2:
                    order_2_array[j].append(code_word)

                elif i == 3:
                    order_3_array[j].append(code_word)
        
        #Calculates size of uncoded input.
        #Assuming each vaule is repsented in 24 bits.
        uncoded_word = ""              
        for j in range(len(input)):
            uncoded_word += np.binary_repr(abs(input[j]),24)



        #Saves uncoded binary input in array
        uncoded_words.append(uncoded_word)
            
            
    #Test Shorten and Golomb coding if it can recreate the input data on the decompressed side
    #It saves all input data in inputs array, all coded words in coded_words array and the inputs as binary values in 32 bits   
    if test == 14:
        input = current_data[best_mic,:]#This mic choice is the mic that will be sent over channel
        code_word =""
        uncoded_word = ""
        #Saves current input values in inputs array
        inputs.append(input)
        
        #uses Shorten to calculate residuals
        residuals, memory, predictions = Shorten_predictor.In(input, memory)

        #Calculates the ideal k-value according to Rice theory
        abs_res = np.absolute(residuals)
        abs_res_avg = np.mean(abs_res)
        
        #if abs_res_avg is less than 4.7 it would give a k value less than 1.
        #k needs tobe a int > 1 and therefore if abs_res_avg < 5 k is set to 1
        #OBS. 4.7 < abs_res_avg < 5 would be rounded of to k=1 so setting the limit to 5 works well
        if abs_res_avg > 5:
            k = int(round(math.log(math.log(2,10) * abs_res_avg,2)))
        else:
            k = 1
        #Saves the current ideal k value to later use for decoding
        m = pow(2,k)
        m_array.append(m)

        #Rice codes the residuals from shorten and saves the code word in code_word
        for i in range(len(residuals)):
            Golomb_coder = GolombCoding(m, sign)
            n = int(residuals[i])
            kodOrd = Golomb_coder.Encode(n)
            code_word += kodOrd
            
            #Saves binary value of input, represented in 32 bits
            uncoded_word += np.binary_repr(input[i],32)

        #Saves Rice coded residuals and binary input values arrays
        code_words.append(code_word)
        uncoded_words.append(uncoded_word)


    #This test tries different k-values for all orders of shorten over several data points.
    #With this it is possible to see:
    #1. What order and k-value gives best cr result.
    #2. What k-value for each order give best cr result.
    #3. How well does the ideal k-value in Rice theory match the practical ideal k-value
    if test == 13:
        input = current_data[silent_mic_1,:]#Input data used in test

            
        #loops though all k values in k_array.

        for j in range(len(k_array)):
            k = k_array[j]

            #loops thorugh all order, i = 0-3
            for i in range(4):
                #Does the shorten calculations and updates memory
                Shorten_predictor = Shorten(i)
                residual, memorys[i], predict = Shorten_predictor.In(input, memorys[i])

                #Calculates the ideal k_vaule for the Shorten residuals
                abs_res = np.absolute(residual)
                abs_res_avg = np.mean(abs_res)
                #if abs_res_avg is less than 4.7 it would give a k value less than 1.
                #k needs tobe a int > 1 and therefore if abs_res_avg < 5 k is set to 1
                #OBS. 4.7 < abs_res_avg < 5 would be rounded of to k=1 so setting the limit to 5 works well
                if abs_res_avg > 5:
                    k_ideal = int(round(math.log(math.log(2,10) * abs_res_avg,2)))
                else:
                    k_ideal = 1

                #Appends the ideal k vaule in the array matching the correct Shorten order
                k_ideal_array[i].append(k_ideal)


                #calculates the Rice code word for the residual
                code_word =""
                for q in range(len(input)):
                    
                    Rice_coder = RiceCoding(k, True)
                    n = int(residual[q])
                    kodOrd = Rice_coder.Encode(n)
                    code_word += kodOrd
                #The rice code word is saved in the array matching both order and k-value
                if i == 0:
                    order_0_array[j].append(code_word)

                elif i == 1:
                    order_1_array[j].append(code_word)

                elif i == 2:
                    order_2_array[j].append(code_word)

                elif i == 3:
                    order_3_array[j].append(code_word)
        
        #Calculates size of uncoded input.
        #Assuming each vaule is repsented in 24 bits.
        uncoded_word = ""              
        for j in range(len(input)):
            uncoded_word += np.binary_repr(abs(input[j]),24)

        #Saves uncoded binary input in array
        uncoded_words.append(uncoded_word)
            

    #This test tries different orders of Shorten to predict input.
    #Output from Shorten is saved so it can be plotted.
    if test == 12:
        input = current_data[best_mic,:]#data used in test
        
        #Saves the amount of data points thats going to be plotted in plot_sig_temp from input data
        plot_sig_temp = []
        if recomnded_limit == 1:
            for j in range(data_points):
                plot_sig_temp.append(input[j])
        else:
            plot_sig_temp = input
        
        #Calculates shorten for all orders for input data
        for i in range(4):
            Shorten_predictor = Shorten(i)

            residual, memorys[i], predict = Shorten_predictor.In(plot_sig_temp, memorys[i])
            
            #Saves results of shorten for all orders to later be plotted
            for j in range(len(residual)):
                plot_residuals[i].append(residual[j])
                plot_predict[i].append(predict[j])
                plot_zero[i].append(plot_sig_temp[j] - ( predict[j] + residual[j]))
                #Input singla only needs sot be saved once
                if i == 0:
                    plot_sig.append(plot_sig_temp[j])


    #Test Shorten and Rice coding if it can recreate the input data on the decompressed side
    #It saves all input data in inputs array, all coded words in coded_words array and the inputs as binary values in 32 bits   
    if test == 11:
        input = current_data[best_mic,:]#This mic choice is the mic that will be sent over channel
        code_word =""
        uncoded_word = ""
        #Saves current input values in inputs array
        inputs.append(input)
        
        #uses Shorten to calculate residuals
        residuals, memory, predictions = Shorten_predictor.In(input, memory)

        #Calculates the ideal k-value according to Rice theory
        abs_res = np.absolute(residuals)
        abs_res_avg = np.mean(abs_res)
        
        #if abs_res_avg is less than 4.7 it would give a k value less than 1.
        #k needs tobe a int > 1 and therefore if abs_res_avg < 5 k is set to 1
        #OBS. 4.7 < abs_res_avg < 5 would be rounded of to k=1 so setting the limit to 5 works well
        if abs_res_avg > 5:
            k = int(round(math.log(math.log(2,10) * abs_res_avg,2)))
        else:
            k = 1
        #Saves the current ideal k value to later use for decoding
        
        k_array.append(k)

        #Rice codes the residuals from shorten and saves the code word in code_word
        for i in range(len(residuals)):
            Rice_coder = RiceCoding(k, sign)
            n = int(residuals[i])
            kodOrd = Rice_coder.Encode(n)
            code_word += kodOrd
            
            #Saves binary value of input, represented in 32 bits
            uncoded_word += np.binary_repr(input[i],32)

        #Saves Rice coded residuals and binary input values arrays
        code_words.append(code_word)
        uncoded_words.append(uncoded_word)

           
    #Test Rice coding and Golomb coding original inputs, compare them to binary coded input values
    if test == 4:   
        input = current_data[best_mic,:]#This mic choice is the mic that will be sent over channel
        code_word_r =""
        code_word_g =""
        uncoded_word_24 = ""
        uncoded_word_smal = ""
        

        #Calculates the ideal k-value according to Rice theory
        abs_res = np.absolute(input)
        abs_res_avg = np.mean(abs_res)

        if abs_res_avg > 5:
            k = int(round(math.log(math.log(2,10) * abs_res_avg,2)))
        else:
            k = 1

        #Calculates what m value to use by taking m = 2^k
        m = pow(2,k)
        


        #Rice codes the inputs and saves the code word in code_word
        uncoded_smal_max = 0
        for i in range(len(input)):

            Golomb_coder = GolombCoding(m, sign)
            Rice_coder = RiceCoding(k, sign)
            n = int(input[i])

            kodOrd_r = Rice_coder.Encode(n)
            code_word_r += kodOrd_r

            kodOrd_g = Golomb_coder.Encode(n)
            code_word_g += kodOrd_g
            
            #Saves binary value of input, represented in 32 bits
            uncoded_word_24 += np.binary_repr(abs(input[i]),24)

            #Have to manualy assign sign bit, since the data is signed
            s = "0"
            if n < 0:
                s = "1"
                #If the input is negative it can be converted to possitve after the sign bit is saved
                n = -n
        
            #Convert input to binary and add sign bit
            temp_smal = (s + bin(n)[2:])

            if len(temp_smal) > uncoded_smal_max:
                uncoded_smal_max = len(temp_smal)

            uncoded_word_smal += temp_smal



        #Saves Rice coded input values, Golomb coded input values, and binary input values arrays (both as 32 bits and smalest possible bit value)
        code_words_r.append(code_word_r)
        code_words_g.append(code_word_g)
        uncoded_words_24.append(uncoded_word_24)
        uncoded_words_smal.append(uncoded_word_smal)
        uncoded_smal_max_array.append(uncoded_smal_max)


    #This test created arrays with minimum binary length for each input value
    if test == 2:
        input = current_data[best_mic,:]#This mic choice is the mic that will be sent over channel
        code_word_len = []

        #loops through the inputs
        for i in range(len(input)):
            n = input[i]
            #Have to manualy assign sign bit, since the data is signed
            s = "0"
            if n < 0:
                s = "1"
                #If the input is negative it can be converted to possitve after the sign bit is saved
                n = -n
            
            n = int(n)
            #Convert input to binary and add sign bit
            kodOrd = s + bin(n)[2:]

            
            #Saves the length of the binary input value in an array
            code_word_len.append(len(kodOrd))
        #Saves all the array values for the data block in an array
        code_words_len.append(code_word_len)


    #This test plots data from all mic
    #Used to find which mices have good/bad recoreded data
    if test == 1: 
        for j in range(256):
            #Picks mic nr j as input
            input_temp = current_data[j,:]#data used in test
            plot_sig_temp = []
            plot_sig.append([])
            
            #Save data_points of sampels for each block in an array for every mic
            for i in range(data_points):
                value = input_temp[i]
                plot_sig_temp.append(value)
            #Appends the arrays of all mics into one array
            if recomnded_limit == 1:
                plot_sig[j].append(plot_sig_temp)
            else:
                for i in range(len(plot_sig_temp)):
                    plot_sig[j].append(plot_sig_temp[i])

    



print("")
if test == 73:
    print("Test 73")
    print("")

    DecodingTime = []

    AdjacentMemoryOut = [0]*4
    ShortenMemoryOut = []

    for mic in range(mic_end + 1 - mic_start):
        ShortenMemoryOut.append([0]*4)


    #recrete the orginal input values for each datablock
    for CodeWords in AllCodeWords:
        start_time = time.time()
        Decodedvalues, ShortenMemoryOut, AdjacentMemoryOut = DoubleCompression_predictor.Out(CodeWords, ShortenMemoryOut, AdjacentMemoryOut)
        stop_time = time.time()
        total_time = stop_time - start_time
        DecodingTime.append(total_time)
        

    avg_time = sum(DecodingTime) / len(DecodingTime)

    print("Average time to recreate values is ",avg_time,"seconds. Using Shorten order ", Order)


if test == 72:
    print("Test 72")
    print("")

    CrArray = []



    for i in range(len(AllCodeWords)):
        MicCodeWord = AllCodeWords[i]
        CurrentUncodedWord = OriginalInputsBinary[i]
        CurrentCodeWord = ""
        for mic in range(len(MicCodeWord)):
            CurrentCodeWord += MicCodeWord[mic]

        cr = len(CurrentCodeWord) / len(CurrentUncodedWord)
        CrArray.append(cr)

    avg_cr = sum(CrArray) / len(CrArray)
    print("Average compression rate for doublecompression is: cr = ", avg_cr,"when using Shorten order ",Order)


if test == 71:
    print("Test 71")
    print("")

    AdjacentMemoryOut = [0]*4
    ShortenMemoryOut = []
    AllRecreatedValues = []
    AllCorrect = 0
    for mic in range(mic_end + 1 - mic_start):
        ShortenMemoryOut.append([0]*4)
        AllRecreatedValues.append([])

    #recrete the orginal input values for each datablock
    for CodeWords in AllCodeWords:
        Decodedvalues, ShortenMemoryOut, AdjacentMemoryOut = DoubleCompression_predictor.Out(CodeWords, ShortenMemoryOut, AdjacentMemoryOut)
        

    

        #Append the decoded values to the correct array depending on mic
        for mic in range(mic_end + 1 - mic_start):
            CurrentDecodedValues = Decodedvalues[mic]
            for value in CurrentDecodedValues:
                AllRecreatedValues[mic].append(value)

    #Check if all values was reacreated correctly by checking if the original values are equal to the reacreated values
    for mic in range(mic_end + 1 - mic_start):
        mic_correct = 0
        zero = []
        OriginalMicValues = OriginalInputs[mic]
        RecreatedMicValues = AllRecreatedValues[mic]
        for i in range(len(RecreatedMicValues)):
            current_zero = OriginalMicValues[i] - RecreatedMicValues[i]

            if current_zero != 0:
                mic_correct += 1

            zero.append(current_zero)

        if mic_correct != 0:
            print("For mic #",mic+mic_start," ",mic_correct,"values was not recreated succesfully")

        AllCorrect += mic_correct

        #Plot the original input, recreated input, and zero (original - recreated)
        if 1 < 0:

            figure_title = "mic #" + str(mic + mic_start)

            fig = plt.figure(figure_title)
            ax = fig.add_subplot(311)
            plt.plot(OriginalMicValues)
            ax.title.set_text("Original input")
            
            ax = fig.add_subplot(312)
            plt.plot(RecreatedMicValues)
            ax.title.set_text("Recreated input")
            
            ax = fig.add_subplot(313)
            plt.plot(zero)
            ax.title.set_text("Original input - recreated input")

            plt.show()

    if AllCorrect == 0:
        print("All values have been recreated succesfully")


if test == 63:
    print("Test 63")
    print("")
    RecreationTime = []
    MemorysOut = []
    
    for mics in range(mic_end + 1 - mic_start):
        MemorysOut.append([0]*4)

    for i in range(len(AllCodeWords)):
        #Recreate the input values
        CodeWords = AllCodeWords[i]
        start_time = time.time()
        CurrentRecreatedValues, MemorysOut =  FlacMod_predictor.Out(CodeWords, MemorysOut)
        stop_time = time.time()
        total_time = stop_time - start_time
        RecreationTime.append(total_time)

    avg_time = sum(RecreationTime) / len(RecreationTime)

    print("Average decompression time is ", avg_time,"seconds")
    

if test == 62:
    print("Test 62")
    print("")
    
    #Calculate compression rate
    cr_array = []

    for itteration in range(len(AllCodeWords)):
        #Grabb CodeWords for all mics for one datablock
        CodeWords = AllCodeWords[itteration]

        for mic in range(len(CodeWords)):
            #Grab one codeword from one mic in current datablock, this coresponds to microphone = mic, datablock =itteration
            CurrentCodeWord = CodeWords[mic]

            #Grab uncoded binary value for all datablocks for one mic
            UncodedWordsMic = OriginalInputsBinary[mic]
            #Grab uncoded binary value for one data block for selected mic, thus corresponds to microphone = mic, datablock = itteartion
            CurrentUncodedWord = UncodedWordsMic[itteration]

            cr = len(CurrentCodeWord) / len(CurrentUncodedWord)

            cr_array.append(cr)

    avg_cr = sum(cr_array) / len(cr_array)

    print("Average compression rate = ", avg_cr)
        

if test == 61:
    print("Test 61")
    print("")
    RecreatedValues = []
    MemorysOut = []
    all_correct = 0
    for mics in range(mic_end + 1 - mic_start):
        MemorysOut.append([0]*4)
        RecreatedValues.append([])

    for i in range(len(AllCodeWords)):
        #Recreate the input values
        CodeWords = AllCodeWords[i]
        CurrentRecreatedValues, MemorysOut =  FlacMod_predictor.Out(CodeWords, MemorysOut)
        
        #Store the recreated input values by sorting after mics
        for mic in range(len(CurrentRecreatedValues)):
            CurrentMicRecreatedValues = CurrentRecreatedValues[mic]
            for CurrentMicValue in CurrentMicRecreatedValues:
                RecreatedValues[mic].append(CurrentMicValue)

    for mic in range(len(RecreatedValues)):
        CurrentReVal = RecreatedValues[mic]
        CurrentOgVal = OriginalInputs[mic]
        #Check if all values have been recreated correctly by taking original value - recreated value
        #This should be equal to zero if everything is done correctly
        zero = []
        all_correct_mic = 0
        for sample in range(len(CurrentReVal)):
            current_zero = CurrentOgVal[sample] - CurrentReVal[sample]
            if current_zero != 0:
                all_correct_mic +=1
            zero.append(current_zero)

        if all_correct_mic != 0:
            print("For mic#",mic," ", all_correct_mic,"values was not decoded correctly")
            
        all_correct += all_correct_mic


        #Plot original values, recreated values, and zero array
        if 1 < 0:
            figure_title = "mic #" + str(mic + mic_start)

            fig = plt.figure(figure_title)
            ax = fig.add_subplot(311)
            plt.plot(CurrentOgVal)
            ax.title.set_text("Original input")
            
            ax = fig.add_subplot(312)
            plt.plot(CurrentReVal)
            ax.title.set_text("Recreated input")
            
            ax = fig.add_subplot(313)
            plt.plot(zero)
            ax.title.set_text("Original input - recreated input")

            plt.show()


            
    if all_correct == 0:
        print("All values was recreated correctly")
            

if test == 53:
    print("Test 53")
    print("")

    print("Shorten k-array = ", k_Shorten,"have lenght ", len(k_Shorten))
    print("LPC k-array = ", k_Lpc,"have lenght ", len(k_Lpc))
    #print("FLAC k-array = ", k_Flac)
    print("Adjacent k-array = ", k_Adjacent,"have lenght ", len(k_Adjacent))

    #Shorten calculations:
    Shorten_cr = []
    len1 = len(CodeWordsShorten)
    #Loops thorugh all mics to get the code_words for the specific mics
    for mic in range(mic_end + 1 - mic_start):
        encodedMic = CodeWordsShorten[mic]
        uncodedMic = UncodedWords[mic]
        len2 = len(encodedMic)
        #loops thorugh all data blocks to get the compression rate of the code word for that data block
        for itteration in range(len(encodedMic)):
            cr = len(encodedMic[itteration]) / len(uncodedMic[itteration])
            Shorten_cr.append(cr)

    print("Average compression rate for Shorten order ",ShortenOrder,"is: cr = ", sum(Shorten_cr) / len(Shorten_cr))
    #print("len shorten: ", len1, "* ", len2,"= ",len1 * len2)#only for a test
    print("")

    #LPC calculations:
    LPC_cr = []
    #Loops thorugh all mics to get the code_words for the specific mics
    for mic in range(mic_end + 1 - mic_start):
        encodedMic = CodeWordsLPC[mic]
        uncodedMic = UncodedWords[mic]
        #loops thorugh all data blocks to get the compression rate of the code word for that data block
        for itteration in range(len(encodedMic)):
            cr = len(encodedMic[itteration]) / len(uncodedMic[itteration])
            LPC_cr.append(cr)

    print("Average compression rate for LPC order ",LpcOrder,"is: cr = ", sum(LPC_cr) / len(LPC_cr))
    
    print("")

    #FLAC calculations:
    FLAC_cr = []
    Choices = ["RLE", "Shorten order 0", "Shorten order 1", "Shorten order 2", "Shorten order 3", "Shorten order 4", "LPC order 1", "LPC order 2", "LPC order 3", "LPC order 4", "LPC order 5", "LPC order 6", "LPC order 7", "LPC order 8", "LPC order 9", "LPC order 10"]
    #Loops thorugh all mics to get the code_words for the specific mics
    for mic in range(mic_end + 1 - mic_start):
        encodedMic = codeWordsFLAC[mic]
        uncodedMic = UncodedWords[mic]
        currentEncoders = Encoding_choice[mic]
        #loops thorugh all data blocks to get the compression rate of the code word for that data block
        for itteration in range(len(encodedMic)):
            currentChoice = int(currentEncoders[itteration],2)
            #print("Current encoding choice is: ", Choices[currentChoice])#Can print out what choice was made to get the current cr
            cr = len(encodedMic[itteration]) / len(uncodedMic[itteration])
            FLAC_cr.append(cr)

    print("Average compression rate for FLAC is: cr = ", sum(FLAC_cr) / len(FLAC_cr))
    print("")

    #Adjacent calculations
    Adjacent_cr = []

    for i in range(len(CodeWordsAdjacent)):
        #Calculate compression rate for current itteration
        cr = len(CodeWordsAdjacent[i]) / len(UncodedWordsAdjacent[i])
        #print("Compression rate for itteration ",i,"is :",cr)#Gives alot of print outs, better to comment out and just look at average
        Adjacent_cr.append(cr)
        
    
    print("Average compression rate for Adjacent is: cr = ", sum(Adjacent_cr)/len(Adjacent_cr))
    print("")


if test == 52:
    print("Test 51")
    print("")

    

    #Shorten calculations:
    Shorten_cr = []
    len1 = len(CodeWordsShorten)
    #Loops thorugh all mics to get the code_words for the specific mics
    for mic in range(mic_end + 1 - mic_start):
        encodedMic = CodeWordsShorten[mic]
        uncodedMic = UncodedWords[mic]
        len2 = len(encodedMic)
        #loops thorugh all data blocks to get the compression rate of the code word for that data block
        for itteration in range(len(encodedMic)):
            cr = len(encodedMic[itteration]) / len(uncodedMic[itteration])
            Shorten_cr.append(cr)

    print("Average compression rate for Shorten order ",ShortenOrder,"is: cr = ", sum(Shorten_cr) / len(Shorten_cr))
    #print("len shorten: ", len1, "* ", len2,"= ",len1 * len2)#only for a test
    print("")

    #LPC calculations:
    LPC_cr = []
    #Loops thorugh all mics to get the code_words for the specific mics
    for mic in range(mic_end + 1 - mic_start):
        encodedMic = CodeWordsLPC[mic]
        uncodedMic = UncodedWords[mic]
        #loops thorugh all data blocks to get the compression rate of the code word for that data block
        for itteration in range(len(encodedMic)):
            cr = len(encodedMic[itteration]) / len(uncodedMic[itteration])
            LPC_cr.append(cr)

    print("Average compression rate for LPC order ",LpcOrder,"is: cr = ", sum(LPC_cr) / len(LPC_cr))
    
    print("")

    #FLAC calculations:
    FLAC_cr = []
    Choices = ["RLE", "Shorten order 0", "Shorten order 1", "Shorten order 2", "Shorten order 3", "Shorten order 4", "LPC order 1", "LPC order 2", "LPC order 3", "LPC order 4", "LPC order 5", "LPC order 6", "LPC order 7", "LPC order 8", "LPC order 9", "LPC order 10"]
    #Loops thorugh all mics to get the code_words for the specific mics
    for mic in range(mic_end + 1 - mic_start):
        encodedMic = codeWordsFLAC[mic]
        uncodedMic = UncodedWords[mic]
        currentEncoders = Encoding_choice[mic]
        #loops thorugh all data blocks to get the compression rate of the code word for that data block
        for itteration in range(len(encodedMic)):
            currentChoice = int(currentEncoders[itteration],2)
            #print("Current encoding choice is: ", Choices[currentChoice])#Can print out what choice was made to get the current cr
            cr = len(encodedMic[itteration]) / len(uncodedMic[itteration])
            FLAC_cr.append(cr)

    print("Average compression rate for FLAC is: cr = ", sum(FLAC_cr) / len(FLAC_cr))
    print("")

    #Adjacent calculations
    Adjacent_cr = []

    for i in range(len(CodeWordsAdjacent)):
        #Calculate compression rate for current itteration
        cr = len(CodeWordsAdjacent[i]) / len(UncodedWordsAdjacent[i])
        #print("Compression rate for itteration ",i,"is :",cr)#Gives alot of print outs, better to comment out and just look at average
        Adjacent_cr.append(cr)
        
    
    print("Average compression rate for Adjacent is: cr = ", sum(Adjacent_cr)/len(Adjacent_cr))
    print("")


if test == 51:
    print("Test 51")
    print("")

    

    #Shorten calculations:
    Shorten_cr = []
    len1 = len(CodeWordsShorten)
    #Loops thorugh all mics to get the code_words for the specific mics
    for mic in range(mic_end + 1 - mic_start):
        encodedMic = CodeWordsShorten[mic]
        uncodedMic = UncodedWords[mic]
        len2 = len(encodedMic)
        #loops thorugh all data blocks to get the compression rate of the code word for that data block
        for itteration in range(len(encodedMic)):
            cr = len(encodedMic[itteration]) / len(uncodedMic[itteration])
            Shorten_cr.append(cr)

    print("Average compression rate for Shorten order ",ShortenOrder,"is: cr = ", sum(Shorten_cr) / len(Shorten_cr))
    #print("len shorten: ", len1, "* ", len2,"= ",len1 * len2)#only for a test
    print("")

    #LPC calculations:
    LPC_cr = []
    #Loops thorugh all mics to get the code_words for the specific mics
    for mic in range(mic_end + 1 - mic_start):
        encodedMic = CodeWordsLPC[mic]
        uncodedMic = UncodedWords[mic]
        #loops thorugh all data blocks to get the compression rate of the code word for that data block
        for itteration in range(len(encodedMic)):
            cr = len(encodedMic[itteration]) / len(uncodedMic[itteration])
            LPC_cr.append(cr)

    print("Average compression rate for LPC order ",LpcOrder,"is: cr = ", sum(LPC_cr) / len(LPC_cr))
    
    print("")

    #FLAC calculations:
    FLAC_cr = []
    Choices = ["RLE", "Shorten order 0", "Shorten order 1", "Shorten order 2", "Shorten order 3", "Shorten order 4", "LPC order 1", "LPC order 2", "LPC order 3", "LPC order 4", "LPC order 5", "LPC order 6", "LPC order 7", "LPC order 8", "LPC order 9", "LPC order 10"]
    #Loops thorugh all mics to get the code_words for the specific mics
    for mic in range(mic_end + 1 - mic_start):
        encodedMic = codeWordsFLAC[mic]
        uncodedMic = UncodedWords[mic]
        currentEncoders = Encoding_choice[mic]
        #loops thorugh all data blocks to get the compression rate of the code word for that data block
        for itteration in range(len(encodedMic)):
            currentChoice = int(currentEncoders[itteration],2)
            #print("Current encoding choice is: ", Choices[currentChoice])#Can print out what choice was made to get the current cr
            cr = len(encodedMic[itteration]) / len(uncodedMic[itteration])
            FLAC_cr.append(cr)

    print("Average compression rate for FLAC is: cr = ", sum(FLAC_cr) / len(FLAC_cr))
    print("")

    #Adjacent calculations
    Adjacent_cr = []

    for i in range(len(CodeWordsAdjacent)):
        #Calculate compression rate for current itteration
        cr = len(CodeWordsAdjacent[i]) / len(UncodedWordsAdjacent[i])
        #print("Compression rate for itteration ",i,"is :",cr)#Gives alot of print outs, better to comment out and just look at average
        Adjacent_cr.append(cr)
        
    
    print("Average compression rate for Adjacent is: cr = ", sum(Adjacent_cr)/len(Adjacent_cr))
    print("")


if test == 49:
    print("Test 49")
    print("")
    

    CrArray = []

    #loop thourgh all codewords and calculate the cr
    for i in range(len(AllCodeWords)):
        #Calculate cr by taking length rice coded residuals and divide it by length of input values represented as 24 bits binary digits
        #each itteration contains the length for all mics of 1 sample
        cr = len(AllCodeWords[i]) / len(AllInputsBinary[i])
        #Save the CR value
        CrArray.append(cr)

    #Calculate average CR
    avg_cr = sum(CrArray) / len(CrArray)

    print("Average compression rate using adjacent with order ", order, "is: cr = ", avg_cr)
    
  
if test == 48:
    print("Test 48")
    print("")
    timeArray = []
    allCorrect = 0
    allCorrectUsed = False
    recreatedValues = []
    if order == 0:
        memoryOut = []
    else:
        memoryOut = [0]*order

    #Loop thorugh all data blocks
    for datablock in range(recomnded_limit):
        #Time how long it takes to recreate the values of all mics and sample from one datablock
        start_time = time.time()
        
        #loop thorugh all samples
        for sample in range(256):
            #Grab data from the current sample
            CodeWordsDataSample = AllCodeWords[sample]
            MvaluesSample = AllMvalues[sample]
            InputSample = AllInputs[sample]

            #Grab data from the current datablock
            CodeWord = CodeWordsDataSample[datablock]
            mValue = MvaluesSample[datablock]
            OgInput = InputSample[datablock]

            Golomb_decoder = GolombCoding(mValue, sign)
            residuals = Golomb_decoder.Decode(CodeWord)

            recreatedValue, memoryOut, predictions = Adjacent_predictor.Out(residuals, memoryOut)

            #Can be used to check if values was recreated correctly, affect timeing so only used to test once to see if it works correctly
            if 1 < 0:
                allCorrectUsed = True
                for i in range(len(recreatedValue)):
                    zero = OgInput[i] - recreatedValue[i]
                    if zero != 0:
                        allCorrect += 1
                        print("Failed to recreate value at datablock=", datablock,", sample=",sample,",mic = ",i)

        stop_time = time.time()
        total_time = stop_time-start_time
        timeArray.append(total_time)

    if allCorrectUsed:
        if allCorrect == 0:
            print("All values recreated succesfully")

    print("")
    #Calculate average time
    avg_time = sum(timeArray) / len(timeArray)

    print("Average time to recreta value using adjacent with order ", order," is ",avg_time,"seconds")
    

if test == 47:
    print("Test 47")
    print("")
    timeArray = []
    allCorrect = 0
    allCorrectUsed = False
    recreatedValues = []
    if order == 0:
        memoryOut = []
    else:
        memoryOut = [0]*order

    #Loop thorugh all data blocks
    for datablock in range(recomnded_limit):
        #Time how long it takes to recreate the values of all mics and sample from one datablock
        start_time = time.time()
        
        #loop thorugh all samples
        for sample in range(256):
            #Grab data from the current sample
            CodeWordsDataSample = AllCodeWords[sample]
            KvaluesSample = AllKvalues[sample]
            InputSample = AllInputs[sample]

            #Grab data from the current datablock
            CodeWord = CodeWordsDataSample[datablock]
            kValue = KvaluesSample[datablock]
            OgInput = InputSample[datablock]

            Rice_decoder = RiceCoding(kValue, sign)
            residuals = Rice_decoder.Decode(CodeWord)

            recreatedValue, memoryOut, predictions = Adjacent_predictor.Out(residuals, memoryOut)

            #Can be used to check if values was recreated correctly, affect timeing so only used to test once to see if it works correctly
            if 1 < 0:
                allCorrectUsed = True
                for i in range(len(recreatedValue)):
                    zero = OgInput[i] - recreatedValue[i]
                    if zero != 0:
                        allCorrect += 1
                        print("Failed to recreate value at datablock=", datablock,", sample=",sample,",mic = ",i)

        stop_time = time.time()
        total_time = stop_time-start_time
        timeArray.append(total_time)

    if allCorrectUsed:
        if allCorrect == 0:
            print("All values recreated succesfully")

    print("")
    #Calculate average time
    avg_time = sum(timeArray) / len(timeArray)

    print("Average time to recreta value using adjacent with order ", order," is ",avg_time,"seconds")
    

if test == 46:
    print("Test 46")
    print("")
    k_array = []
    code_words = []


    for order in range(5):
        #Create array to store code words
        code_words.append([])

        #Calculates the ideal k-value according to Rice theory
        Current_abs_res = abs_res[order]
        abs_res_avg = np.mean(abs_res)
            
        #if abs_res_avg is less than 4.7 it would give a k value less than 1.
        #k needs tobe a int > 1 and therefore if abs_res_avg < 5 k is set to 1
        #OBS. 4.7 < abs_res_avg < 5 would be rounded of to k=1 so setting the limit to 5 works well
        if abs_res_avg > 5:
            k = int(round(math.log(math.log(2,10) * abs_res_avg,2)))
        else:
            k = 1
        #Saves the current ideal k value to later use for decoding
        
        k_array.append(k)

        #All residuals for current order
        OrderResiduals = AllResiduals[order]
        for i in range(len(OrderResiduals)):
            CurRes = OrderResiduals[i]
            code_word = ""
            for j in range(len(CurRes)):
                Rice_coder = RiceCoding(k, sign)
                n = int(CurRes[j])
                kodOrd = Rice_coder.Encode(n)
                code_word += kodOrd
            code_words[order].append(code_word)


    print("k_array = ",k_array)
    memorysOut = [[],[0],[0,0],[0,0,0],[0,0,0,0]]





    
    #Calculate average compression rate for all orders
    cr = []
    avg_cr = []
    #loop thorugh all orders
    for order in range(5):
        #Calculate cr for each code word in that order
        cr.append([])
        current_code_words = code_words[order]
        for i in range((len(current_code_words))):
            current_cr = len(current_code_words[i]) / len(uncoded_words[i])
            cr[order].append(current_cr)

        #Calculate the avg cr for the current order
        avg_cr.append(sum(cr[order]) / len(cr[order]))

    print("")
    print("Average cr = ", avg_cr)


if test == 45:
    print("Test 45")
    print("")
    print("Adjacent with order ", order)
    print("")
    #Create array for compression rate for each m value
    cr = []
    avg_cr = []
    for i in range(len(m_array)):
        cr.append([])

    #Calculate compression rate for each data block and m-value
    for i in range(len(code_words)):
        #Take the code words that belong to a specific m-value
        m_code_words = code_words[i]

        for j in range(len(m_code_words)):
            #calculate the compression rate for the current code word
            current_cr = len(m_code_words[j]) / len(uncoded_words[j])
            #save the cr in the array for the k value
            cr[i].append(current_cr)

        #calculate average compression rate forthe current k value
        current_avg_cr = sum(cr[i]) / len(cr[i])

        avg_cr.append(current_avg_cr)

    #print("m-values: ", m_array)
    print("")
    #print("Average compression rate: ", avg_cr)
    print("")
    print("")
    

    m_best = m_start
    cr_best = avg_cr[0]

    for i in range(1, len(m_array)):
        if avg_cr[i] < cr_best:
            cr_best = avg_cr[i]
            m_best = m_array[i]
    
    print("")
    print("Best m-values = ", m_best,"Gives compression rate, cr = ", cr_best)



    
    
    plt.figure("Test_45_")

    plt.plot(m_array, avg_cr, "o")

        
        
    plt.xlabel("m-value")
    plt.ylabel("Average compression ratio")
    plt.legend()

    plt.show()


if test == 44:
    print("Test 44")
    print("")
    print("Adjacent with order ", order)
    print("")
    #calculate ideal k_value
    #Calculates the ideal k-value according to Rice theory
    abs_res_avg = np.mean(abs_res)
    
    #if abs_res_avg is less than 4.7 it would give a k value less than 1.
    #k needs tobe a int > 1 and therefore if abs_res_avg < 5 k is set to 1
    #OBS. 4.7 < abs_res_avg < 5 would be rounded of to k=1 so setting the limit to 5 works well
    if abs_res_avg > 5:
        k_ideal = int(round(math.log(math.log(2,10) * abs_res_avg,2)))
    else:
        k_ideal = 1
    

    #Create array for compression rate for each k value
    cr = []
    avg_cr = []
    for i in range(len(k_array)):
        cr.append([])

    #Calculate compression rate for each data block and k-value
    for i in range(len(code_words)):
        #Take the code words that belong to a specific k-value
        k_code_words = code_words[i]

        for j in range(len(k_code_words)):
            #calculate the compression rate for the current code word
            current_cr = len(k_code_words[j]) / len(uncoded_words[j])
            #save the cr in the array for the k value
            cr[i].append(current_cr)

        #calculate average compression rate forthe current k value
        current_avg_cr = sum(cr[i]) / len(cr[i])

        avg_cr.append(current_avg_cr)

    print("k-values: ", k_array)
    print("")
    print("Average compression rate: ", avg_cr)
    print("")
    print("")
    

    k_best = k_start
    cr_best = avg_cr[0]

    for i in range(1, len(k_array)):
        if avg_cr[i] < cr_best:
            cr_best = avg_cr[i]
            k_best = i + k_start
    
    print("Ideal k-value = ", k_ideal, "Gives compression rate, cr = ",avg_cr[k_ideal - k_start] )
    print("")
    print("Best k-values = ", k_best,"Gives compression rate, cr = ", cr_best)



    if 1 < 0:#Plots for report only

        #K values for sine: 2 = k 8-16
        Sine_2 = [0.8500504811604804, 0.6653977711995446, 0.5942123413085907, 0.5801274617513004, 0.5951808929443353, 0.6281656901041665, 0.667703755696605, 0.708484268188506, 0.75]
    
        #K values for Drone: 2 = k 12-20
        Drone_2 =[1.0085985819498702, 0.8280771891276049, 0.7590602874755846, 0.7461541493733703, 0.7623184204101547, 0.7942623138427689, 0.8335726420085013, 0.8750035603841146, 0.9166666666666524]

        #K values for static: 2 = k 13-20
        Static_2 = [0.9175244649251315, 0.8035437266031901, 0.7679500579833974, 0.7721909840901684, 0.7975072224934917, 0.8339841206868762, 0.8750086466471352, 0.9166666666666524]

        plt.figure("Test44_fixed_values")

        #Plot sine
        plt.plot(list(range(8,17)), Sine_2, 'yo', label='1k Hz tone')


        #plot drone
        plt.plot(list(range(12,21)), Drone_2, 'bo', label='Drone sound')


        #plot Static oise
        plt.plot(list(range(13,21)), Static_2, 'go', label='Static noise')


         
        #plt.title("Comparison of comression ratio for differente orders")
        plt.yticks(fontsize=20)
        plt.xticks(fontsize=20)
        plt.xlabel("k-value", fontsize=25)
        plt.ylabel("Average compression ratio", fontsize=25)
        plt.legend(fontsize=20)

        plt.show()


    else:
    

        plt.figure("Test_44_")

        plt.plot(k_array, avg_cr, "o")

            
            
        plt.xlabel("k-value")
        plt.ylabel("Average compression ratio")
        plt.legend()

        plt.show()


if test == 43:
    print("Test 43")
    print("")
    #Just some checks on how k differs
    if 1 > 0:
        print("k array length = ", len(k_array))
        print("Max k value = ", np.max(k_array))
        print("Min k value = ", np.min(k_array))
        print("k varriance = ",np.var(k_array))

    compressionRateArray = []
    recreatedInputs = []
    
    memorysOut = [[],[0],[0,0],[0,0,0],[0,0,0,0]]
    memoryOut = memorysOut[order]
    for i in range(len(code_words)):
        #Calculate compression rate for current itteration
        cr = len(code_words[i]) / len(uncoded_words[i])
        #print("Compression rate for itteration ",i,"is :",cr)#Gives alot of print outs, better to comment out and just look at average
        compressionRateArray.append(cr)
        
        #Decode the Rice coded residual
        Rice_decoder = RiceCoding(k_array[i], sign)
        currentResiduals = Rice_decoder.Decode(code_words[i])

        #Recreate the original inputs
        CurrentRecreatedInputs, memoryOut, recreatedPredictions = Adjacant_predictor.Out(currentResiduals, memoryOut)
        recreatedInputs.append(CurrentRecreatedInputs)

    print("Average compression rate is: ", sum(compressionRateArray)/len(compressionRateArray))


    #Store original and recreated inputs from each mic in an array
    #Start by creating the arrays
    mics_og = []#Original inputs
    mics_re = []#Recreated inputs
    mics_zero = []#Original inputs - recreated inputs (Hopefully equals 0)
    for i in range(mic_end+1 - mic_start):
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

    if 1 > 0:#Plots for report only

        plt.figure("Test_43_Original_")
        plt.plot(mics_og[0])

        plt.figure("Test_43_recreated_")
        plt.plot(mics_re[0])

        plt.figure("Test_43_zero_")
        plt.plot(mics_zero[0])

        plt.show()

    elif 1 < 0:#Some silent and blasted mics when looking at all mics

        fig = plt.figure("Mic 19")
            
        ax = fig.add_subplot(311)
        plt.plot(mics_og[19])
        ax.title.set_text("Original input")
        
        ax = fig.add_subplot(312)
        plt.plot(mics_re[19])
        ax.title.set_text("Recreated input")
        
        ax = fig.add_subplot(313)
        plt.plot(mics_zero[19])
        ax.title.set_text("Original input - recreated input")

        plt.show()

        fig = plt.figure("Mic 20")
            
        ax = fig.add_subplot(311)
        plt.plot(mics_og[20])
        ax.title.set_text("Original input")
        
        ax = fig.add_subplot(312)
        plt.plot(mics_re[20])
        ax.title.set_text("Recreated input")
        
        ax = fig.add_subplot(313)
        plt.plot(mics_zero[20])
        ax.title.set_text("Original input - recreated input")

        plt.show()

        fig = plt.figure("Mic 217")
            
        ax = fig.add_subplot(311)
        plt.plot(mics_og[217])
        ax.title.set_text("Original input")
        
        ax = fig.add_subplot(312)
        plt.plot(mics_re[217])
        ax.title.set_text("Recreated input")
        
        ax = fig.add_subplot(313)
        plt.plot(mics_zero[217])
        ax.title.set_text("Original input - recreated input")

        plt.show()

    else:

        #Loop thorugh each microphone and plots the original input, recreated input and zero (origina - recreated)
        for i in range(mic_end + 1 - mic_start):

            fig_title = "Mic #" + str(i+mic_start)
            fig = plt.figure(fig_title)
            
            ax = fig.add_subplot(311)
            plt.plot(mics_og[i])
            ax.title.set_text("Original input")
            
            ax = fig.add_subplot(312)
            plt.plot(mics_re[i])
            ax.title.set_text("Recreated input")
            
            ax = fig.add_subplot(313)
            plt.plot(mics_zero[i])
            ax.title.set_text("Original input - recreated input")

            plt.show()
  

if test == 42:
    print("Test 42")
    print("")
    memoryOut = [0] * order
    RecreatedInputs = []
    
    
    #Create arrays for all mics
    mic_og = []#Original inputs
    mic_re = []#Recreated inputs
    mic_zero = []#Original - recreated (Hopefully =0)
    for i in range(mic_start, mic_end+1):
        mic_og.append([])
        mic_re.append([])
        mic_zero.append([])

    #Recreated the original inputs from residuals
    for i in range(len(AllResiduals)):
        CurrentRecreatedInputs, memoryOut, CurrentPredictions = Adjacant_predictor.Out(AllResiduals[i], memoryOut)
        RecreatedInputs.append(CurrentRecreatedInputs)

    #Sort all sampels from origianl and recreated so that each mic gets its own array
    for i in range(len(AllInputs)):
        CurrentOg = AllInputs[i]
        CurrentRe = RecreatedInputs[i]

        for microphone in range(mic_end+1 - mic_start):
            CurrentMicOg = CurrentOg[microphone]
            CurrentMicRe = CurrentRe[microphone]
            CurrentZero = CurrentMicOg - CurrentMicRe

            mic_og[microphone].append(CurrentMicOg)
            mic_re[microphone].append(CurrentMicRe)
            mic_zero[microphone].append(CurrentZero)



    for i in range(mic_end + 1 - mic_start):

        figTitle = "Mic #" + str(i+mic_start)


        fig = plt.figure(figTitle)
        ax = fig.add_subplot(311)
        plt.plot(mic_og[i])
        ax.title.set_text("Original inputs")

        ax = fig.add_subplot(312)
        plt.plot(mic_re[i])
        ax.title.set_text("Recreated inputs")

        ax = fig.add_subplot(313)
        plt.plot(mic_zero[i])
        ax.title.set_text("zero")
        plt.show()
    

if test == 41:
    print("Test 41")
    print("")
    plot_nr = 1
    #loops thorugh the array with mic data, ploting each mic
    #this is done in subplot so that each figure conatins 4 mic
    for i in range(64):
        fig = plt.figure(plot_nr)
        sub_nr =(i%4 + 1)

        ax = fig.add_subplot(220+sub_nr)
        plt.plot(mic_residuals[i])
        mic_title = "Mic #" + str(i+64)
        ax.title.set_text(mic_title)
        
        if i % 4 == 3:
        
            plot_nr +=1
            plt.show()#Each figure is plotted one at a time, to plot all at the same time move this outsie for-loop


if test == 34:
    print("Test 34")
    print("")
    AllDecodedInputs = []
    MemorysOut = []
    time_array = []
    for mic in range(end_mic + 1 - start_mic):
        AllDecodedInputs.append([])
        if LPC_Order > 4:
            MemorysOut.append([0]*LPC_Order)
        else:
            MemorysOut.append([0]*4)

    AllCorrect = 0
  

    #For each mic values for all data blocks

    #loop thourgh all data blocks
    for datablock in range(recomnded_limit):
    
        #Time how long time it takes to decode every mic in a data block
        start_time = time.time()
        #loop thorugh all mics
        for microphone in range(end_mic + 1 - start_mic):
            
            #Grab data corresponding to each mic
            OriginalMicAllDatablocks = AllOriginalInputs[microphone]
            CodeWordMic = AllCodeWords[microphone]
            KvaluesMic = AllKvalues[microphone]
            EncodingChoicesMic = AllEncodingChoices[microphone]
            CofficentsMic = AllCofficents[microphone]
            
            #rab that datablocks values
            CodeWord = CodeWordMic[datablock]
            OriginalInputs = OriginalMicAllDatablocks[datablock]
            EncodingChoice = EncodingChoicesMic[datablock]
            kValue = KvaluesMic[datablock]
            LpcCofficents = CofficentsMic[datablock]

            #Decode the codeword and get the original inputs, time how long it takes
            
            DecodedInputs, MemorysOut[microphone] = FLAC_prediction.Out(CodeWord, MemorysOut[microphone], kValue, EncodingChoice, LpcCofficents)
        
        

            #Can be used to check if every thing is decoded correctly, this is will affect time and is just done to check that the code works
            if 1 < 0:
                #Check that all values was decoded correctly, 
                #since LPC get it somewhat wrong if the encoding choice is indecating that LPC have been used an error of up to 10 in magnitude will be allowed
                for i in range(len(OriginalInputs)):
                    zero = OriginalInputs[i] - DecodedInputs[i]

                    if int(EncodingChoice, 2) > 5:
                        if zero > 10:
                            AllCorrect +=1
                            print("Failed recreate value at datablock ", datablock, "mic ", microphone)

                    else:
                        if zero != 0:
                            AllCorrect +=1
                            print("Failed recreate value at datablock ", datablock, "mic ", microphone)


                    if AllCorrect == 0:
                        print("All values where recreated succesfully")
                    print("Len total time = ", len(total_time))
                    print("")


        end_time = time.time()
        total_time = end_time - start_time


        #save the total time in the time array to later calculate average time
        time_array.append(total_time)


    #Calculate average time it took to reacreate values
    avg_time = sum(time_array) / len(time_array)
    print("Average time to recreate values using FLAC with max LPC Order ", LPC_Order," is ", avg_time, "seconds")
                        

if test == 33:
    print("Test 33")
    print("")
    print("FLAC with max LPC order ", LPC_Order)
    print("")
    CrArray = []
    #loop through all code words
    for i in range(len(AllCodeWords)):
        #Calculate the cr for the current codeword
        cr = len(AllCodeWords[i]) / len(OriginalInputsBinary[i])
        #Save the current cr
        CrArray.append(cr)

    #Calulcate the average cr
    avg_cr = sum(CrArray) / len(CrArray)
    print("Average compression rate is, cr = ", avg_cr)
    print("")
    for i in range(len(AllEncodingChoices)):
        if i == 0:
            print("RLE used to encode ", AllEncodingChoices[i],"code words")

        elif i < 6:
            print("Shorten Order ",i-1,"used to encode ", AllEncodingChoices[i],"code words")

        else:
            print("LPC Order ",i-5,"is used to encode ", AllEncodingChoices[i],"code words")
        print("")


if test == 32:
    print("Test 32")
    print("")
    decoded_Inputs = []
    if LPC_Order > 4:
        OutMemory = [0]*LPC_Order
    else:
        OutMemory = [0]*4
    OutMemoryArray = []
    OutMemoryArray.append(OutMemory)
    AllCr = []

    

    #Loop through all data blocks
    for i in range(len(Encoding_choice)):

        #Print out what was used to encode each data blcok
        current_encoding_Value = int(Encoding_choice[i],2)
        if current_encoding_Value < 1:
            print("For itteration ", i,"best encoder is RLE")
            plot_title = "RLE"#Later used for plotting
        else:
            print("Error, should allways be RLE")


        #Decompress to get original inputs
        Current_decoded_Inputs, OutMemory = FLAC_prediction.Out(Encoded_inputs[i], OutMemory, k_value[i], Encoding_choice[i], LPC_Cofficents[i])
        OutMemoryArray.append(OutMemory)
        decoded_Inputs.append(Current_decoded_Inputs)

        #To plot later
        plot_zero = []

        #Calculate compression rate for current itteration
        compressed_length = len(Encoded_inputs[i])
        current_test_input = AllTestInputs[i]
        uncoded_inputs = ""
        for j in range(len(current_test_input)):
            uncoded_inputs += np.binary_repr(abs(current_test_input[j]), 32)
            current_zero = current_test_input[j] - Current_decoded_Inputs[j]
            plot_zero.append(current_zero)

        uncompressed_length = len(uncoded_inputs)

        cr = compressed_length / uncompressed_length
        print("Compression rate = ", cr)
        AllCr.append(cr)

    print("Average compression rate = ", sum(AllCr) / len(AllCr))

    
    
    if current_encoding_Value == 0:
        plt.figure("Test_32__Original")
        plt.plot(current_test_input)

        plt.figure("Test_32__decoded")
        plt.plot(Current_decoded_Inputs)

        plt.figure("Test_32__zero")
        plt.plot(plot_zero)

        plt.show()


if test == 31:
    print("Test 31")
    print("")
    decoded_Inputs = []
    if LPC_Order > 4:
        OutMemory = [0]*LPC_Order
    else:
        OutMemory = [0]*4
    OutMemoryArray = []
    OutMemoryArray.append(OutMemory)

    #Limit 1 shows that all residuals bellow it would be correct if rounded to closest integer
    round_lim_up_1 = [0.5]*256
    round_lim_down_1 = [-0.5]*256

    #Limit 2 show that all residuals bellow it would be correct if negative integers are rounded up
    #and positive integers are rounded down
    round_lim_up_2 = [1]*256
    round_lim_down_2 = [-1]*256

    #Loop through all data blocks
    for i in range(len(Encoding_choice)):

        #Print out what was used to encode each data blcok
        current_encoding_Value = int(Encoding_choice[i],2)
        if current_encoding_Value < 1:
            print("For itteration ", i,"best encoder is RLE")
            plot_title = "RLE"#Later used for plotting
        elif current_encoding_Value < 6:
            print("For itteration ", i,"best encoder is Shorten order ", current_encoding_Value - 1)
            plot_title = "Shorten order " + str(current_encoding_Value - 1)#Later used for plotting
        else:
            print("For itteration ", i,"best encoder is LPC ", current_encoding_Value - 5)
            plot_title = "LPC order " + str(current_encoding_Value - 5)#Later used for plotting


        #Decompress to get original inputs
        Current_decoded_Inputs, OutMemory = FLAC_prediction.Out(Encoded_inputs[i], OutMemory, k_value[i], Encoding_choice[i], LPC_Cofficents[i])
        OutMemoryArray.append(OutMemory)
        decoded_Inputs.append(Current_decoded_Inputs)

        #To plot later
        plot_zero = []

        #Calculate compression rate for current itteration
        compressed_length = len(Encoded_inputs[i])
        current_test_input = AllTestInputs[i]
        uncoded_inputs = ""
        for j in range(len(current_test_input)):
            #Fixed to compare to 24 bits
            uncoded_inputs += np.binary_repr(abs(current_test_input[j]), 24)
            current_zero = current_test_input[j] - Current_decoded_Inputs[j]
            plot_zero.append(current_zero)

        uncompressed_length = len(uncoded_inputs)

        cr = compressed_length / uncompressed_length
        print("Compression rate = ", cr)

        
        fig = plt.figure(plot_title)

        ax = fig.add_subplot(311)
        plt.plot(current_test_input)
        ax.title.set_text("Original input values")

        ax = fig.add_subplot(312)
        plt.plot(Current_decoded_Inputs)
        ax.title.set_text("Decoded input values")

        ax = fig.add_subplot(313)
        plt.plot(plot_zero)
        plt.plot(round_lim_up_1, 'r')
        plt.plot(round_lim_down_1, 'r')
        plt.plot(round_lim_up_2, 'g')
        plt.plot(round_lim_down_2, 'g')
        ax.title.set_text("Original input values - decoded input values")

        plt.show()

            





        

    



    AllTestInputs.append(testInput)
    Encoded_inputs.append(Current_Encoded_inputs)
    k_value.append(Current_k_value)
    Encoding_choice.append(Current_Encoding_choice)
    AllMemorys.append(testMemory)
    LPC_Cofficents.append(Current_LPC_Cofficents)


if test == 28:
    print("Test 28")
    print("")
    print("LPC Order ", Order)
    print("")

    time_array = []
    memorysOut = []
    InputsRecreated = []
    for i in range(mic_start, mic_end+1):
        InputsRecreated.append([])
        if Order > 0:
            memorysOut.append([0]*Order)
        else:
            memorysOut.append([])


    for itteration in range(recomnded_limit):
        print(itteration)
        start_time = time.time()
        ItterationCofficent = AllCofficents[itteration]
        for mic in range(mic_end + 1 - mic_start):
            #Grab the current k value and code word for the current itteration and mic
            m_mic = m_array[mic]
            CodeWords_mic = AllCodeWords[mic]
            m = m_mic[itteration]
            CodeWord = CodeWords_mic[itteration]

            #Calculate the orginal residuals by decodeing the golomb codes
            Golomb_decoder = GolombCoding(m, sign)
            CurrentResiduals = Golomb_decoder.Decode(CodeWord)

            #Grab the current cofficents to recreate inputs
            CurrentCoff = ItterationCofficent[mic]

            #Recreate the original inputs from residuals
            InputsRecreated[mic], memorysOut[mic], CurrentPrediction = LPC_predictor.Out(CurrentCoff, CurrentResiduals, memorysOut[mic])
        
        stop_time = time.time()
        total_time = stop_time - start_time
        
        #Save the time it took to recreate the full array
        time_array.append(total_time)


        if 1 < 0: #only needed when plotting
            for mic in range(mic_end + 1 - mic_start):
                CurrentOriginalInputs = OriginalInputs[itteration]
                figure_title = "Mic #" + str(mic + mic_start) + ", Itteration#" + str(itteration) 

                CurrentOriginalInputs_mic = CurrentOriginalInputs[mic]
                CurrentRecreatedInput = InputsRecreated[mic]
                zero_count = 0
                zero = []
                for i in range(len(CurrentOriginalInputs_mic)):
                    current_zero = CurrentOriginalInputs_mic[i] - CurrentRecreatedInput[i]
                    zero.append(current_zero)
                    if current_zero != 0:
                        zero_count += 1
                        
                if zero_count != 0:
                    print("Failed recreating ", zero_count,"inputs for ", figure_title)

                    

                

                    fig = plt.figure(figure_title)
                    
                    ax=fig.add_subplot(311)
                    plt.plot(CurrentOriginalInputs[mic])
                    ax.title.set_text("Original inputs")

                    ax=fig.add_subplot(312)
                    plt.plot(InputsRecreated[mic])
                    ax.title.set_text("Recreated inputs")

                    ax=fig.add_subplot(313)
                    plt.plot(zero)
                    ax.title.set_text("Original inputs - Recreated inputs")

                    plt.show()
                else:

                    print("All inputs recreated succesfully for ", figure_title)
 
    print("Average time to recreate original input is ", sum(time_array) / len(time_array)," seconds")


if test == 27:
    print("Test 27")
    print("")
    print("LPC Order ", Order)
    print("")

    time_array = []
    memorysOut = []
    InputsRecreated = []
    for i in range(mic_start, mic_end+1):
        InputsRecreated.append([])
        if Order > 0:
            memorysOut.append([0]*Order)
        else:
            memorysOut.append([])


    for itteration in range(recomnded_limit):
        start_time = time.time()
        ItterationCofficent = AllCofficents[itteration]
        for mic in range(mic_end + 1 - mic_start):
            #Grab the current k value and code word for the current itteration and mic
            k_mic = k_array[mic]
            CodeWords_mic = AllCodeWords[mic]
            k = k_mic[itteration]
            CodeWord = CodeWords_mic[itteration]
            
            #Grab the current cofficents to recreate inputs
            CurrentCoff = ItterationCofficent[mic]

            #Calculate the orginal residuals by decodeing the rice codes
            Rice_decoder = RiceCoding(k, sign)
            CurrentResiduals = Rice_decoder.Decode(CodeWord)

            #Recreate the original inputs from residuals
            InputsRecreated[mic], memorysOut[mic], CurrentPrediction = LPC_predictor.Out(CurrentCoff, CurrentResiduals, memorysOut[mic])
        
        stop_time = time.time()
        total_time = stop_time - start_time
        
        #Save the time it took to recreate the full array
        time_array.append(total_time)


        if 1 < 0: #only needed when plotting
            for mic in range(mic_end + 1 - mic_start):
                CurrentOriginalInputs = OriginalInputs[itteration]
                figure_title = "Mic #" + str(mic + mic_start) + ", Itteration#" + str(itteration) 

                CurrentOriginalInputs_mic = CurrentOriginalInputs[mic]
                CurrentRecreatedInput = InputsRecreated[mic]
                zero_count = 0
                zero = []
                for i in range(len(CurrentOriginalInputs_mic)):
                    current_zero = CurrentOriginalInputs_mic[i] - CurrentRecreatedInput[i]
                    zero.append(current_zero)
                    if current_zero != 0:
                        zero_count += 1
                        
                if zero_count != 0:
                    print("Failed recreating ", zero_count,"inputs for ", figure_title)

                    

                

                    fig = plt.figure(figure_title)
                    
                    ax=fig.add_subplot(311)
                    plt.plot(CurrentOriginalInputs[mic])
                    ax.title.set_text("Original inputs")

                    ax=fig.add_subplot(312)
                    plt.plot(InputsRecreated[mic])
                    ax.title.set_text("Recreated inputs")

                    ax=fig.add_subplot(313)
                    plt.plot(zero)
                    ax.title.set_text("Original inputs - Recreated inputs")

                    plt.show()
                else:

                    print("All inputs recreated succesfully for ", figure_title)
 
    print("Average time to recreate original input is ", sum(time_array) / len(time_array)," seconds")


if test == 26:
    print("Test 26")
    print("")
    if 1 < 0:#Some info about k values
        for i in range(len(k_array)):
            currentKs = k_array[i]
            print("Current max k = ", np.max(currentKs))
            print("Current min k = ", np.min(currentKs))
            print("Current k varriance = ", np.var(currentKs))


        print("all_k max = ", np.max(all_k))
        print("all_k mix = ", np.min(all_k))
        print("all_k varraince = ", np.var(all_k))

    all_cr = []
    #Loops thorugh all mics to get the code_words for the specific mics
    for mic in range(mic_end + 1 - mic_start):
        encodedMic = AllCodeWords[mic]
        uncodedMic = UncodedWords[mic]
        #loops thorugh all data blocks to get the compression rate of the code word for that data block
        for itteration in range(len(encodedMic)):
            cr = len(encodedMic[itteration]) / len(uncodedMic[itteration])
            all_cr.append(cr)

    print("Average compression rate for LPC order ",Order,"is: cr = ", sum(all_cr) / len(all_cr))


if test == 25:
    print("Test 25")
    print("")

    #Arrays for average compression rates
    # cr[order][k-value] = compression rate for given order and m-value
    cr = []
    for i in range(len(orders)):
        cr.append([])

    for i in range(len(m_array)):
        for j in range(len(order_array)):
            cr[j].append([])




    


    #loop thorugh all m-values
    for i in range(len(m_array)):
        #loops thorugh all orders of LPC
        for q in range(len(orders)):
            temp_cr_array = []

            #The code words for a given order of LPC, q, and a given m-value, i.
            temp_code_word_array = order_array[q][i]




            #loops thorugh all sampled blocks of data
            for j in range(len(uncoded_words)):
                #Calculates the cr rate for each data block 
                #by comparing rice coded length with 32 bit representation
                temp_cr = len(temp_code_word_array[j]) / len(uncoded_words[j])
                
                #Saves the cr for current code word in array
                temp_cr_array.append(temp_cr)

            #Calculates avg cr for all data blocks given a LPC order, q, and k-value, i.
            avg_temp_cr = np.sum(temp_cr_array) / len(temp_cr_array)

            #Saves avg cr in array
            cr[q][i] = avg_temp_cr

                

                    
                        

            
    if 1 < 0:#this gives alot of outputs in text since alot of m-values are looked at
    #if statement can be changed if print out is desired
        print("For a given value: m = ", m_array)
        for i in range(len(orders)):
            print("Average compression rate for order ",orders[i]," = ", cr[i])
            print("")


        print("")


    


    
    #find the m-value that gives the best compression rate for each order of LPC
    m_best = []
    cr_best = []
    for q in range(len(orders)):
        temp_best_cr = cr[q][5]
        temp_best_m = m_array[5]
        for i in range(5,len(m_array)-1):
            if cr[q][i+1] < temp_best_cr:
                temp_best_cr = cr[q][i+1]
                temp_best_m = m_array[i+1]

        m_best.append(temp_best_m)
        cr_best.append(temp_best_cr)
    
    for i in range(len(orders)):
        print("LPC order ",orders[i],"have best cr at m = ",m_best[i],"with cr = ",cr_best[i])
        print("")


    #plotting compression rate over m-values for differente orders
        
    if 1 > 0:#only for plots in report

        colors = ['k', 'c', 'm', 'y', 'r', 'b', 'g', 'purple']
        #Plots Order 1, 2, and 3 of shorten in the same plot for some k-values
        for i in range(len(orders)):
            label_order = "Order " + str(orders[i])
            plt.plot(m_array, cr[i], "o", color = colors[i], label=label_order)

            
        
        plt.xlabel("m-value")
        plt.ylabel("Compression ratio")
        plt.legend()

        plt.show()

        

    else:
        
        
        #Plots sub plots with each subplot being a specific order of LPC
        #y-axis is compression ratio and x-axis is m value
        plot_nr = 1

        for i in range(len(orders)):
            fig = plt.figure(plot_nr)
            sub_nr = i%4 + 1
            order_text = "LPC Order " + str(orders[i])

            ax = fig.add_subplot(220+sub_nr)
            plt.plot(m_array, cr[i], 'ro')
            ax.title.set_text(order_text)
            plt.xlabel("m-value")
            plt.ylabel("Cmpression ratio")


            if i % 4 == 3:
                plot_nr +=1
                plt.show()

        if len(orders)%4 != 0:
            plt.show()


        


        
        
        colors = ['yo', 'ro', 'bo', 'go']
        #Plots some orders of LPC in the same plot for some m-values
        for i in range(len(orders)):
            label_order = "Order " + str(orders[i])
            plt.plot(m_array, cr[i], colors[i%4], label=label_order)

            if i % 4 == 3:
                plt.title("Comparison of comression ratio for differente orders")
                plt.xlabel("m-value")
                plt.ylabel("Compression ratio")
                plt.legend()

                plt.show()

        if len(orders)%4 != 0:
            plt.title("Comparison of comression ratio for differente orders")
            plt.xlabel("m-value")
            plt.ylabel("Compression ratio")
            plt.legend()

            plt.show()


#Test compression rate for different k-values and orders
#using LPC and Rice codes                       
if test == 24:
    print("Test 24")
    
    
    print("")

    #Arrays for average compression rates
    # cr[order][k-value] = compression rate for given order and k-value
    cr = []
    for i in range(len(orders)):
        cr.append([])

    for i in range(len(k_array)):
        for j in range(len(order_array)):
            cr[j].append([])


    #loop thorugh all k-values
    for i in range(len(k_array)):
        #loops thorugh all orders of LPC
        for q in range(len(orders)):
            temp_cr_array = []

            #The code words for a given order of LPC, q, and a given k-value, i.
            temp_code_word_array = order_array[q][i]




            #loops thorugh all sampled blocks of data
            for j in range(len(uncoded_words)):
                #Calculates the cr rate for each data block 
                #by comparing rice coded length with 32 bit representation
                temp_cr = len(temp_code_word_array[j]) / len(uncoded_words[j])
                
                #Saves the cr for current code word in array
                temp_cr_array.append(temp_cr)

            #Calculates avg cr for all data blocks given a LPC order, q, and k-value, i.
            avg_temp_cr = np.sum(temp_cr_array) / len(temp_cr_array)

            #Saves avg cr in array
            cr[q][i] = avg_temp_cr

                

                    
                        

               
                        
    print("For a given value: k = ", k_array)
    for i in range(len(orders)):
        print("Average compression rate for order ",orders[i]," = ", cr[i])


    print("")

    #Calculate the recomdnded k-value for each order based on Rice codeing theory
    k_ideal_avg_array = []

    for i in range(len(orders)):
        #calculate average for recomended k-value for each order and save in array
        k_ideal_avg = sum(k_ideal_array[i])/len(k_ideal_array[i])
        k_ideal_avg_array.append(k_ideal_avg)

    #prints ideal k-values for each order
    #prints cr with ideal k-value (roundest to closest int) for each order

    print("ideal k-value (LPC order ",order_start,"-",order_stop,")= ", k_ideal_avg_array)

    for i in range(len(orders)):

        print("LPC order ",orders[i], "with k = ", int(round(k_ideal_avg_array[i]))," gives cr = ",cr[i][int(round(k_ideal_avg_array[i])) - k_array[0]])

   

    print("")

    k_best = []
    cr_best = []
    for q in range(len(orders)):
        temp_best_cr = cr[q][0]
        temp_best_k = k_array[0]
        for i in range(len(k_array)-1):
            if cr[q][i+1] < temp_best_cr:
                temp_best_cr = cr[q][i+1]
                temp_best_k = k_array[i+1]

        k_best.append(temp_best_k)
        cr_best.append(temp_best_cr)
    
    for i in range(len(orders)):
        print("LPC order ",orders[i],"have best cr at k = ",k_best[i],"with cr = ",cr_best[i])


    if 1 > 0:#only for plots in report
        

    
        #Values from testing sine sound, k= 8-16 for order 1, k=7-16 order 2, k = 7-16 for order 3, k = 7-16 order 4, k = 7-16 for order 5
        Sine_order1 = [0.7995198567708334, 0.6397867838541667, 0.58076171875, 0.5725748697916667, 0.5897460937500001, 0.6253417968749999, 0.666796875, 0.7083658854166668, 0.75]

        Sine_order2 = [0.9288818359375, 0.6835774739583332, 0.5820475260416667, 0.5524739583333333, 0.5596923828125, 0.586181640625, 0.6255452473958333, 0.6668701171874999, 0.7083740234375001, 0.75]

        Sine_order3 = [0.8458658854166666, 0.6416259765625, 0.5608479817708333, 0.5417968750000001, 0.5546793619791667, 0.5852213541666667, 0.6255777994791667, 0.6668375651041667, 0.7083740234375001, 0.75]
        Sine_order4 = [0.7119547526041666, 0.5751871744791667, 0.5279947916666667, 0.5262125651041667, 0.5483317057291667, 0.5848063151041667, 0.6255777994791666, 0.666845703125, 0.7083740234375001, 0.75]
        Sine_order5 = [0.7107747395833334, 0.5746744791666667, 0.5276936848958333, 0.5258382161458333, 0.5481526692708334, 0.584814453125, 0.6255289713541667, 0.6668294270833333, 0.7083740234375001, 0.75]

        #Values from testing silent (mic 20), k = 1-8 for all
        Silent_order1 =  [0.125, 0.16666666666666663, 0.20833333333333334, 0.25, 0.29166666666666674, 0.33333333333333326, 0.375, 0.4166666666666667]
        Silent_order2 = [0.125, 0.16666666666666663, 0.20833333333333334, 0.25, 0.29166666666666674, 0.33333333333333326, 0.375, 0.4166666666666667]
        Silent_order3 =  [0.125, 0.16666666666666663, 0.20833333333333334, 0.25, 0.29166666666666674, 0.33333333333333326, 0.375, 0.4166666666666667]
        Silent_order4 = [0.125, 0.16666666666666663, 0.20833333333333334, 0.25, 0.29166666666666674, 0.33333333333333326, 0.375, 0.4166666666666667]
        Silent_order5 = [0.125, 0.16666666666666663, 0.20833333333333334, 0.25, 0.29166666666666674, 0.33333333333333326, 0.375, 0.4166666666666667]

        #Values from testing Drone, k = 12-20 for all
        Drone_order1 =  [1.1723307291666667, 0.9091634114583333, 0.7989420572916666, 0.764892578125, 0.7698974609374999, 0.7954264322916667, 0.8334147135416667, 0.875, 0.9166666666666667]

        Drone_order2 = [1.0881510416666664, 0.8672119140625, 0.7778727213541666, 0.7544514973958333, 0.7651448567708333, 0.7940022786458335, 0.8333984375000002, 0.875, 0.9166666666666667]

        Drone_order3 = [1.0695393880208333, 0.8576416015625, 0.7733072916666667, 0.752490234375, 0.7640380859375, 0.7938802083333334, 0.8333984375000002, 0.875, 0.9166666666666667] 
        Drone_order4 = [1.06240234375, 0.8544026692708332, 0.7717692057291667, 0.7512125651041666, 0.7636881510416667, 0.7936686197916667, 0.8333902994791668, 0.875, 0.9166666666666667]

        Drone_order5 = [0.99404296875, 0.8203938802083334, 0.7546630859375, 0.7431396484375, 0.7598225911458334, 0.7926920572916666, 0.8333577473958333, 0.875, 0.9166666666666667]

        #Values from testing static noise, k = 13-20 for all
        Static_order1 = [1.038134765625, 0.8631022135416666, 0.7969401041666667, 0.7851318359375, 0.8017008463541666, 0.8340087890625, 0.875, 0.9166666666666667]

        Static_order2 = [0.9714192708333332, 0.8300211588541668, 0.7802571614583333, 0.7771728515625, 0.7982666015625, 0.8336344401041667, 0.875, 0.9166666666666667]

        Static_order3 = [0.9663818359375, 0.8274332682291666, 0.7792073567708333, 0.7765055338541667, 0.798046875, 0.8336669921875, 0.875, 0.9166666666666667]

        Static_order4 = [0.9208984375, 0.8046549479166665, 0.7679361979166667, 0.7709879557291667, 0.7954833984375, 0.8334147135416667, 0.875, 0.9166666666666667]

        Static_order5 = [0.8694905598958332, 0.7792236328125, 0.7555094401041667, 0.7656331380208332, 0.7939127604166666, 0.8333902994791668, 0.875, 0.9166666666666667]

        plt.figure("Test24_fixed_values")

        #Plot sine
        plt.plot(list(range(8,17)), Sine_order1, 'yv', label='1k Hz tone, Order 1')
        plt.plot(list(range(7,17)), Sine_order2, 'ys', label='1k Hz tone, Order 2')
        plt.plot(list(range(7,17)), Sine_order3, 'y*', label='1k Hz tone, Order 3')
        plt.plot(list(range(7,17)), Sine_order4, 'yo', label='1k Hz tone, Order 4')
        plt.plot(list(range(7,17)), Sine_order5, 'y^', label='1k Hz tone, Order 5')
    
        #plot silent
        plt.plot(list(range(1,9)), Silent_order1, 'ro', label='Silent mic, Order 1')
        plt.plot(list(range(1,9)), Silent_order2, 'rv', label='Silent mic, Order 2')
        plt.plot(list(range(1,9)), Silent_order3, 'rs', label='Silent mic, Order 3')
        plt.plot(list(range(1,9)), Silent_order4, 'r*', label='Silent mic, Order 4')
        plt.plot(list(range(1,9)), Silent_order5, 'r^', label='Silent mic, Order 5')

        #plot drone
        plt.plot(list(range(12,21)), Drone_order1, 'bo', label='Drone sound, Order 1')
        plt.plot(list(range(12,21)), Drone_order2, 'bv', label='Drone sound, Order 2')
        plt.plot(list(range(12,21)), Drone_order3, 'bs', label='Drone sound, Order 3')
        plt.plot(list(range(12,21)), Drone_order4, 'b*', label='Drone sound, Order 4')
        plt.plot(list(range(12,21)), Drone_order5, 'b^', label='Drone sound, Order 5')

        #plot Static oise
        plt.plot(list(range(13,21)), Static_order1, 'go', label='Static noise, Order 1')
        plt.plot(list(range(13,21)), Static_order2, 'gv', label='Static noise, Order 2')
        plt.plot(list(range(13,21)), Static_order3, 'gs', label='Static noise, Order 3')
        plt.plot(list(range(13,21)), Static_order4, 'g*', label='Static noise, Order 4')
        plt.plot(list(range(13,21)), Static_order5, 'g^', label='Static noise, Order 5')

        #plt.plot(k_array, cr_2, 'bo', label='Order 2')
        #plt.plot(k_array, cr_3, 'go', label='Order 3')
        #plt.title("Comparison of comression ratio for differente orders")
        plt.yticks(fontsize=20)
        plt.xticks(fontsize=20)
        plt.xlabel("k-value", fontsize=25)
        plt.ylabel("Average compression ratio", fontsize=25)
        plt.legend(fontsize=15)

        plt.show()

    
    elif 1 < 0:#only for plots in report

        colors = ['k', 'c', 'm', 'y', 'r', 'b', 'g', 'purple']
        #Plots Order 1, 2, and 3 of shorten in the same plot for some k-values
        for i in range(len(orders)):
            label_order = "Order " + str(orders[i])
            plt.plot(k_array, cr[i], "o", color = colors[i], label=label_order)

            
        
        plt.xlabel("k-value")
        plt.ylabel("Average compression ratio")
        plt.legend()

        plt.show()

        

    else:
        
        
        #Plots sub plots with each subplot being a specific order of LPC
        #y-axis is compression ratio and x-axis is k value
        plot_nr = 1

        for i in range(len(orders)):
            fig = plt.figure(plot_nr)
            sub_nr = i%4 + 1
            order_text = "LPC Order " + str(orders[i])

            ax = fig.add_subplot(220+sub_nr)
            plt.plot(k_array, cr[i], 'ro')
            ax.title.set_text(order_text)
            plt.xlabel("k-value")
            plt.ylabel("Average compression ratio")


            if i % 4 == 3:
                plot_nr +=1
                plt.show()

        if len(orders)%4 != 0:
            plt.show()


        


        
        
        colors = ['yo', 'ro', 'bo', 'go']
        #Plots Order 1, 2, and 3 of shorten in the same plot for some k-values
        for i in range(len(orders)):
            label_order = "Order " + str(orders[i])
            plt.plot(k_array, cr[i], colors[i%4], label=label_order)

            if i % 4 == 3:
                plt.title("Comparison of comression ratio for differente orders")
                plt.xlabel("k-value")
                plt.ylabel("Average compression ratio")
                plt.legend()

                plt.show()

        if len(orders)%4 != 0:
            plt.title("Comparison of comression ratio for differente orders")
            plt.xlabel("k-value")
            plt.ylabel("Average compression ratio")
            plt.legend()

            plt.show()
        
               
#Plots the results for using LPC of different orders
if test == 23:
    print("Test 23")
    print("")

    #These are to plot rounding error limits in the zero_plot
    #LPC gives some error due to having to round the residuals beffore encoding them
    
    #Limit 1 shows that all residuals bellow it would be correct if rounded to closest integer
    round_lim_up_1 = [0.5]*len(plot_zero[0])
    round_lim_down_1 = [-0.5]*len(plot_zero[0])

    #Limit 2 show that all residuals bellow it would be correct if negative integers are rounded up
    #and positive integers are rounded down
    round_lim_up_2 = [1]*len(plot_zero[0])
    round_lim_down_2 = [-1]*len(plot_zero[0])



    if 1 < 0:#Only for plots in report
        num_plot = 7#the number decides what order to plot, the plotted order is num_plot+1
        plots_report = [plot_sig, plot_predict[num_plot], plot_residuals[num_plot], plot_zero[num_plot]]
        plots_label = ["Test23_input_order_","Test23_predict_order_","Test23_res_order_","Test23_zero_order_"]
        for i in range(4):

            figure_title = plots_label[i] + str(num_plot + 1)

            plt.figure(figure_title)
            

            plt.plot(plots_report[i])

            if i == 3:
                plt.plot(round_lim_up_1, 'r')
                plt.plot(round_lim_down_1, 'r')

                plt.plot(round_lim_up_2, 'g')
                plt.plot(round_lim_down_2, 'g')


        plt.show()
            

    else:
        for i in range(len(orders)):
            figure_title = "LPC order " + str(i+1)
            fig = plt.figure(figure_title)

            #Each figure plots 4 subplots with:
            #Input signal, prediction of LPC, Residual of LPC Zero (Input - (residual + prediciton) = 0)
            ax = fig.add_subplot(221)
            plt.plot(plot_sig)
            ax.title.set_text("Input signal")

            ax = fig.add_subplot(222)
            plt.plot(plot_predict[i])
            ax.title.set_text("Predicted signal")

            ax = fig.add_subplot(223)
            plt.plot(plot_residuals[i])
            ax.title.set_text("Residual signal")

            ax = fig.add_subplot(224)
            plt.plot(plot_zero[i])
            plt.plot(round_lim_up_1, 'r')
            plt.plot(round_lim_down_1, 'r')
            plt.plot(round_lim_up_2, 'g')
            plt.plot(round_lim_down_2, 'g')

            ax.title.set_text("Input - (Predict + Residual) = 0")


            plt.show()
    

#Test if LPC can recreate input using Golomb coding
#Indicates if any words was wrongly decoded and if so how many of the sampled datablock
#Plots Original input and decoded input
#Gives compression rate of encoded values
if test == 22:
    print("Test 22")
    print("")
    compression_ratio = []
    uncoded_residuals_array = []
    uncoded_values_array = []
    predictions_array = []
    memory_out = [0] * order

    #Limit 1 shows that all residuals bellow it would be correct if rounded to closest integer
    round_lim_up_1 = [0.5]*256
    round_lim_down_1 = [-0.5]*256

    #Limit 2 show that all residuals bellow it would be correct if negative integers are rounded up
    #and positive integers are rounded down
    round_lim_up_2 = [1]*256
    round_lim_down_2 = [-1]*256


    

    #Calcuates compression ratios of LPC by comparing length of binary values of input to length of Rice coded residuals
    for i in range(len(code_words)):
        temp_comp_r = len(code_words[i]) / len(uncoded_words[i])
        compression_ratio.append(temp_comp_r)
    print("Compression ratio of LPC using Golomb code is: ", compression_ratio)

    #Recreates the original inputs
    for i in range(len(inputs)):
        #Grabs the original input values, k-value used to encode, and code_word from arrays
        input = inputs[i]
        m = m_array[i]
        code_word = code_words[i]
        coef = cof_array[i]
        plot_zero = []
        
        #Decodes the residuals from the Rice code
        Golomb_coder = GolombCoding(m, sign)
        uncoded_residuals = Golomb_coder.Decode(code_word)
        uncoded_residuals_array.append(uncoded_residuals)
        
        #Calculates the original inputs from the decoded residuals using Shorten
        uncoded_values, memory_out, predictions = LPC_predictor.Out(coef, uncoded_residuals, memory_out)
        uncoded_values_array.append(uncoded_values)
        predictions_array.append(predictions)

        #Checks if the uncoded values match the original inputs
        value_check = 0
        for j in range(len(uncoded_values)):
            #If the orignal input dont match the uncoded values (rounded to neartest int) value check will increment by 1 
            #and the data block containing the faulty decoded value can be printed out
            if round(uncoded_values[j]) != input[j]:
                #print("Failed decode at data block i = ",i," Original input =  ",input[j]," Uncoded value = ", uncoded_values[j])
                value_check += 1
            plot_zero.append(input[j] - uncoded_values[j])
        #Once all the values have been checked:
        #If there are no wrongly decoded values the code will print out that all values have been correctly decoded for the data block
        if value_check == 0:
            print("Itteration nr",i," correctly decoded all orignal values")
        #If there is some wrongly decoded values the code will print in which data block they are and how many there are
        else:
            print("Itteration nr",i," failed decodeing ",value_check," values")



        if 1 > 0:
            fig_title = "Test22_order_" + str(order)
            plt.figure(fig_title)
            plt.plot(input, 'b', label='Original values')
            plt.plot(uncoded_values, 'r-.', label='Decoded values')
            
            plt.legend(fontsize=25)
            plt.yticks(fontsize=20)
            plt.xticks(fontsize=20)
            plt.show()

            new_fig_title = fig_title + "_zero"
            plt.figure(new_fig_title)
            plt.plot(plot_zero, 'g')
            #plt.legend(fontsize=25)
            plt.yticks(fontsize=20)
            plt.xticks(fontsize=20)
            plt.show()

             #plt.plot(k_array, cr_2, 'bo', label='Order 2')
        #plt.plot(k_array, cr_3, 'go', label='Order 3')
        #plt.title("Comparison of comression ratio for differente orders")
        #plt.yticks(fontsize=20)
        #plt.xticks(fontsize=20)
        #plt.xlabel("k-value", fontsize=25)
        #plt.ylabel("Average compression ratio", fontsize=25)
        #
        #plt.legend(fontsize=20)


        elif 1 > 0:#Only plots for report


            plt.figure("Original values")

            plt.plot(input)

            plt.figure("Uncoded values")

            plt.plot(uncoded_values)

            plt.figure("Test_21_zero")

            plt.plot(plot_zero)

            plt.plot(round_lim_up_1, 'r')
            plt.plot(round_lim_down_1, 'r')
            plt.plot(round_lim_up_2, 'g')
            plt.plot(round_lim_down_2, 'g')



            plt.show()


        else:#Plots the original input values and the decoded input valus in subplots
            fig = plt.figure(i)

            ax = fig.add_subplot(311)
            plt.plot(input)
            ax.title.set_text("Original input values")

            ax = fig.add_subplot(312)
            plt.plot(uncoded_values)
            ax.title.set_text("Decoded input values")

            ax = fig.add_subplot(313)
            plt.plot(plot_zero)
            plt.plot(round_lim_up_1, 'r')
            plt.plot(round_lim_down_1, 'r')
            plt.plot(round_lim_up_2, 'g')
            plt.plot(round_lim_down_2, 'g')
            ax.title.set_text("Original input values - decoded input values")

            plt.show()


#Test if LPC using Rice codes can correctly decode the original inputs
#Prints the cr for each data block
#Prints how many misses of decoded values there are in each data block (uncoded rounded to int)
#Can print where the misses are aswell
#Plots original input and recreated input for each data block
if test == 21:
    print("Test 21")
    print("")
    compression_ratio = []
    uncoded_residuals_array = []
    uncoded_values_array = []
    predictions_array = []
    memory_out = [0] * order

    #Limit 1 shows that all residuals bellow it would be correct if rounded to closest integer
    round_lim_up_1 = [0.5]*256
    round_lim_down_1 = [-0.5]*256

    #Limit 2 show that all residuals bellow it would be correct if negative integers are rounded up
    #and positive integers are rounded down
    round_lim_up_2 = [1]*256
    round_lim_down_2 = [-1]*256

    

    #Calcuates compression ratios of LPC by comparing length of binary values of input to length of Rice coded residuals
    for i in range(len(code_words)):
        temp_comp_r = len(code_words[i]) / len(uncoded_words[i])
        compression_ratio.append(temp_comp_r)
    print("Compression ratio of LPC is: ", compression_ratio)


    #Recreates the original inputs
    for i in range(len(inputs)):
        #Grabs the original input values, k-value used to encode, and code_word from arrays
        input = inputs[i]
        k = k_array[i]
        code_word = code_words[i]
        coef = cof_array[i]
        
        #Decodes the residuals from the Rice code
        Rice_coder = RiceCoding(k, sign)
        uncoded_residuals = Rice_coder.Decode(code_word)
        uncoded_residuals_array.append(uncoded_residuals)
        
        #Calculates the original inputs from the decoded residuals using LPC
        uncoded_values, memory_out, predictions = LPC_predictor.Out(coef, uncoded_residuals, memory_out)
        uncoded_values_array.append(uncoded_values)
        predictions_array.append(predictions)

        #Checks if the uncoded values match the original inputs
        value_check = 0
        plot_zero = []
        for j in range(len(uncoded_values)):
            #If the orignal input dont match the uncoded values value check will increment by 1 
            #and the data block containing the faulty decoded value will be printed out

            if uncoded_values[j] < 0:
                rounded_value = math.ceil(uncoded_values[j])
            else:
                rounded_value = math.floor(uncoded_values[j])

            plot_zero.append(input[j] - uncoded_values[j])

            if rounded_value != input[j]:
                if 1 < 0:#Alot of print outs from this, can be toggled out to see where the errors are
                    print("Failed decode at data block i = ",i)
                    print(" Original input =  ",input[j])
                    print(" Uncoded value = ", uncoded_values[j])
                    print("Rounrded to = ", rounded_value)
                value_check += 1
        #Once all the values have been checked:
        #If there are no wrongly decoded values the code will print out that all values have been correctly decoded for the data block
        if value_check == 0:
            print("Itteration nr",i," correctly decoded all orignal values")
        #If there is some wrongly decoded values the code will print in which data block they are and how many there are
        else:
            print("Itteration nr",i," failed decodeing ",value_check," values")

        
        if 1 < 0:#only for report
            fig_title = "Test21_order_" + str(order)
            plt.figure(fig_title)
            plt.plot(input, 'b', label='Original values')
            plt.plot(uncoded_values, 'r-.', label='Decoded values')
            
            plt.legend(fontsize=25)
            plt.yticks(fontsize=20)
            plt.xticks(fontsize=20)
            plt.show()

            new_fig_title = fig_title + "_zero"
            plt.figure(new_fig_title)
            plt.plot(plot_zero, 'g')
            #plt.legend(fontsize=25)
            plt.yticks(fontsize=20)
            plt.xticks(fontsize=20)
            plt.show()

             #plt.plot(k_array, cr_2, 'bo', label='Order 2')
        #plt.plot(k_array, cr_3, 'go', label='Order 3')
        #plt.title("Comparison of comression ratio for differente orders")
        #plt.yticks(fontsize=20)
        #plt.xticks(fontsize=20)
        #plt.xlabel("k-value", fontsize=25)
        #plt.ylabel("Average compression ratio", fontsize=25)
        #
        #plt.legend(fontsize=20)



        elif 1 < 0:#Only plots for report

            if i == 1:#Only want to display one plot

                plt.figure("Test21_Original_values")

                plt.plot(input)

                plt.figure("Test21_Uncoded_values")

                plt.plot(uncoded_values)


                plt.figure("Test_21_zero")

                plt.plot(plot_zero)

                plt.plot(round_lim_up_1, 'r')
                plt.plot(round_lim_down_1, 'r')
                plt.plot(round_lim_up_2, 'g')
                plt.plot(round_lim_down_2, 'g')

                plt.show()


        else:
            #Plots the original input values and the decoded input valus in subplots
            fig = plt.figure(i)

            ax = fig.add_subplot(311)
            plt.plot(input)
            ax.title.set_text("Original input values")

            ax = fig.add_subplot(312)
            plt.plot(uncoded_values)
            ax.title.set_text("Decoded input values")

            ax = fig.add_subplot(313)
            plt.plot(plot_zero)
            plt.plot(round_lim_up_1, 'r')
            plt.plot(round_lim_down_1, 'r')
            plt.plot(round_lim_up_2, 'g')
            plt.plot(round_lim_down_2, 'g')
            ax.title.set_text("Original input values - decoded input values")

            plt.show()


if test == 18:
    print("Test 18")
    print("")
    print("Shorten Order ", Order)
    print("")

    time_array = []
    memorysOut = []
    InputsRecreated = []
    for i in range(mic_start, mic_end+1):
        InputsRecreated.append([])
        if Order > 0:
            memorysOut.append([0]*Order)
        else:
            memorysOut.append([])


    for itteration in range(recomnded_limit):
        print(itteration)
        start_time = time.time()
        for mic in range(mic_end + 1 - mic_start):
            #Grab the current k value and code word for the current itteration and mic
            m_mic = m_array[mic]
            CodeWords_mic = AllCodeWords[mic]
            m = m_mic[itteration]
            CodeWord = CodeWords_mic[itteration]

            #Calculate the orginal residuals by decodeing the golomb codes
            Golomb_decoder = GolombCoding(m, sign)
            CurrentResiduals = Golomb_decoder.Decode(CodeWord)

            #Recreate the original inputs from residuals
            InputsRecreated[mic], memorysOut[mic], CurrentPrediction = Shorten_predictor.Out(CurrentResiduals, memorysOut[mic])
        
        stop_time = time.time()
        total_time = stop_time - start_time
        
        #Save the time it took to recreate the full array
        time_array.append(total_time)


        if 1 < 0: #only needed when plotting
            for mic in range(mic_end + 1 - mic_start):
                CurrentOriginalInputs = OriginalInputs[itteration]
                figure_title = "Mic #" + str(mic + mic_start) + ", Itteration#" + str(itteration) 

                CurrentOriginalInputs_mic = CurrentOriginalInputs[mic]
                CurrentRecreatedInput = InputsRecreated[mic]
                zero_count = 0
                zero = []
                for i in range(len(CurrentOriginalInputs_mic)):
                    current_zero = CurrentOriginalInputs_mic[i] - CurrentRecreatedInput[i]
                    zero.append(current_zero)
                    if current_zero != 0:
                        zero_count += 1
                        
                if zero_count != 0:
                    print("Failed recreating ", zero_count,"inputs for ", figure_title)

                    

                

                    fig = plt.figure(figure_title)
                    
                    ax=fig.add_subplot(311)
                    plt.plot(CurrentOriginalInputs[mic])
                    ax.title.set_text("Original inputs")

                    ax=fig.add_subplot(312)
                    plt.plot(InputsRecreated[mic])
                    ax.title.set_text("Recreated inputs")

                    ax=fig.add_subplot(313)
                    plt.plot(zero)
                    ax.title.set_text("Original inputs - Recreated inputs")

                    plt.show()
                else:

                    print("All inputs recreated succesfully for ", figure_title)
 
    print("Average time to recreate original input is ", sum(time_array) / len(time_array)," seconds")


if test == 17:
    print("Test 17")
    print("")
    print("Shorten Order ", Order)
    print("")

    time_array = []
    memorysOut = []
    InputsRecreated = []
    for i in range(mic_start, mic_end+1):
        InputsRecreated.append([])
        if Order > 0:
            memorysOut.append([0]*Order)
        else:
            memorysOut.append([])


    for itteration in range(recomnded_limit):
        start_time = time.time()
        for mic in range(mic_end + 1 - mic_start):
            #Grab the current k value and code word for the current itteration and mic
            k_mic = k_array[mic]
            CodeWords_mic = AllCodeWords[mic]
            k = k_mic[itteration]
            CodeWord = CodeWords_mic[itteration]

            #Calculate the orginal residuals by decodeing the rice codes
            Rice_decoder = RiceCoding(k, sign)
            CurrentResiduals = Rice_decoder.Decode(CodeWord)

            #Recreate the original inputs from residuals
            InputsRecreated[mic], memorysOut[mic], CurrentPrediction = Shorten_predictor.Out(CurrentResiduals, memorysOut[mic])
        
        stop_time = time.time()
        total_time = stop_time - start_time
        
        #Save the time it took to recreate the full array
        time_array.append(total_time)


        if 1 < 0: #only needed when plotting
            for mic in range(mic_end + 1 - mic_start):
                CurrentOriginalInputs = OriginalInputs[itteration]
                figure_title = "Mic #" + str(mic + mic_start) + ", Itteration#" + str(itteration) 

                CurrentOriginalInputs_mic = CurrentOriginalInputs[mic]
                CurrentRecreatedInput = InputsRecreated[mic]
                zero_count = 0
                zero = []
                for i in range(len(CurrentOriginalInputs_mic)):
                    current_zero = CurrentOriginalInputs_mic[i] - CurrentRecreatedInput[i]
                    zero.append(current_zero)
                    if current_zero != 0:
                        zero_count += 1
                        
                if zero_count != 0:
                    print("Failed recreating ", zero_count,"inputs for ", figure_title)

                    

                

                    fig = plt.figure(figure_title)
                    
                    ax=fig.add_subplot(311)
                    plt.plot(CurrentOriginalInputs[mic])
                    ax.title.set_text("Original inputs")

                    ax=fig.add_subplot(312)
                    plt.plot(InputsRecreated[mic])
                    ax.title.set_text("Recreated inputs")

                    ax=fig.add_subplot(313)
                    plt.plot(zero)
                    ax.title.set_text("Original inputs - Recreated inputs")

                    plt.show()
                else:

                    print("All inputs recreated succesfully for ", figure_title)
 
    print("Average time to recreate original input is ", sum(time_array) / len(time_array)," seconds")


if test == 16:
    print("Test 16")
    print("")
    if 1 < 0:#Some info about k values
        for i in range(len(k_array)):
            currentKs = k_array[i]
            print("Current max k = ", np.max(currentKs))
            print("Current min k = ", np.min(currentKs))
            print("Current k varriance = ", np.var(currentKs))


        print("all_k max = ", np.max(all_k))
        print("all_k mix = ", np.min(all_k))
        print("all_k varraince = ", np.var(all_k))

    all_cr = []
    #Loops thorugh all mics to get the code_words for the specific mics
    for mic in range(mic_end + 1 - mic_start):
        encodedMic = AllCodeWords[mic]
        uncodedMic = UncodedWords[mic]
        #loops thorugh all data blocks to get the compression rate of the code word for that data block
        for itteration in range(len(encodedMic)):
            cr = len(encodedMic[itteration]) / len(uncodedMic[itteration])
            all_cr.append(cr)

    print("Average compression rate for Shorten order ",Order,"is: cr = ", sum(all_cr) / len(all_cr))


#Test compression ratios for all orders of Shorten using Golomb codes for some m-values
if test == 15:

    print("Test 15")
    print("")

    #Arrays for average compression rates
    cr_0 = []
    cr_1 = []
    cr_2 = []
    cr_3 = []
    
   
    #loop thorugh all m-values
    for i in range(len(m_array)):
        #loops thorugh all orders of shorten
        for q in range(4):
            temp_cr_array = []
            #loops thorugh all sampled blocks of data
            for j in range(len(uncoded_words)):
                #depending on what order being calculated the compressed codeword is saved in a speicific array
                #order_q_array[i][j] where q is oder, i is m-value, and j is code word from sampled data block

                #compression ratio is calculated by dividing lenght of code word by length of uncoded word
                #lenght of uncoded word is assumed to be 32 bits accourding to aucostic warefare paper
                if q == 0:
                    temp_cr = len(order_0_array[i][j]) / len(uncoded_words[j])

                elif q == 1:
                    temp_cr = len(order_1_array[i][j]) / len(uncoded_words[j])

                elif q == 2:
                    temp_cr = len(order_2_array[i][j]) / len(uncoded_words[j])

                elif q == 3:
                    temp_cr = len(order_3_array[i][j]) / len(uncoded_words[j])

                #for each k-value several sampled blocks of data is saved
                #for each block a compression ratio is calculated
                temp_cr_array.append(temp_cr)


            #The average compression ratio for all data block, given a specific m value and order is calculated
            if q == 0:
                cr_0.append(np.sum(temp_cr_array) / len(temp_cr_array))

            elif q == 1:
                cr_1.append(np.sum(temp_cr_array) / len(temp_cr_array))

            elif q == 2:
                cr_2.append(np.sum(temp_cr_array) / len(temp_cr_array))

            elif q == 3:
                cr_3.append(np.sum(temp_cr_array) / len(temp_cr_array))

    #Print result of all average compression ratios for given order and m value
    if 1 < 0:
        print("For a given value: m = ", m_array)
        print("Average compression rate for order 0 = ", cr_0)

        print("Average compression rate for order 1 = ", cr_1)

        print("Average compression rate for order 2 = ", cr_2)

        print("Average compression rate for order 3 = ", cr_3)
        print("")


    


    #calculate ideal choice of m-value for each order

    #appends all orders CR into one array
    all_cr = []
    all_cr.append(cr_0)
    all_cr.append(cr_1)
    all_cr.append(cr_2)
    all_cr.append(cr_3)


    for i in range(4):
        #looks thorugh one order at a time to find the m that gives the best cr for that order
        temp_min_cr_array = all_cr[i]
        temp_m_min = 0
        for j in range(1, len(temp_min_cr_array)):
            
            if temp_min_cr_array[temp_m_min] > temp_min_cr_array[j]:
                #print(j)
                temp_m_min = j

            #if the next m gives a better cr that k-value is saved
            #if temp_min_cr_array[j+1] < temp_min_cr_array[temp_m_min]:
             #   print(j)
              #  temp_m_min = j+1
                
        #prints out the shorten order and its ideal k with the corresponding cr
        print("Shorten order ",i," and m = ", m_array[temp_m_min]," gives best result with cr = ", temp_min_cr_array[temp_m_min])

    print("")

    if 1 < 0:


        #calculate ideal choice of order and m-value

        #Finds the array with the lowest CR value
        o = 0
        for i in range(len(all_cr)-1):
            if np.min(all_cr[i+1]) < np.min(all_cr[i]):
                o = i+1

        #Saves the array with the lowest cr value into its own varaible
        min_cr_array = all_cr[o]

        
        #Loops trough the array with the lowest cr value to find the lowest cr value.
        #Save the index of the lowest cr value
        m_min = 0
        for i in range(len(min_cr_array)-1):
            if min_cr_array[i+1] < min_cr_array[i]:
                m_min = i+1
        #To find which m value corresponds to the index, take the index and add m_array[0]
        print("The best compression ratio is given by Shorten order ",o," with m-value ", m_min+m_array[0], ": cr = ", min_cr_array[m_min])
        print("")

        


        #Plots sub plots with each subplot being a specific order of Shorten
        #y-axis is compression ratio and x-axis is m value
        fig = plt.figure(1)

        ax=fig.add_subplot(221)
        plt.plot(m_array, cr_0, 'ro')
        ax.title.set_text("Shorten Order 0")
        plt.xlabel("m-value")
        plt.ylabel("Compression ratio")

        ax=fig.add_subplot(222)
        plt.plot(m_array, cr_1, 'ro')
        ax.title.set_text("Shorten Order 1")
        plt.xlabel("m-value")
        plt.ylabel("Compression ratio")

        ax=fig.add_subplot(223)
        plt.plot(m_array, cr_2, 'ro')
        ax.title.set_text("Shorten Order 2")
        plt.xlabel("m-value")
        plt.ylabel("Compression ratio")

        ax=fig.add_subplot(224)
        plt.plot(m_array, cr_3, 'ro')
        ax.title.set_text("Shorten Order 3")
        plt.xlabel("m-value")
        plt.ylabel("Compression ratio")
    


    #Plots Order 1, 2, and 3 of shorten in the same plot showing cr depending on m used in Golomb code
    #y-axis is compression rate [cr] and x-axis is m-value
    plt.figure(2)
    plt.plot(m_array, cr_0, 'yo', label='Order 0')
    plt.plot(m_array, cr_1, 'ro', label='Order 1')
    plt.plot(m_array, cr_2, 'bo', label='Order 2')
    plt.plot(m_array, cr_3, 'go', label='Order 3')
    plt.title("Comparison of comression ratio for differente orders")
    plt.xlabel("m-value")
    plt.ylabel("Compression ratio")
    plt.legend()

    plt.show()


#Test if Shorten can recreate input using Golomb coding
#Indicates if any words was wrongly decoded and if so how many of the sampled datablock
#Plots Original input and decoded input
#Gives compression rate of encoded values
if test == 14:
    print("Test 14")
    print("")
    compression_ratio = []
    uncoded_residuals_array = []
    uncoded_values_array = []
    predictions_array = []
    memory_out = memorys[order].copy()

    

    #Calcuates compression ratios of Shorten by comparing length of binary values of input to length of Rice coded residuals
    for i in range(len(code_words)):
        temp_comp_r = len(code_words[i]) / len(uncoded_words[i])
        compression_ratio.append(temp_comp_r)
    print("Compression ratio of Shorten using Golomb code is: ", compression_ratio)


    #Recreates the original inputs
    for i in range(len(inputs)):
        #Grabs the original input values, k-value used to encode, and code_word from arrays
        input = inputs[i]
        m = m_array[i]
        code_word = code_words[i]
        plot_zero = []
        
        #Decodes the residuals from the Rice code
        Golomb_coder = GolombCoding(m, sign)
        uncoded_residuals = Golomb_coder.Decode(code_word)
        uncoded_residuals_array.append(uncoded_residuals)
        
        #Calculates the original inputs from the decoded residuals using Shorten
        uncoded_values, memory_out, predictions = Shorten_predictor.Out(uncoded_residuals, memory_out)
        uncoded_values_array.append(uncoded_values)
        predictions_array.append(predictions)

        #Checks if the uncoded values match the original inputs
        value_check = 0
        for j in range(len(uncoded_values)):
            #If the orignal input dont match the uncoded values value check will increment by 1 
            #and the data block containing the faulty decoded value will be printed out
            if uncoded_values[j] != input[j]:
                print("Failed decode at data block i = ",i," Original input =  ",input[j]," Uncoded value = ", uncoded_values[j])
                value_check += 1
            #Save any error to plot later, if it works correctly it should allways be zero
            plot_zero.append(input[j]-uncoded_values[j])
        #Once all the values have been checked:
        #If there are no wrongly decoded values the code will print out that all values have been correctly decoded for the data block
        if value_check == 0:
            print("Itteration nr",i," correctly decoded all orignal values")
        #If there is some wrongly decoded values the code will print in which data block they are and how many there are
        else:
            print("Itteration nr",i," failed decodeing ",value_check," values")



        if 1 > 0:#Only plots for report
            fig_title = "Test14_order_" + str(order)
            plt.figure(fig_title)
            plt.plot(input, 'b', label='Original values')
            plt.plot(uncoded_values, 'r-.', label='Decoded values')
            plt.legend(fontsize=25)
            plt.yticks(fontsize=20)
            plt.xticks(fontsize=20)
            plt.show()

             #plt.plot(k_array, cr_2, 'bo', label='Order 2')
        #plt.plot(k_array, cr_3, 'go', label='Order 3')
        #plt.title("Comparison of comression ratio for differente orders")
        #plt.yticks(fontsize=20)
        #plt.xticks(fontsize=20)
        #plt.xlabel("k-value", fontsize=25)
        #plt.ylabel("Average compression ratio", fontsize=25)
        #
        #plt.legend(fontsize=20)

        elif 1 < 0:#Only plots for report


            plt.figure("Original values")

            plt.plot(input)

            plt.figure("Uncoded values")

            plt.plot(uncoded_values)

            plt.figure("Original input values - Decoded input values")
            plt.plot(plot_zero)

            plt.show()


        else:#Plots the original input values and the decoded input valus in subplots
            fig = plt.figure(i)

            ax = fig.add_subplot(311)
            plt.plot(input)
            ax.title.set_text("Original input values")

            ax = fig.add_subplot(312)
            plt.plot(uncoded_values)
            ax.title.set_text("Decoded input values")

            ax = fig.add_subplot(313)
            plt.plot(plot_zero)
            ax.title.set_text("Original input values - Decoded input values")

            

            plt.show()


#Test compression ratios for all orders of Shorten using Rice codes for some k-values
if test == 13:
    print("Test 13")
    
    
    print("")

    #Arrays for average compression rates
    cr_0 = []
    cr_1 = []
    cr_2 = []
    cr_3 = []
    

    #loop thorugh all k-values
    for i in range(len(k_array)):
        #loops thorugh all orders of shorten
        for q in range(4):
            temp_cr_array = []
            #loops thorugh all sampled blocks of data
            for j in range(len(uncoded_words)):
                #depending on what order being calculated the compressed codeword is saved in a speicific array
                #order_q_array[i][j] where q is oder, i is k-value, and j is code word from sampled data block

                #compression ratio is calculated by dividing lenght of code word by length of uncoded word
                #lenght of uncoded word is assumed to be 32 bits accourding to aucostic warefare paper
                if q == 0:
                    temp_cr = len(order_0_array[i][j]) / len(uncoded_words[j])

                elif q == 1:
                    temp_cr = len(order_1_array[i][j]) / len(uncoded_words[j])

                elif q == 2:
                    temp_cr = len(order_2_array[i][j]) / len(uncoded_words[j])

                elif q == 3:
                    temp_cr = len(order_3_array[i][j]) / len(uncoded_words[j])

                #for each k-value several sampled blocks of data is saved
                #for each block a compression ratio is calculated
                temp_cr_array.append(temp_cr)


            #The average compression ratio for all data block, given a specific k value and order is calculated
            if q == 0:
                cr_0.append(np.sum(temp_cr_array) / len(temp_cr_array))

            elif q == 1:
                cr_1.append(np.sum(temp_cr_array) / len(temp_cr_array))

            elif q == 2:
                cr_2.append(np.sum(temp_cr_array) / len(temp_cr_array))

            elif q == 3:
                cr_3.append(np.sum(temp_cr_array) / len(temp_cr_array))

    #Print result of all average compression ratios for given order and k value
    
    print("For a given value: k = ", k_array)
    print("Average compression rate for order 0 = ", cr_0)

    print("Average compression rate for order 1 = ", cr_1)

    print("Average compression rate for order 2 = ", cr_2)

    print("Average compression rate for order 3 = ", cr_3)
    print("")


 

    


    #Calculate the recomdnded k-value for each order based on Rice codeing theory
    k_ideal_avg_array = []

    for i in range(4):
        #calculate average for recomended k-value for each order and save in array
        k_ideal_avg = sum(k_ideal_array[i])/len(k_ideal_array[i])
        k_ideal_avg_array.append(k_ideal_avg)

    #prints ideal k-values for each order
    #prints cr with ideal k-value (roundest to closest int) for each order
    print("ideal k-value (Shorten order 0-3)= ", k_ideal_avg_array)
    if k_ideal_avg_array[0] > k_array[0] and (k_ideal_avg_array[0] - k_array[0]) <= len(k_array):
        print("Shorten order 0 with k = ", int(round(k_ideal_avg_array[0])), " gives cr = ", cr_0[int(round(k_ideal_avg_array[0])) - k_array[0]])

    if k_ideal_avg_array[1] > k_array[0] and (k_ideal_avg_array[1] - k_array[0]) <= len(k_array):
        print("Shorten order 1 with k = ", int(round(k_ideal_avg_array[1])), " gives cr = ", cr_1[int(round(k_ideal_avg_array[1])) - k_array[0]])

    if k_ideal_avg_array[2] > k_array[0] and (k_ideal_avg_array[2] - k_array[0]) <= len(k_array):
        print("Shorten order 2 with k = ", int(round(k_ideal_avg_array[2])), " gives cr = ", cr_2[int(round(k_ideal_avg_array[2])) - k_array[0]])

    if k_ideal_avg_array[3] > k_array[0] and (k_ideal_avg_array[3] - k_array[0]) <= len(k_array):
        print("Shorten order 3 with k = ", int(round(k_ideal_avg_array[3])), " gives cr = ", cr_3[int(round(k_ideal_avg_array[3])) - k_array[0]])

    print("")

    #calculate ideal choice of k-value for each order

    #appends all orders CR into one array
    all_cr = []
    all_cr.append(cr_0)
    all_cr.append(cr_1)
    all_cr.append(cr_2)
    all_cr.append(cr_3)

    for i in range(4):
        #looks thorugh one order at a time to find the k that gives the best cr for that order
        temp_min_cr_array = all_cr[i]
        temp_k_min = 0
        for j in range(len(temp_min_cr_array)-1):
            #if the next k gives a better cr than the previous best cr that k-value is saved
            if temp_min_cr_array[j+1] < temp_min_cr_array[temp_k_min]:
                temp_k_min = j+1
        #prints out the shorten order and its ideal k with the corresponding cr
        print("Shorten order ",i," and k = ", temp_k_min + k_array[0]," gives best result with cr = ", temp_min_cr_array[temp_k_min])

    print("")


    #calculate ideal choice of order and k-value

    #Finds the array with the lowest CR value
    o = 0
    for i in range(len(all_cr)-1):
        if np.min(all_cr[i+1]) < np.min(all_cr[i]):
            o = i+1

    #Saves the array with the lowest cr value into its own varaible
    min_cr_array = all_cr[o]

    
    #Loops trough the array with the lowest cr value to find the lowest cr value.
    #Save the index of the lowest cr value
    k_min = 0
    for i in range(len(min_cr_array)-1):
        if min_cr_array[i+1] < min_cr_array[i]:
            k_min = i+1
    #To find which k value corresponds to the index, take the index and add k_array[0]
    print("The best compression ratio is given by Shorten order ",o," with k-value ", k_min+k_array[0], ": cr = ", min_cr_array[k_min])
    print("")



    #Plots sub plots with each subplot being a specific order of Shorten
    #y-axis is compression ratio and x-axis is k value
    fig = plt.figure(1)

    ax=fig.add_subplot(221)
    plt.plot(k_array, cr_0, 'ro')
    ax.title.set_text("Shorten Order 0")
    plt.xlabel("k-value")
    plt.ylabel("Average compression ratio")

    ax=fig.add_subplot(222)
    plt.plot(k_array, cr_1, 'ro')
    ax.title.set_text("Shorten Order 1")
    plt.xlabel("k-value")
    plt.ylabel("Average compression ratio")

    ax=fig.add_subplot(223)
    plt.plot(k_array, cr_2, 'ro')
    ax.title.set_text("Shorten Order 2")
    plt.xlabel("k-value")
    plt.ylabel("Average compression ratio")

    ax=fig.add_subplot(224)
    plt.plot(k_array, cr_3, 'ro')
    ax.title.set_text("Shorten Order 3")
    plt.xlabel("k-value")
    plt.ylabel("Average compression ratio")


    

    #Plots Order 1, 2, and 3 of shorten in the same plot for some k-values
    plt.figure(2)

    plt.plot(k_array, cr_0, 'yo', label='Order 0')#Sometimes comented out when Order 0 gives to large CR
    plt.plot(k_array, cr_1, 'ro', label='Order 1')
    plt.plot(k_array, cr_2, 'bo', label='Order 2')
    plt.plot(k_array, cr_3, 'go', label='Order 3')
    plt.title("Comparison of comression ratio for differente orders")
    plt.xlabel("k-value")
    plt.ylabel("Average compression ratio")
    plt.legend()

    plt.show()

    #These are values saved from test and plotted for report
    if 1 > 0:
        print("plot report")
        k_plot = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
        #Values from testing sine sound, k= 11-15 for order 0, k=8-15 order 1, k = 8-15 for order 2, k = 8-15 order 3
        Sine_order0 = [0.88515625, 0.7446940104166666, 0.6957600911458334, 0.691748046875, 0.7091064453125]
        Sine_order1 = [0.7937744140625, 0.6391438802083333, 0.5803059895833333, 0.5723795572916666, 0.58974609375, 0.6253743489583334, 0.6668212890625002, 0.7083577473958335]
        Sine_order2 = [0.6918619791666667, 0.5924886067708333, 0.5577067057291667, 0.5619140624999999, 0.5873860677083333, 0.6258138020833334, 0.6670003255208333, 0.7083984375000002]
        Sine_order3 = [0.9262125651041668, 0.7160400390625001, 0.6189046223958334, 0.5917643229166667, 0.6001627604166668, 0.6279134114583333, 0.6674235026041667, 0.7085693359375]
        #Values from testing silent (mic 20), k = 1-8
        Silent_order0 =  [0.125, 0.16666666666666663, 0.20833333333333334, 0.25, 0.29166666666666674, 0.33333333333333326, 0.375, 0.4166666666666667]
        Silent_order1 = [0.125, 0.16666666666666663, 0.20833333333333334, 0.25, 0.29166666666666674, 0.33333333333333326, 0.375, 0.4166666666666667]
        Silent_order2 =  [0.125, 0.16666666666666663, 0.20833333333333334, 0.25, 0.29166666666666674, 0.33333333333333326, 0.375, 0.4166666666666667]
        Silent_order3 = [0.125, 0.16666666666666663, 0.20833333333333334, 0.25, 0.29166666666666674, 0.33333333333333326, 0.375, 0.4166666666666667]
        #Values from testing Drone, k = 13-20 for all orders but 3 wich is k= 14-20
        Drone_order0 =  [0.9572916666666667, 0.8228434244791666, 0.7768636067708334, 0.77548828125, 0.7971842447916666, 0.8335286458333334, 0.875, 0.9166666666666667]
        Drone_order1 = [0.9583170572916666, 0.8236083984375, 0.7773030598958333, 0.7756266276041667, 0.7973714192708334, 0.8336018880208333, 0.875, 0.9166666666666667]
        Drone_order2 =  [1.0740071614583333, 0.8810791015625001, 0.8058430989583334, 0.7895426432291667, 0.8037353515625, 0.8348551432291668, 0.875048828125, 0.9166666666666667]
        Drone_order3 =[0.9959472656250001, 0.8629313151041668, 0.8175862630208334, 0.8169677734375, 0.8393717447916668, 0.8754964192708332, 0.9166666666666667]
        #Values from testing static noise, k = 13-20 order 0, k= 14-20 for order 1 and order 2, k= 15-20 for order 3
        Static_order0 = [1.0679524739583335, 0.8781494140625, 0.8041178385416666, 0.7887207031250001, 0.8031575520833332, 0.8342936197916666, 0.875, 0.9166666666666667]
        Static_order1 = [0.9243652343750002, 0.827392578125, 0.800244140625, 0.8084879557291668, 0.8358154296875, 0.8750162760416667, 0.9166666666666667]
        Static_order2 = [1.0432942708333335, 0.8866048177083332, 0.8293619791666667, 0.8226725260416667, 0.8415852864583332, 0.8756266276041667, 0.9166666666666667]
        Static_order3 = [0.9977783203125001, 0.8848958333333332, 0.8495035807291667, 0.853662109375, 0.8788574218749998, 0.9167724609375]
        
        plt.figure("Test13_fixed_values")

        #Plot sine
        plt.plot(k_plot[10:15], Sine_order0, 'yo', label='1k Hz sine soundwave, Shorten order 0')
        plt.plot(k_plot[7:15], Sine_order1, 'yv', label='1k Hz sine soundwave, Shorten order 1')
        plt.plot(k_plot[7:15], Sine_order2, 'ys', label='1k Hz sine soundwave, Shorten order 2')
        plt.plot(k_plot[7:15], Sine_order3, 'y*', label='1k Hz sine soundwave, Shorten order 3')

        #plot silent
        plt.plot(k_plot[0:8], Silent_order0, 'ro', label='Silent mic, Shorten order 0')
        plt.plot(k_plot[0:8], Silent_order1, 'rv', label='Silent mic, Shorten order 1')
        plt.plot(k_plot[0:8], Silent_order2, 'rs', label='Silent mic, Shorten order 2')
        plt.plot(k_plot[0:8], Silent_order2, 'r*', label='Silent mic, Shorten order 3')

        #plot drone
        plt.plot(k_plot[12:20], Drone_order0, 'bo', label='Drone sound, Shorten order 0')
        plt.plot(k_plot[12:20], Drone_order1, 'bv', label='Drone sound, Shorten order 1')
        plt.plot(k_plot[12:20], Drone_order2, 'bs', label='Drone sound, Shorten order 2')
        plt.plot(k_plot[13:20], Drone_order3, 'b*', label='Drone sound, Shorten order 3')

        #plot Static oise
        plt.plot(k_plot[12:20], Static_order0, 'go', label='Static noise, Shorten order 0')
        plt.plot(k_plot[13:20], Static_order1, 'gv', label='Static noise, Shorten order 1')
        plt.plot(k_plot[13:20], Static_order2, 'gs', label='Static noise, Shorten order 2')
        plt.plot(k_plot[14:20], Static_order3, 'g*', label='Static noise, Shorten order 3')

        #plt.plot(k_array, cr_2, 'bo', label='Order 2')
        #plt.plot(k_array, cr_3, 'go', label='Order 3')
        #plt.title("Comparison of comression ratio for differente orders")
        plt.yticks(fontsize=20)
        plt.xticks(fontsize=20)
        plt.xlabel("k-value", fontsize=25)
        plt.ylabel("Average compression ratio", fontsize=25)
        plt.legend(fontsize=15)

        plt.show()



#Plot input signal, residual, predicted value to see how good the result of shorten is
if test == 12:
    print("Test 12")
    print("")
    #One figure for each order, created by a for loop of range 4
    

    if 1 < 0:#Only for plots in report
        plots_report = [plot_sig, plot_predict[2], plot_residuals[2], plot_zero[2]]#the number decides what order to plot
        for i in range(4):

            plt.figure(i)

            plt.plot(plots_report[i])

        plt.show()
            

    else:
        for i in range(4):
            figure_title = "Shorten order " + str(i)
            fig = plt.figure(figure_title)

            #Each figure plots 4 subplots with:
            #Input signal, prediction of Shorten, Residual of shorten, Zero (Input - (residual + prediciton) = 0)
            ax = fig.add_subplot(221)
            plt.plot(plot_sig)
            ax.title.set_text("Input signal")

            ax = fig.add_subplot(222)
            plt.plot(plot_predict[i])
            ax.title.set_text("Predicted signal")

            ax = fig.add_subplot(223)
            plt.plot(plot_residuals[i])
            ax.title.set_text("Residual signal")

            ax = fig.add_subplot(224)
            plt.plot(plot_zero[i])
            ax.title.set_text("Input - (Predict + Residual) = 0")

            plt.show()


#Test if Shorten can recreate input using Rice coding
#Indicates if any words was wrongly decoded and if so how many of the sampled datablock
#Plots Original input and decoded input
#Gives compression rate of encoded values
if test == 11:
    print("Test 11")
    print("")
    compression_ratio = []
    uncoded_residuals_array = []
    uncoded_values_array = []
    predictions_array = []
    memory_out = memorys[order].copy()

    

    #Calcuates compression ratios of Shorten by comparing length of binary values of input to length of Rice coded residuals
    for i in range(len(code_words)):
        temp_comp_r = len(code_words[i]) / len(uncoded_words[i])
        compression_ratio.append(temp_comp_r)
    print("Compression ratio of Shorten is: ", compression_ratio)


    
    

    #Recreates the original inputs
    for i in range(len(inputs)):
        #Grabs the original input values, k-value used to encode, and code_word from arrays
        input = inputs[i]
        k = k_array[i]
        code_word = code_words[i]

        plot_zero = []
        
        #Decodes the residuals from the Rice code
        Rice_coder = RiceCoding(k, sign)
        uncoded_residuals = Rice_coder.Decode(code_word)
        uncoded_residuals_array.append(uncoded_residuals)
        
        #Calculates the original inputs from the decoded residuals using Shorten
        uncoded_values, memory_out, predictions = Shorten_predictor.Out(uncoded_residuals, memory_out)
        uncoded_values_array.append(uncoded_values)
        predictions_array.append(predictions)

        #Checks if the uncoded values match the original inputs
        value_check = 0
        for j in range(len(uncoded_values)):
            #If the orignal input dont match the uncoded values value check will increment by 1 
            #and the data block containing the faulty decoded value will be printed out
            plot_zero.append(input[j] - uncoded_values[j])
            if uncoded_values[j] != input[j]:
                print("Failed decode at data block i = ",i," Original input =  ",input[j]," Uncoded value = ", uncoded_values[j])
                value_check += 1
        #Once all the values have been checked:
        #If there are no wrongly decoded values the code will print out that all values have been correctly decoded for the data block
        if value_check == 0:
            print("Itteration nr",i," correctly decoded all orignal values")
        #If there is some wrongly decoded values the code will print in which data block they are and how many there are
        else:
            print("Itteration nr",i," failed decodeing ",value_check," values")

        


        if 1 < 0:#Only plots for repport
            fig_title = "Test11_order_" + str(order)
            plt.figure(fig_title)
            plt.plot(input, 'b', label='Original values')
            plt.plot(uncoded_values, 'r-.', label='Decoded values')
            plt.legend(fontsize=25)
            plt.yticks(fontsize=20)
            plt.xticks(fontsize=20)
            plt.show()

             #plt.plot(k_array, cr_2, 'bo', label='Order 2')
        #plt.plot(k_array, cr_3, 'go', label='Order 3')
        #plt.title("Comparison of comression ratio for differente orders")
        #plt.yticks(fontsize=20)
        #plt.xticks(fontsize=20)
        #plt.xlabel("k-value", fontsize=25)
        #plt.ylabel("Average compression ratio", fontsize=25)
        #
        #plt.legend(fontsize=20)

            


        elif 1 < 0:#Only plots for report


            plt.figure("Original values")

            plt.plot(input)

            plt.figure("Uncoded values")

            plt.plot(uncoded_values)

            plt.figure("Original input values - Decoded input values")
            plt.plot(plot_zero)

            plt.show()


        else:
            #Plots the original input values and the decoded input valus in subplots
            fig = plt.figure(i)

            ax = fig.add_subplot(311)
            plt.plot(input)
            ax.title.set_text("Original input values")

            ax = fig.add_subplot(312)
            plt.plot(uncoded_values)
            ax.title.set_text("Decoded input values")

            ax = fig.add_subplot(313)
            plt.plot(plot_zero)
            ax.title.set_text("Original input values - Decoded input values")


            plt.show()


#Calculates compression rate of using Golomb and Rice codes directly on the input values (Assuming input values at 32 bits)
#Compares average length of input values with average binary length of input values
#Also states the longest binary input value
if test == 4:
    print("Test 4")
    print("")
    cr_r = []
    cr_g = []
    avg_len_r = []
    avg_len_g = []
    avg_len_smal = []

    print("Array lengths:")
    print("Rice: ", len(code_words_r[0]))
    print("Golomb: ", len(code_words_g[0]))
    print("32 bit: ", len(uncoded_words_24[0]))
    print("Smal bit: ", len(uncoded_words_smal[0]))

    

    for i in range(len(code_words_r)):
        cr_r.append(len(code_words_r[i])/len(uncoded_words_24[i]))
        cr_g.append(len(code_words_g[i])/len(uncoded_words_24[i]))

        avg_len_r.append(len(code_words_r[i])/256)
        avg_len_g.append(len(code_words_g[i])/256)
        avg_len_smal.append(len(uncoded_words_smal[i])/256)

    print("Rice codes compression rates: ", cr_r)
    print("Golomb codes compression rates: ", cr_g)
    print("")
    print("Average compression rate of Rice codes: ", sum(cr_r)/len(cr_r))
    print("Average compression rate of Golomb codes: ", sum(cr_g)/len(cr_g))
    print("")
    print("Average length of Rice coded inputs: ", sum(avg_len_r)/len(avg_len_r))
    print("Average length of Golomb coded inputs: ", sum(avg_len_g)/len(avg_len_g))
    print("Average length of binary inputs: ", sum(avg_len_smal)/len(avg_len_smal))
    print("Largest binary representation of inputs: ", np.max(uncoded_smal_max_array))
        

#Test average length of binary representation for input data and the largest bit representation of input data
if test == 2:
    print("Test 2")
    print("")
    avg_len = []
    max_len = []
    #loops trough each sample data block
    for i in range(len(code_words_len)):
        #Calculates the maximum and average length for the binary inputs of each data block sample
        code_word_len = code_words_len[i]
        sum_len = sum(code_word_len)
        temp_max = np.max(code_word_len)

        avg_len.append(sum_len / len(code_word_len))
        max_len.append(temp_max)
    #Prints the results of maximum and average length for the binary inputs of each data block sample
    print("Average length of uncoded words: ", avg_len)
    print("Max length of uncoded words: ", max_len)


#Plot all mics to find which ones have good recorded values
if test == 1:
    print("Test 1")
    print("")

    
    if 1 < 0:#only for report

        sine = [-24104, -24632, -24245, -22717, -21856, -18517, -16941, -14584, -12349, -9949, -5617, -4457, -1172, 3212, 4075, 8452, 11111, 11103, 15540, 16312, 17251, 20076, 19695, 20463, 23027, 20603, 20279, 20791, 17919, 18296, 14751, 12851, 12299, 8715, 6304, 3320, 1231, -3436, -6036, -8261, -14236, -14273, -16876, -19732, -21793, -23557, -23588, -25857, -25433, -24104, -26105, -23264, -22245, -22893, -18661, -18461, -16588, -12604, -9377, -7761, -4172, -2888, 1356, 4188, 5135, 9591, 12587, 13132, 16267, 17091, 18875, 19064, 19631, 20099, 21071, 19759, 17824, 18032, 18247, 14335, 12532, 11540, 7675, 5132, 4136, -1788, -4316, -7289, -11804, -13492, -16097, -18924, -20833, -22056, -23804, -24964, -23853, -26569, -26133, -24069, -24740, -22844, -20305, -21256, -16756, -15385, -13584, -7920, -7188, -3636, -145, 1179, 4304, 7920, 9636, 11348, 14548, 15987, 17627, 18371, 19531, 19428, 20264, 21007, 18816, 18647, 16547, 16048, 12671, 10459, 10051, 6327, 3443, 1224, -2672, -6300, -8168, -11805, -15284, -17437, -19745, -21904, -23377, -24493, -25257, -25585, -27033, -26757, -25096, -25725, -23736, -21604, -19877, -18996, -15372, -13225, -10084, -6945, -5568, -2865, 2039, 3199, 6515, 9735, 11084, 11996, 15683, 15836, 15907, 17635, 18443, 17332, 18971, 16991, 16595, 15523, 12796, 12624, 9864, 6300, 5304, 1631, -1745, -3640, -7905, -10105, -13501, -15937, -18977, -20768, -22377, -24457, -25848, -26141, -27720, -27144, -28068, -26805, -25684, -25324, -23209, -20012, -18736, -16760, -12901, -11896, -7085, -5161, -3437, 796, 2523, 6199, 9315, 9676, 13679, 14763, 15543, 16292, 17240, 17755, 17527, 17984, 15627, 16203, 14663, 12335, 11212, 10076, 5232, 3668, 1419, -3324, -5317, -8505, -12080, -14464, -18404, -19941, -22697, -25464, -24076, -28209, -27457, -27677, -29389, -27552, -27948, -26964, -24932, -24188, -20869, -19857, -17249, -14744, -12481, -9137, -11485, -14489, -17909, -21781, -23057, -25665, -26904, -29912, -31773, -31165, -32604, -33216, -31612, -31997, -29656, -27577, -28276, -24508, -22225, -21392, -17349, -16329, -11972, -9285, -6580, -3809, 256, 2524, 3728, 6719, 9696, 10956, 12016, 13307, 14523, 14171, 13760, 14339, 12923, 11004, 11535, 7320, 7620, 4215, 1467, 451, -3236, -7329, -10693, -12768, -15757, -19844, -22585, -25380, -27076, -29201, -30936, -31552, -33344, -33356, -33349, -34240, -32832, -30425, -31264, -26876, -25360, -23493, -20409, -17045, -15896, -11877, -8393, -5949, -2525, 0, 2624, 6108, 9116, 8120, 12087, 13979, 12279, 16256, 14304, 14448, 15392, 13652, 12715, 11652, 9080, 8203, 6211, 1547, 479, -2556, -6509, -9372, -12416, -15289, -18884, -21385, -23876, -25192, -26700, -28621, -29753, -29845, -29992, -31217, -28889, -29328, -28488, -25101, -24736, -23569, -19429, -17705, -15168, -10980, -9228, -5792, -2713, 156, 3219, 4783, 7787, 10903, 11968, 13520, 16731, 15051, 15216, 17904, 15964, 15936, 15967, 13384, 11488, 11388, 8959, 5495, 3968, 591, -2568, -5325, -7777, -11805, -14841, -17720, -20424, -23780, -25173, -27773, -28741, -29972, -30264, -32229, -30608, -30897, -29784, -28113, -27932, -24436, -22084, -20045, -19465, -15028, -12312, -10601, -6332, -3732, -1132, 1984, 5212, 6772, 9727, 11880, 12096, 14527, 16103, 14488, 16616, 15832, 15212, 14575, 13000, 11684, 8535, 7475, 3399, 2383, -1561, -4572, -7140, -10785, -14000, -16929, -19917, -22724, -23977, -26733, -28328, -30024, -31853, -29821, -31484, -33008, -29393, -29501, -28940, -25609, -26368, -21516, -19980, -18297, -13305, -11633, -9228, -4589, -2641, -240, 3407, 4968, 8228, 10536, 10244, 15219, 14972, 14152, 16792, 16548, 14831, 15983, 13564, 13583, 11883, 9160, 7764, 5167, 1979, 511, -3940, -6729, -10032, -13112, -16576, -19252, -21885, -24000, -26196, -26901, -29085, -29564, -28916, -30792]

        drone = [128223, -40169, -125481, -108628, -179677, -151228, -60312, -30768, 93931, 4195, -280889, -45693, 73391, 22392, 137320, 200243, -18765, 8236, 142391, -51097, -160164, -33245, 79299, -78804, -207936, -80368, -16484, 57379, 14687, 13571, 178231, -42864, -272492, -92509, 100548, 26691, -88060, -25288, 83655, 194636, 12568, -49176, 94676, 9900, 9615, 215472, 138495, -169189, -238668, -215261, -76484, 72824, -25425, -80517, 69276, 18664, -130289, -100321, 7955, -93137, -151809, -14025, 124823, 211744, 37175, -144025, -11941, 66464, 177312, 425560, 330200, -33673, -187512, -185133, -89284, 89592, -613, -172185, -237893, -235533, -79117, 81843, 41968, -41484, 6704, 57571, 96447, 85159, 62419, 101963, -11065, -73684, -17197, 105956, 274528, 151920, -145780, -177737, 62516, 170963, 42684, -101732, -212788, -221937, -141460, -120669, -71256, 20707, -84105, -105580, 4823, 138995, 230520, 99260, 62703, 125543, 59311, 134644, 110027, -66985, -65924, -146749, -23752, 64023, -82196, -82125, -98764, -145712, -27792, 26912, -110036, -67376, 63416, -48605, -150721, -56056, 22239, -13809, 40463, 131395, 127720, 112492, 48524, -72837, -69824, 20132, 94516, 43727, -110924, -172161, -64465, 58263, 115683, -6808, -86676, -58617, -26864, 7748, 50344, 113248, 35332, -105609, -150761, -54380, 84544, 21104, -79292, 12968, 84804, 71387, 78407, -8788, -41088, 43247, 58832, 33992, 22140, -39757, -74821, -12761, 50540, -44908, -201552, -211852, -106060, 44903, 110012, -117748, -216417, -10697, 48055, 156168, 100736, 12407, 152996, 132628, 78304, 194416, 232571, -95565, -186184, -196657, -22044, 72059, -177353, -181633, -243501, -343316, -174729, 138416, 225583, 60764, -116933, -125668, 83187, 191492, 91367, 39259, -59285, -119140, 19384, 148248, 173920, 168108, 31643, -145452, -41121, 117975, -1993, -63180, -227068, -278677, -128949, -92945, -49532, -116776, -52077, 171, 39700, 120635, 110432, 135132, 73023, -65872, -80961, 38912, 132916, -10593, -197585, -44168, 134523, 80339, -5297, -67537, -111392, -72985, -24789, -5485, 114923, 98755, -19925, 14023, 70008, 58580, 50503, 40740, -19193, -38356, 44319, 83232, 93003, 98967, -132145, -261565, -22693, 79820, 50915, -159601, -311385, -92229, 105295, 122867, 46004, -124333, -90520, -42500, -99065, 17340, 133547, 83308, -79905, -92389, 42059, 103911, 156496, 124924, 0, -5477, 104571, 147612, 81639, -98001, -178485, -91908, 13759, 62380, 27987, -68496, -70093, -42700, -65273, -45785, 16092, -36880, -112893, -67177, 13039, -1093, -51684, -76896, -87472, 40995, 183476, 93352, -60364, -45685, 72748, 103595, 11523, -83957, -106829, -47100, 22704, 46808, 463, -33773, 14771, 62260, 52752, 73660, 96527, 26791, -24537, -11960, -14680, 73679, 85539, -40804, -78881, -119669, -52105, 90307, 92779, 3123, -63613, -111524, -76141, -16657, 16192, 4724, -108789, -72353, 28928, 76235, 133792, 56795, 13444, -53365, -22485, 97223, 118055, 84940, 6051, -115541, -159912, -49309, 101243, 147868, 1500, -146617, -43853, 42092, 49119, 18084, -82377, -11116, 104648, 19448, -93285, -22068, 24683, -10396, 29027, 1724, 87539, 54968, -138865, -106100, 117471, 168396, 2824, -201349, -215729, 87824, 284808, 175187, -46048, -128757, -65885, -31680, 27400, 206280, 156483, -101356, -324008, -241925, 46300, 145483, 68100, -61389, -96473, 3108, 71080, 130067, 226148, 123527, -46440, -37608, 52060, 118380, 131787, -62480, -197793, -73152, 12547, -71961, -145285, -160613, -142800, 6244, 136260, 36647, -69876, -116372, 17464, 143024, 164596, 62584, 11255, -11689, -125525, -92753, 138656, 125764, -145680, -222504, -158357, 58443, 149971, -42112, -47380, 93404, 106211, 40640, 8, 52560, 95231, 57420, -63756, -64001, 105896, 151595, 1612, -70829, -10600, 70263, 57792, -5084, -18785, -9801, -1229, 2764, -47889, -105789, -113340, -159832, -149596, 19951, 114963, 48608, 17847, -45232, 7479, 92447, 109835, 147244, 81248, 23128, 58220, 16287, -6416, 107767, 73304, -5932, -78933, -126201, -29036, -7080, -27456, -65972, -90788, -119732]


        static = [-19001, 43808, 73104, 195403, -32880, -32548, 73251, -183364, -101596, 121528, -2656, -50484, 24347, -82912, -219092, -56832, 90995, -57064, -204941, -86421, -45400, -79565, 113023, 16183, -142177, 97203, -836, -100092, 205647, 152895, -54777, 60952, 118035, 15675, 22312, 82296, 11308, -124700, -101104, 38591, 62179, 59603, 45140, -94812, -185124, 31955, 61547, -108045, 115455, 168784, -107056, -62693, 17952, 39491, 250219, 279519, -34220, -258849, 25548, 248735, -65340, 23548, 20860, -306008, -146573, 12284, -50269, -119981, -37956, -48761, -295380, 209440, 267863, -191465, 181075, 199000, -195585, 125899, 248643, 84707, 41776, -94837, -106612, 54620, 285111, 113171, -353113, -94492, 193743, -70444, -12653, 24135, -282969, -60948, 179727, -144852, -157733, -20637, -99297, -2917, 123831, 37912, -56953, 44139, 175459, 190396, 37503, -157660, -53628, 213239, 190272, -51725, -127044, -99817, -77728, 128056, 176244, -68324, -128844, -81317, -84804, 179852, 203040, -204832, -102440, 175084, -61437, -173252, -19436, -1333, 95335, 199932, -74720, -114920, 44364, -17133, 57543, 137787, 79979, 32863, 47160, -43216, -249873, 5448, 172203, 2740, -5876, -110312, -208236, -130140, 55764, 137203, 38252, 73812, -15120, -186741, -22877, 138531, -5788, 17028, 126436, -133084, -277653, -50188, 159772, 157979, 20347, -57037, -82621, 42783, 190416, 136800, 46356, 27763, -277, -91916, -62084, 113228, 28063, -190244, -97204, 65496, -92269, -153268, 72943, 72995, 6715, 99927, -25564, -134973, 62023, 46919, -51129, 145356, -10069, -439212, -254776, 216539, 142508, -89125, 68723, -146240, -246505, 302716, 140791, -173108, 142884, 137791, -34901, 65687, 83731, -202721, -181989, 264460, 212963, 535, 88136, -120157, -264261, 132672, 253267, 11068, -78113, -207769, -205532, -8997, 21592, -37864, -87241, -76536, 46472, 71752, 45836, -59461, -82360, 229932, 344619, 71883, -227709, -172433, 166623, 179859, 61248, -7077, -197333, -218976, -16476, 103480, 45852, -33373, -160617, -166264, 97555, 151100, -114605, -177344, -97012, 34083, -66164, -147896, 10252, 55627, -24688, -73481, -61541, 18356, 127644, 160564, -400, -115412, -55472, -24993, 73048, 185976, 69167, -39596, -14776, -55849, -53584, 66635, 169931, 142600, -30308, -162953, -171380, -104101, 102375, 170423, -91208, -199080, -115813, -81937, 82847, 160835, -98125, -124465, 115115, 116368, 67267, 28843, -180101, -142504, 121748, 191031, 94907, -79920, -163392, -230217, -30628, 266616, 58023, -70529, -6600, -165725, -1428, 234323, 60755, -1016, 86579, -45837, -138977, 74607, 79959, -194224, -65381, 226856, 12611, -196933, -103453, -216732, -20420, 363864, 108563, -171848, -75396, -74700, 55660, 281759, 205143, -43576, -172449, -68632, 167147, 217243, 143643, 4012, -223537, -58372, 132568, 1000, 66148, 70228, -159689, -115132, 20696, -38289, -45816, -9744, -110797, -151012, -4941, 113784, -26220, -121045, 715, -49417, 60468, 258391, 60031, -83217, -27652, -39780, 24415, 140600, 163179, -104897, -281064, -53632, 8320, 95583, 169327, -239992, -241044, 72580, -42253, -1237, 141107, 18847, -55065, -67533, -43560, 23167, 42168, 32163, 39668, 88843, 37424, -124516, -106580, 77851, 146836, 81663, 43767, -57445, -137605, 31380, 118387, 50344, 101688, -5757, -231928, -93385, 134339, 62708, -15737, -23653, -64344, -18168, 89775, -36573, -228500, -15129, 242259, 57320, -58964, -13577, -222053, -96101, 273308, 164971, -94228, -126620, -126093, 65760, 293028, 118664, -167092, -98985, -7421, 0, 33167, 37544, 95804, -44452, -254177, -10877, 200656, 3467, -27120, -29297, -123709, 151627, 188187, -189049, -121876, 130143, 56096, 90847, 111112, -113980, -187037, 48427, 178300, 31851, -103373, -101229, -133865, -7877, 151455, -115733, -327961, -46789, 122232, -22160, 30588, 101064, -148585, -131897, 138571, 98768, 23983, 119024, 74055, -24737, -8925, 83328, 78023, 28619, 46700, 23316, 22764, 23592, -65305, -51229, 48492, -39212, -194876, -124808, 17359, 1687, -44549, -42704, -34941, -50161, -40041, -59752, -42872, 131003, 100623, -70480, 22427, 62343]

        print("len sine = ", len(sine))

        print("len drone = ", len(drone))

        print("len static = ", len(static))

        white_plot = [-100000,100000] + [-200000]*510

        plt.figure("Test_1_Mic_79_all_sounds")
        plt.plot(white_plot, 'w')
        plt.plot([-300000]*512, 'w')
        plt.plot(sine, 'b', label = '1k Hz tone')
        plt.plot(drone, 'g-.', label = 'Drone sound')
        
        plt.plot(static, 'r:', label = 'Static noise')
        
        
        plt.yticks(fontsize=20)
        plt.xticks(fontsize=20)
        plt.legend(fontsize=25)


        plt.show()



        plt.figure("Test_1_Mic_136_233")
        plt.plot(plot_sig[233], 'g', label = 'Mic #233')
        
        plt.plot(plot_sig[136], 'r', label = 'Mic #136')
        
        
        plt.yticks(fontsize=20)
        plt.xticks(fontsize=20)
        plt.legend(fontsize=25)


        plt.show()

    elif 1 < 0:

       

      




    
        
        
        plt.figure("Test_1_Mic_79_136_233")
        plt.plot(plot_sig[233], 'g', label = 'Mic #233')
        
        plt.plot(plot_sig[136], 'r', label = 'Mic #136')
        plt.plot(plot_sig[79], 'b', label = 'Mic #79')
        
        plt.yticks(fontsize=20)
        plt.xticks(fontsize=20)
        plt.legend(fontsize=25)


        plt.show()

    

        plt.figure("Test_1_Mic_233")
        plt.plot(plot_sig[233], 'b', label = 'Mic #233')
        
        
        
        plt.yticks(fontsize=20)
        plt.xticks(fontsize=20)
        #plt.legend(fontsize=25)


        plt.show()

        plt.figure("Test_1_Mic_136")
        plt.plot(plot_sig[136], 'b', label = 'Mic #136')
        
        
        
        plt.yticks(fontsize=20)
        plt.xticks(fontsize=20)
        #plt.legend(fontsize=25)


        plt.show()

        plt.figure("Test_1_Mic_79")
        plt.plot(plot_sig[79], 'b', label = 'Mic #79')
        
        
        
        plt.yticks(fontsize=20)
        plt.xticks(fontsize=20)
        #plt.legend(fontsize=25)


        plt.show()

        plt.figure("Test_1_Mic_19_20")
        plt.plot([0,1],[-3,3],'w')
        plt.plot(plot_sig[19], 'r', label = 'Mic #19')
        plt.plot(plot_sig[20], 'b', label = 'Mic #20')
        
        
        plt.yticks(fontsize=20)
        plt.xticks(fontsize=20)
        plt.legend(fontsize=25)


        plt.show()

        plt.figure("Test_1_Mic_19")
        plt.plot([0,1],[-3,3],'w')
        plt.plot(plot_sig[19], label = 'Mic #19')
        
        
        
        plt.yticks(fontsize=20)
        plt.xticks(fontsize=20)
        #plt.legend(fontsize=25)


        plt.show()

        plt.figure("Test_1_Mic_20")
        plt.plot([0,1],[-3,3],'w')
        plt.plot(plot_sig[19], label = 'Mic #20')
        
        
        
        plt.yticks(fontsize=20)
        plt.xticks(fontsize=20)
        #plt.legend(fontsize=25)

    
        plt.show()

        plt.figure("Test_1_Mic_217")

        plt.rc('font', **{'size':'30'})
        plt.plot(plot_sig[217], 'b', label = 'Mic #217')
        
        plt.yticks(fontsize=30)
        plt.xticks(fontsize=30)
        plt.legend(fontsize=25)


        plt.show()


        plt.figure("Test_1_Mic_217_no_label")

        plt.rc('font', **{'size':'30'})
        plt.plot(plot_sig[217], label = 'Mic #217')
        
        plt.yticks(fontsize=30)
        plt.xticks(fontsize=30)
        #plt.legend(fontsize=25)


        plt.show()





    #This if statment only plots some graphs deemed interesting in the report
    elif 1 < 0:

        fig = plt.figure(0)

        ax = fig.add_subplot(221)
        plt.plot(plot_sig[best_mic])
        mic_title = "Mic #" + str(best_mic) + ", example of good mic"
        ax.title.set_text(mic_title)

        ax = fig.add_subplot(222)
        plt.plot(plot_sig[blasted_mic])
        mic_title = "Mic #" + str(blasted_mic) + ", example of broken mic (high volume)"
        ax.title.set_text(mic_title)

        ax = fig.add_subplot(223)
        plt.plot(plot_sig[silent_mic_1])
        mic_title = "Mic #" + str(silent_mic_1) + ", example of broken mic (silent)"
        ax.title.set_text(mic_title)

        ax = fig.add_subplot(224)
        plt.plot(plot_sig[silent_mic_2])
        mic_title = "Mic #" + str(silent_mic_2) + ", example of broken mic (silent)"
        ax.title.set_text(mic_title)

        plt.show()

    #Test that only shows best mic
    elif 1 < 0:
    
   
        plt.figure("Test1_mic79")

        plt.plot(plot_sig[79])

        plt.figure("Test1_mic19")

        plt.plot(plot_sig[19])

        plt.figure("Test1_mic20")

        plt.plot(plot_sig[20])

        plt.figure("Test1_mic217")

        plt.plot(plot_sig[217])

        plt.figure("Test1_mic136")

        plt.plot(plot_sig[136])

        plt.figure("Test1_mic235")

        plt.plot(plot_sig[235])

        plt.show()
        



    else:
        plot_nr = 1
        #loops thorugh the array with mic data, ploting each mic
        #this is done in subplot so that each figure conatins 4 mic
        for i in range(256):
            fig = plt.figure(plot_nr)
            sub_nr =(i%4 + 1)

            ax = fig.add_subplot(220+sub_nr)
            plt.plot(plot_sig[i])
            mic_title = "Mic #" + str(i)
            ax.title.set_text(mic_title)
            



            if i % 4 == 3:
            
                plot_nr +=1
                plt.show()#Each figure is plotted one at a time, to plot all at the same time move this outsie for-loop


