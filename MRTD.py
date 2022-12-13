PASSPORT_LENGTH = 9
COUNTRY_CODE_LENGTH = 3
DATE_LENGTH = 6
SEX_LENGTH = 1
LINE_LENGTH = 44

class TravelData:
    #Fields (all are stored as strings)
    #docType
    #issuingCountry
    #lastName
    #firstName
    #middleName
    #passportNo
    #passportCheck
    #countryCode
    #birthday
    #birthdayCheck
    #sex
    #expirationDate
    #expirationCheck
    #personalNo
    #personalNoCheck

    def __init__(self, dT="", iC="", lN="", fN="", mN="", passN="", pC="", cC="", b="", bC="", s="", eD="", eC="", perN="", perC=""):
        self.docType = dT
        self.issuingCountry = iC
        self.lastName = lN
        self.firstName = fN
        self.middleName = mN
        self.passportNo = passN
        self.passportCheck = pC
        self.countryCode = cC
        self.birthday = b
        self.birthdayCheck = bC
        self.sex = s
        self.expirationDate = eD
        self.expirationCheck = eC
        self.personalNo = perN
        self.personalNoCheck = perC



class TravelDataError:
    #Fields (all booleans)
    #passportError
    #birthdayError
    #expirationError
    #personalError

    def __init__(self, passE=False, bE=False, eE=False, perE=False): #Assume that there are no errors to begin with
        self.passportError = passE
        self.birthdayError = bE
        self.expirationError = eE
        self.personalError = perE



#Functions
#General
def getNumericalValue(i):
    try:
        int(i)
        return int(i)
    except ValueError:
        if (str(i) >= 'A' and str(i) <= 'Z'):
            return int(ord(str(i)) - 55)
        elif(str(i) >= 'a' and str(i) <= 'z'):
            return int(ord(str(i)) - 87)
        else:
            return 0

def calculateCheck(lst):
    weights = [7, 3, 1]
    weightIdx = 0
    total = 0
    
    for i in lst:
        numVal = getNumericalValue(i)
        total += (numVal * weights[weightIdx])
        weightIdx = (weightIdx + 1) % len(weights)
    return total % 10

def validateDate(date):
    for char in date:
        if(char != "<" and (char < "0" or char > "9")):
            raise Exception("Invalid character " + char + " in date")
    

#Requirement 1
def scanMRZ():
    #Empty function, needs to be mocked
    return


