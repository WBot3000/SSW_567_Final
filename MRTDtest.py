#TODO: Define input, mocks, and test cases
import unittest
from unittest import mock
from MRTD import TravelData, TravelDataError, getNumericalValue, calculateCheck, decodeMRZ, encodeMRZ, checkMismatches

#For calculating check values
testData = ['A','B','2','1','3','4','<','<','<']
testData2 = ['L','8','9','8','9','0','2','C','3']
testData3 = ['7','4','0','8','1','2']
testData4 = ['1','2','0','4','1','5']
testData5 = ['Z','E','1','8','4','2','2','6','B']

#For checking other functions
annaLine1 = "P<UTOERIKSSON<<ANNA<MARIA<<<<<<<<<<<<<<<<<<<"
annaLine2 = "L898902C36UTO7408122F1204159ZE184226B<<<<<<1"
georgeLine1 = "P<UTOJORGE<<GEORGE<G<<<<<<<<<<<<<<<<<<<<<<<<"
georgeLine2 = "G30RG3ABC6UTO6909264M1405116EGROEG<<<<<<<<<7"
willLine1 = "P<UTOFRANKLIN<<WILLIAM<TRAVIS<<<<<<<<<<<<<<<"
willLine2 = "46NQW09071UTO9201302M1603039WX123U22XIESAL<9"
tooLongLine = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
tooShortLine = "B"

annaData = TravelData("P", "UTO", "ERIKSSON", "ANNA", "MARIA", "L898902C3", "6", "UTO", "740812", "2", "F", "120415", "9", "ZE184226B<<<<<<", "1")
georgeData = TravelData("P", "UTO", "JORGE", "GEORGE", "G", "G30RG3ABC", "6", "UTO", "690926", "4", "M", "140511", "6", "EGROEG<<<<<<<<<", "7")
willData = TravelData("P", "UTO", "FRANKLIN", "WILLIAM", "TRAVIS", "46NQW0907", "1", "UTO", "920130", "2", "M", "160303", "9", "WX123U22XIESAL<", "9" )

annaCheck = TravelDataError(False, False, False, False)
georgeCheck = TravelDataError(False, False, True, True)
willCheck = TravelDataError(True, True, False, False)

#Used to check if two objects have all the same field values or not
def checkDataEquality(d1, d2):
    d1Fields = vars(d1)
    d2Fields = vars(d2)
    keys = list(d1Fields)
    for key in keys:
        if(d1Fields[key] != d2Fields[key]):
            return False
    return True


def mockDBFunc(personalNo):
    if(personalNo == "ZE184226B<<<<<<"):
        return annaData
    if(personalNo == "EGROEG<<<<<<<<<"):
        return georgeData
    if(personalNo == "WX123U22XIESAL<"):
        return willData
    

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
        self.assertEqual(calculateCheck(testData4), 9, "should be 9")
        self.assertEqual(calculateCheck(testData5), 1, "should be 1")

    def testDecodeMRZ(self):
        self.assertTrue(checkDataEquality(decodeMRZ(annaLine1, annaLine2), annaData))
        self.assertTrue(checkDataEquality(decodeMRZ(georgeLine1, georgeLine2), georgeData))
        self.assertTrue(checkDataEquality(decodeMRZ(willLine1, willLine2), willData))


    @mock.patch("MRTD.getTravelDataFromDB", side_effect = mockDBFunc)
    def testEncodeMRZ(self, mockData):
        self.assertEqual(encodeMRZ("ZE184226B<<<<<<"), (annaLine1, annaLine2))
        self.assertEqual(encodeMRZ("EGROEG<<<<<<<<<"), (georgeLine1, georgeLine2))
        self.assertEqual(encodeMRZ("WX123U22XIESAL<"), (willLine1, willLine2))


    def testCheckMismatches(self):
        self.assertTrue(checkDataEquality(checkMismatches(annaData), annaCheck))
        self.assertTrue(checkDataEquality(checkMismatches(georgeData), georgeCheck))
        self.assertTrue(checkDataEquality(checkMismatches(willData), willCheck))
        

if __name__ == '__main__':
    print('Running unit tests')
    unittest.main()
