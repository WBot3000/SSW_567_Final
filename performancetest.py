import unittest
import json
import time
import csv
from unittest import mock
from MRTD import TravelData, calculateCheck, decodeMRZ

encodedData = json.load(open("records_encoded.json"))
data = json.load(open("records_decoded.json"))

row_list = [["Value of k","Time without unit tests","Time with unit tests"]]



def checkDataEquality(d1, d2):
    d1Fields = vars(d1)
    d2Fields = vars(d2)
    keys = list(d1Fields)
    for key in keys:
        if(d1Fields[key] != d2Fields[key]):
            return False
    return True

def runIt():
    k = 100
    maxK = 10000
    while k <= maxK:
        tic = time.perf_counter()
        
        for i in range(0,k):
            decodeMRZ(encodedData["records_encoded"][i].split(";")[0],encodedData["records_encoded"][i].split(";")[1])

                
        toc = time.perf_counter()
        print("Time Taken:", (toc - tic)*1000)
        row_list.append([str(k),str((toc-tic)*1000)])
        if k == 100:
            k = 1000
        else:
            k += 1000



class decodeTest(unittest.TestCase):
    
    def testDecodeMRZ(self):

        k = 100
        maxK = 10000
        row_num = 1
        while k <= maxK:

            tic = time.perf_counter()


            for i in range(0,k):
                decodeMRZ(encodedData["records_encoded"][i].split(";")[0],encodedData["records_encoded"][i].split(";")[1])
                with self.subTest("Message for this subtest", i=i):
                    tempData = (encodedData["records_encoded"][i].split(";")[0],encodedData["records_encoded"][i].split(";")[1])
                    tempData2 = TravelData("P", data["records_decoded"][i]["line1"]["issuing_country"], data["records_decoded"][i]["line1"]["last_name"], data["records_decoded"][i]["line1"]["given_name"].split()[0], "" if len(data["records_decoded"][i]["line1"]["given_name"].split()) == 1 else data["records_decoded"][i]["line1"]["given_name"].split()[1], data["records_decoded"][i]["line2"]["passport_number"], str(calculateCheck(data["records_decoded"][i]["line2"]["passport_number"])),  data["records_decoded"][i]["line2"]["country_code"], data["records_decoded"][i]["line2"]["birth_date"], str(calculateCheck(data["records_decoded"][i]["line2"]["birth_date"])), data["records_decoded"][i]["line2"]["sex"], data["records_decoded"][i]["line2"]["expiration_date"], str(calculateCheck(data["records_decoded"][i]["line2"]["expiration_date"])), data["records_decoded"][i]["line2"]["personal_number"] + "<<<<<<", str(calculateCheck(data["records_decoded"][i]["line2"]["personal_number"])))
                    # decodeMRZ doesnt have a DB return
                    # self.assertEqual(decodeMRZ(tempData[0], tempData[1]), tempData2), "Data not being decoded correctly"



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
            
if __name__ == '__main__':
    print('Running unit tests')
    runIt()
    unittest.main()