from lib.beamformer import *
import config as config
import numpy as np
import math
from Shorten import Shorten
from Rice import RiceCoding
import matplotlib.pyplot as plt






connect()

NORM_FACTOR = 16777216

#for Shorten
order = 3

memorys = [[],[0],[0,0],[0,0,0]]
memory = memorys[order]

input = 0
inputs = []
k_array = []

w_limit = 0

plot_sig = []

code_words = []

uncoded_words = []

code_words_len = []

code_words_order = [[],[],[],[]]




test = 10

if test == 10:
    k_ideal_array = [[],[],[],[]]
    k_array = [4,5,6,7,8,9,10,11,12,13,14,15,16]
    order_0_array = []
    order_1_array = []
    order_2_array = []
    order_3_array = []
    for i in range(len(k_array)):
        order_0_array.append([])
        order_1_array.append([])
        order_2_array.append([])
        order_3_array.append([])




#From looking at the plots in test 2
best_mic = 79

residuals = []


#Grabs one package from the sound file
#Each packet contains 256 smples from all 256 microphones
data = np.empty((config.N_MICROPHONES, config.N_SAMPLES), dtype=np.float32)
while w_limit < 10:
    
    receive(data)

    #Multyply by NORM_FACTOR to remove decimals
    data2 = data * NORM_FACTOR


    #convert data into integer
    data2 = data2.astype(int)
    
    #Pick a micrphone by giving left argument, and sample by giving right arbument
    #To pick all sampels for a specific mic choose a number x for desired mic and ":" for samples:
    #data2[x,:]
    
    #This test tries different k-values for all orders of shorten over several data points.
    #With this it is possible to see:
    #1. What order and k-value gives best cr result.
    #2. What k-value for each order give best cr result.
    #3. How well does the ideal k-value in Rice theory match the practical ideal k-value

    if test == 10:
        #Only starts calculations when a new sample block is available
        if np.all(data2[best_mic,:]) != np.all(input):
            input = data2[best_mic,:]
            
            #loops though all k values in k_array.

            for j in range(len(k_array)):
                k = k_array[j]

                #loops thorugh all order, i = 0-3
                for i in range(4):
                    #Does the shorten calculations and updates memory
                    residual, memorys[i], predict = Shorten(input, i, memorys[i])

                    #Calculates the ideal k_vaule for the Shorten residuals
                    abs_res = np.absolute(residual)
                    abs_res_avg = np.mean(abs_res)
                    if abs_res_avg > 0:
                        k_ideal = math.log(math.log(2,10) * abs_res_avg,2)
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
            
            w_limit += 1





            
            
            





    if test == 9:
        if np.all(data2[best_mic,:]) != np.all(input):
            input = data2[best_mic,:]
            
            uncoded_word = ""
            for j in range(len(input)):
                uncoded_word += np.binary_repr(input[j],32)
            code_words_order[0].append(uncoded_word)



            for i in range(1,4):
                order = i
                residual, memory, predict = Shorten(input, order, memorys[i])
                memorys[i] = memory

                abs_res = np.absolute(residual)
                abs_res_avg = np.mean(abs_res)
                if abs_res_avg > 0:
                    k = int(math.log(math.log(2,10) * abs_res_avg,2))
                else:
                    k = 1


                code_word =""
                for j in range(len(input)):
                    Rice_coder = RiceCoding(k, True)
                    n = int(residual[j])
                    kodOrd = Rice_coder.Encode(n)
                    code_word += kodOrd
                code_words_order[i].append(code_word)


    if test == 8:
        if np.all(data2[best_mic,:]) != np.all(input):
            input = data2[best_mic,:]
            code_word =""
            uncoded_word = ""

            residuals, memory, predictions = Shorten(input, order, memory)
            abs_res = np.absolute(residuals)
            abs_res_avg = np.mean(abs_res)
            if abs_res_avg > 0:
                k = int(math.log(math.log(2,10) * abs_res_avg,2))
            else:
                k = 1



            for i in range(len(residuals)):
                Rice_coder = RiceCoding(k, True)
                n = int(residuals[i])
                kodOrd = Rice_coder.Encode(n)
                code_word += kodOrd

                uncoded_word += np.binary_repr(input[i],32)

            code_words.append(code_word)
            uncoded_words.append(uncoded_word)


    if test == 7:
        if np.all(data2[best_mic,:]) != np.all(input):
            input = data2[best_mic,:]
            code_word_len = []

            for i in range(len(input)):
                n = input[i]
                s = "0"
                if n < 0:
                    s = "1"
                    n = -n
                
                n = int(n)
                kodOrd = s + bin(n)[2:]
                if len(kodOrd) > 16:
                    print("Uncoded word have: ", kodOrd, " have length: ", len(kodOrd))
                
                code_word_len.append(len(kodOrd))
            code_words_len.append(code_word_len)


    if test == 6:
        if np.all(data2[best_mic,:]) != np.all(input):
            input = data2[best_mic,:]
            code_word = []


            residuals, memory, predictions = Shorten(input, order, memory)
            abs_res = np.absolute(residuals)
            abs_res_avg = np.mean(abs_res)
            if abs_res_avg > 0:
                k = int(math.log(math.log(2,10) * abs_res_avg,2))
            else:
                k = 1

                print("Rice constant, k = ",k)

            for i in range(len(residuals)):
                Rice_coder = RiceCoding(k, True)
                n = int(residuals[i])
                kodOrd = Rice_coder.Encode(n)
                code_word.append(kodOrd)

            code_words_len.append(code_word)


    if test == 5:
        if np.all(data2[best_mic,:]) != np.all(input):
            input = data2[best_mic,:]
            temp_residuals = []
            for i in range(1,4):
                order = i
                residual, memory, predict = Shorten(input, order, memorys[i-1])
                memorys[i-1] = memory
                temp_residuals.append(residual)
            residuals.append(temp_residuals)


    if test == 4:
        if np.all(data2[best_mic,:]) != np.all(input):
            input = data2[best_mic,:]
            
            print(memorys)
            for i in range(1,4):
                order = i
                residual, memory, predict = Shorten(input, order, memorys[i-1])
                memorys[i-1] = memory
                residuals.append(residual)


    if test == 3:
        if np.all(data2[best_mic,:]) != np.all(input):
            input = data2[best_mic,:]
            plot_residual = []
            plot_predict = []
            plot_zero = []

            for j in range(2):
                plot_sig_temp = []

                for i in range(55*j, 55*(j+1)):
                    plot_sig_temp.append(input[i])

                print(memory)
                residual, memory, predict = Shorten(plot_sig_temp, order, memory)
                plot_sig.append(plot_sig_temp)
                plot_residual.append(residual)
                plot_predict.append(predict)
                plot_zero_temp = []

                for i in range(len(plot_sig_temp)):
                    temp_value = plot_sig_temp[i] - ( predict[i] + residual[i] )
                    plot_zero_temp.append(temp_value)

                plot_zero.append(plot_zero_temp)


    if test == 2:
        if np.all(data2[0,:]) != np.all(input):
            print("Test start")
            input = data[0,:]
            
            for j in range(256):
            
                input_temp = data2[j,:]
                plot_sig_temp = []
                for i in range(256):
                    value = input_temp[i]
                    #print(len(plot_sig))
                    plot_sig_temp.append(value)
                plot_sig.append(plot_sig_temp)
                    
    
    if test == 1:
        if np.all(data2[best_mic,:]) != np.all(input):
            input = data2[best_mic,:]
            code_word =""
            uncoded_word = ""
            inputs.append(input)
            

            residuals, memory, predictions = Shorten(input, order, memory)
            abs_res = np.absolute(residuals)
            abs_res_avg = np.mean(abs_res)
            if abs_res_avg > 0:
                k = int(math.log(math.log(2,10) * abs_res_avg,2))
            else:
                k = 1

            k_array.append(k)

            for i in range(len(residuals)):
                Rice_coder = RiceCoding(k, True)
                n = int(residuals[i])
                kodOrd = Rice_coder.Encode(n)
                code_word += kodOrd

                uncoded_word += np.binary_repr(input[i],32)

            code_words.append(code_word)
            uncoded_words.append(uncoded_word)



