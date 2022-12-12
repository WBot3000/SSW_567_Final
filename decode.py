import unittest
import json
import time
import csv
from unittest import mock
from MRTD import TravelData, TravelDataError, getNumericalValue, calculateCheck, decodeMRZ, encodeMRZ, checkMismatches

tooShortLine = "B"
tooShortData = TravelData("P", "UTO", "ERIKSSON", "ANNA", "MARIA", "L898902C3", "6", "UTO", "740812", "2", "F", "120415", "9", tooShortLine, "1")
annaData = TravelData("P", "UTO", "ERIKSSON", "ANNA", "MARIA", "L898902C3", "6", "UTO", "740812", "2", "F", "120415", "9", "ZE184226B<<<<<<", "1")
annaLine1 = "P<UTOERIKSSON<<ANNA<MARIA<<<<<<<<<<<<<<<<<<<"
annaLine2 = "L898902C36UTO7408122F1204159ZE184226B<<<<<<1"

row_list = [["Value of k","Time without unit tests","Time with unit tests"]]

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

def checkDataEquality(d1, d2):
    d1Fields = vars(d1)
    d2Fields = vars(d2)
    keys = list(d1Fields)
    for key in keys:
        if(d1Fields[key] != d2Fields[key]):
            # print(d1Fields[key])
            # print(d2Fields[key])
            return False
    return True


def runIt():
    k = 100
    maxK = 10000
    while k <= maxK:
        tic = time.perf_counter()
        
        for i in range(0,k):
                # print(data["records_decoded"][i]["line1"]["issuing_country"])
                tempData = TravelData("P", data["records_decoded"][i]["line1"]["issuing_country"], data["records_decoded"][i]["line1"]["last_name"], data["records_decoded"][i]["line1"]["given_name"].split()[0], "" if len(data["records_decoded"][i]["line1"]["given_name"].split()) == 1 else data["records_decoded"][i]["line1"]["given_name"].split()[1], data["records_decoded"][i]["line2"]["passport_number"], str(calculateCheck(data["records_decoded"][i]["line2"]["passport_number"])),  data["records_decoded"][i]["line2"]["country_code"], data["records_decoded"][i]["line2"]["birth_date"], str(calculateCheck(data["records_decoded"][i]["line2"]["birth_date"])), data["records_decoded"][i]["line2"]["sex"], data["records_decoded"][i]["line2"]["expiration_date"], str(calculateCheck(data["records_decoded"][i]["line2"]["expiration_date"])), data["records_decoded"][i]["line2"]["personal_number"] + "<<<<<<", str(calculateCheck(data["records_decoded"][i]["line2"]["personal_number"])))
                assert encodeMRZ(tempData) == (encodedData["records_encoded"][i].split(";")[0],encodedData["records_encoded"][i].split(";")[1]), "Data for {} not being decoded correctly".format(i)
            
        toc = time.perf_counter()
        print("Time Taken:", (toc - tic)*1000)
        row_list.append([str(k),str((toc-tic)*1000)])
        if k == 100:
            k = 1000
        else:
            k += 1000

encodedData = json.load(open("records_encoded.json"))
data = json.load(open("records_decoded.json"))

class encodetest(unittest.TestCase):

    # def scanEnc(ctr):
    #     return (encodedData["records_encoded"][ctr].split(";")[0],encodedData["records_encoded"][ctr].split(";")[1])

    # def mockDBFunc(personalNo):
    #     print("--------------",personalNo)
    #     if (personalNo == "ZE184226B<<<<<<"):
    #         return annaData
    #     if (personalNo == tooShortLine):
    #         return tooShortData
    

    # @mock.patch("MRTD.getTravelDataFromDB", side_effect = scanEnc)
    def testEncodeMRZ(self):

        k = 100
        maxK = 10000
        row_num = 1
        while k <= maxK:

            tic = time.perf_counter()
            for i in range(0,k):
                with self.subTest("Message for this subtest", i=i):
                    # print(data["records_decoded"][i]["line1"]["issuing_country"])
                    tempData = TravelData("P", data["records_decoded"][i]["line1"]["issuing_country"], data["records_decoded"][i]["line1"]["last_name"], data["records_decoded"][i]["line1"]["given_name"].split()[0], "" if len(data["records_decoded"][i]["line1"]["given_name"].split()) == 1 else data["records_decoded"][i]["line1"]["given_name"].split()[1], data["records_decoded"][i]["line2"]["passport_number"], str(calculateCheck(data["records_decoded"][i]["line2"]["passport_number"])),  data["records_decoded"][i]["line2"]["country_code"], data["records_decoded"][i]["line2"]["birth_date"], str(calculateCheck(data["records_decoded"][i]["line2"]["birth_date"])), data["records_decoded"][i]["line2"]["sex"], data["records_decoded"][i]["line2"]["expiration_date"], str(calculateCheck(data["records_decoded"][i]["line2"]["expiration_date"])), data["records_decoded"][i]["line2"]["personal_number"] + "<<<<<<", str(calculateCheck(data["records_decoded"][i]["line2"]["personal_number"])))
                    self.assertEqual(encodeMRZ(tempData), (encodedData["records_encoded"][i].split(";")[0],encodedData["records_encoded"][i].split(";")[1]), "Data for Anna not being decoded correctly")
            
            toc = time.perf_counter()

            print("Time Taken:", (toc - tic)*1000)
            row_list[row_num].append(str((toc-tic)*1000))
            row_num += 1
            if k == 100:
                k = 1000
            else:
                k += 1000
        
        with open('timegraph.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(row_list)
                # print("----------------",encodeMRZ(tempData))
        # self.assertEqual(encodeMRZ("ZE184226B<<<<<<"), (annaLine1,
        #                  annaLine2), "Data for Anna not being encoded properly")
        # with self.assertRaises(Exception):
        #     encodeMRZ("TESTINGLONG<<<<")
        # with self.assertRaises(Exception):
        #     encodeMRZ(tooShortLine)

    # @mock.patch("MRTD.scanMRZ", side_effect = scanEnc)
    # def testDecodeMRZ(self, mockScan):
        
 



if __name__ == '__main__':
    print('Running unit tests')
    runIt()
    unittest.main()
    # data = json.load(f)
    # print(data["records_decoded"][0])
    # annaData = TravelData("P", "UTO", "ERIKSSON", "ANNA", "MARIA", "L898902C3", "6", "UTO", "740812", "2", "F", "120415", "9", "ZE184226B<<<<<<", "1")
    # tempData = TravelData("P", data["records_decoded"][0]["line1"]["issuing_country"], data["records_decoded"][0]["line1"]["last_name"], data["records_decoded"][0]["line1"]["given_name"], "", data["records_decoded"][0]["line2"]["passport_number"], "6",  data["records_decoded"][0]["line2"]["country_code"], data["records_decoded"][0]["line2"]["birth_date"], "2", data["records_decoded"][0]["line2"]["sex"],  data["records_decoded"][0]["line2"]["expiration_date"], "9", data["records_decoded"][0]["line2"]["personal_number"] + "<<<<<<", 1)
    # encodedData = json.load(open('records_encoded.json'))
    # print(encodedData["records_encoded"][0])
    # print(str(tempData))
    # print(calculateCheck("591010"))

print("I am here")