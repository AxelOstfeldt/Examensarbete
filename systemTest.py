from lib.beamformer import *
import config as config
import numpy as np
from Shorten import Shorten




connect()

NORM_FACTOR = 16777216

#for Shorten
order = 3
memory = [0] * 3


#Grabs one package from the sound file
#Each packet contains 256 smples from all 256 microphones
data = np.empty((config.N_MICROPHONES, config.N_SAMPLES), dtype=np.float32)
while True:
    receive(data)

    #Multyply by NORM_FACTOR to remove decimals
    data2 = data * NORM_FACTOR


    #convert data into integer
    data2 = data2.astype(int)

    #Pick a micrphone by giving left argument, and sample by giving right arbument
    #To pick all sampels for a specific mic choose a number x for desired mic and ":" for samples:
    #data2[x,:]

    input = data2[1,:]

    

    residuals, memory, predictions = Shorten(input, order, memory)

    
    print(data2[1,:])
    print("Predictions: ",predictions)
        
    #print("Residuals: ",residuals)
    #print("Memory: ",memory)

    #print(data2[1,:])

    

    