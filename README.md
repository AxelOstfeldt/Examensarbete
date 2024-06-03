This GitHub repository contains the master's thesis work completed by Axel Östfeldt at Saab AB, serving as the culminating task in the pursuit of an electrical engineering degree at Uppsala University. The final paper can be found in the file "Report.pdf" within this repository.

The code in the repository can be summarized in four parts:

1. The repository includes several Python files containing compression algorithms for audio data in the form of classes. The following files contain these classes: "Adjacent.py", "AdjacentAndShorten.py", "AdjacentMeta.py", "FLAC.py", "FLAC_Meta.py", "FlacModified.py", "Golomb.py", "LPC.py", "LPC_Meta.py", "Rice.py", "Shorten.py", and "ShortenMeta.py". Information on how these different algorithms work can be found in the final paper (note: "AdjacentAndShorten.py" is referred to as "DoubleCompression" in the report). Some of these algorithms have the word "meta" attached to their file names, indicating that the metadata needed to decode them is attached in the codeword produced by the algorithm.

2. For evaluating the algorithms in a Python environment, the Acoustic Warfare System by Saab was utilized. More information on this system can be found at https://github.com/acoustic-warfare. From this project, the files found in the "lib" folder and the "config.py" file were extracted. By utilizing the "replay.py" file, recorded sound files from the Acoustic Warfare System could be replayed, and the data was processed in the Python code "AcousticWarfareSystemTest.py". This file contains all the tests performed to obtain the results displayed in the final paper.

3. To enable individuals without access to the Acoustic Warfare System to test the code, the "PythonTest" folder was created. Here, zipped .txt files containing data recorded by the Acoustic Warfare System can be found. "AllTest.py" contains the tests from "AcousticWarfareSystemTest.py", excluding some that were deemed redundant. To run the tests, the user only needs to execute the "TestFunction.py" file, which provides instructions on accessing available tests and running them within "TestFunction.py". Ensure that the "path" variable in "TestFunction.py" is set to the folder containing the unzipped .txt files with sound data.

4. The "VHDL" folder contains the VHDL code for the Adjacent algorithm. To execute this, ensure that VUnit and GTKwave are installed. The folder contains a PNG file, "AdjacentCombined_BlockDiagram.png", displaying how the different entities are connected to each other. The "src" folder contains all entities, while the "test" folder contains the testbenches. Each entity has a specific testbench with the same filename as the entity but with "tb_" prefixed. There's also a testbench for all entities combined in the "tb_adjacent_combined.vhd" file. Ensure that the "my_file" variable is set to the path and file to read data from, and the "file_handler" variable is set to the path and file to save data to when running this testbench. The "VHDL" folder also contains two zipped files: "data_block_binary.zip", which is a zipped .txt file with audio data that can be read by the testbench, and "EncodedData.zip", containing a zipped .txt file with the results from compressing this data with the testbench code. To validate the compressed data, the main "Examensarbete" folder contains a file named "DecodeTestbench.py". Ensure that the "Path" variable is set to a folder containing both the audio data fed to the testbench and the encoded data from the testbench. Set the "FileName" variable to the filename containing the original data, and the "EncodedFile" variable to the filename containing the compressed codewords.