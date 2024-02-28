from lib.beamformer import *
import config as config
import numpy as np
import math
from Rice import RiceCoding
from Golomb import GolombCoding
from Shorten import Shorten
from LPC import LPC
from FLAC import FLAC
#from Adjacant import Shorten_adjacent

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
test = 31

#General tests
#Test 0. Saves all new input data in an array and return it outside read data loop
#Test 1. This test plots microphone data
#Test 2. This test checks average binary len and max length of input data if every data point was written with minimal amount of bits
#Test 4. Try Rice and Golom codes on original inputs

#Shorten tests
#Test 11. Test if Shorten using Rice code can correctly decode the input values
#Test 12. Plots results for differente orders of Shorten
#Test 13. This test tries different k-values in Rice codes for all orders of shorten over several data blocks.
#Test 14. Test if Shorten using Golomb code can correctly decode the input values
#Test 15. This test tries different m-values in Golomb codes for all orders of shorten. 
#Can be done over several data blocks in theory but computer dont seem to manage it 

#LPC tests
#Test 21. Test if LPC using Rice code can correctly decode the input values
#Test 22. Test if LPC using Golomb code can correctly decode the input values
#Test 23. Test what order of LPC gives best result, also test how large of an order it is possible to try
#Test 24. Test what k-value gives the best compression rate when using LPC and Rice codes for different orders of LPC
#Test 25. Test what m-value gives the best compression rate when using LPC and Golomb codes for different order of LPC

#FLAC tests
#Test 31.


#Initial values for tests
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
    
    



if test == 25:
    uncoded_words = []
    orders = []
    order_start = 1
    order_stop = 8
    order_array = []
    memorys = []
    for i in range(order_start, order_stop+1):
        orders.append(i)
        order_array.append([])
        memorys.append([0]*i)
    
    #m starting and stop value will be their assigned values times factorr
    #m will increment by step factor each time
    factorr = 1
    m_start = 1
    m_stop = 100
    m_array = []

    for i in range(m_start, m_stop+1):
        m_array.append(int(i*factorr))
        for j in range(len(order_array)):
            order_array[j].append([])


if test == 24:
    uncoded_words = []
    orders = []
    order_start = 1
    order_stop = 8
    order_array = []
    k_ideal_array = []
    memorys = []
    for i in range(order_start, order_stop+1):
        orders.append(i)
        order_array.append([])
        k_ideal_array.append([])
        memorys.append([0]*i)
    
    k_start = 7
    k_stop = 16
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
    order = 32
    memory = [0] * order
    LPC_predictor = LPC(order)
    cof_array = []
    m_array = []
    sign = True


if test == 21:
    inputs = []
    code_words = []
    uncoded_words = []
    order = 8
    memory = [0] * order
    LPC_predictor = LPC(order)
    cof_array = []
    k_array = []
    sign = True

   
if test == 15:
    uncoded_words = []
    m_start = 30
    m_stop = 70
    m_array = []
    order_0_array = []
    order_1_array = []
    order_2_array = []
    order_3_array = []
    for i in range(m_start, m_stop+1):
        m_array.append(i*1000)
        order_0_array.append([])
        order_1_array.append([])
        order_2_array.append([])
        order_3_array.append([])


if test == 14:
    inputs = []
    code_words = []
    uncoded_words = []
    order = 2
    memory = memorys[order].copy()
    Shorten_predictor = Shorten(order)
    m_array = []
    sign = True


if test == 13:
    uncoded_words = []
    k_ideal_array = [[],[],[],[]]
    k_start = 8
    k_stop = 16
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
    order = 2
    memory = memorys[order].copy()
    Shorten_predictor = Shorten(order)
    k_array = []
    sign = True


