import numpy as np

 #Function to calculate the autocorrelation of the input values
def autocorrelation(x, lag):

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
def prediciton_LPC(self, memory, coef):
    prediction = 0

    for j in reversed(range(1, self.order)):
        prediction += coef[j] * memory[j]
        memory[j] = memory[j-1]#updates the memory with the earlier values taking one step in the memory array

    prediction += coef[0] * memory[0]

    return prediction, memory



def In_LPC(self, inputs, memory):

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



 def predict_shorten(self, memory):
        prediction = 0

        if self.order > 1:
            #this forloop is reversed so that memory values needed are not overwritten when values are shuffled one index back
            for j in reversed(range(1, self.order)):
                prediction = prediction + self.coeficents[j] * memory[j]
                memory[j] = memory[j-1]

            prediction = prediction + self.coeficents[0] * memory[0]

        elif self.order == 1:
            #in case of order 1 the current prediction is the last input
            prediction = memory[0]

        elif self.order == 0:
            #in case of order zero the prediciton is allways zero.
            #in this case the full current value is sent as residual
            prediction = 0

        else:
            raise ValueError(f"Order can only have integer values between 0 and 3. Current value of is {self.order}")
        return prediction, memory


def In_SHorten(self, input, memory: list = [0] * 3):


    
    
    #raises error if memory is not the length of order
    if self.order != len(memory):
        raise ValueError(f"Order and memory length should match. Current values are: order = {order}, memory length = {len(memory)}")
    
    predictions = []#only needed for testing?
    residuals = []
    

    
    #loops through the input array 
    for i in range(len(input)):
        prediction, memory = self.predict(memory)


        #calculates residual by taking the current value and subtract the predicted value
        residual = input[i] - prediction

        #update the first memory slot with the current input value
        #This should not be done for order 0 since that have an empty memory
        if self.order > 0:
            memory[0] = input[i]
        
        
        #saves residuals and prediction in their respective array
        predictions.append(prediction)
        residuals.append(residual)

    #returns residual. memory. and prediction array
    #The memory array can then be used for the next set of data inputs if the come in blocks
    return residuals, memory, predictions