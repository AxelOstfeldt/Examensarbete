

class TestFunctions:

    def __init__(self, TestNr, datablocks: int = 20):
        self.TestNr = TestNr
        self.datablocks = datablocks

    #TestInfo function prints info for what each test does
    def TestInfo(self):
        #Raw data tests
        if self.TestNr == 1:
            print('Test 1. This test plots data for specific microphones.')
        elif self.TestNr == 2:
            print('Test 2. Compression rate when using Rice codes on raw data.')
        elif self.TestNr == 3:
            print('Test 3. Compression rate when using Golomb codes on raw data.')

        #Shorten tests
        elif self.TestNr == 4:
            print('Test 4. Compare original input with recreated values when using Shorten with Rice codes to see if all values have been recreated correctly.')
        elif self.TestNr == 5:
            print('Test 5. Compare original input with recreated values when using Shorten with Golomb codes to see if all values have been recreated correctly.')
        elif self.TestNr == 6:
            print('Test 6. Plots compression rate for differnte k-values when using Shorten with Rice codes.')
        elif self.TestNr == 7:
            print('Test 7. Compression rate using Shorten with Rice codes.')
        elif self.TestNr == 8:
            print('Test 8. Average speed to recreate values from codewords using Shorten with Rice codes.')
        elif self.TestNr == 9:
            print('Test 9. Average speed to recreate values from codewords using Shorten with Golomb codes.')

        #LPC tests
        elif self.TestNr == 10:
            print('Test 10. Compare original input with recreated values when using LPC with Rice codes to see if all values have been recreated correctly.')
        elif self.TestNr == 11:
            print('Test 11. Compare original input with recreated values when using LPC with Golomb codes to see if all values have been recreated correctly.')
        elif self.TestNr == 12:
            print('Test 12. Plots compression rate for differnte k-values when using LPC with Rice codes.')
        elif self.TestNr == 13:
            print('Test 13. Compression rate using LPC with Rice codes.')
        elif self.TestNr == 14:
            print('Test 14. Average speed to recreate values from codewords using LPC with Rice codes.')
        elif self.TestNr == 15:
            print('Test 15. Average speed to recreate values from codewords using LPC with Golomb codes.')

        #FLAC tests
        elif self.TestNr == 16:
            print('Test 16. Compare original input with recreated values when using FLAC to see if all values have been recreated correctly.')
        elif self.TestNr == 17:
            print('Test 17. Test compression rate using FLAC.')
        elif self.TestNr == 18:
            print('Test 18. Average speed to recreate values from codewords using FLAC.')

        #Adjacent tests

        
        