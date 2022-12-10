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

#For checking all the other functions
#Standard user MRZ lines
annaLine1 = "P<UTOERIKSSON<<ANNA<MARIA<<<<<<<<<<<<<<<<<<<"
annaLine2 = "L898902C36UTO7408122F1204159ZE184226B<<<<<<1"
georgeLine1 = "P<UTOJORGE<<GEORGE<G<<<<<<<<<<<<<<<<<<<<<<<<"
georgeLine2 = "G30RG3ABC6UTO6909264M1405116EGROEG<<<<<<<<<7"
willLine1 = "P<UTOFRANKLIN<<WILLIAM<TRAVIS<<<<<<<<<<<<<<<"
willLine2 = "46NQW09071UTO9201302M1603039WX123U22XIESAL<9"

#Used to check edge cases for decoding MRZ. Besides too long/too short, they are based off of Anna's lines
tooLongLine = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
tooShortLine = "B"
invalidLastNameLine = "P<UTOERIKSS0N<<ANNA<MARIA<<<<<<<<<<<<<<<<<<<"
invalidFirstNameLine = "P<UTOERIKSSON<<ANN@<MARIA<<<<<<<<<<<<<<<<<<<"
invalidMiddleNameLine = "P<UTOERIKSSON<<ANNA<MAR1A<<<<<<<<<<<<<<<<<<<"
invalidBirthdayLine = "L898902C36UTO7N08122F1204159ZE184226B<<<<<<1"
partialBirthdayLine = "L898902C36UTO74<<122F1204159ZE184226B<<<<<<1"
invalidExpirationLine = "L898902C36UTO7408122F1204L59ZE184226B<<<<<<1"
partialExpirationLine = "L898902C36UTO7408122F<<04159ZE184226B<<<<<<1"

#Three users
annaData = TravelData("P", "UTO", "ERIKSSON", "ANNA", "MARIA", "L898902C3", "6", "UTO", "740812", "2", "F", "120415", "9", "ZE184226B<<<<<<", "1")
georgeData = TravelData("P", "UTO", "JORGE", "GEORGE", "G", "G30RG3ABC", "6", "UTO", "690926", "4", "M", "140511", "6", "EGROEG<<<<<<<<<", "7")
willData = TravelData("P", "UTO", "FRANKLIN", "WILLIAM", "TRAVIS", "46NQW0907", "1", "UTO", "920130", "2", "M", "160303", "9", "WX123U22XIESAL<", "9" )

#Used to make sure partial dates are accepted
partialBDayData = TravelData("P", "UTO", "ERIKSSON", "ANNA", "MARIA", "L898902C3", "6", "UTO", "74<<12", "2", "F", "120415", "9", "ZE184226B<<<<<<", "1")
partialExpirationData = TravelData("P", "UTO", "ERIKSSON", "ANNA", "MARIA", "L898902C3", "6", "UTO", "740812", "2", "F", "<<0415", "9", "ZE184226B<<<<<<", "1")

#Checks to make sure decoded data isn't too much
tooLongData = TravelData("P", "UTO", "ERIKSSON", "ANNA", tooLongLine, "L898902C3", "6", "UTO", "740812", "2", "F", "120415", "9", "TESTINGLONG<<<<", "1")
#Should throw b/c it's second line, would be padded otherwise
tooShortData = TravelData("P", "UTO", "ERIKSSON", "ANNA", "MARIA", "L898902C3", "6", "UTO", "740812", "2", "F", "120415", "9", tooShortLine, "1")

annaCheck = TravelDataError(False, False, False, False)
georgeCheck = TravelDataError(False, False, True, True)
willCheck = TravelDataError(True, True, False, False)

#Used to check if two objects have all the same field values or not, helpful for testing object equality
def checkDataEquality(d1, d2):
    d1Fields = vars(d1)
    d2Fields = vars(d2)
    keys = list(d1Fields)
    for key in keys:
        if(d1Fields[key] != d2Fields[key]):
            return False
    return True

#Since scanMRZ doesn't take in any input arguments, multiple functions mock it based on what card it would be scanning
def scanAnna():
    return (annaLine1, annaLine2)

def scanGeorge():
    return (georgeLine1, georgeLine2)

def scanWill():
    return (willLine1, willLine2)

def scanTooMuch():
    return(annaLine1, tooLongLine)

def scanTooLittle():
    return (tooShortLine, annaLine2)

def scanInvalidLast():
    return (invalidLastNameLine, annaLine2)

def scanInvalidFirst():
    return (invalidFirstNameLine, annaLine2)

def scanInvalidMiddle():
    return (invalidMiddleNameLine, annaLine2)

def scanInvalidBirthday():
    return (annaLine1, invalidBirthdayLine)

def scanPartialBirthday():
    return (annaLine1, partialBirthdayLine)

def scanInvalidExpiration():
    return (annaLine1, invalidExpirationLine)

def scanPartialExpiration():
    return (annaLine1, partialExpirationLine)


#Replicates the function of database retrieval, assumes that the personal number is unique for each user
def mockDBFunc(personalNo):
    if(personalNo == "ZE184226B<<<<<<"):
        return annaData
    if(personalNo == "EGROEG<<<<<<<<<"):
        return georgeData
    if(personalNo == "WX123U22XIESAL<"):
        return willData
    if(personalNo == "TESTINGLONG<<<<"):
        return tooLongData
    if(personalNo == tooShortLine):
        return tooShortData
    

