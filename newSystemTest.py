from lib.beamformer import *
import config as config
import numpy as np
import math
from Rice import RiceCoding
from Golomb import GolombCoding
from Shorten import Shorten
from LPC import LPC
#from Adjacant import Shorten_adjacent

import matplotlib.pyplot as plt
import time




connect()


#Some general inital values for testing
NORM_FACTOR = 16777216
input_new = 0#Used to check if new data is available
w_limit = 0#Is incremented in while loop until limit is reached
recomnded_limit = 10#Is the limit to reach in the while loop, set different at different tests
best_mic = 79#From looking at the plots in test 1
blasted_mic = 217#From looking at the plots in test 1, seems to have realy high values
silent_mic_1 = 20#From looking at the plots in test 1, allways 0
silent_mic_2 = 19#From looking at the plots in test 1, allways [-1, 0]

#Some inital values for Shorten
memorys = [[],[0],[0,0],[0,0,0]]


#Choose what test to do:
test = 0

#General tests
#Test 0. Saves all new input data in an array and return it outside read data loop
#Test 1. This test plots microphone data
#Test 2. This test checks average binary len and max length of input data if every data point was written with minimal amount of bits
#Test 3. Suposed to test how long time it takes to grab a new sample. 
#In theory it should be around 0.005 s, calculated from 256 samples at a sampling frequency of about 48 k Hz
#However this does not seem to hold because of other processes runing on the computer makeing it slower
#Test 4. Try Rice and Golom codes on original inputs

#Shorten tests
#Test 11. Test if Shorten using Rice code can correctly decode the input values
#Test 12. Plots results for differente orders of Shorten
#Test 13. This test tries different k-values in Rice codes for all orders of shorten over several data blocks.
#Test 14. Test if Shorten using Golomb code can correctly decode the input values
#Test 15. This test tries different m-values in Golomb codes for all orders of shorten. 
#Can be done over several data blocks in theory but computer dont seem to manage it 
#Test 16. Uses Shorten to predict values on adjacent mics

#LPC tests
#Test 21. Test if LPC using Rice code can correctly decode the input values
#Test 22. Test if LPC using Golomb code can correctly decode the input values
#Test 23. Test what order of LPC gives best result, also test how large of an order it is possible to try
#Test 24. Test what k-value gives the best compression rate when using LPC and Rice codes for different orders of LPC
#Test 25. Test what m-value gives the best compression rate when using LPC and Golomb codes for different order of LPC


#Initial values for tests
if test == 25:
    recomnded_limit = 3
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
    factorr = 60
    m_start = 3
    m_stop = 38
    m_array = []

    for i in range(m_start, m_stop+1):
        m_array.append(int(i*factorr))
        for j in range(len(order_array)):
            order_array[j].append([])


if test == 24:
    recomnded_limit = 10
    uncoded_words = []
    orders = []
    order_start = 8
    order_stop = 8
    order_array = []
    k_ideal_array = []
    memorys = []
    for i in range(order_start, order_stop+1):
        orders.append(i)
        order_array.append([])
        k_ideal_array.append([])
        memorys.append([0]*i)
    
    k_start = 13
    k_stop = 16
    k_array = []
    for i in range(k_start, k_stop+1):
        k_array.append(i)
        for j in range(len(order_array)):
            order_array[j].append([])

   
if test == 23:
    recomnded_limit = 1
    
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
    recomnded_limit = 10#Limit not tested over 10 with order 32
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
    recomnded_limit = 10#Limit not tested over 10 with order 32
    inputs = []
    code_words = []
    uncoded_words = []
    order = 8
    memory = [0] * order
    LPC_predictor = LPC(order)
    cof_array = []
    k_array = []
    sign = True


if test == 16:
    #The mics to use are based on what mics gives good values.
    #The starting mic is mic 83, the 4 following mics are next to startin mic, the 4 following after that is diagonaly next from starting mic
    mics = [83, 84, 82, 91, 75, 93, 90, 76, 74]

    recomnded_limit = 1

   
if test == 15:
    recomnded_limit = 1
    uncoded_words = []
    m_start = 30000
    m_stop = 70000
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
    recomnded_limit = 2#Should not go over 23
    inputs = []
    code_words = []
    uncoded_words = []
    order = 2
    memory = memorys[order].copy()
    Shorten_predictor = Shorten(order)
    m_array = []
    sign = True


if test == 13:
    recomnded_limit = 15#15 is good value if k_start and k_stop are choosen well
    uncoded_words = []
    k_ideal_array = [[],[],[],[]]
    k_start = 10
    k_stop = 20
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
    recomnded_limit = 1
    
    data_points = 256#How many samples for each block is gonna be plotted, lower value gives a more zoomed in picture.
    #Can only be changed if recomdended limit = 1
    
    plot_residuals = [[],[],[],[]]
    plot_predict = [[],[],[],[]]
    plot_sig = []
    plot_zero = [[],[],[],[]]


if test == 11:
    recomnded_limit = 2#Should not go over 23
    inputs = []
    code_words = []
    uncoded_words = []
    order = 2
    memory = memorys[order].copy()
    Shorten_predictor = Shorten(order)
    k_array = []
    sign = True


if test == 4:
    recomnded_limit = 15
    sign = True
    code_words_r = []
    code_words_g = []
    uncoded_words_32 = []
    uncoded_words_smal = []
    uncoded_smal_max_array = []


if test == 3:
    loop_time = []
    recomnded_limit = 10


if test == 2:
    code_words_len = []
    recomnded_limit = 10



if test == 1:
    recomnded_limit = 1
    plot_sig = []
    data_points = 256#How many samples for each block is gonna be plotted, lower value gives a more zoomed in picture



#Grabs one package from the sound file
#Each packet contains 256 smples from all 256 microphones

#The data from the while loop is appended in the test_data array
#It loops recomended_limit amount of time, this depends on the size of the sound file
#23 was found to be a good number to use
recomnded_limit = 23
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
        print(w_limit)
        test_data.append(data2)
    
    

    
    #Pick a micrphone by giving left argument, and sample by giving right arbument
    #To pick all sampels for a specific mic choose a number x for desired mic and ":" for samples:
    #data2[x,:]


print("len inputs: ", len(test_data))
temp_input = test_data[0]
print("dimension of each input is: ", len(temp_input[0,:]),"by ",len(temp_input[:,0]))

temp_input = test_data[0]

plt.plot(temp_input[best_mic,:])
plt.show()
