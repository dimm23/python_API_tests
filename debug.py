import unittest
import json
import time
import re
import api
import settings
import pandas as pd

class MyTestResult(unittest.TestResult):
    def addFailure(self, test, err):
        #print(str(test) + ": " + str(err))
        test_name = str(test).split(" ")[0]
        print(str(test_name) + ": Failed")
        super(MyTestResult, self).addFailure(test, err)

    def addError(self, test, err):
        test_name = str(test).split(" ")[0]
        print(str(test_name) + ": " + str(err[1]))
        super(MyTestResult, self).addError(test, err)

class All_api_methods_testing(unittest.TestCase):
    u = api.Utopia("http://127.0.0.1:"+settings.API_PORT+"/api/1.0",settings.TOKEN)
    pattern = re.compile("^([A-Z0-9]){32}")   
    getInvoicesParams = '{ "cardId": "", "invoiceId": "", "pk": "", "transactionId": "", "status": "", "startDateTime": "", "endDateTime": "", "referenceNumber": "" }'
    
    def setUp(self):        
        self.status = False        
       
    def test_deleteCard(self):
        # Setup
        result = ""
        card = list()
        
        # Action
        s, cards = self.u.getCards()        
        if len(cards) < 30 and not 'error' in cards:
            card = list(filter(lambda x: x['name'] == 'API card' or '', cards))
            if len(card) == 0:                
                self.u.addCard("#FBEDC0","API card", "")
                time.sleep(3)
                s, cards = self.u.getCards()
                card = list(filter(lambda x: x['name'] == 'API card', cards))
                print("DEBUG: card: " + str(card[0]))
        elif 'error' in cards:
            raise Exception("Error in getCards: " + str(cards))
        else:
            card = list(filter(lambda x: x['name'] == 'API card' or '', cards))
        try:
            self.status, result = self.u.deleteCard(card[0]['cardid'])
            print("delete result: " + str(result))
        except Exception as e:
            print("Exception: " + str(e))                
        finally:
            # Assertion
            self.assertTrue(self.status)
            self.assertTrue(self.pattern.match(str(result)), "Result '" + str(result) + "' is not reference number")
               
    def tearDown(self):
        #print("status: " + str(self.status))
        #print("result: " + str(self.result))
        try:
            if "error" in str(self.result):
                print("If result: " + str(self.result))
            self.assertFalse("Unable" in str(self.result), msg = "result: " + str(self.result))
        except Exception:
            time.sleep(0.001)            
        self.assertTrue(bool(self.status), "Status of request execution is False")

if __name__ == "__main__":
    unittest.main(testRunner=unittest.TextTestRunner(resultclass=MyTestResult))
