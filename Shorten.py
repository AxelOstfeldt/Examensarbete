order = 1
input = [1,2,3,4,5,6,7,8,9,9,9,10,11,12,5,4,3,2,1,0]
samples = [0] * order
predictions = []
residuals = []


all_coeficents = [[0],[1],[2, -1],[3, -3, 1]]

coeficents = all_coeficents[order]



for i in range(len(input)):

    prediction = 0

    if order > 1:
        for j in reversed(range(1, order)):
            
            prediction = prediction + coeficents[j] * samples[j]
            samples[j] = samples[j-1]


    prediction = prediction + coeficents[0] * samples[0]
    residual = input[i] - prediction
    samples[0] = input[i]
        
    predictions.append(prediction)
    residuals.append(residual)


print(predictions)
    
print(residuals)
print(samples)