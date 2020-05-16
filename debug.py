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
    getInvoicesParams = '{ "cardId": "", "invoiceId": "", "pk": "", "transactionId": "", "status": "", ' \
                        '"startDateTime": "", "endDateTime": "", "referenceNumber": "" }'
    
    def setUp(self):        
        self.status = False

    def test_requestUnsTransfer(self, pk: str = settings.CONTACT_PK) -> json:
        """Method requestUnsTransfer allows to transfer the uNS record to contact. The method is called with mandatory
        'Name' and 'Public Key' parameters. Name parameter is the name of the uNS record from the list of own uNS
        records. hexNewOwnerPk represents hash of the public portion of the key (as in some instances, key is now
        known, only hash is), to which the transfer is being made. In the Response field the status of completion of
        the operation is displayed."""

        # Action
        _, unss = self.u.unsRegisteredNames()
        print(unss)
        if len(unss) > 0 and 'error' not in unss:
            try:
                self.status, self.result = self.u.requestUnsTransfer(str(unss[0]['nick']), pk)
            except Exception as e:
                print(e)
        else:
            self.u.unsCreateRecordRequest(settings.random_uns)
            _, unss = self.u.unsRegisteredNames()
            self.status, self.result = self.u.requestUnsTransfer(unss[0]['nick'], pk)

        # Assertion
        self.assertTrue(self.status, "Status or request: " + str(self.status) + ". uNS is " + str(unss[0]['nick']))
        self.assertTrue(self.result != "" and "error" not in str(self.result), str(self.result))

    def tearDown(self):
        print("status: " + str(self.status))
        print("result: " + str(self.result))
        try:
            if "error" in str(self.result):
                print("If result: " + str(self.result))
            self.assertFalse("Unable" in str(self.result), msg = "result: " + str(self.result))
        except Exception:
            time.sleep(0.001)            
        self.assertTrue(bool(self.status), "Status of request execution is False")

if __name__ == "__main__":
    unittest.main(testRunner=unittest.TextTestRunner(resultclass=MyTestResult))
