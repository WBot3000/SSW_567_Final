PASSPORT_LENGTH = 9
COUNTRY_CODE_LENGTH = 3
DATE_LENGTH = 6
SEX_LENGTH = 1
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

    def __init__():
        pass

    def __init__(dT, iC, lN, fN, mN, passN, pC, cC, b, bC, s, eD, eC, perN, perC):
        docType = dT
        issuingCountry = iC
        lastName = lN
        firstName = fN
        middleName = mN
        passportNo = passN
        passportCheck = pC
        countryCode = cC
        birthday = b
        birthdayCheck = bC
        sex = s
        expirationDate = eD
        expirationCheck = eC
        personalNo = perN
        personalNoCheck = perC

#TODO: Should this have a reference to the TravelData it checks?
class TravelDataError:
    #Fields (all booleans)
    #passportError
    #birthdayError
    #expirationError
    #personalError

    def __init__(): #Assume that there are no errors to begin with
        passportError = False
        birthdayError = False
        expirationError = False
        personalError = False


#Functions
#General
def getNumericalValue(char):
    if len(char) != 1:
        return -1 #TODO: Might want to throw an exception instead
    elif (char >= 'A' and char <= 'Z'):
        return ord(char) - 55 #Because ord(A) = 65, and A = 10 in example
    else:
        return 0

#TODO: Should this return a string instead?
def calculateCheck(field):
    weights = [7, 3, 1]
    weightIdx = 0
    total = 0
    for char in field:
        numVal = getNumericalValue(char)
        total += (numVal * weights[weightIdx])
        weightIdx = (weightIdx + 1) % len(weights)
    return total % 10
    

#Requirement 1
def scanMRZ():
    #Empty function
    return


#Requirement 2
#Each line seems to be 44 characters
def decodeMRZ(line1, line2):
    #TODO
    travelData = TravelData()
    linePos = 0
    currentString = ""
    #Reading Line 1
    #TODO

    #Reading Line 2
    linePos = 0
    travelData.passportNo = line2[linePos:PASSPORT_LENGTH]
    linePos += PASSPORT_LENGTH
    travelData.passportCheck = line2[linePos:linePos+1]
    linePos += 1
    travelData.countryCode = line2[linePos:linePos+COUNTRY_CODE_LENGTH]
    linePos += COUNTRY_CODE_LENGTH
    travelData.birthday = line2[linePos:linePos+DATE_LENGTH]
    linePos += DATE_LENGTH
    travelData.birthdayCheck = line2[linePos:linePos+1]
    linePos += 1
    travelData.sex = line2[linePos:linePos+SEX_LENGTH]
    linePos += 1
    travelData.expirationDate = line2[linePos:linePos+DATE_LENGTH]
    linePos += DATE_LENGTH
    travelData.expirationCheck = line2[linePos:linePos+1]
    linePos += 1
    travelData.personalNo = line2[linePos:len(line2)-1]
    linePos = len(line2)-1
    travelData.personalNoCheck = line2[linePos]
    linePos += 1 #Technically unneccesary but did it to keep consistency
    return travelData


#Requirement 3
def getTravelDataFromDB():
    #Empty function
    return
    
def encodeMRZ():
    #TODO
    return


#Requirement 4
def checkMismatches(travelData):
    #TODO
    errors = TravelDataError()
    if (int(travelData.passportCheck) == calculateCheck(travelData.passport)):
        errors.passportError = True
    if (int(travelData.birthdayCheck) == calculateCheck(travelData.birthday)):
        errors.birthdayError = True
    if (int(travelData.expirationCheck) == calculateCheck(travelData.expirationDate)):
        errors.expirationError = True
    if (int(travelData.personalNoCheck) == calculateCheck(travelData.personalNo)):
        errors.personalError = True
    return errors