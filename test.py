import numpy as np
#import statsmodels.tsa.api as smt
#smt.acf(in)[:lag] autocorelation return as array, in = inputs, lag = how many lags back the array will go
import random
from Shorten import Shorten
from LPC import LPC


if 1 > 0:
    for i in range(1,5):
        shorten_order = i
        print("Shorten order ",i)
        memory = [1,2,3,4,5,6,7,8,9,10]
        testArray = np.array(memory[:shorten_order])
        print("TestArray = ",testArray)

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




