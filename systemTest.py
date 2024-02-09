from lib.beamformer import *
import config as config
import numpy as np
import math
from Shorten import Shorten
import matplotlib.pyplot as plt





connect()

NORM_FACTOR = 16777216

#for Shorten
order = 3
memory = [0] * 3
input = 0

plot_sig = []
test = 2
best_mic = 0





#Grabs one package from the sound file
#Each packet contains 256 smples from all 256 microphones
data = np.empty((config.N_MICROPHONES, config.N_SAMPLES), dtype=np.float32)
while len(plot_sig) < 256:
    
    receive(data)

    #Multyply by NORM_FACTOR to remove decimals
    data2 = data * NORM_FACTOR


    #convert data into integer
    data2 = data2.astype(int)
    #print(data2)
#    for i in range(256):
    



   

    if test == 0:
        if np.any(data2[:,1]) != 0:
            input = data2[:,1]
            for i in range(255):
                
                value = input[i]
                print(value)
                if value < 50000 and value > -50000 and value != 0:
                    plot_sig.append(input[i])
                    print("i = ", i)
                    print("len = ",len(plot_sig))


    if test == 3:
        if np.all(data2[1,:]) != np.all(input):
                input = data2[1,:]
                print(len(plot_sig))
                for i in range(256):
                    plot_sig.append(input[i])

    if test == 2:
        if np.all(data2[best_mic,:]) != np.all(input):
            input = data2[best_mic,:]
            
            for i in range(256):
                value = input[i]
                print(len(plot_sig))
                plot_sig.append(value)

            

    #print(input)       
    #print(data2[216,:])

    #Pick a micrphone by giving left argument, and sample by giving right arbument
    #To pick all sampels for a specific mic choose a number x for desired mic and ":" for samples:
    #data2[x,:]
    if test == 1:
        if np.all(data2[best_mic,:]) != np.all(input):
            input = data2[best_mic,:]

            

            residuals, memory, predictions = Shorten(input, order, memory)

            for i in range(256):
                if i > 252:
                    print(i)
                    print("Data", data2[1,i])
                    print("Prediction: ",predictions[i])
                    print("Residual: ",residuals[i])
                    print("Memory: ",memory)
                plot_sig.append(residuals[i])

            abs_res = np.absolute(residuals)
            abs_res_avg = np.mean(abs_res)
            #print(data2[1,:])
            #print("Mean value of residuals: ", np.mean(residuals))
            print("Variance of absolute residuals: ", np.var(abs_res))
            print("Mean value of absolute residuals: ", abs_res_avg)
            print("Largest residual: ", np.max(abs_res))

            if abs_res_avg > 0:
                k = math.log(math.log(2,10) * abs_res_avg,2)

                print("Rice constant, k = ",k)
                
            #print("Residuals: ",residuals)
            #print("Memory: ",memory)

            

            

print("While done")
plot_t = np.arange(len(plot_sig))

if len(plot_t) == len(plot_sig):
    print("Rätt längd")
else:
    print("fel längd")

plt.plot(plot_sig)
plt.show()

plt.plot(plot_sig)
plt.show()