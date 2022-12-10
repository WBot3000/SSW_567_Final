import json

with open("records_encoded.json", "r") as persondata:
    encoded = json.load(persondata)["records_encoded"]


encodedLists = [item.split(";") for item in encoded]

# print(encodedLists[2][1])


line1 = []
line2 = []
PASSPORT_LENGTH = 9
COUNTRY_CODE_LENGTH = 3
DATE_LENGTH = 6
SEX_LENGTH = 1
LINE_LENGTH = 44
#PERSONAL_NUMBER_LENGTH = 9 #Commented out b/c I think this is actually variable

#TODO: Should checks be stored as strings or integers?
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

    def __init__(self, dT=None, iC=None, lN=None, fN=None, mN=None, passN=None, pC=None, cC=None, b=None, bC=None, s=None, eD=None, eC=None, perN=None, perC=None):
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

#    def printData(self): #Check digits are in parenthesis next to the appropriate field
#        print("Document Type: " + self.docType)
#        print("Issuing Country: " + self.issuingCountry)
#        print("Last Name: " + self.lastName)
#        print("First Name: " + self.firstName)
#        print("Middle Name: " + self.middleName)
#        print("Passport Number: " + self.passportNo + " (" + self.passportCheck + ")")
#        print("Country Code: " + self.countryCode)
#        print("Birthday: " + self.birthday + " (" + self.birthdayCheck + ")")
#        print("Sex: " + self.sex)
#        print("Expiration Date: " + self.expirationDate + " (" + self.expirationCheck + ")")
#        print("Personal Number: " + self.personalNo + " (" + self.personalNoCheck + ")")



#TODO: Should this have a reference to the TravelData it checks?
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

#    def report(self):
#        errorsFound = False
#        if(self.passportError):
#            print("Error in Passport Check Digit")
#            errorsFound = True
#        if(self.birthdayError):
#            print("Error in Birthday Check Digit")
#            errorsFound = True
#        if(self.expirationError):
#            print("Error in Expiration Date Check Digit")
#            errorsFound = True
#        if(self.personalError):
#            print("Error in Personal Number Check Digit")
#            errorsFound = True
#        if(not errorsFound):
#            print("No errors found")


#Functions
#General
def getNumericalValue(i):
    try:
        int(i)
        return int(i)
    except ValueError:
        if (str(i) >= 'A' and str(i) <= 'Z'):
            return int(ord(str(i)) - 55)
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
def scanMRZ(x):
    for i in range(100):
        line1.append(encodedLists[i][0])
        line2.append(encodedLists[i][1])

    return (line1, line2)

# print(scanMRZ()[0])
# print(scanMRZ()[1])

#Requirement 2
#Each line seems to be 44 characters
def decodeMRZ():
    (line1, line2) = scanMRZ(100)

    for i in line1:
        for j in line2:
            
            if(len(i) != LINE_LENGTH or len(j) != LINE_LENGTH):
                raise Exception("Lines must both be " + str(LINE_LENGTH) + " characters.")
            travelData = TravelData()
            linePos = 0
            #Reading Line 1
            currentString = "" #Used for variable sized strings
            travelData.docType = i[linePos:linePos+1]
            linePos += 2 #To account for <
            travelData.issuingCountry = i[linePos:linePos+3]
            linePos +=3
            while(i[linePos] != "<"): #Parsing last name
                if(i[linePos] < "A" or i[linePos] > "Z"): #Check to make sure the name is valid
                    raise Exception("Invalid character " + i[linePos] + " in last name")
                currentString += i[linePos]
                linePos += 1
            travelData.lastName = currentString
            linePos += 2 #Skip the second < and go straight to the first letter of the first name
            currentString = "" #So you can use it again for the other fields
            while(i[linePos] != "<"):
                if(i[linePos] < "A" or i[linePos] > "Z"):
                    raise Exception("Invalid character " + i[linePos] + " in first name")
                currentString += i[linePos]
                linePos += 1
            travelData.firstName = currentString
            linePos += 1
            currentString = ""
            while(i[linePos] != "<"):
                if(i[linePos] < "A" or i[linePos] > "Z"):
                    raise Exception("Invalid character " + i[linePos] + " in middle name")
                currentString += i[linePos]
                linePos += 1
            travelData.middleName = currentString
            currentString = "" #Not necessary, just used to keep pattern
    

    #Reading Line 2
            linePos = 0
            travelData.passportNo = j[linePos:PASSPORT_LENGTH]
            linePos += PASSPORT_LENGTH
            travelData.passportCheck = j[linePos:linePos+1]
            linePos += 1
            travelData.countryCode = j[linePos:linePos+COUNTRY_CODE_LENGTH]
            linePos += COUNTRY_CODE_LENGTH
            travelData.birthday = j[linePos:linePos+DATE_LENGTH]
            validateDate(travelData.birthday)
            linePos += DATE_LENGTH
            travelData.birthdayCheck = j[linePos:linePos+1]
            linePos += 1
            travelData.sex = j[linePos:linePos+SEX_LENGTH]
            linePos += 1
            travelData.expirationDate = j[linePos:linePos+DATE_LENGTH]
            validateDate(travelData.expirationDate)
            linePos += DATE_LENGTH
            travelData.expirationCheck = j[linePos:linePos+1]
            linePos += 1
            travelData.personalNo = j[linePos:len(j)-1]
            linePos = len(j)-1
            travelData.personalNoCheck = j[linePos]
            linePos += 1 #Technically unneccesary but did it to keep consistency
            return travelData

decodeMRZ()

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
    line2 = data.passportNo + data.passportCheck + data.countryCode + data.birthday + data.birthdayCheck + data.sex + data.expirationDate + data.expirationCheck + data.personalNo + data.personalNoCheck
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

