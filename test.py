import numpy as np
#import statsmodels.tsa.api as smt
#smt.acf(in)[:lag] autocorelation return as array, in = inputs, lag = how many lags back the array will go
import random
from Shorten import Shorten
from LPC import LPC


    
class LPC:

    def __init__(self, order):
        #Order have to be an integer of size 1 or larger for LPC
        #No upperlimit exist other than when the order is larger than the number of inputs the lag when caluclating autocorrelation will raise an error
        if  order < 0 or not isinstance(order, int):
            raise ValueError(f"Order can only have integer values larger than 0. Current value of is {order}")
        
        self.order = order


    #Function to calculate the autocorrelation of the input values
       #Function to calculate the autocorrelation of the input values
    def autocorrelation(self, x, lag):

        if lag >= len(x):
            raise ValueError(f"Lag must be shorter than array length")
        if not isinstance(lag, int) or lag < 0:
            raise ValueError(f"Lag must be an positive int")
        
 

        

        x_mean = np.mean(x)
        n = 0
        t = 0

            
        for i in range(len(x)):
            n += pow(x[i] - x_mean, 2)
            if i >= lag:
                t += (x[i] - x_mean) * (x[i-lag] - x_mean)


        #In the case where all x values are identical to each other the equation for autocorrelation dont work
        #This is beceause n will be equal to 0 and this can not be used to dicide t
        #In the case that all values are identical the autocorrelation should be =1 regardless of lag-value
        if n == 0:
            t = 1
            n = 1
            

                       

        return t/n


    #Calculates the coefficents for LPC using the Levinson-Durbin algorithm
    #The coefficents can be calculated with matrix multiplications
    #How ever it is faster to use this algorithm
    def Coefficents(self, inputs):

        if all(element == inputs[0] for element in inputs):
            a = [1] + [0] * (self.order - 1)

        else:
            E = self.autocorrelation(inputs, 0)
            a = []

            for i in range(self.order):

                k = self.autocorrelation(inputs, i+1)
                if i > 0:
                    for j in range(i):
                        k -= a[j] * self.autocorrelation(inputs, i-j)

                k = k / E
                a.append(k)

                if i > 0:
                    a_old = a.copy()
                    for j in range(i):
                        a[j] = a_old[j] - k * a_old[(i-1)-j]
                E = (1 - pow(k,2)) * E

        return a

if 1 > 0:
    order = 8
    input_1 = [2.0]*32
    input_2 = input_1.copy()
    input_1.append(2.00000000001)
    input_2.append(1)


    LPC_predictor = LPC(order)
    Test_output = LPC_predictor.Coefficents(input_1)
    #for i in range(5):
    #    Test_output = LPC_predictor.autocorrelation(input_3, i)

    print(Test_output)
    print("Test done")





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




