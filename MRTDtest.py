#TODO: Define input, mocks, and test cases
import unittest
from MRTD import checkMismatches, getTravelDataFromDB, decodeMRZ, scanMRZ, calculateCheck,getNumericalValue


testData = ['A','B','2','1','3','4','<','<','<']
testData2 = ['L','8','9','8','9','0','2','C','3']
testData3 = ['U','T','O','7','4','0','8','1','2']
testData4 = ['F','1','2','0','4','1','5']
testData5 = ['Z','E','1','8','4','2','2','6','B']

class TestMRTD(unittest.TestCase):
    # define multiple sets of tests as functions with names that begin

    def testGetNumericalValue(self):
        self.assertEqual(getNumericalValue("A"), 10, "A should be 10")
        self.assertEqual(getNumericalValue("Z"), 35, "Z should be 35")
        self.assertEqual(getNumericalValue("<"), 0, "< should be 0")
        
    def testCalculateCheck(self):
        self.assertEqual(calculateCheck(testData), 5, "should be 5")
        self.assertEqual(calculateCheck(testData2), 6, "should be 6")
        self.assertEqual(calculateCheck(testData3), 2, "should be 2")
        
        #Failed
        self.assertEqual(calculateCheck(testData4), 9, "should be 9")
        self.assertEqual(calculateCheck(testData5), 1, "should be 1")



if __name__ == '__main__':
    print('Running unit tests')
    unittest.main()