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
#New, used to kill boundary condition mutations
testData6 = ["a", "z"]

#For checking all the other functions
#Standard user MRZ lines
annaLine1 = "P<UTOERIKSSON<<ANNA<MARIA<<<<<<<<<<<<<<<<<<<"
annaLine2 = "L898902C36UTO7408122F1204159ZE184226B<<<<<<1"
georgeLine1 = "P<UTOJORGE<<GEORGE<G<<<<<<<<<<<<<<<<<<<<<<<<"
georgeLine2 = "G30RG3ABC6UTO6909264M1405116EGROEG<<<<<<<<<7"
#Used for encodeMRZ, since that corrects the incorrect check digits
fixedGeorgeLine2 = "G30RG3ABC6UTO6909264M1405118EGROEG<<<<<<<<<9"
willLine1 = "P<UTOFRANKLIN<<WILLIAM<TRAVIS<<<<<<<<<<<<<<<"
willLine2 = "46NQW09071UTO9201302M1603039WX123U22XIESAL<9"
#Same as George's fixed line
fixedWillLine2 = "46NQW09077UTO9201305M1603039WX123U22XIESAL<9"
#New data, used to kill name boundary mutations
nameBoundaryLine1 = "P<UTOAZaz<<AZaz<AZazBCDEFGHIJKLMNOPQRSTUVWXY"
nameBoundaryLine2 = "L898902C36UTO7408122F1204159ZE184226B000<<<1"
lastNamePad = "P<UTOAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
firstNamePad = "P<UTOA<<AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"

#Used to check edge cases for decoding MRZ. Besides too long/too short, they are based off of Anna's lines
tooLongLine = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
tooShortLine = "B"
invalidLastNameLine = "P<UTOERIKSS0N<<ANNA<MARIA<<<<<<<<<<<<<<<<<<<"
invalidFirstNameLine = "P<UTOERIKSSON<<ANN@<MARIA<<<<<<<<<<<<<<<<<<<"
invalidMiddleNameLine = "P<UTOERIKSSON<<ANNA<MAR1A<<<<<<<<<<<<<<<<<<<"
invalidBirthdayLine = "L898902C36UTO7!08122F1204159ZE184226B<<<<<<1" #Newly altered line to handle edge case
partialBirthdayLine = "L898902C36UTO74<<122F1204159ZE184226B<<<<<<1"
invalidExpirationLine = "L898902C36UTO7408122F1204L59ZE184226B<<<<<<1"
partialExpirationLine = "L898902C36UTO7408122F<<04159ZE184226B<<<<<<1"

#Three users
annaData = TravelData("P", "UTO", "ERIKSSON", "ANNA", "MARIA", "L898902C3", "6", "UTO", "740812", "2", "F", "120415", "9", "ZE184226B<<<<<<", "1")
georgeData = TravelData("P", "UTO", "JORGE", "GEORGE", "G", "G30RG3ABC", "6", "UTO", "690926", "4", "M", "140511", "6", "EGROEG<<<<<<<<<", "7")
willData = TravelData("P", "UTO", "FRANKLIN", "WILLIAM", "TRAVIS", "46NQW0907", "1", "UTO", "920130", "2", "M", "160303", "9", "WX123U22XIESAL<", "9" )
#New data, used to kill name boundary mutations
nameBoundaryData = TravelData("P", "UTO", "AZaz", "AZaz", "AZazBCDEFGHIJKLMNOPQRSTUVWXY", "L898902C3", "6", "UTO", "740812", "2", "F", "120415", "9", "ZE184226B000<<<", "1")
lastPadData = TravelData("P", "UTO", "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA", "", "", "L898902C3", "6", "UTO", "740812", "2", "F", "120415", "9", "ZE184226B<<<<<<", "1")
firstPadData = TravelData("P", "UTO", "A", "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA", "", "L898902C3", "6", "UTO", "740812", "2", "F", "120415", "9", "ZE184226B<<<<<<", "1")

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

#New mock, used to check edge boundaries
def scanBoundary():
    return (nameBoundaryLine1, nameBoundaryLine2)

def scanLastPad():
    return (lastNamePad, annaLine2)

def scanFirstPad():
    return (firstNamePad, annaLine2)


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
    if(personalNo == "ZE184226B000<<<"): #New clause, Used to test line length boundaries in encodeMRZ
        return nameBoundaryData