#disconect()


#Test compression ratios for all orders of Shorten for some k-values
if test == 10:
    print("Test 10")
    
    
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
    print("Shorten order 0 with k = ", int(round(k_ideal_avg_array[0])), " gives cr = ", cr_0[int(round(k_ideal_avg_array[0])) - k_array[0]])

    print("Shorten order 1 with k = ", int(round(k_ideal_avg_array[1])), " gives cr = ", cr_1[int(round(k_ideal_avg_array[1])) - k_array[0]])

    print("Shorten order 2 with k = ", int(round(k_ideal_avg_array[2])), " gives cr = ", cr_2[int(round(k_ideal_avg_array[2])) - k_array[0]])

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
            #if the next k gives a better cr that k-value is saved
            if temp_min_cr_array[j+1] < temp_min_cr_array[j]:
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


    #Plots sub plots with each subplot being a specific order of Shorten
    #y-axis is compression ratio and x-axis is k value
    #This plot is a zoomed in version of figure 1.
    #The first data points are ususaly not that interesting since compression ratio is high
    #(Assuming starting k-value of 4)
    fig = plt.figure(2)

    ax=fig.add_subplot(221)
    plt.plot(k_array[3:], cr_0[3:], 'ro')
    ax.title.set_text("Shorten Order 0")
    plt.xlabel("k-value")
    plt.ylabel("Average compression ratio")

    ax=fig.add_subplot(222)
    plt.plot(k_array[3:], cr_1[3:], 'ro')
    ax.title.set_text("Shorten Order 1")
    plt.xlabel("k-value")
    plt.ylabel("Average compression ratio")

    ax=fig.add_subplot(223)
    plt.plot(k_array[3:], cr_2[3:], 'ro')
    ax.title.set_text("Shorten Order 2")
    plt.xlabel("k-value")
    plt.ylabel("Average compression ratio")

    ax=fig.add_subplot(224)
    plt.plot(k_array[3:], cr_3[3:], 'ro')
    ax.title.set_text("Shorten Order 3")
    plt.xlabel("k-value")
    plt.ylabel("Average compression ratio")

    #Plots Order 1, 2, and 3 of shorten in the same plot for some k-values
    plt.figure(3)

    plt.plot(k_array[3:], cr_1[3:], 'ro', label='Order 1')
    plt.plot(k_array[3:], cr_2[3:], 'bo', label='Order 2')
    plt.plot(k_array[3:], cr_3[3:], 'go', label='Order 3')
    plt.title("Comparison of comression ratio for differente orders")
    plt.xlabel("k-value")
    plt.ylabel("Average compression ratio")
    plt.legend()

    plt.show()


  





    

    


    




    