class TestMRTD(unittest.TestCase):
    #Define multiple sets of tests as functions with names that begin

    #Make sure non-numerical characters are returning the right numerical values
    def testGetNumericalValue(self):
        self.assertEqual(getNumericalValue("A"), 10, "A should be 10")
        self.assertEqual(getNumericalValue("Z"), 35, "Z should be 35")
        self.assertEqual(getNumericalValue("<"), 0, "< should be 0")

    #Make sure check digit calculator is calculating the correct check digits
    def testCalculateCheck(self):
        self.assertEqual(calculateCheck(testData), 5, "Should be 5")
        self.assertEqual(calculateCheck(testData2), 6, "Should be 6")
        self.assertEqual(calculateCheck(testData3), 2, "Should be 2")
        self.assertEqual(calculateCheck(testData4), 9, "Should be 9")
        self.assertEqual(calculateCheck(testData5), 1, "Should be 1")

    #Test cases for decodeMRZ. Check to see that lines can be converted into data fields properly. Need multiple since a different mock is used for each scenario
    #Anna
    @mock.patch("MRTD.scanMRZ", side_effect = scanAnna)
    def testDecodeMRZ(self, mockScan):
        self.assertTrue(checkDataEquality(decodeMRZ(), annaData), "Data for Anna not being decoded correctly")

    #George
    @mock.patch("MRTD.scanMRZ", side_effect = scanGeorge)
    def testDecodeMRZ2(self, mockScan):
        self.assertTrue(checkDataEquality(decodeMRZ(), georgeData), "Data for George not being decoded correctly")

    #Will
    @mock.patch("MRTD.scanMRZ", side_effect = scanWill)
    def testDecodeMRZ3(self, mockScan):
        self.assertTrue(checkDataEquality(decodeMRZ(), willData), "Data for William not being decoded correctly")

    #Line too long
    @mock.patch("MRTD.scanMRZ", side_effect = scanTooMuch)
    def testDecodeMRZ4(self, mockScan):
        with self.assertRaises(Exception):
            decodeMRZ()

    #Line too short
    @mock.patch("MRTD.scanMRZ", side_effect = scanTooLittle)
    def testDecodeMRZ5(self, mockScan):
        with self.assertRaises(Exception):
            decodeMRZ()

    #Last name has invalid characters
    @mock.patch("MRTD.scanMRZ", side_effect = scanInvalidLast)
    def testDecodeMRZ6(self, mockScan):
        with self.assertRaises(Exception):
            decodeMRZ()

    #First name has invalid characters
    @mock.patch("MRTD.scanMRZ", side_effect = scanInvalidFirst)
    def testDecodeMRZ7(self, mockScan):
        with self.assertRaises(Exception):
            decodeMRZ()

    #Middle name has invalid characters
    @mock.patch("MRTD.scanMRZ", side_effect = scanInvalidMiddle)
    def testDecodeMRZ8(self, mockScan):
        with self.assertRaises(Exception):
            decodeMRZ()

    #Birthday has invalid characters
    @mock.patch("MRTD.scanMRZ", side_effect = scanInvalidBirthday)
    def testDecodeMRZ9(self, mockScan):
        with self.assertRaises(Exception):
            decodeMRZ()

    #Birthday has placeholder characters
    @mock.patch("MRTD.scanMRZ", side_effect = scanPartialBirthday)
    def testDecodeMRZ10(self, mockScan):
        self.assertTrue(checkDataEquality(decodeMRZ(), partialBDayData), "Data for partial birthday user not being decoded correctly")

    #Expiration Date has invalid characters
    @mock.patch("MRTD.scanMRZ", side_effect = scanInvalidExpiration)
    def testDecodeMRZ11(self, mockScan):
        with self.assertRaises(Exception):
            decodeMRZ()

    #Expiration Date has partial characters
    @mock.patch("MRTD.scanMRZ", side_effect = scanPartialExpiration)
    def testDecodeMRZ12(self, mockScan):
        self.assertTrue(checkDataEquality(decodeMRZ(), partialExpirationData), "Data for partial expiration date user not being decoded correctly")


    #Checks to see if data from database is being converted into appropriate MRZ lines
    @mock.patch("MRTD.getTravelDataFromDB", side_effect = mockDBFunc)
    def testEncodeMRZ(self, mockData):
        self.assertEqual(encodeMRZ("ZE184226B<<<<<<"), (annaLine1, annaLine2), "Data for Anna not being encoded properly")
        self.assertEqual(encodeMRZ("EGROEG<<<<<<<<<"), (georgeLine1, georgeLine2), "Data for George not being encoded properly")
        self.assertEqual(encodeMRZ("WX123U22XIESAL<"), (willLine1, willLine2), "Data for William not being encoded properly")
        with self.assertRaises(Exception):
            encodeMRZ("TESTINGLONG<<<<")
        with self.assertRaises(Exception):
            encodeMRZ(tooShortLine)

    #Checks to see if mismatch data is being calculated correctly
    def testCheckMismatches(self):
        self.assertTrue(checkDataEquality(checkMismatches(annaData), annaCheck), "Improper errors calculated for Anna")
        self.assertTrue(checkDataEquality(checkMismatches(georgeData), georgeCheck), "Improper errors calculated for George")
        self.assertTrue(checkDataEquality(checkMismatches(willData), willCheck), "Improper errors calculated for William")
        

if __name__ == '__main__':
    print('Running unit tests')
    unittest.main()
