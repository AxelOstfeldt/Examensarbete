#Takes data as input
#order of predicuter as order
#memory as the last sampels beffore the input data
#memory should be the length of order
#if memory is the start of the data stream it should be an array of zeros

def Shorten(input, order, memory):


    #Order can only be between 0 and 3 for Shorten, and have to be an int
    if not (0 <= order <= 3) or not isinstance(order, int):
        raise ValueError(f"Order can only have integer values between 0 and 3. Current value of is {order}")
    
    #raises error if memory is not the length of order
    if order != len(memory):
        raise ValueError(f"Order and memory length should match. Current values are: order = {order}, memory length = {len(memory)}")
    
    predictions = []
    residuals = []
    #Coeficents for differente orders, from 0 to 3
    all_coeficents = [[0],[1],[2, -1],[3, -3, 1]]
    #Assigns the coeificents to be used based on order
    coeficents = all_coeficents[order]

    
    #loops through the input array 
    for i in range(len(input)):
        #prediction of current value is calculated in this variable
        prediction = 0

        #if order is larger than 1 this loop is entered to calculate predictions and shuffle index in memory one step back
        if order > 1:
            #this forloop is reversed so that memory values needed are not overwritten when values are shuffled one index back
            for j in reversed(range(1, order)):
                
                prediction = prediction + coeficents[j] * memory[j]
                memory[j] = memory[j-1]


            prediction = prediction + coeficents[0] * memory[0]

            #current input is saved in first slot of memory
            memory[0] = input[i]
        elif i > 0:
            #in case of order 1 the current prediction is the last input
            prediction = input[i-1]
        else:
            #in case of order zero the prediciton is allways zero.
            #in this case the full current value is sent as residual
            prediction = 0
        #calculates residual by taking the current value and subtract the predicted value
        residual = input[i] - prediction
        
        #saves residuals and prediction in their respective array
        predictions.append(prediction)
        residuals.append(residual)
    #returns residual. memory. and prediction array
    #The memory array can then be used for the next set of data inputs if the come in blocks
    return residuals, memory, predictions


order = 3
input = [1,2,3,4,5,6,7,8,9,9,9,10,11,12,5,4,3,2,1,0]
samples = [0] * 3

residuals, memory, predictions = Shorten(input, order, samples)

print("Predictions: ",predictions)
    
print("Residuals: ",residuals)
print("Memory: ",memory)