#Test to find which order of shorten gives the best compression ratio
if test == 9:
    compression_ratios = [[],[],[]]
    uncoded_words = code_words_order[0]
    for i in range(1,4):
        code_words = code_words_order[i]
        for j in range(len(code_words)):
            temp_comp_ratio = len(code_words[j]) / len(uncoded_words[j])
            compression_ratios[i-1].append(temp_comp_ratio)

        print("Shorten order ", i," gives an average compression ratio: cr = ", sum(compression_ratios[i-1]) / len(compression_ratios[i-1]))



#Test the compression ratio of Shorten (Assuming original data values are encoded in 32 bits)
if test == 8:
    compression_ratio = []
    for i in range(len(code_words)):
        temp_comp_r = len(code_words[i]) / len(uncoded_words[i])
        compression_ratio.append(temp_comp_r)
    print("Compression ratio of Shorten are: ", compression_ratio)
    print("Average compression ratio over several itterations is: ", sum(compression_ratio)/len(compression_ratio))



#Test average length of binary representation for input data and the largest bit representation of input data
if test == 7:
    avg_len = []
    max_len = []
    for i in range(len(code_words_len)):
        code_word_len = code_words_len[i]
        sum_len = sum(code_word_len)
        temp_max = np.max(code_word_len)

        avg_len.append(sum_len / len(code_word_len))
        max_len.append(temp_max)

    print("Average length of uncoded words: ", avg_len)
    print("Max length of uncoded words: ", max_len)


#Test average length of code words
if test == 6:
    avg_len = []
    for i in range(len(code_words)):
        code_word = code_words[i]
        sum_len = 0
        for j in range(len(code_word)):
            sum_len += len(code_word[j])
        avg_len.append(sum_len / len(code_word))

    print("Average length of code words: ", avg_len)



