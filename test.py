        for i in range(len(residuals)):
            prediction = 0


            if order == 0:
                prediction = 0

            elif order > 1:
                #this forloop is reversed so that memory values needed are not overwritten when values are shuffled one index back
                for j in reversed(range(1, order)):
                    
                    prediction = prediction + coeficents[j] * memory[j]
                    memory[j] = memory[j-1]

                prediction = prediction + coeficents[0] * memory[0]

            elif order == 1:
                prediction = memory[0]
                
            current_input = residuals[i] + prediction

            input.append(current_input)
            predictions.append(prediction)
            memory[0] = current_input


        return input, memory, predictions
