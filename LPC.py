import numpy as np



class LPC:

    def __init__(self, order):
        #Order have to be an integer of size 1 or larger for LPC
        #No upperlimit exist other than when the order is larger than the number of inputs the lag when caluclating autocorrelation will raise an error
        if  order < 0 or not isinstance(order, int):
            raise ValueError(f"Order can only have integer values larger than 0. Current value of is {order}")
        
        self.order = order


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
            if lag == 0:
                t = 1
            else:
                t = 0
            
            n = 1
            

                       

        return t/n


    #Calculates the coefficents for LPC using the Levinson-Durbin algorithm
    #The coefficents can be calculated with matrix multiplications
    #How ever it is faster to use this algorithm
    def Coefficents(self, inputs):

        #If all inputs are constant a division by 0 error will occur
        #To handle this this if statement is created.
        #Since all values are exactly the same it is enough to predict the next value with the previous value
        #hence the first cofficent is a 1 and the rest are 0
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


    #Calculates the prediction of the current value using the cofficents and earlier values
    def prediciton(self, memory, coef):
        prediction = 0

        for j in reversed(range(1, self.order)):
            prediction += coef[j] * memory[j]
            memory[j] = memory[j-1]#updates the memory with the earlier values taking one step in the memory array

        prediction += coef[0] * memory[0]

        return prediction, memory
    
    

    def In(self, inputs, memory):

        coef = self.Coefficents(inputs)

        residuals = []
        predictions = []

        for i in range(len(inputs)):
            predict, memory = self.prediciton(memory, coef)

            memory[0] = inputs[i]#Updates the first slot in the memory array with the current value
            residual = inputs[i] - predict#caltulcates the residual
            residual = round(residual)#Since Rice and Golomb codes need to have interger the residual is rounded to closest int


            #Append current prediction and residual in array to returned
            residuals.append(residual)
            predictions.append(predict)

        return coef, residuals, memory, predictions

        
        
    def Out(self, coef, residuals, memory):
        predictions = []
        inputs = []

        for i in range(len(residuals)):
            predict, memory = self.prediciton(memory, coef)

            #Recreates the current input
            #This maybe should also use round as in LPC.In
            #since the values in this project to be recreated always are int
            input = residuals[i] + predict

            memory[0] = input#Uppdates the first memory slot with the recreated input


            #Appends the current prediction and recrated input in arrays to be returned
            predictions.append(predict)
            inputs.append(input)

        return inputs, memory, predictions



#Tests

#Test contant input array for LPC
    
if 1 > 0:
    order = 3
    input_1 = [2]*32
    input_2 = input_1.copy()
    input_1.append(2)
    input_2.append(1)
    input_3 = [1, 2, 3, 4, 5]

    LPC_predictor = LPC(order)
    Test_output = LPC_predictor.Coefficents(input_3)
    for i in range(len(input_3)):
        Test_output = LPC_predictor.autocorrelation(input_3, i)

        print(Test_output)
    print("Test done")




#Testing that LPC works correctly
#It can create residuals that are integers
#It can recreate the original inputs, but with some rounding errors
if 1 < 0:
    
    order = 3
    inputs = [1,2,3,4,5,6,7,8,9,9,9,10,11,12,5,4,3,2,1,0]
    LPC_predictor = LPC(order)
    mem = [0]*order

    cof_l, res_l, mem_l, pred_l = LPC_predictor.In(inputs, mem.copy())


    print("Coefficents: ", cof_l)
    print("Residuals: ",res_l)
    print("Memory in: ",mem_l)
    print("Predicitons in: ", pred_l)

    input_o, mem_o, pred_o =LPC_predictor.Out(cof_l, res_l, mem.copy())
    print("Original inputs: ", inputs)
    print("Recreated inputs: ",input_o)
    print("Memory out: ",mem_o)
    print("Predicitons out: ", pred_o)




#Test to compare matrix multiplication with function
#works correctly
if 1 < 0:
    #need import:
    import statsmodels.tsa.api as smt
    order = 5
    inputs = [1,2.9,4.4,6.6,8.7,11.5,13,16,19]
    R = smt.acf(inputs)

    array_RS = []
    for i in range(order):
        temp_array = []
        for j in range(order):
            r_val = abs(i-j)
            temp_array.append(R[r_val])
        array_RS.append(temp_array)

    #Should go up to order-1
    RM = np.array([array_RS[0],
                   array_RS[1],
                   array_RS[2],
                   array_RS[3],
                   array_RS[4]])
    
    RMI = np.linalg.inv(RM)
    
    #should go up to order
    RV = np.array([R[1],
                   R[2],
                   R[3],
                   R[4],
                   R[5]])
    

    cof = np.matmul(RMI,RV)
    print("Coeficents from matrix multiplication: ",cof)

    LPC_predictor = LPC(order)
    mem_l = [0]*order

    cof_l, res_l, mem_l, pred_l = LPC_predictor.In(inputs, mem_l)

    print("Coeficents from function: ", cof_l)
