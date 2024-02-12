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
order = 2
memory = [0] * order
memorys = [[0],[0,0],[0,0,0]]
input = 0

plot_sig = []
code_words = []
uncoded_words = []
code_words_len = []
code_words_order = [[],[],[],[]]




test = 9

#From looking at the plots in test 2
best_mic = 79

residuals = []

print("Hello")

#Grabs one package from the sound file
#Each packet contains 256 smples from all 256 microphones
data = np.empty((config.N_MICROPHONES, config.N_SAMPLES), dtype=np.float32)
while len(code_words_order[0]) < 20:
    
    receive(data)

    #Multyply by NORM_FACTOR to remove decimals
    data2 = data * NORM_FACTOR


    #convert data into integer
    data2 = data2.astype(int)
    
    #Pick a micrphone by giving left argument, and sample by giving right arbument
    #To pick all sampels for a specific mic choose a number x for desired mic and ":" for samples:
    #data2[x,:]
    

    if test == 9:
        if np.all(data2[best_mic,:]) != np.all(input):
            input = data2[best_mic,:]
            
            uncoded_word = ""
            for j in range(len(input)):
                uncoded_word += np.binary_repr(input[j],32)
            code_words_order[0].append(uncoded_word)



            for i in range(1,4):
                order = i
                residual, memory, predict = Shorten(input, order, memorys[i-1])
                memorys[i-1] = memory

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
                    

            

    #print(input)       
    #print(data2[216,:])

    
    if test == 1:
        if np.all(data2[best_mic,:]) != np.all(input):
            input = data2[best_mic,:]
            code_word =""
            uncoded_word = ""
            k_array = []

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
    for i in range(len(code_words)):
        temp_comp_r = len(code_words[i]) / len(uncoded_words[i])
        compression_ratio.append(temp_comp_r)
    print("Compression ratio of Shorten are: ", compression_ratio)


