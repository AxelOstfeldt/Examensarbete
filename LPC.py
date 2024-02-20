import numpy as np



class LPC:

    def __init__(self, order):
        self.order = order



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

                

        return t/n



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



    def prediciton(self, memory, coef):
        prediction = 0

        for j in reversed(range(1, self.order)):
            prediction += coef[j] * memory[j]
            memory[j] = memory[j-1]

        prediction += coef[0] * memory[0]

        return prediction, memory
    
    

    def In(self, inputs, memory):

        coef = self.Coefficents(inputs)

        residuals = []
        predictions = []

        for i in range(len(inputs)):
            predict, memory = self.prediciton(memory, coef)

            memory[0] = inputs[i]
            residual = inputs[i] - predict

            residuals.append(residual)
            predictions.append(predict)

        return coef, residuals, memory, predictions

        
        
    def Out(self, coef, residuals, memory):
        predictions = []
        inputs = []

        for i in range(len(residuals)):
            predict, memory = self.prediciton(memory, coef)

            memory[0] = residuals[i]
            input = residuals[i] + predict

            predictions.append(predict)
            inputs.append(input)

        return inputs, memory, predictions



#Tests
if 1 > 0:
    input = []
    for i in range(1, 100):
        input.append(i*3)


    order = 8
    memory = [0]*order
    LPC_predictor = LPC(order)

    coff, res, memory, pred = LPC_predictor.In(input, memory)

    print("Inputs = ", input)
    print("Prediction = ", np.array(pred).astype(int))
    print("Memory = ", memory)
    print("Coefficents = ", coff)


    


