import matplotlib.pyplot as plt
import numpy as np
import math
from TestBenchRice import RiceCoding
from Adjacent import Adjacent



#Load original data
# Create an empty list to store loaded data
loaded_data = []
# Open the file containing all data, remember to set correct filename
#Path = "C:\\Users\\axelo\\OneDrive\\Skrivbord\\Exjobb\\GIT\\SoundData\\"
Path = "/home/luigi/Desktop/DataTxt/"#Saab dator
FileName = "1kHzTone.txt"
FullDirectory = Path+FileName
with open(FullDirectory, 'r') as file:
    array = []
    for line in file:
        # Check if the line is empty, indicating the end of an array
        if not line.strip():
            # Convert the collected lines into a NumPy array and append to loaded_data
            loaded_data.append(np.array(array, dtype=int))
            # Reset the array for the next set of lines
            array = []
        else:
            # Convert the line into integers and append to the array
            array.append([int(x) for x in line.split()])

# Append the last array since there's no empty line after it
if array:
    loaded_data.append(np.array(array, dtype=int))


#Grab the first datablock for all mics
FirstDatablock = loaded_data[0]

#Grab the the data from array2
OrginalData = FirstDatablock[64:128,:]






#Load the encoded data
#File name
EncodedFile = "EncodedData.txt"
#Same path as previous file. May need to change path depending on where the file is saved
EndocedDirectory = Path + EncodedFile
# Create an empty list to store loaded data
loaded_data = []

with open(EndocedDirectory, 'rb') as file:
    array = []
    for line in file:
        # Decode the binary data into a string
        decoded_line = line.decode('utf-8').strip()
        
        # Append the decoded string to the array
        array.append(decoded_line)

        # Check if the line is empty, indicating the end of an array
        if not decoded_line:
            # Append the array to loaded_data
            loaded_data.append(array)
            # Reset the array for the next set of lines
            array = []

# Append the last array since there's no empty line after it
if array:
    loaded_data.append(array)

#Grab the binary codewords
EncodedData = loaded_data[0]

#Calculate average compression rate
#The original data consist of 64 mics, each having a 24 bits sample, per datablock
OrginalDataLen = 64*24

cr_array=[]

for datablock in range(256):
    CodeWordLen = len(EncodedData[datablock])
    cr = CodeWordLen / OrginalDataLen

    cr_array.append(cr)

avg_cr = sum(cr_array) / len(cr_array)

print("Average compression rate is, cr = ", avg_cr)



#Decode the data
DecodedData = []
for sample in range(len(EncodedData)):
    CodeWord = EncodedData[sample]
    k_value = CodeWord[:5]
    k = int(k_value,2)
    NewCodeWord = CodeWord[13:]
    Rice_coder = RiceCoding(k, True)
    DecodedValues = Rice_coder.Decode(NewCodeWord)
    DecodedData.append(DecodedValues)





#Recreate values from decoded residuals
AdjacentAlgorithm = Adjacent(1)
memory = [0]
RecreatedValues = []

for residuals in DecodedData:
    values, memory, prediciton = AdjacentAlgorithm.Out(residuals,memory)
    RecreatedValues.append(values)


#to plot all microphones
orgiginal_plot = []
recreated_plot = []
zero_plot = []

#To see that all values have been decoded correctly
AllCorrect = 0


#Calculate if all values have been recreated succesfully
for sample in range(256):
    CurrentOriginalValues = OrginalData[:,sample]
    CurrentRecreatedValues = RecreatedValues[sample]
    
    for mic in range(64):
        if sample == 0:
            orgiginal_plot.append([])
            recreated_plot.append([])
            zero_plot.append([])

        OrgValue = CurrentOriginalValues[mic]
        ReValue = CurrentRecreatedValues[mic]

        orgiginal_plot[mic].append(OrgValue)
        recreated_plot[mic].append(ReValue)
        zero = OrgValue - ReValue

        zero_plot[mic].append(zero)

        if zero != 0:
            print("Failed to recreate value at mic = ",mic, "and sample = ",sample)
            AllCorrect += 1

if AllCorrect == 0:
    print("All values have been recreated succesfully")

        

for mic in range(64):
    if 1 < 0:#plots for report
        print("For report")

    else:
        figure_title = "Mic #" +str(64+mic)
        fig = plt.figure(figure_title, layout = 'constrained')

        ax = fig.add_subplot(311)
        plt.plot(orgiginal_plot[mic])
        ax.title.set_text("Original values")

        ax = fig.add_subplot(312)
        plt.plot(recreated_plot[mic])
        ax.title.set_text("Recreated values")

        ax = fig.add_subplot(313)
        plt.plot(zero_plot[mic])
        ax.title.set_text("Original values - Recreated values (Should always be 0)")


        plt.show()


    
    