class TestMRTD(unittest.TestCase):
    #Define multiple sets of tests as functions with names that begin

    #Make sure non-numerical characters are returning the right numerical values
    def testGetNumericalValue(self):
        self.assertEqual(getNumericalValue("A"), 10, "A should be 10")
        self.assertEqual(getNumericalValue("a"), 10, "a should be 10") #New test case
        self.assertEqual(getNumericalValue("Z"), 35, "Z should be 35")
        self.assertEqual(getNumericalValue("z"), 35, "z should be 35") #New test case
        self.assertEqual(getNumericalValue("D"), 13, "D should be 13") #New test case
        self.assertEqual(getNumericalValue("d"), 13, "d should be 13") #New test case
        self.assertEqual(getNumericalValue("W"), 32, "W should be 32") #New test case
        self.assertEqual(getNumericalValue("w"), 32, "w should be 32") #New test case
        self.assertEqual(getNumericalValue("<"), 0, "< should be 0")

    #Make sure check digit calculator is calculating the correct check digits
    def testCalculateCheck(self):
        self.assertEqual(calculateCheck(testData), 5, "Should be 5")
        self.assertEqual(calculateCheck(testData2), 6, "Should be 6")
        self.assertEqual(calculateCheck(testData3), 2, "Should be 2")
        self.assertEqual(calculateCheck(testData4), 9, "Should be 9")
        self.assertEqual(calculateCheck(testData5), 1, "Should be 1")
        self.assertEqual(calculateCheck(testData6), 5, "Should be 5") #New test case

    #New Test, kills off mutations that change default values for TravelData to mutpy
    def testInitTravelData(self):
        initData = TravelData()
        self.assertEqual(initData.docType, "")
        self.assertEqual(initData.issuingCountry, "")
        self.assertEqual(initData.lastName, "")
        self.assertEqual(initData.firstName, "")
        self.assertEqual(initData.middleName, "")
        self.assertEqual(initData.passportNo, "")
        self.assertEqual(initData.passportCheck, "")
        self.assertEqual(initData.countryCode, "")
        self.assertEqual(initData.birthday, "")
        self.assertEqual(initData.birthdayCheck, "")
        self.assertEqual(initData.sex, "")
        self.assertEqual(initData.expirationDate, "")
        self.assertEqual(initData.expirationCheck, "")
        self.assertEqual(initData.personalNo, "")
        self.assertEqual(initData.personalNoCheck, "")

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

    #New Test Case, Checks the length of Anna's second line fields
    @mock.patch("MRTD.scanMRZ", side_effect = scanAnna)
    def testFieldLengths(self, mockScan):
        scanData = decodeMRZ()
        self.assertEqual(len(scanData.passportNo), 9)
        self.assertEqual(len(scanData.countryCode), 3)
        self.assertEqual(len(scanData.birthday), 6)
        self.assertEqual(len(scanData.sex), 1)
        self.assertEqual(len(scanData.expirationDate), 6)
        self.assertEqual(len(scanData.personalNo), 15)

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

    #New test, used to kill mutations for name boundaries
    @mock.patch("MRTD.scanMRZ", side_effect = scanBoundary)
    def testDecodeMRZ13(self, mockScan):
        self.assertTrue(checkDataEquality(decodeMRZ(), nameBoundaryData), "Data for name boundary not being decoded correctly")

    #New test, used to kill mutations for name boundaries
    @mock.patch("MRTD.scanMRZ", side_effect = scanLastPad)
    def testDecodeMRZ14(self, mockScan):
        self.assertTrue(checkDataEquality(decodeMRZ(), lastPadData), "Data for last name padding not being decoded correctly")

    #New test, used to kill mutations for name boundaries
    @mock.patch("MRTD.scanMRZ", side_effect = scanFirstPad)
    def testDecodeMRZ15(self, mockScan):
        self.assertTrue(checkDataEquality(decodeMRZ(), firstPadData), "Data for first name padding not being decoded correctly")
    
    #Checks to see if data from database is being converted into appropriate MRZ lines
    @mock.patch("MRTD.getTravelDataFromDB", side_effect = mockDBFunc)
    def testEncodeMRZ(self, mockData):
        self.assertEqual(encodeMRZ("ZE184226B<<<<<<"), (annaLine1, annaLine2), "Data for Anna not being encoded properly")
        self.assertEqual(encodeMRZ("EGROEG<<<<<<<<<"), (georgeLine1, fixedGeorgeLine2), "Data for George not being encoded properly")
        self.assertEqual(encodeMRZ("WX123U22XIESAL<"), (willLine1, fixedWillLine2), "Data for William not being encoded properly")
        self.assertEqual(encodeMRZ("ZE184226B000<<<"), (nameBoundaryLine1, nameBoundaryLine2), "Data for name boundary not being encoded properly")
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
