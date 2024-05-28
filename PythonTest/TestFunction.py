import numpy as np
from AllTests import TestFunctions



#Initial values
DoTests = True
flag = True
MaxDataBlocks = 20
#Set the directory to the where the unziped files are saved
#Path = "/home/luigi/Desktop/DataTxt/"#Saab dator
Path = "C:\\Users\\axelo\\OneDrive\\Skrivbord\\Exjobb\\GIT\\SoundData\\"
#Hem dator

while DoTests:

    #Choose a test of info about the tests
    StartTest = input('Choose Test (1-28), for test info type info, to exit testing type quit: ')
    print("")

    if StartTest.lower() == 'info':
        print("Test info")
        #Loop trough all test numbers and call TestInfo function that prints test info for a tests but returns nothing
        for TestNumber in range(1, 29):
            print("")
            CurrentTest = TestFunctions(TestNumber)
            CurrentTest.TestInfo()

    elif StartTest.lower() == 'quit':
        print("Testing complete")
        DoTests = False
    else:
        #If info is not typed the value choosen should be able to be converted to int
        try:
            int(StartTest)
        #If the value can not be converted to int set the flag to false
        except ValueError:
            flag = False
        #If flag is true StartTest can be converted to int and is the test choosen
        if flag:
            TestNumber = int(StartTest)
        #If it can not be converted to int the user have choosen an invalid value
        else:
            raise ValueError(f"Select an integer between 1-28 for a test or type info for test info")

        #print info about the selected test
        CurrentTest = TestFunctions(TestNumber)
        CurrentTest.TestInfo()
        print("")

        
        #Set the FileName to the name of the file with the data for the test
        print('Choose what sound data to use for testing:')
        print('1. 1k Hz Tone')
        print('2. Droun sound')
        print('3. Static noise')
        SoundFile = input('Select a number, 1-3: ')

        #Check if the SoundFile value choosen can be converted to int
        try:
            int(SoundFile)
        #If the value can not be converted to int set the flag to false
        except ValueError:
            flag = False

        if flag:
            SoundFile = int(SoundFile)
        else:
            raise ValueError(f"The value selected needs to be an integer.")

        if SoundFile == 1:
            FileName = "1kHzTone.txt"
            MaxDataBlocks = 23
        elif SoundFile == 2:
            FileName = "DroneSound.txt"
            MaxDataBlocks = 47
        elif SoundFile == 3:
            FileName = "StaticNoise.txt"
            MaxDataBlocks = 39
        else:
            raise ValueError(f"The number selected is not found. Selcted numer = {SoundFile}, please select a number between 1 and 3.")
        
        DataBlocks = input(f'How many datablocks do you want to test over? (For {FileName} maximum is {MaxDataBlocks} datablocks): ')

        #Check if the DataBlocks value choosen can be converted to int
        try:
            int(DataBlocks)
        #If the value can not be converted to int set the flag to false
        except ValueError:
            flag = False

        if flag:
            DataBlocks = int(DataBlocks)
        else:
            raise ValueError(f"The value selected needs to be an integer.")


        if DataBlocks > MaxDataBlocks:
            raise ValueError(f"The number of datablocks is to large. For {FileName} maximum is {MaxDataBlocks} datablocks.")
        elif DataBlocks < 1:
            raise ValueError(f"The number of datablocks is to small. Needs to be atleast 1 datablock.")

        
        

        #Full dircetory of the test data
        FullDirectory = Path+FileName

        #The code to load the data:
        if 1 > 0:
            # Create an empty list to store loaded data
            loaded_data = []

            # Open the file containing all data, remember to set correct filename
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

            CurrentTest.StartTest(loaded_data, DataBlocks)
            #loaded_data = CurrentTest.DataSelect(loaded_data,64,64)


            #This code is to test how correct the loaded data is:
            if 1 < 0:
                print("len loaded data = ",len(loaded_data))
                for i in range(len(loaded_data)):
                    print("i = ",i)
                    datablock = loaded_data[i]
                    print("datablock shape = ",datablock.shape)

                    #for mic in range(256):
                    #    print("datablock[mic,0] = ", datablock[mic,:])