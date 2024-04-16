import numpy as np
#import statsmodels.tsa.api as smt
#smt.acf(in)[:lag] autocorelation return as array, in = inputs, lag = how many lags back the array will go
import random
from Shorten import Shorten
from LPC import LPC
import math
from Rice import RiceCoding

if 1 < 0:
    Path = "C:\\Users\\axelo\\OneDrive\\Skrivbord\\Exjobb\\GIT\\SoundData\\"
    FileName = "1kHzTone.txt"
    FullDirectory = Path+FileName
    

    # Create an empty list to store loaded data
    loaded_data = []

    # Open the file containing all data, remember to set correct filename
    with open(FullDirectory, 'r') as file:
        array = []
        for line in file:
            # Check if the line is empty, indicating the end of an array
            if not line.strip():
                # Convert the collected lines into a NumPy array and append to loaded_data
                loaded_data.append(np.array(array, dtype=int))
                # Reset the array for the next set of lines
                array = []
            else:
                # Convert the line into integers and append to the array
                array.append([int(x) for x in line.split()])

    # Append the last array since there's no empty line after it
    if array:
        loaded_data.append(np.array(array, dtype=int))

    print("len loaded data = ",len(loaded_data))
    


    FirstDatablock = loaded_data[0]

    print("Shape FirstDatablock = ", FirstDatablock.shape)

    Array2 = FirstDatablock[64:128,:]

    print("SHape array2 = ",Array2.shape)

    FirstSample = Array2[:,0]

    print("FirstSample = ", len(FirstSample))

    #Creates txt file for first sample in array
    if 1 < 0:
        with open("FirstSampleBinary.txt", "w") as file:
            for value in FirstSample:
                BinaryValue = np.binary_repr(value, 24)
                file.write(str(BinaryValue) + "\n")



    

    

    




if 1 < 0:


    max_val = pow(2,23) - 1
    min_val = -1 * (max_val +1)
    zero_val = 0
    
    #This For loop is used to find limits for k-values, it goes from k = 8 to k = 22
    new_k = 7
    for i in range(425, 6966588):
        k = int(round(math.log(math.log(2,10) * i,2))) + 1
        if k > new_k:
            print("")
            print("")
            print("elsif TotalSum < ",i*256,"then --",i,"*256")
            print("k_val_int = ",new_k,";")
            new_k = k
            print("")
            print("")
            print("k = ", new_k)
            print("i = ", i)
            print("i * 256 (limit??) = ", i * 256)

            if k == 22:
                print("((i*256) + max_val) - max_val*256 = ", ((i*256) + max_val )- (max_val*256))

        



    if 1 > 0:

        

        for k in range(8, 23):
            summan = pow(2, k-1) * 256 / math.log10(2)

            print("summan = ", summan," ger k = ", k)

        

        #Calculates the ideal k-value according to Rice theory
        abs_res = np.absolute(max_val)
        abs_res_avg = np.mean(abs_res)
        
        #if abs_res_avg is less than 4.7 it would give a k value less than 1.
        #k needs tobe a int > 1 and therefore if abs_res_avg < 5 k is set to 1
        #OBS. 4.7 < abs_res_avg < 5 would be rounded of to k=1 so setting the limit to 5 works well
        if abs_res_avg > 5:
            k = int(round(math.log(math.log(2,10) * abs_res_avg,2)))
        else:
            k = 1

        print("Sugested k for this is, k = ", k)




        print("Max val: ", max_val)
        print("Min val: ", min_val)
        print("Zero val: ", zero_val)
        for k in range(5, 32):
            RiceEncoder = RiceCoding(k, True)
            max_kodord = RiceEncoder.Encode(max_val)

            min_kodord = RiceEncoder.Encode(min_val)

            zero_kodord = RiceEncoder.Encode(zero_val)

            print("k = ",k)
            print("len max value = ", len(max_kodord))
            print("len min value = ", len(min_kodord))
            print("len 0 value = ", len(zero_kodord))
            print("")
       

if 1 < 0:

    LPC_order = 2

    if LPC_order > 4:
        memory = [0] * LPC_order
    else:
        memory = [0] * 4

    print("Original memory = ", memory)

    Rle_output = [1,2,3,4]#,5,6,7,8,9,10,12,14,16,17,23,24,27]

    print("RLE values = ", Rle_output)

    copy_RLE = Rle_output.copy()

    if LPC_order > 4:
        if len(Rle_output) > LPC_order:
            memory = copy_RLE[len(Rle_output)-LPC_order:]
        else:
            memory = copy_RLE
            while len(memory) < LPC_order:
                memory.append(0)
    else:
        if len(Rle_output) > 4:
            memory = copy_RLE[len(copy_RLE)-4:]
        else:
            memory = copy_RLE
            while len(memory) < 4:
                memory.append(0)
        


    print("New memory = ", memory)





if 1 < 0:
    for_loop_cnt = 99


    test_RLE = [4,3,2,1,0]

    test_RLE = [for_loop_cnt] + test_RLE[:-1]

    print("test RLE ",test_RLE)


    test_float = 0.51

    print(round(test_float))

    test_short_array = ["Shorten order 0","Shorten order 1","Shorten order 2","Shorten order 3","Shorten order 4"]

    LPC_order = 8

    test_lpc_array = ["LPC order 1", "LPC order 2", "LPC order 3", "LPC order 4", "LPC order 5", "LPC order 6", "LPC order 7", "LPC order 8"]



    memory = ["Spot 1", "SPot 2", "Spot 3", "Spot 4"]#, "Spot 5", "Spot 6", "Spot 7", "Spot 8"]

    for i in range(len(memory)):
        if i <= 3:
            print(test_short_array[i+1])

    test_array = [1,2,3,4]

    test_1 = [1,0,1,0]

        

    short_cof = [[0],[1],[2, -1],[3, -3, 1],[4,-6,4,-1]]

    memory = [1,1,1,1,1,1]



    

    
#Compare Shorten and LPC
if 1 < 0:

    order_S = 2
    order_L = 25

    Shorten_predictor = Shorten(order_S)
    LPC_predictor = LPC(order_L)

    MAS = []
    MAL = []

    

    for q in range(100):
        mem_s = [0]*order_S
        mem_l = [0]*order_L
        input = []
        x = 1
        for i in range(4):
            leng = 64
            lut = random.randint(-5,5)
            x_start = x
            for j in range(leng):
                x = x_start + j * lut
                input.append(x)


        



        res_s, mem_s, pred_s = Shorten_predictor.In(input.copy(), mem_s)
        cof_l, res_l, mem_l, pred_l = LPC_predictor.In(input.copy(), mem_l)

        MSE_S = 0
        MSE_L = 0

        es = np.mean(res_s)
        el = np.mean(res_l)

        for i in range(len(res_l)):
            MSE_S += pow(res_s[i]-es, 2)
            MSE_L += pow(res_l[i]-el,2)

        MSE_S = MSE_S / len(res_s)

        MSE_L = MSE_L / len(res_l)

        MAS.append(MSE_S)
        MAL.append(MSE_L)

    print("AVG mean square error Shorten = ", sum(MAS)/len(MAS))

    print("AVG mean square error LPC = ", sum(MAL)/len(MAL))




