import numpy as np



class Adjacant:

    def __init__(self, order):
        self.order = order
        #Coeficents for differente orders, from 0 to 4
        all_coeficents = [[0],[1],[2, -1],[3, -3, 1],[4,-6,4,-1]]
        #Assigns the coeificents to be used based on order
        self.coeficents = all_coeficents[order]


    def FirstIn(self, firstInput, memory):
        firstPrediction = 0

        if self.order > 0:
            firstPrediction = sum( np.array(self.coeficents) * np.array(memory) )

        firstResidual = firstInput - firstPrediction

        if self.order > 0:
            memory = [firstInput] + memory[:-1]
        print("mem = ", memory)

        return firstResidual, memory, firstPrediction
    
    def In(self, inputs, memory):
        
        #Use Shorten to calculate the residual for the first microphone in the array
        firstResidual, memory, firstPrediction = self.FirstIn(inputs[0], memory)

        #Save the first residual and prediciton in the residual and prediciton arrays
        Residuals = [firstResidual]
        Predictions = [firstPrediction]


        #Save the first value as the previous value and previous row value
        #Previous indicates the value of the previous mice
        #PreviousRow indicates the first value of the previous row
        #The rest of the resiudals are calculated by taking the difference between the current mic value and the previous mic value
        Previous = inputs[0]
        PreviousRow = inputs[0]
        for i in range(1, len(inputs)):
            #When i modulos 8 is equal to 0 it indicates that a new row has started (8 mics per row)
            if i % 8 == 0:
                #The previous value is then taken from the previous row and not the previous mic
                #This will give a mic that is closer to the current mic
                CurrentResidual, CurrentPrediction = self.PredicitorIn(inputs[i], PreviousRow)
                #A new PreviousRow value is calculculated
                #This is the first value of the new row
                PreviousRow = inputs[i]
            else:
                CurrentResidual, CurrentPrediction = self.PredicitorIn(inputs[i], Previous)

            #Update the previous value
            Previous = inputs[i]

            #Save the residual and predicted value in their respective array
            Residuals.append(CurrentResidual)
            Predictions.append(CurrentPrediction)

        #Return the residuals, memory, and predictions
        return Residuals, memory, Predictions


    def PredicitorIn(self, CurrentInput, PreviousInput):
        #Predicted value is the previous mic value
        Predcition = PreviousInput
        #The residual is the difference of the current mic value and the previous mic value
        Residual = CurrentInput - Predcition
        #Return the residual and prediciton
        return Residual, Predcition
    

    def FirstOut(self, firstResidual, memory):
        firstPrediction = 0

        #If order is larger than 0 calculate prediciton, else prediciton is always 0
        if self.order > 0:
            firstPrediction = sum( np.array(self.coeficents) * np.array(memory) )

        #Recreate the original input by adding the residual and prediction value
        firstInput = firstResidual + firstPrediction

        #Update memory
        if self.order > 0:
            memory = [firstInput] + memory[:-1]

        return firstResidual, memory, firstPrediction
    

    def Out(self, residuals, memory):
        #Use Shorten to calculate the original input for the first microphone in the array
        firstInput, memory, firstPrediction = self.FirstOut(residuals[0], memory)

        #Save the first residual and prediciton in the residual and prediciton arrays
        Inputs = [firstInput]
        Predictions = [firstPrediction]

        #Save the first value as the previous value and previous row value
        #Previous indicates the value of the previous mice
        #PreviousRow indicates the first value of the previous row
        #The original inputs are calculated unsing previous mic values and residuals
        Previous = firstInput
        PreviousRow = firstInput
        for i in range(1, len(residuals)):
            #When i modulos 8 is equal to 0 it indicates that a new row has started (8 mics per row)
            if i % 8 == 0:
                #The previous value is then taken from the previous row and not the previous mic
                #This will give a mic that is closer to the current mic
                CurrentInput, CurrentPrediction = self.PredicitorOut(residuals[i], PreviousRow)
                #A new PreviousRow value is calculculated
                #This is the first value of the new row
                PreviousRow = CurrentInput
            else:
                CurrentInput, CurrentPrediction = self.PredicitorOut(residuals[i], Previous)

            #Update previous value
            Previous = CurrentInput

            #Save the recreated input value and predicted value in their respective array
            Inputs.append(CurrentInput)
            Predictions.append(CurrentPrediction)


        #Return recreated inputs, memory and predictions
        return Inputs, memory, Predictions
        

    def PredicitorOut(self, CurrentResidual, PreviousInput):
        #Predicted value is the previous mic value
        Predcition = PreviousInput
        #The original input value will be the residual + previous mic value
        CurrentInput = CurrentResidual + Predcition
        #Return the residual and prediciton
        return CurrentInput, Predcition
        


#Test
    
if 1 < 0:
    import random
    testInput = [1,2,3,4]

    for i in range(64):
        current_value = random.randint(0,3)
        testInput.append(current_value)

    print("Original inputs: ",testInput)


    ShortenOrder = 4
    memoryIn = [0] * ShortenOrder
    Adjacant_predictor = Adjacant(ShortenOrder)
    testResiduals, memoryIn, PredictionsIn = Adjacant_predictor.In(testInput, memoryIn)

    print("memory in ",memoryIn)

    memoryOut = [0] * ShortenOrder
    recreatedInputs, memoryOut, PredictionsOut = Adjacant_predictor.Out(testResiduals, memoryOut)

    #print("Recreated inputs: ", recreatedInputs)
    print("Memory out ", memoryOut)


    allCorrect = 0
    for i in range(len(recreatedInputs)):
        if recreatedInputs[i] != testInput[i]:
            print("Failed to recreate inputs at ", i,"Original input = ",testInput[i],"Recreted input = ",recreatedInputs[i])
            allCorrect +=1

    if allCorrect == 0:
        print("All inputs recreated correctly")
    else:
        print("Failed recreating ", allCorrect,"inputs")