#Test which Shorten order that gives the best mean and varriance
if test == 5:
    best_mean = []
    best_var = []
    best_mean_value = []
    best_var_value = []
    current_best_mean = 0
    current_best_var = 0
    order_mean = 0
    order_var = 0
    for i in range(len(residuals)):
        temp_residuals = residuals[i]
        for j in range(len(temp_residuals)):
            abs_res = np.absolute(temp_residuals[j])
            abs_res_mean = np.mean(abs_res)
            abs_res_var = np.var(abs_res)

            if j == 0:
                current_best_mean = abs_res_mean
                current_best_var = abs_res_var
                order_mean = j+1
                order_var = j+1
            else:
                if abs_res_mean < current_best_mean:
                    current_best_mean = abs_res_mean
                    current_best_var = abs_res_var
                    order_mean = j+1
                if abs_res_var < current_best_var:
                    current_best_var = abs_res_var
                    order_var = j+1
        best_mean.append(order_mean)
        best_var.append(order_var)
        

    

    print("Order for best mean: ", best_mean)
    
    print("Order for best var: ", best_var)





#Plot residuals of different orders to find which order gives the best residuals
if test == 4:
    print("Hello world")
    for i in range(int(len(residuals)/3)):
        fig = plt.figure(i)
        for j in range(3):
            sub_nr = j+1
            ax = fig.add_subplot(220+sub_nr)
            plt.plot(residuals[j + i*3])
            order_title = "Order " + str(j+1)
            ax.title.set_text(order_title)

            abs_res = np.absolute(residuals[j + i*3])
            abs_res_avg = np.mean(abs_res)
            print("Variance of absolute residual[",j+i*3,"]: (Order",1+j,") ", np.var(abs_res))
            print("Mean value of absolute residual[",j+i*3,"]: (Order",1+j,") ", abs_res_avg)
            print("Largest residual[",j+i*3,"]: (Order",1+j,") ", np.max(abs_res))



    plt.show()




        



#Plot input signal, residual, predicted value to see how good the result of shorten is
if test == 3:
    for i in range(len(plot_sig)):
        fig = plt.figure(i)

        ax = fig.add_subplot(221)
        plt.plot(plot_sig[i])
        ax.title.set_text("Input signal")

        ax = fig.add_subplot(222)
        plt.plot(plot_predict[i])
        ax.title.set_text("Predicted signal")

        ax = fig.add_subplot(223)
        plt.plot(plot_residual[i])
        ax.title.set_text("Residual signal")

        ax = fig.add_subplot(224)
        plt.plot(plot_zero[i])
        ax.title.set_text("Input - (Predict + Residual) = 0")

        abs_res = np.absolute(plot_residual[i])
        abs_res_avg = np.mean(abs_res)
        print("Variance of absolute residual[",i,"]: ", np.var(abs_res))
        print("Mean value of absolute residual[",i,"]: ", abs_res_avg)
        print("Largest residual[",i,"]: ", np.max(abs_res))


    plt.show()








#Plot all mics to find which ones have good recorded values
if test == 2:
    plot_nr = 1
    for i in range(256):
        fig = plt.figure(plot_nr)
        sub_nr =(i%4 + 1)

        ax = fig.add_subplot(220+sub_nr)
        plt.plot(plot_sig[i])
        mic_title = "Mic #" + str(i)
        ax.title.set_text(mic_title)
        



        if i % 4 == 3:
         
            plot_nr +=1
            plt.show()
        


if test == 1:
    compression_ratio = []
    uncoded_values = []
    sign = True
    for i in range(len(code_words)):
        temp_comp_r = len(code_words[i]) / len(uncoded_words[i])
        compression_ratio.append(temp_comp_r)
    print("Compression ratio of Shorten are: ", compression_ratio)

    for i in range(len(inputs)):
        input = inputs[i]
        k = k_array[i]
        code_word = code_words[i]
        Rice_coder = RiceCoding(k, sign)
        values = Rice_coder.Decode(code_word)
        uncoded_values.append(values)

        for j in range(len(values)):
            if values[j] != input[j]:
                print("For sample ",i," value #",j," the values does not match. Input = ", input[j]," decoded value = ",values[j])
            else:
                print("Input = ", input[j])
                print("Decoded value = ", values[j])





