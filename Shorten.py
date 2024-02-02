

def Shorten(input, order, memory):

    if not (0 <= order <= 3) or not isinstance(order, int):
        raise ValueError(f"Order can only have integer values between 0 and 3. Current value of is {order}")
    
    predictions = []
    residuals = []
    all_coeficents = [[0],[1],[2, -1],[3, -3, 1]]
    coeficents = all_coeficents[order]

    

    for i in range(len(input)):

        prediction = 0

        if order != len(memory):
            raise ValueError(f"Order and memory length should match. Current values are: order = {order}, memory length = {len(memory)}")

        if order > 1:
            for j in reversed(range(1, order)):
                
                prediction = prediction + coeficents[j] * memory[j]
                memory[j] = memory[j-1]


            prediction = prediction + coeficents[0] * memory[0]
            memory[0] = input[i]
        elif i > 0:
            prediction = input[i-1]
        else:
            prediction = 0
        residual = input[i] - prediction
        
            
        predictions.append(prediction)
        residuals.append(residual)

    return residuals, memory, predictions


order = 3
input = [1,2,3,4,5,6,7,8,9,9,9,10,11,12,5,4,3,2,1,0]
samples = [0] * 3

residuals, memory, predictions = Shorten(input, order, samples)

print("Predictions: ",predictions)
    
print("Residuals: ",residuals)
print("Memory: ",memory)