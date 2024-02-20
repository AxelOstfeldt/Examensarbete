import numpy as np
import statsmodels.tsa.api as smt
#smt.acf(in)[:lag] autocorelation return as array, in = inputs, lag = how many lags back the array will go
import random
from Shorten import Shorten
from LPC import LPC




if 1 > 0:

    order_S = 3
    order_L = 5

    Shorten_predictor = Shorten(order_S)
    LPC_predictor = LPC(order_L)

    MAS = []
    MAL = []

    

    for q in range(10):
        mem_s = [0]*order_S
        mem_l = [0]*order_L
        input = []
        x = 1
        for i in range(10):
            leng = random.randint(20,30)
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

    print("Mean square error Shorten = ", MAS)

    print("Mean square error LPC = ", MAL)




