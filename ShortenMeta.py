class ShortenMeta:

    def __init__(self, order: int = 3):
        #Order can only be between 0 and 3 for Shorten, and have to be an in
        if not (0 <= order <= 3) or not isinstance(order, int):
            raise ValueError(f"Order can only have integer values between 0 and 3. Current value of is {order}")

        self.order = order
        #Coeficents for differente orders, from 0 to 3
        all_coeficents = [[0],[1],[2, -1],[3, -3, 1]]
        #Assigns the coeificents to be used based on order
        self.coeficents = all_coeficents[order]

    def predict(self, memory):
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


    def In(self, input, memory: list = [0] * 3):


        
        
        #raises error if memory is not the length of order
        if self.order != len(memory):
            raise ValueError(f"Order and memory length should match. Current values are: order = {self.order}, memory length = {len(memory)}")
        
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
            
            
            #saves residuals 
            residuals.append(residual)

        #returns residual. memory. and prediction array
        #The memory array can then be used for the next set of data inputs if the come in blocks
        return residuals, memory, self.order


    def Out(self, residuals, memory: list = [0] * 3):
        

        input = []
        
        #loops through the residuals array 
        for i in range(len(residuals)):
            prediction, memory = self.predict(memory)


            #calculates original input by taking the current residual and adding the predicted value
            current_input = residuals[i] + prediction

            #update the first memory slot with the current input value
            #This should not be done for order 0 since that have an empty memory
            if self.order > 0:
                memory[0] = current_input
            
            #saves residuals 
            input.append(current_input)


        return input, memory