#Requirement 2
#Each line seems to be 44 characters
def decodeMRZ():
    (line1, line2) = scanMRZ()
    if(len(line1) != LINE_LENGTH or len(line2) != LINE_LENGTH):
        raise Exception("Lines must both be " + str(LINE_LENGTH) + " characters.")
    travelData = TravelData()
    linePos = 0
    #Reading Line 1
    currentString = "" #Used for variable sized strings
    travelData.docType = line1[linePos:linePos+1]
    linePos += 2 #To account for <
    travelData.issuingCountry = line1[linePos:linePos+3]
    linePos +=3
    while(line1[linePos] != "<" and linePos < LINE_LENGTH): #Parsing last name
        if(line1[linePos] < "A" or line1[linePos] > "Z"): #Check to make sure the name is valid
            raise Exception("Invalid character " + line1[linePos] + " in last name")
        currentString += line1[linePos]
        linePos += 1
    travelData.lastName = currentString
    linePos += 2 #Skip the second < and go straight to the first letter of the first name
    currentString = "" #So you can use it again for the other fields
    while(line1[linePos] != "<" and linePos < LINE_LENGTH):
        if(line1[linePos] < "A" or line1[linePos] > "Z"):
            raise Exception("Invalid character " + line1[linePos] + " in first name")
        currentString += line1[linePos]
        linePos += 1
    travelData.firstName = currentString
    linePos += 1
    currentString = ""
    while(line1[linePos] != "<" and linePos < LINE_LENGTH):
        if(line1[linePos] < "A" or line1[linePos] > "Z"):
            raise Exception("Invalid character " + line1[linePos] + " in middle name")
        currentString += line1[linePos]
        linePos += 1
    travelData.middleName = currentString
    currentString = "" #Not necessary, just used to keep pattern
    

    #Reading Line 2
    linePos = 0
    travelData.passportNo = line2[linePos:PASSPORT_LENGTH]
    linePos += PASSPORT_LENGTH
    travelData.passportCheck = line2[linePos:linePos+1]
    linePos += 1
    travelData.countryCode = line2[linePos:linePos+COUNTRY_CODE_LENGTH]
    linePos += COUNTRY_CODE_LENGTH
    travelData.birthday = line2[linePos:linePos+DATE_LENGTH]
    validateDate(travelData.birthday)
    linePos += DATE_LENGTH
    travelData.birthdayCheck = line2[linePos:linePos+1]
    linePos += 1
    travelData.sex = line2[linePos:linePos+SEX_LENGTH]
    linePos += 1
    travelData.expirationDate = line2[linePos:linePos+DATE_LENGTH]
    validateDate(travelData.expirationDate)
    linePos += DATE_LENGTH
    travelData.expirationCheck = line2[linePos:linePos+1]
    linePos += 1
    travelData.personalNo = line2[linePos:len(line2)-1]
    linePos = len(line2)-1
    travelData.personalNoCheck = line2[linePos]
    linePos += 1 #Technically unneccesary but did it to keep consistency
    return travelData


#Requirement 3
def getTravelDataFromDB(personalNo):
    #Empty function, needs to be mocked
    return

#TODO: Determine whether a line being too long/short throws an error or is just padded/cut off
def encodeMRZ(personalNo):
    data = getTravelDataFromDB(personalNo) #What needs to be mocked in test cases, this implementation expects a TravelData object
    #Encoding Line 1
    line1 = data.docType + "<" + data.issuingCountry + data.lastName + "<<" + data.firstName + "<" + data.middleName
    if (len(line1) > LINE_LENGTH):
        raise Exception("First line is not " + str(LINE_LENGTH) + " characters.")
    while(len(line1) < LINE_LENGTH):
        line1 += "<"

    #Encoding Line 2
    line2 = data.passportNo + str(calculateCheck(data.passportNo)) + data.countryCode + data.birthday + str(calculateCheck(data.birthday)) + data.sex + data.expirationDate + str(calculateCheck(data.expirationDate)) + data.personalNo + str(calculateCheck(data.personalNo))
    #NOTE: Padding is stored in the personal number according to decodeMRZ, so none added here
    if (len(line2) != LINE_LENGTH):
        raise Exception("Second line is not " + str(LINE_LENGTH) + " characters.")
    return (line1, line2)


#Requirement 4
def checkMismatches(travelData):
    #TODO
    errors = TravelDataError()
    if (int(travelData.passportCheck) != calculateCheck(travelData.passportNo)):
        errors.passportError = True
    else:
        errors.passportError = False

    if (int(travelData.birthdayCheck) != calculateCheck(travelData.birthday)):
        errors.birthdayError = True
    else:
        errors.birthdayError = False

    if (int(travelData.expirationCheck) != calculateCheck(travelData.expirationDate)):
        errors.expirationError = True
    else:
        errors.expirationError = False

    if (int(travelData.personalNoCheck) != calculateCheck(travelData.personalNo)):
        errors.personalError = True
    else:
        errors.personalError = False
    return errors

#def quickRun():
#    line1 = "P<UTOERIKSSON<<ANNA<MARIA<<<<<<<<<<<<<<<<<<<"
#    line2 = "L898902C36UTO7408122F1204159ZE184226B<<<<<<1"
#    data = decodeMRZ(line1, line2)
#    data.printData()
#    errors = checkMismatches(data)
#    errors.report()