if test == 4:
    sign = True
    code_words_r = []
    code_words_g = []
    uncoded_words_32 = []
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

    if test == 31:
        testInput = current_data[best_mic,:]#Input data used in test

        
        Current_Encoded_inputs, Current_k_value, Current_Encoding_choice, testMemory, Current_LPC_Cofficents = FLAC_prediction.In(testInput, testMemory)
        
        Encoded_inputs.append(Current_Encoded_inputs)
        k_value.append(Current_k_value)
        Encoding_choice.append(Current_Encoding_choice)
        AllMemorys.append(testMemory)
        LPC_Cofficents.append(Current_LPC_Cofficents)
        AllTestInputs.append(testInput)

        
    if test == 25:
    

        input = current_data[silent_mic_2,:]#Input data used in test

        
        #loops though all k values in k_array.

        for j in range(len(m_array)):
            m = m_array[j]

            #loops thorugh all order, i = 0-3
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
        #Assuming each vaule is repsented in 32 bits.
        uncoded_word = ""              
        for j in range(len(input)):
            uncoded_word += np.binary_repr(input[j],32)



        #Saves uncoded binary input in array
        uncoded_words.append(uncoded_word)


    if test == 24:
        input = current_data[best_mic,:]#Input data used in test

        
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
        #Assuming each vaule is repsented in 32 bits.
        uncoded_word = ""              
        for j in range(len(input)):
            uncoded_word += np.binary_repr(input[j],32)



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
        #Assuming each vaule is repsented in 32 bits.
        uncoded_word = ""              
        for j in range(len(input)):
            uncoded_word += np.binary_repr(input[j],32)



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
        input = current_data[best_mic,:]#Input data used in test

            
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
        #Assuming each vaule is repsented in 32 bits.
        uncoded_word = ""              
        for j in range(len(input)):
            uncoded_word += np.binary_repr(input[j],32)

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
        uncoded_word_32 = ""
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
            uncoded_word_32 += np.binary_repr(input[i],32)

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
        uncoded_words_32.append(uncoded_word_32)
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
            plot_title = "Shorten order " + str(current_encoding_Value - 5)#Later used for plotting


        #Decompress to get original inputs
        Current_LPC_Cofficents = LPC_Cofficents[i]
        Current_decoded_Inputs, OutMemory = FLAC_prediction.Out(Encoded_inputs[i], OutMemory, k_value[i], Encoding_choice[i], Current_LPC_Cofficents[current_encoding_Value - 6])
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

        
        if 0 < 1:
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


    


    
    #find the m-value that gives the best compression rate for each order of LPC
    m_best = []
    cr_best = []
    for q in range(len(orders)):
        temp_best_cr = cr[q][0]
        temp_best_m = m_array[0]
        for i in range(len(m_array)-1):
            if cr[q][i+1] < temp_best_cr:
                temp_best_cr = cr[q][i+1]
                temp_best_m = m_array[i+1]

        m_best.append(temp_best_m)
        cr_best.append(temp_best_cr)
    
    for i in range(len(orders)):
        print("LPC order ",orders[i],"have best cr at m = ",m_best[i],"with cr = ",cr_best[i])


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

    
    if 1 < 0:#only for plots in report

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


        if 1 > 0:#Only plots for report


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

        


        if 1 < 0:#Only plots for report

            if i == 1:#Only want to display on plot

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
    if 1 > 0:
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
        for j in range(len(temp_min_cr_array)-1):
            
            #if the next k gives a better cr that k-value is saved
            if temp_min_cr_array[j+1] < temp_min_cr_array[temp_m_min]:
                
                temp_m_min = j+1
                
        #prints out the shorten order and its ideal k with the corresponding cr
        print("Shorten order ",i," and m = ", m_array[temp_m_min]," gives best result with cr = ", temp_min_cr_array[temp_m_min])

    print("")

    


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


        if 1 < 0:#Only plots for report


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

        

        if 1 < 0:#Only plots for report


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
    print("32 bit: ", len(uncoded_words_32[0]))
    print("Smal bit: ", len(uncoded_words_smal[0]))

    

    for i in range(len(code_words_r)):
        cr_r.append(len(code_words_r[i])/len(uncoded_words_32[i]))
        cr_g.append(len(code_words_g[i])/len(uncoded_words_32[i]))

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

    #This if statment only plots some graphs deemed interesting in the report
    if 1 < 0:

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


