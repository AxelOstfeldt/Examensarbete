This Github repository conatins the master thesis work done by Axel Östfeldt and is the terminal task in the study to become an electrical engineer at Uppsala university. The final paper can be read in the file "Report.pdf" in the repository.
The code in the repository can be summarized in four parts.


1. The repository have several python files containing compression algorithms for audio data in the form of classes. The following files contains these classes "Adjacent.py", "AdjacentAndShorten.py", "AdjacentMeta.py", "FLAC.py", "FLAC_Meta.py", "FlacModified.py", 
"Golomb.py", "LPC.py", "LPC_Meta.py", "Rice.py", "Shorten.py", and "ShortenMeta.py". Information on how these differente algorithms work can be found the final paper (AdjacenAndShorten.py is refered to as DoubleCompression in the report). Some of these algoritms have the word
"meta" atached in the file name, this indicates that the meta data needed to decode them are atached in the codeword produced by the algorithm.

2. The evaluation of the algorithms in a python enviorment I have used the acustic warfare system by Saab (more info at https://github.com/acoustic-warfare). From this project I was able to grab the files found in the "lib" folder and the "config.py" file. By using the "replay.py"
file I could reaply the recorded soundfiles from the acustic warfare system and get the data into my python code "AcousticWarfareSystemTest.py". This file contains all the test I have performed to get the results displayed in the final paper.

3. In order to allow people who do not have acess to the acustic warfare system to test the code I crated the "PythonTest" folder. Here zipped .txt files can be found, containing data recorded by the acustic warfare system. "AllTest.py" contains the test from "AcousticWarfareSystemTest.py",
except some that where deemed redundant. In order to run the test the user only needs to run the "TestFunction.py" file, this will give the user instuctions on how to find information on available test and how to run them inside the "TestFunction.py". Make sure the path
variable in "TestFunction.py" is set to the folder containing the unzipped .txt files with sound data.

4. The folder "VHDL" contains the VHDL code for the Adjacent algorithm, to be able to run this ensure that vunit and GTKwave is installed. The folder conatins png file "AdjacentCombined_BlockDiagram.png" displaying how the differente entities are conected to eachother. The "src"
folder contains all entities, and the "test" folder conatins the testbenches. All entites have a specific testbench with same file name as the entity but with an added "tb_" infront. There is also a testbench for all entites combined in the "tb_adjacent_combined.vhd" file,
make sure the "my_file" variable is set to the path and file to read data from and "file_handler" variable is set to the path and file to save data to when runing this testbench. The VHDL folder contains two zipped files, "data_block_binary.zip" is a zipped .txt file with audio
data that can be read by the testbench, and "EncodedData.zip" contains a zipped .txt file with the results from compressing this data with the testbench code. In order to validate the compressed data the main Examensarbete folder have a file named "DecodeTestbench.py". Make sure
the "Path" variable is set to the a folder containing both the audio data feed to the testbench and the encoded data from the testbench. The "FileName" variable should be set to the file name containing the original data, and "EncodedFile" variable to the file name containing
the compressed codewords.
