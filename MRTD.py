class TravelData:
    #Fields
    docType
    issuingCountry
    lastName
    firstName
    middleName
    passportNo
    passportCheck
    countryCode
    birthday
    birthdayCheck
    sex
    expirationDate
    expirationCheck
    personalNo
    personalNoCheck

    def __init__(dT, iC, lN, fN, mN, passN, pC, cC, b, b, s, eD, eC, perN, perC):
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
    
    

#Functions
#General
def getNumericalValue(char):
    if len(char) != 1:
        return -1 #TODO: Might want to throw an exception instead
    elif (char >= 'A' and char <= 'Z'):
        return ord(char) - 55 #Because ord(A) = 65, and A = 10 in example
    else:
        return 0

    
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


#Requirement 2
def decodeMRZ(line1, line2):
    #TODO


#Requirement 3
def getTravelDataFromDB():
    #TODO
    
def encodeMRZ():
    #TODO


#Requirement 4
def checkMismatches():
