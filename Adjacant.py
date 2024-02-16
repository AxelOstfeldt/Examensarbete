#Simalrly to Shorten but predicts adjacent microphones


#Takes data as input
#order of predicuter as order
#memory as the last sampels beffore the input data
#memory should be the length of order
#if memory is the start of the data stream it should be an array of zeros
class Shorten_adjacent:

    def __init__(self, order: int = 1):
        #Order can only be between 0 and 3 for Shorten, and have to be an int
        if not (0 <= order <= 3) or not isinstance(order, int):
            raise ValueError(f"Order can only have integer values between 0 and 3. Current value of is {order}")

        self.order = order
        #Coeficents for differente orders, from 0 to 3
        all_coeficents = [[0],[1],[2, -1],[3, -3, 1]]
        #Assigns the coeificents to be used based on order
        self.coeficents = all_coeficents[order]



    def In(self, input0, input1):


        
        predictions = []#only needed for testing?
        residuals = []
        

        
        #loops through the input array 
        for i in range(len(input0)):

            prediction = input0[i]
            residual = input1[i] - prediction
            
            
            
            #saves residuals and prediction in their respective array
            predictions.append(prediction)
            residuals.append(residual)

        #returns residual. memory. and prediction array
        #The memory array can then be used for the next set of data inputs if the come in blocks
        return residuals, predictions





#test
if 1 > 0:
    mic0 = [1,2,3,4,5,6]
    mic1 = [0,1,2,3,4,5]

    Shorten_predictor = Shorten_adjacent(1)
    res, pred = Shorten_predictor.In(mic0,mic1)

    print("Residuals = ", res)
    print("Predictions = ", pred)


